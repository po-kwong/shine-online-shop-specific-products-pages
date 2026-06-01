import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT_DIR = ROOT / "products"
DATA_PATH = ROOT / "tools" / "product_data.json"


def load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def image_url(file_id, width=720):
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{width}"


def local_image_url(page_file, code, width=720):
    page_slug = page_file.removesuffix(".html")
    return f"../assets/images/{page_slug}/{code}-{width}.webp"


def local_image_srcset(page_file, code):
    page_slug = page_file.removesuffix(".html")
    return ", ".join(
        f"../assets/images/{page_slug}/{code}-{width}.webp {width}w"
        for width in (480, 720, 960)
    )


def original_url(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"


def render_page(page, order_note):
    meta = "\n".join(f"        <li>{escape(value)}</li>" for value in page["meta"])
    cards = []
    for index, item in enumerate(page["items"]):
        code = item["code"]
        file_id = item["drive_id"]
        loading = "eager" if index == 0 else "lazy"
        fetchpriority = "high" if index == 0 else "auto"
        cards.append(
            f"""      <article class="product-card">
        <div class="image-frame">
          <img src="{local_image_url(page['file'], code)}" srcset="{local_image_srcset(page['file'], code)}" sizes="(max-width: 768px) calc(100vw - 50px), (min-width: 1024px) 360px, 50vw" alt="{escape(code)}" width="720" height="720" loading="{loading}" decoding="async" fetchpriority="{fetchpriority}">
        </div>
        <div class="product-info">
          <p class="code-label">編號</p>
          <p class="product-code">{escape(code)}</p>
          <a class="original-link" href="{original_url(file_id)}" target="_blank" rel="noopener">開啟原圖</a>
        </div>
      </article>"""
        )
    gallery = "\n".join(cards)
    title = escape(page["title"])
    note = escape(order_note)
    return f"""<!doctype html>
<html lang="zh-Hant-HK">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
  <main class="page-shell">
    <header class="product-header">
      <p class="brand-line">網尚店</p>
      <h1>{title}</h1>
      <ul class="series-meta" aria-label="系列資料">
{meta}
      </ul>
    </header>

    <section class="order-note" aria-label="訂購提示">
      <p>{note}</p>
    </section>

    <section class="gallery" aria-label="產品圖片及編號">
{gallery}
    </section>
  </main>
</body>
</html>
"""


def main():
    data = load_data()
    PRODUCT_DIR.mkdir(exist_ok=True)
    active_files = {page["file"] for page in data["pages"]}
    for old_page in PRODUCT_DIR.glob("*.html"):
        if old_page.name not in active_files:
            old_page.unlink()
    for page in data["pages"]:
        (PRODUCT_DIR / page["file"]).write_text(render_page(page, data["order_note"]), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
