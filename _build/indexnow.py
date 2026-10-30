"""Kirim semua URL di sitemap.xml ke IndexNow (Bing, Yandex, Seznam, Naver).

ChatGPT Search memakai indeks Bing, jadi jalankan ini setiap kali ada
halaman baru atau perubahan besar, SETELAH perubahan tayang di main:

    python _build/indexnow.py
"""
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "harshaadvisory.com"
KEY = "b2682cd32aae43877f484331cbe5602b"


def main():
    urls = re.findall(r"<loc>(.*?)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt",
                       "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(r.status, f"{len(urls)} URL dikirim")


if __name__ == "__main__":
    main()
