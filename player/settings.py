import toml
from pathlib import Path


conf_file: Path
(conf_file,) = list(Path.cwd().glob("**/conf.toml"))


class Settings:
    def __init__(self, config) -> None:
        for k, v in config.items():
            if isinstance(v, dict):
                setattr(self, k, Settings(v))
            else:
                setattr(self, k, v)


with open(conf_file, "r") as fp:
    config = toml.load(fp)


settings = Settings(config)
