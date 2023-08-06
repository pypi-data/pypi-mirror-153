from typing import List, Dict, Any

from tabulate import tabulate

from gpd.models.dependent import Dependent


class DependentsStats:
    dependents: List[Dependent]

    def __init__(self, dependents: List[Dependent]):
        self.dependents = dependents

    def get_count(self):
        return len(self.dependents)

    def get_top_stars(self, max: int = 20) -> str:
        self.dependents.sort(key=lambda x: x.stars, reverse=True)
        return self._prettify_dependents(self.dependents[:max])

    def get_top_forks(self, max: int = 20) -> str:
        self.dependents.sort(key=lambda x: x.forks, reverse=True)
        return self._prettify_dependents(self.dependents[:max])

    def _prettify_dependents(self, dependents: List[Dependent]) -> str:
        return tabulate(self._group_dependents_by_key(dependents), headers="keys")

    def _group_dependents_by_key(self, dependents: List[Dependent]) -> Dict[str, Any]:
        groups = {}
        for dependent in dependents:
            for key, value in dependent.dict().items():
                if groups.get(key):
                    groups[key].append(value)
                else:
                    groups[key] = [value]
        return groups
