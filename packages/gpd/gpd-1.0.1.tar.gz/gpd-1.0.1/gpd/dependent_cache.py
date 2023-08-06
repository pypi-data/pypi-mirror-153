import pickle
from pathlib import Path
from typing import List

from loguru import logger

from gpd.models.dependent import Dependent


class DependentCache:
    path: Path
    owner: str
    project: str
    max_page: int

    def __init__(self, owner: str, project: str, max_page: int, directory: Path = Path("./cache")):
        self.owner = owner
        self.project = project
        self.max_page = max_page

        self.path = directory / "{}-{}-{}.pickle".format(self.owner, self.project, self.max_page)

    def dependents_from_file(self) -> List[Dependent]:
        try:
            with open(self.path, 'rb') as f:
                return pickle.load(f)
        except:
            logger.exception("path={path}", path=self.path)

    def dependents_to_file(self, dependents: List[Dependent]) -> None:
        if dependents:
            with open(self.path, 'wb') as f:
                pickle.dump(dependents, f)

