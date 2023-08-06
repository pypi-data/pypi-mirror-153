from bs4 import Tag


class DependentParser:
    dependent: Tag

    def __init__(self, table_row: Tag):
        self.dependent = table_row

    def get_name(self) -> str:
        return self.dependent.find('a', {"data-hovercard-type": "repository"}).text

    def get_stars(self) -> int:
        return int(self.dependent.findAll('span', class_="color-fg-muted text-bold pl-3")[0].text.strip().replace(",", ""))

    def get_forks(self) -> int:
        return int(self.dependent.findAll('span', class_="color-fg-muted text-bold pl-3")[1].text.strip().replace(",", ""))

    def get_author(self) -> str:
        return self.dependent.find('a', {"data-repository-hovercards-enabled": ""}).text

    def get_url(self) -> str:
        return self.urlify_for_github(self.get_href())

    def urlify_for_github(self, href: str):
        if href.find("http") == 0:
            return href
        return "https://github.com{}".format(href)

    def get_href(self) -> str:
        return self.dependent.find('a', {"data-hovercard-type": "repository"})["href"]

    def to_dict(self):
        return {"name": self.get_name(), "stars": self.get_stars(), "forks": self.get_forks(), "author": self.get_author(), "url": self.get_url()}
