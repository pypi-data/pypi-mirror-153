from typing import List

from bs4 import BeautifulSoup, Tag

from gpd.models.dependent import Dependent
from gpd.parsers.dependent_parser import DependentParser


class TablePageParser:
    soup: BeautifulSoup

    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def get_dependents_estimate(self) -> int:
        estimate = self.soup.find("a", class_="btn-link selected").text.strip().replace(",", "")
        return int(estimate.split("\n")[0])

    def get_dependents(self) -> List[Dependent]:
        dependents = []
        for row in self.get_rows():
            dependents.append(Dependent(**DependentParser(row).to_dict()))
        return dependents

    def get_rows(self) -> List[Tag]:
        return self.soup.findAll("div", {"class": "Box-row"})

    def get_next_page_url(self) -> str:
        for tag in self.soup.find("div", {"class": "paginate-container"}).findAll('a'):
            if tag.text == "Next":
                return tag["href"]
        return ""
