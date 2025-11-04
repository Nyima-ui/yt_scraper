import time
import random
from pathlib import Path
from bs4 import BeautifulSoup
from utils.logger import logger
from patchright.sync_api import sync_playwright
from loader.loader import write_html, append_in_json, write_json, json_to_excel


def get_video_links():
    try:
        file_path = Path(__file__).parent.parent / "data" / "home.html"
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        link_elements = soup.find_all("a", id="video-title-link")
        video_links = [
            f"https://www.youtube.com{link['href']}" for link in link_elements
        ]
        return video_links
    except Exception as e:
        logger.error(f"❌ Error extracting video links: {e}")
        return []


def extract_video_data(soup, vid_link):
    try:
        title = soup.find("h1", class_="style-scope ytd-watch-metadata")
        title = title.get_text(strip=True) if title else "N/A"

        description = soup.find("div", id="expanded")
        description = description.get_text(strip=True) if description else "N/A"

        transcription_elem = soup.find_all(
            "yt-formatted-string",
            class_="segment-text style-scope ytd-transcript-segment-renderer",
        )
        transcription_list = [t.get_text(strip=True) for t in transcription_elem]
        full_transcription = (
            " ".join(transcription_list) if transcription_list else "N/A"
        )
        return {
            "video_link": vid_link,
            "title": title,
            "description": description,
            "transcription": full_transcription,
        }
    except Exception as e:
        logger.error(f"⚠️ Error extracting data from {vid_link}: {e}")
        return None


def scarpe_video(page, video_links):
    for i, link in enumerate(video_links):
        try:
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

            time.sleep(random.uniform(5, 7))

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            data = extract_video_data(soup, link)

            file_path = Path(__file__).parent.parent / "data" / "video.json"
            append_in_json(data, file_path)
            logger.info(f"✅ Scraped {i}/{len(video_links)}")
        except Exception as e:
            logger.error(f"❌ failed to scrape {link}: {e}")
            continue


def get_html(page):
    html = page.content()
    html_file_path = Path(".").resolve() / "data" / "home.html"
    write_html(html, html_file_path)


def scroll_to_bottom(page):
    previous_height = 0
    max_scrolls = 50
    scroll_count = 0
    no_change_count = 0

    while scroll_count < max_scrolls:
        page.evaluate("window.scrollBy(0, document.documentElement.scrollHeight)")
        page.wait_for_timeout(2000)

        current_height = page.evaluate("document.documentElement.scrollHeight")

        if current_height == previous_height:
            no_change_count += 1
            if no_change_count >= 2:
                logger.info("✅ Reached end of the vidoes")
                break

        previous_height = current_height
        scroll_count += 1
        logger.info(f"Scroll {scroll_count}/{max_scrolls} - Height: {current_height}")

    if scroll_count >= max_scrolls:
        logger.warning("⚠️ Reached maximum scroll limit")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="temp/data",
            channel="chrome",
            headless=False,
            no_viewport=True,
        )
        page = browser.new_page()
        try:
            page.goto("https://www.youtube.com/@loistalagrand/videos")
            scroll_to_bottom(page)
            get_html(page)
            video_links = get_video_links()
            write_json(
                video_links,
                f"{Path(__file__).parent.parent / "data" / "vid_links.json"}",
            )
            if not video_links:
                logger.error("❌ No video links found!")
                return
            scarpe_video(page, video_links[0:10])
            # json_to_excel()
            time.sleep(5)
            browser.close()
        except Exception as e:
            logger.error(f"❌ Error in main: {e}")
            browser.close()


if __name__ == "__main__":
    main()
