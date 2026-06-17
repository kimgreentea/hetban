import os
from bs4 import BeautifulSoup
from ebooklib import epub


os.chdir(os.path.dirname(os.path.realpath(__file__)))

BOOK_TITLE = "논어의 문법적 구조"
BOOK_ID = "kongzi"

book = epub.EpubBook()

book.set_identifier(BOOK_ID)
book.set_title(BOOK_TITLE)
book.set_language("ko")

# -------------------
# CSS 추가
# -------------------

style = """
body {
    line-height: 1.8;
}

h1 {
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
}

blockquote {
    margin: 1em 2em;
    padding-left: 1em;
    border-left: 4px solid #888;
}

blockquote em {
    display: block;
    margin-top: 0.5em;
    font-size: 0.9em;
}
"""

css_item = epub.EpubItem(
    uid="style",
    file_name="style/style.css",
    media_type="text/css",
    content=style.encode("utf-8")
)

book.add_item(css_item)

chapters = []

# -------------------
# HTML 파일 읽기
# -------------------

html_files = sorted(
    f for f in os.listdir("output")
    if f.endswith(".html") and f != "index.html"
)

for i, filename in enumerate(html_files, start=1):

    path = os.path.join("output", filename)

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1")

    title = (
        title_tag.get_text(strip=True)
        if title_tag
        else f"Chapter {i}"
    )

    chapter = epub.EpubHtml(
        title=title,
        file_name=f"chap_{i:04d}.xhtml",
        lang="ko"
    )

    chapter.content = html

    # CSS 연결
    chapter.add_item(css_item)

    book.add_item(chapter)
    chapters.append(chapter)

# -------------------
# 목차
# -------------------

book.toc = chapters

# 필수 파일
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# 읽기 순서
book.spine = ["nav"] + chapters

# 저장
epub.write_epub(
    "논어의 문법적 구조.epub",
    book
)

print(f"완료! {len(chapters)}개 챕터 저장")
