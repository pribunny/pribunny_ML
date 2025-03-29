"""
문서 로더 메인 파일
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from glob import glob

from LlamaParser import split_pdf_by_page, parse_pages_to_md, process_md_files

from utils.chromaDB_client import get_vectorstore
from langchain_core.documents import Document

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

input_dir = '../data/pdf/법률'
output_dir = 'output'
parse_output = 'output/md'

pdf_files = glob(os.path.join(input_dir, '*.pdf')) # output dir 안에 있는 pdf 전체
all_failed_pages = []

i = 0

for input_pdf in pdf_files:

    if i==3:
        break

    basename = os.path.splitext(os.path.basename(input_pdf))[0]

    page_output_dir = os.path.join(output_dir, basename)
    md_output_dir = os.path.join(parse_output, basename)

    try:
        os.makedirs(page_output_dir, exist_ok=False)
        os.makedirs(md_output_dir, exist_ok=False)
    except FileExistsError as e:
        # 디렉토리가 존재하면 이미 파싱한 파일임
        print(f"❌ 디렉토리가 이미 존재합니다: {e.filename}")
        continue

    page_paths = split_pdf_by_page(input_pdf, page_output_dir)

    failed_pages = parse_pages_to_md(page_paths, md_output_dir)
    print(f"=============={basename} 파싱 실패 페이지 =================")
    if failed_pages:
        for failed_page in failed_pages:
            print(failed_page)

    print(f"{basename} 파싱 완료")

    raw_chunks = process_md_files(md_output_dir, basename, '법률')
    chunks = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in raw_chunks  # raw_chunks는 dict 리스트
    ]

    vectorstore=get_vectorstore(collection_name="test")

    # 문서 저장
    vectorstore.add_documents(chunks)

    print(f"{basename} chunks 저장 완료")
    i += 1

print("모든 파일 파싱 완료")