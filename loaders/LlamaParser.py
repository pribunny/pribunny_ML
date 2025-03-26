import os

from llama_parse import LlamaParse
from PyPDF2 import PdfReader, PdfWriter

import nest_asyncio

"""
입력 받은 파일을 파싱해서 넘겨줌
PDF는 한 장씩 파싱
Todo
 파일 인덱싱 못할 때, 예외 처리
"""


nest_asyncio.apply()

def get_parser():
    api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
    print(api_key)
    #파서 설정
    parser = LlamaParse(
        api_key = api_key,
        result_type="markdown",
        num_workers=4,
        verbose=True,
        language= "ko",
    )

    return parser

def split_pdf_by_page(input_pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    reader = PdfReader(input_pdf_path)
    page_paths = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        page_path = os.path.join(output_dir, f"page_{i+1}.pdf")
        with open(page_path, "wb") as f:
            writer.write(f)
        page_paths.append(page_path)

    return page_paths

def parse_pages_to_md(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    parser = get_parser()

    for i, page_path in enumerate(file_path):
        print(f"Parsing page {i+1}: {page_path}")
        documents = parser.load_data(page_path)

        md_output_path = os.path.join(output_dir, f"page_{i+1}.md")
        with open(md_output_path, "w", encoding="utf-8") as f:
            f.write(documents[0].text)

        print(f"Saved: {md_output_path}")

def split_by_paragraph(text):
    # 문단 단위 분리(빈 줄 있는 경우)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def merge_short_paragraphs(paragraphs, min_length=200):
    # 짧은 문단 합치기
    merged = []
    buffer = ""

    for para in paragraphs:
        if len(buffer) + len(para) < min_length:
            buffer += " " + para
        else:
            if buffer:
                merged.append(buffer.strip())
            buffer = para
    if buffer:
        merged.append(buffer.strip())

    return merged

def process_md_files(md_dir, source_name, source_type):
    # 파일을 청크 단위로 나눠서 저장
    all_chunks=[]

    for filename in sorted(os.listdir(md_dir)):
        if not filename.endswith(".md"):
            continue

        page_number = int(filename.split('_')[1].split('.')[0])
        file_path = os.path.join(md_dir, filename)

        with open(file_path, "r", encoding='utf-8') as f:
            text = f.read()

        paragraphs = split_by_paragraph(text)
        chunks = merge_short_paragraphs(paragraphs, min_length=200)

        for i, chunk in enumerate(chunks):
            chunk_data = {
                "metadata": {
                    "source": source_name,
                    "type": source_type,
                    "page_number": page_number,
                    "chunk_index": i,
                },
                "text": chunk,
            }
            all_chunks.append(chunk_data)

    return all_chunks