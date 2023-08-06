from typing import Any, List, Optional
from dataclasses import dataclass

from arthurai.core.base import ArthurBaseJsonDataclass

@dataclass
class AuthInfo(ArthurBaseJsonDataclass):
    issuer: str
    username: str
    first_name: str
    last_name: str
    email: str
    roles: List[str]
    organization_ids: List[str]
    internal_user_id: Optional[str] = None
    external_user_id: Optional[str] = None

    def __post_init__(self):
        """
        Special initialization method for dataclasses that is called after the generated __init__() method.

        Input parameters to __post_init__ (may) be parsed out of the class variables and into this
        method. E.g. defining ArthurModel.client allows you to create an ArthurModel instance as
        `ArthurModel(client=...)` where client is only passed into __post_init__ and does not show
        up as an instance variable. To do so, the class variable type must be defined with an
        InitVar[] wrapper (refer to link to Python docs below).
        https://docs.python.org/3/library/dataclasses.html#init-only-variables
        
        Variables created here will only be accessible directly on the object itself, they will not
        be in the result of object.to_dict() even if marked as public (does not have preceding
        underscore).
        """
        pass
