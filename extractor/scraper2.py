import time
import random
from pathlib import Path
from loader.loader import write_json
from bs4 import BeautifulSoup
from patchright.sync_api import sync_playwright


# https://www.youtube.com/watch?v=Z0ZvfCxVXiA

video_links = ["https://www.youtube.com/watch?v=MDcu37rrNUE&t=5s"]


def main(video_links):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="temp/data",
            channel="chrome",
            headless=False,
            no_viewport=False,
        )
        page = browser.new_page()
        # new function
        for link in video_links:
            page.goto(link)
            more_button = (
                page.locator("tp-yt-paper-button#expand")
                .filter(has_not=page.locator("[hidden]"))
                .first
            )
            more_button.click()
            time.sleep(random.uniform(1, 2))
            transcript_button = page.get_by_role("button", name="Show transcript")
            transcript_button.click()
            time.sleep(random.uniform(3, 4))
            # new function
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            # new function - title
            title = soup.find("h1", class_="style-scope ytd-watch-metadata").get_text(
                strip=True
            )
            # new function - description
            description = soup.find("div", id="expanded").get_text(strip=True)
            # new function - transcription
            transcription_elem = soup.find_all(
                "yt-formatted-string",
                class_="segment-text style-scope ytd-transcript-segment-renderer",
            )
            transcription_list = [
                transcription.get_text(strip=True)
                for transcription in transcription_elem
            ]
            full_transcription = " ".join(transcription_list)
            # new function
            file_path = Path(__file__).parent.parent / "data" / "video.json"
            write_json(
                {
                    "video_link": link,
                    "title": title,
                    "description": description,
                    "transcription": full_transcription,
                },
                file_path,
            )
        time.sleep(5)
        browser.close()


if __name__ == "__main__":
    main(video_links)
