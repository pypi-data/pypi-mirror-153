from dataclasses import field
from typing import List, Optional

import marshmallow_dataclass
from marshmallow import pre_load

SINGLE_ENV_DEFAULT_IMG_NAME = "visible_spectrum.png"


@marshmallow_dataclass.dataclass(unsafe_hash=True)
class Environment:
    image_name: str
    environment: Optional[str] = field(compare=False)
    time_of_day: Optional[str] = field(compare=False)
    background: Optional[str] = field(compare=False)
    behaviour: Optional[str] = field(compare=False)
    domain: Optional[str] = field(compare=False)

    def matches(self, **env_attributes) -> bool:
        is_match = True
        for attr_name, attr_value in env_attributes.items():
            is_match &= self.__dict__[attr_name] == attr_value
        return is_match


@marshmallow_dataclass.dataclass
class Environments:
    environments: List[Environment]

    def __iter__(self):
        for environment in self.environments:
            yield environment

    def __getitem__(self, image_name: str) -> Environment:
        return next(env for env in self if env.image_name == image_name)

    @pre_load
    def rearrange_fields(self, in_data: dict, **kwargs):
        """
        handling older versions of environment.json,
        where we assumed there's only one env per scene.
        The content of environment.json would like this:

           {
               "time_of_day": "morning",
               "environment": "indoor",
               "background": "hdri"
            }

        and we'd like to change it to the environments modality structure, e.g.:

            {
                "environments": [
                    {
                       "image_name": "visible_spectrum.png"
                       "time_of_day": "morning",
                       "environment": "indoor",
                       "background": "hdri"
                    }
                ]
            }
        """
        if "environments" not in in_data:
            in_data["image_name"] = SINGLE_ENV_DEFAULT_IMG_NAME
            in_data = {"environments": [in_data]}
        return in_data
