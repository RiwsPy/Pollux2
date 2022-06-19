from .greenalp_map import Config as BaseConfig


class Config(BaseConfig):
    class Meta:
        abstract = False
    _ID = "mairin"
    CLONE_ID = "00"
