from typing import Callable

import pandas as pd
import numpy as np
import re
import json

import pytest

from arthurai.explainability.arthur_explainer import ArthurExplainer
from arthurai.common.constants import InputType, OutputType
from arthurai.common.exceptions import ArthurUserError


# FIXTURES

def predict_reg(input_x):
    pass_class = np.array(input_x)[:, 0]
    prediction = 120 / (2 * pass_class)
    return prediction


def predict_class(input_x):
    age = np.array(input_x)[:, 2]
    prediction = np.clip(age / 60, a_min=0., a_max=1.0)
    return np.stack([1 - prediction, prediction], axis=1)


@pytest.fixture
def titanic_df() -> pd.DataFrame:
    return pd.DataFrame({
            'pass_class': [1, 1, 3, 1, 3, 3, 3, 1, 3, 3],
            'sex': ['F', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'M', 'M'],
            'age': [16.0, 24.0, 19.0, 58.0, 30.0, 22.0, 40.0, 37.0, 65.0, 32.0],
            'fare': [86.5, 49.5042, 8.05, 153.4625, 7.8958, 7.75, 7.8958, 29.7, 7.75, 7.8958],
            'survived': [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]})


# parametrize by output type
@pytest.fixture(params=[OutputType.Multiclass, OutputType.Regression])
def output_type(request) -> OutputType:
    return request.param


# parametrize by lime / shap
@pytest.fixture(params=["lime", "shap"])
def algo(request) -> str:
    return request.param


# parametrize by doing nothing or nullifying input columns as "nan" or None
@pytest.fixture(params=["regular", "nan", "none"])
def X(request, titanic_df: pd.DataFrame, output_type: OutputType) -> pd.DataFrame:
    if output_type == OutputType.Multiclass:
        X = titanic_df.drop(columns="survived")
    elif output_type == OutputType.Regression:
        X = titanic_df.drop(columns=["fare", "survived"])
    else:
        raise ValueError()

    # convert string categorical to int
    X['sex'] = pd.factorize(titanic_df['sex'])[0]

    if request.param == "regular":
        replacement_val = None
    elif request.param == "nan":
        replacement_val = float("nan")
    elif request.param == "none":
        replacement_val = None
    else:
        raise ValueError()

    if replacement_val is not None:
        X['age'].iloc[2] = replacement_val
        X['pass_class'].iloc[3] = replacement_val

    return X


@pytest.fixture
def predict_func(output_type: OutputType) -> Callable:
    if output_type == OutputType.Multiclass:
        return predict_class
    elif output_type == OutputType.Regression:
        return predict_reg
    else:
        raise ValueError()


def significant_feature(output_type: OutputType) -> int:
    # the predict_class function uses only the age input in column 2
    if output_type == OutputType.Multiclass:
        return 2
    # the predict_reg function uses only the pass class input in column 0
    elif output_type == OutputType.Regression:
        return 0
    else:
        raise ValueError()


# TESTS

def test_arthur_explainer_tabular(X: pd.DataFrame, output_type: OutputType, algo: str, predict_func: Callable) -> None:
    # [None, None, ... ] number of columns
    num_cols = len(X.columns)
    label_mapping = [None for _ in range(num_cols)]
    # create explainer
    if algo == "shap":
        enable_shap = True
    elif algo == "lime":
        enable_shap = False
    else:
        raise ValueError()

    # drop rows with NaNs for "training"
    explainer = ArthurExplainer(model_type=output_type,
                                model_input_type=InputType.Tabular,
                                num_predicted_attributes=1,
                                predict_func=predict_func,
                                data=X,
                                enable_shap=enable_shap,
                                label_mapping=label_mapping)
    feature_vector = X.to_numpy().tolist()
    explanations = np.array(explainer.explain_tabular(algo=algo, raw_feature_vectors=feature_vector))

    average_feature_explanations = (
        np.nanmean(  # take average ignoring NaNs
            np.abs(explanations)  # absolute value to look at magnitude of feature importance, not direction
            [:, 0, :],  # pick the first "predicted column" to give us a data_rows X num_features matrix
            axis=0)  # average across all the rows to get average importance of each feature
    )

    # assert most significant feature is expected
    assert np.argmax(average_feature_explanations) == significant_feature(output_type)

    # assert rows with nans produce explanations with all nans
    rows_with_nans = np.nonzero(np.any(np.isnan(explanations), axis=1))[0]
    for i in rows_with_nans:
        assert np.all(np.isnan(explanations[i]))


