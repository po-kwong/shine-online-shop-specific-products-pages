from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import shutil

from PIL import Image

from build_product_pages import image_url, load_data


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "assets" / "images"
WIDTHS = (480, 720, 960)


def download_thumbnail(file_id):
    request = Request(
        image_url(file_id, 1200),
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def resize_for_width(image, target_width):
    source = image.convert("RGB")
    width, height = source.size
    if width <= target_width:
        return source.copy()
    target_height = round(height * (target_width / width))
    return source.resize((target_width, target_height), Image.Resampling.LANCZOS)


def optimize_item(page_file, code, file_id):
    page_slug = page_file.removesuffix(".html")
    out_dir = OUTPUT_ROOT / page_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(BytesIO(download_thumbnail(file_id)))
    written = []
    for width in WIDTHS:
        resized = resize_for_width(image, width)
        out_path = out_dir / f"{code}-{width}.webp"
        resized.save(out_path, "WEBP", quality=78, method=6)
        written.append(out_path)
    return written


def clean_output(data):
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    active_slugs = {page["file"].removesuffix(".html") for page in data["pages"]}

    for child in OUTPUT_ROOT.iterdir():
        if child.is_dir() and child.name not in active_slugs:
            shutil.rmtree(child)

    for page in data["pages"]:
        out_dir = OUTPUT_ROOT / page["file"].removesuffix(".html")
        if out_dir.exists():
            for old_image in out_dir.glob("*.webp"):
                old_image.unlink()


def main():
    data = load_data()
    clean_output(data)
    all_written = []
    for page in data["pages"]:
        for item in page["items"]:
            all_written.extend(optimize_item(page["file"], item["code"], item["drive_id"]))
    total = sum(path.stat().st_size for path in all_written)
    print(f"Wrote {len(all_written)} WebP files, {total / 1024:.1f} KB total")


if __name__ == "__main__":
    main()
