"""
문서 로더 메인 파일
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from LlamaParser import split_pdf_by_page, parse_pages_to_md, process_md_files

from utils.chromaDB_client import get_chroma_client
from langchain_core.documents import Document

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

input_pdf = '../data/pdf/개인정보 처리 통합 안내서(안)(2024.12).pdf'
output_dir = 'output'
parse_output = 'output/md'

# page_paths = split_pdf_by_page(input_pdf, output_dir)
#
# parse_pages_to_md(page_paths, parse_output)
#
# print("파싱 완료")

raw_chunks = process_md_files(parse_output, '개인정보 처리 통합 안내서(안)(2024.12)', '안내서')
print(os.listdir(output_dir))
for i in raw_chunks:
    print(i)
chunks = [
    Document(page_content=chunk["text"], metadata=chunk["metadata"])
    for chunk in raw_chunks  # raw_chunks는 dict 리스트
]

vectorstore = get_chroma_client(collection_name="test")

# 문서 저장
vectorstore.add_documents(chunks)

print("문서 수:", vectorstore._collection.count())  # ✅ 저장 확인
# 재불러오기
vectorstore = get_chroma_client(collection_name="test")
print("문서 수:", vectorstore._collection.count())  # ✅ 저장 확인