def test_arthur_explainer_user_error_tabular(X: pd.DataFrame, predict_func: Callable) -> None:
    # [None, None, ... ] number of columns
    num_cols = len(X.columns)
    label_mapping = [None for _ in range(num_cols)]
    # enable_shap is currently always set to True for non NLP data
    enable_shap = True

    def predict_wrong_shape(input_x):
        age = np.array(input_x)[:, 2]
        prediction = np.clip(age / 60, a_min=0., a_max=1.0)
        #incorrect output format due to concatenation along wrong axis should raise an error in caller
        return np.stack([1 - prediction, prediction], axis=0)

    with pytest.raises(ArthurUserError):
        ArthurExplainer(model_type=OutputType.Regression,
                        model_input_type=InputType.Tabular,
                        num_predicted_attributes=1,
                        predict_func=predict_wrong_shape,
                        data=X,
                        enable_shap=enable_shap,
                        label_mapping=label_mapping)


def test_arthur_explainer_nlp_regression() -> None:
    def regression_predict(feature_vecs):
        results = []
        for fv in feature_vecs:
            results.append(np.array([0.2, 0.8]))
        return np.array(results)

    sample_data = pd.DataFrame([
        ['this is a test'],
        ['a second test with more words'],
        ['and a third test']
    ])

    explainer = ArthurExplainer(model_type=OutputType.Regression,
                                model_input_type=InputType.NLP,
                                num_predicted_attributes=1,
                                predict_func=regression_predict,
                                data=sample_data,
                                enable_shap=False,
                                label_mapping=[None])

    raw_feat_vecs = [
        ['first test test'],
        ['and a longer second test']
    ]
    exps = explainer.explain_nlp("lime", raw_feature_vectors=raw_feat_vecs, nsamples=100)

    # confirm we got 2 explanations
    assert len(exps) == 2

    for i, exp in enumerate(exps):
        # ensure single class
        assert len(exp) == 1
        # assert one explanation per unique word
        assert len(exp[0]) == len(re.split(explainer.text_delimiter, raw_feat_vecs[i][0]))


def test_arthur_explainer_nlp_classification() -> None:
    def regression_predict(feature_vecs):
        results = []
        for fv in feature_vecs:
            results.append(np.array([0.2, 0.7, 0.1]))
        return np.array(results)

    sample_data = pd.DataFrame([
        ['this is a test'],
        ['a second test with more words'],
        ['and a third test']
    ])

    explainer = ArthurExplainer(model_type=OutputType.Multiclass,
                                model_input_type=InputType.NLP,
                                num_predicted_attributes=3,
                                predict_func=regression_predict,
                                data=sample_data,
                                enable_shap=False,
                                label_mapping=[None])

    raw_feat_vecs = [
        ['first test test'],
        ['and a longer second test']
    ]
    exps = explainer.explain_nlp("lime", raw_feature_vectors=raw_feat_vecs, nsamples=100)

    # confirm we got 2 explanations
    assert len(exps) == 2

    for i, exp in enumerate(exps):
        # ensure single class
        assert len(exp) == 3
        # assert one explanation per unique word
        assert len(exp[0]) == len(re.split(explainer.text_delimiter, raw_feat_vecs[i][0]))


def test_arthur_explainer_image_classification() -> None:
    def load_image(image_path):
        return np.array([
            [[20, 4, 6], [5, 7, 12], [5, 12, 4]],
            [[20, 4, 106], [5, 7, 112], [5, 12, 104]],
            [[20, 4, 206], [5, 7, 212], [5, 12, 204]],
        ])

    def cv_predict(images):
        results = []
        for image in images:
            results.append(np.array([0.2, 0.7, 0.1]))
        return np.array(results)

    sample_data = pd.DataFrame([
        ['this is a test'],
        ['a second test with more words'],
        ['and a third test']
    ])

    explainer = ArthurExplainer(model_type=OutputType.Multiclass,
                                model_input_type=InputType.Image,
                                num_predicted_attributes=3,
                                predict_func=cv_predict,
                                data=sample_data,
                                enable_shap=False,
                                label_mapping=[None],
                                load_image_func=load_image)

    image_paths = [
        'path/to/image',
        'path/to/another/image'
    ]
    exps = explainer.explain_image("lime", image_paths=image_paths)

    # confirm we got 2 explanations
    assert len(exps) == 2

    for i, exp in enumerate(exps):
        """
        Example Output:
            {
                "lime_segment_mask": [
                    [1, 1, 1, 3, 3, 1, 0],
                    [1, 1, 1, 3, 3, 1, 0],
                    [1, 1, 1, 3, 3, 1, 0],
                    [2, 2, 2, 3, 3, 1, 0]
                ],
                "lime_region_mapping": {
                    "0": [[0, 0.23], [1, 0.3], [2, 0.001], [3, -0.5]]
                }
            }
        """
        # confirm we got an appropriate-sized mask
        assert len(exp["lime_segment_mask"]) == len(load_image(image_paths[i]))

        # sanity check on mask values
        # ideally would actually check schema here
        sample_mask_value = exp["lime_segment_mask"][0][0]
        assert sample_mask_value >= 0
        assert next(iter(exp["lime_region_mapping"].values()))

        # ensure serializable
        assert json.dumps(exp)
