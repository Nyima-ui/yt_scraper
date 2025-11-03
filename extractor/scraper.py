import time
from pathlib import Path
from loader.loader import write_html
from parser.parser import get_video_links
from patchright.sync_api import sync_playwright


def get_video_title(page, video_links):
    for link in video_links:
        page.goto(link)


def get_html(page):
    html = page.content()
    html_file_path = Path(".").resolve() / "data" / "home.html"
    write_html(html, html_file_path)


def scroll_to_bottom(page):
    previous_height = 0
    max_scrolls = 50
    scroll_count = 0

    while scroll_count < max_scrolls:
        page.evaluate("window.scrollBy(0, document.documentElement.scrollHeight)")
        time.sleep(3)

        current_height = page.evaluate("document.documentElement.scrollHeight")
        if current_height == previous_height:
            print("✅ Reached end of the vidoes")
            break
        previous_height = current_height
        scroll_count += 1
        print(f"Scroll {scroll_count}/{max_scrolls} - Height: {current_height}")

    if scroll_count >= max_scrolls:
        print("⚠️ Reached maximum scroll limit")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="temp/data",
            channel="chrome",
            headless=False,
            no_viewport=True,
        )
        page = browser.new_page()
        page.goto("https://www.youtube.com/@loistalagrand/videos")
        scroll_to_bottom(page)
        get_html(page)
        video_links = get_video_links()
        get_video_title(page, video_links[0:1])
        time.sleep(10)
        browser.close()


if __name__ == "__main__":
    main()
