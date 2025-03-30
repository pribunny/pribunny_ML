from bs4 import BeautifulSoup

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")

    # 불필요한 script/style 제거
    for tag in soup(["script", "style"]):
        tag.decompose()

    # 텍스트 추출
    text = soup.get_text(separator="\n")

    # 공백 정리
    clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    return clean_text

