import os
from pathlib import Path
from dotenv import load_dotenv
from glob import glob

from llama_parse import LlamaParse
from PyPDF2 import PdfReader, PdfWriter
from langchain_core.documents import Document

import nest_asyncio
import time

"""
입력 받은 파일을 파싱해서 넘겨줌
PDF는 한 장씩 파싱
Todo
 파일 인덱싱 못할 때, 예외 처리
"""
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

nest_asyncio.apply()

def get_parser():
    api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
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

    failed_pages = []
    retry_pages = []

    for i, page_path in enumerate(file_path):
        print(f"Parsing page {i+1}: {page_path}")
        try:
            documents = parser.load_data(page_path)

            md_output_path = os.path.join(output_dir, f"page_{i+1}.md")
            with open(md_output_path, "w", encoding="utf-8") as f:
                f.write(documents[0].text)

            print(f"Saved: {md_output_path}")
            time.sleep(1)  # 슬립 추가
        except Exception as e:
            print(f"Failed to parse page{i+1}: {page_path}")
            print(f"Error: {e}")
            retry_pages.append({
                "page_num": i + 1,
                "page_path": page_path
            })

    time.sleep(1)  # 슬립 추가

    if retry_pages:
        for page in retry_pages:
            try:
                documents = parser.load_data(page["page_path"])
                md_output_path = os.path.join(output_dir, f"page_{page["page_num"]}.md")
                with open(md_output_path, "w", encoding="utf-8") as f:
                    f.write(documents[0].text)
                print(f"Saved: {md_output_path}")
            except Exception as e:
                print(f"Failed to parse page{i+1}: {page["page_path"]}")
                print(f"Error: {e}")

                failed_pages.append(page["page_path"])

        return failed_pages

def split_by_paragraph(text):
    # 문단 단위 분리(빈 줄 있는 경우)
    paragraphs = [p.strip() for p in text.split('#') if p.strip()]
    return paragraphs

def merge_short_paragraphs(paragraphs, min_length=500):
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

def law_chunks(input_dir = '../data/pdf/법률', output_dir = 'output/txt'):
    laws = os.listdir(input_dir)

    chunks = []

    for law in laws:
        input_path = os.path.join(input_dir, law)

        chunks_by_clause = os.listdir(input_path)
        for clause in chunks_by_clause:
            clause_path = os.path.join(input_path, clause)
            with open(clause_path, 'r', encoding='utf-8') as f:
                content = f.read()

            title = clause.split('_')
            chapter = title[0] # 장
            section = title[1] # 절
            clause_name = title[2] # 조
            delete = False
            if title[3] == '삭제':
                delete = True
            metadata = {
                "chapter": chapter,
                "section": section,
                "clause": clause_name,
                "type": "법률",
                "delete": delete,
            }
            doc = Document(page_content=content, metadata=metadata)
            chunks.append(doc)

    return chunks

from utils.chromaDB_client import get_vectorstore

vectorstore=get_vectorstore(collection_name="test")
chunks = law_chunks()

vectorstore.add_documents(chunks)


