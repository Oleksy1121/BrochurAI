import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

class Website:
    def __init__(self, url: str):
        self.url = url
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        self.title = soup.title.string if soup.title else "Title not found"

        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        self.links = [
            urljoin(self.url, link.get("href"))
            for link in soup.find_all("a")
            if link.get("href")
        ]

    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n"
