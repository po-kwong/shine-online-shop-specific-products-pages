import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "tools" / "product_data.json"


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    errors = []
    page_count = 0
    item_count = 0
    expected_images = set()

    for page in data["pages"]:
        page_count += 1
        html_path = ROOT / "products" / page["file"]
        if not html_path.exists():
            errors.append(f"Missing page: {html_path}")
            continue

        html = html_path.read_text(encoding="utf-8")
        if "drive.google.com/thumbnail" in html:
            errors.append(f"Drive thumbnail source found in {html_path}")
        if "../assets/images/" not in html:
            errors.append(f"Local WebP image source missing in {html_path}")
        if "請先記下心儀款式的編號" not in html:
            errors.append(f"Order note missing in {html_path}")

        page_slug = page["file"].removesuffix(".html")
        for item in page["items"]:
            item_count += 1
            code = item["code"]
            if re.search(r"\.(png|jpe?g|webp|gif)$", code, re.IGNORECASE):
                errors.append(f"Code still contains extension: {code}")
            if f">{code}<" not in html:
                errors.append(f"Code {code} missing in {html_path}")
            for width in (480, 720, 960):
                image_path = ROOT / "assets" / "images" / page_slug / f"{code}-{width}.webp"
                expected_images.add(image_path.resolve())
                if not image_path.exists():
                    errors.append(f"Missing optimized image: {image_path}")

    images_root = ROOT / "assets" / "images"
    if images_root.exists():
        for image_path in images_root.rglob("*.webp"):
            if image_path.resolve() not in expected_images:
                errors.append(f"Stale optimized image: {image_path}")

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)

    print(f"Verified {page_count} page(s), {item_count} item(s), local WebP assets OK.")


if __name__ == "__main__":
    main()
