#!/usr/bin/env python3
"""Đóng gói web app thành MỘT tệp HTML dùng được khi không có mạng.

Chạy:  python3 scripts/dong_goi.py

Đọc    docs/ (index.html, style.css, app.js, data, hình)
Sinh   So-tay-Doc-chat.html ở thư mục gốc dự án.

Tệp sinh ra mở thẳng bằng trình duyệt, chép qua USB hay gửi Zalo đều chạy,
không cần máy chủ và không cần mạng.
"""

import base64
import json
import os
import re
import sys

GOC = os.path.join(os.path.dirname(__file__), "..")
DOCS = os.path.join(GOC, "docs")
DICH = os.path.join(GOC, "So-tay-Doc-chat.html")


def doc(ten):
    with open(os.path.join(DOCS, ten), encoding="utf-8") as f:
        return f.read()


def anh_base64(ten):
    with open(os.path.join(DOCS, ten), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def main():
    html = doc("index.html")
    css = doc("style.css")
    js = doc("app.js")
    with open(os.path.join(DOCS, "data", "doc-chat.json"), encoding="utf-8") as f:
        du_lieu = json.load(f)

    # nhúng hình vào dữ liệu luôn, để app không phải tải tệp rời
    for c in du_lieu["chat"]:
        if c.get("hinh"):
            c["hinhNhung"] = anh_base64(os.path.join("hinh", c["hinh"]))

    # bỏ các thẻ liên kết tới tệp rời
    html = re.sub(r'\s*<link rel="manifest"[^>]*>', "", html)
    html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', "", html)
    html = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', "", html)
    html = html.replace(
        '<link rel="icon" href="icon.svg" type="image/svg+xml">',
        '<link rel="icon" href="' + anh_base64("icon-192.png") + '">',
    )
    html = html.replace('<script src="app.js"></script>', "")

    # trong bản một tệp, hình nằm sẵn trong dữ liệu
    js = js.replace('src="hinh/\' + thoat(c.hinh) + \'"',
                    "src=\"' + (c.hinhNhung || ('hinh/' + c.hinh)) + '\"")

    nhung = (
        "<style>\n" + css + "\n</style>\n</head>"
    )
    html = html.replace("</head>", nhung)

    duoi = (
        "<script>window.DU_LIEU_NHUNG="
        + json.dumps(du_lieu, ensure_ascii=False, separators=(",", ":"))
        + ";</script>\n<script>\n"
        + js
        + "\n</script>\n</body>"
    )
    html = html.replace("</body>", duoi)

    with open(DICH, "w", encoding="utf-8") as f:
        f.write(html)

    mb = os.path.getsize(DICH) / 1024 / 1024
    print(f"Đã sinh {DICH} — {mb:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
