import json


def write_html(html, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        print("⚠️ Error writing to html file.")


def write_json(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("⚠️ Error writing to json file")
