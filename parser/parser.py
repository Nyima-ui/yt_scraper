from pathlib import Path
from bs4 import BeautifulSoup


def get_video_links():
    file_path = Path(__file__).parent.parent / "data" / "home.html"
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    link_elements = soup.find_all("a", id="video-title-link")
    video_links = [f"https://www.youtube.com{link['href']}" for link in link_elements]
    return video_links
