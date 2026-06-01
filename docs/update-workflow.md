# 更新產品展示頁流程

本專案支援一種更新方式：

- 手動指令：Jason 在此專案說「refresh」或「更新」時，Codex 應按本文件刷新網站。

## 資料來源

Google Drive 主 folder：

```text
https://drive.google.com/drive/folders/1tJDzPefoX8tVQqhUJyh-ppPTuJsTVJ0K
```

本地資料 manifest：

```text
tools/product_data.json
```

`product_data.json` 是網站的單一資料來源，包含：

- `drive_root`：Google Drive 主 folder 資料。
- `pages[]`：每個產品系列頁。
- `pages[].folder_id`：對應 Drive 子 folder。
- `pages[].items[]`：該頁要展示的產品圖片。
- `items[].code`：網站顯示的「編號」，不可包含 `.png`、`.JPEG` 等副檔名。
- `items[].drive_id`：Google Drive 圖片 file ID。

## 「refresh / 更新」時要做甚麼

1. 用 Google Drive connector 讀取 `drive_root.folder_id` 的直接子 folder。
2. 對每個子 folder 讀取圖片檔案清單。
3. 用 Drive folder title 對應 `product_data.json` 內既有頁面：
   - 優先用 `folder_id` 配對。
   - 若是新 folder，新增一個 `pages[]` entry。
   - 若 folder 內沒有圖片，該系列不放入 `pages[]`，並在重建時清走舊頁面、舊圖片及 link。
4. 對每張圖片：
   - `code` 使用檔名主體，例如 `A01_CP.png` -> `A01_CP`。
   - `drive_id` 使用該 Drive file ID。
   - 圖片按 `code` 自然排序。
5. 更新每頁 `meta` 的「共 N 款」數字。
6. 執行：

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\refresh_site.py'
```

7. 驗證：
   - 5 個或更多 `products/*.html` 皆正確生成。
   - HTML 圖片來源應使用 `../assets/images/...webp`。
   - HTML 不應使用 `drive.google.com/thumbnail` 作圖片來源。
   - 每個產品卡顯示「編號」，不顯示副檔名。
   - `assets/images/` 有對應 `480/720/960.webp`。
   - `products/` 和 `assets/images/` 不應保留 manifest 以外的舊頁面或舊圖片。
   - 或直接執行：

```powershell
& 'C:\Users\Jason\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'tools\verify_site.py'
```

8. Commit and push：

```powershell
git add assets/images products docs tools README.md AGENTS.md
git commit -m "Refresh product pages from Drive"
git push
```

9. 等 GitHub Pages build 完成後，檢查 live pages 回 `200`。

## 不使用定時自動更新

本專案現時不使用 GitHub Actions 定時讀取 Google Drive，因此不需要設定 `GOOGLE_DRIVE_API_KEY`、`GOOGLE_SERVICE_ACCOUNT_JSON` 或其他 Drive secret。

更新節奏改為：Jason 將新相片或新系列 folder 放入 Google Drive 後，在此專案對 Codex 說 `refresh` 或 `更新`，Codex 便按上方流程更新網站、文件、commit 及 push。

## 新系列 folder 規則

如果 Drive 出現新子 folder：

- `title` 使用 Drive folder 名稱。
- `file` 使用穩定英文 slug，例如 `new-series-name.html`。
- 如果 folder 名稱難以英文化，使用 `series-<folder_id 前 8 字元>.html`。
- `meta` 建議：
  - 第一格：`共 N 款`
  - 若 folder 名稱含 `_`，用 `_` 前後拆成產品類別與系列名。
  - 例如 `眼鏡布_名畫喵系列` -> `["共 12 款", "眼鏡布", "名畫喵系列"]`

## 為甚麼不是即時讀 Drive

為了加快載入速度，網站不直接向 Google Drive 載入圖片。刷新流程會先把 Drive 圖片轉成 GitHub Pages 本地 WebP 圖片：

- `480.webp`：手機或細卡片
- `720.webp`：預設顯示
- `960.webp`：較大螢幕備用

頁面用 `srcset` 和 `sizes` 自動選合適圖片。這比即時讀 Google Drive thumbnail 更快和更穩定。
