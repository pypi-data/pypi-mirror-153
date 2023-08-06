from pydantic import BaseModel, Extra


class ImmutableBaseModel(BaseModel):
    class Config:
        allow_mutation = False
        frozen = True
        extra = Extra.forbid
