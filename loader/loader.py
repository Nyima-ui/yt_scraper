import json
import pandas as pd
from pathlib import Path
from utils.logger import logger


def write_html(html, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        logger.error(f"⚠️ Error writing to html file. : {e}")


def append_in_json(data, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
    existing_data.append(data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)


def write_json(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"❌ Error writing video links in json. {e}")


def json_to_excel():
    try:
        json_file_path = Path(__file__).parent.parent / "data" / "video.json"
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        excel_file_path = (
            r"C:\Users\Tenzin Nyima\OneDrive\Documents\excel_files\youtube_videos.xlsx"
        )
        df.to_excel(excel_file_path, index=False, engine="openpyxl")
    except Exception as e:
        logger.error(f"❌ Error saving to excel file. {e}")
