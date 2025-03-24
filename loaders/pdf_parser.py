"""
PDF parser 테스트 코드
"""
import os.path
import re

from nltk.corpus.reader import documents

# PymuPDF4LLM
from .PymuPDF4LLM_Parser import change_pdf_to_md
from llama_index.core.schema import Document
from langchain_community.document_loaders import UnstructuredPDFLoader, PyMuPDFLoader

def pdf_to_document():
    data_path = "(2024.4.) 해외사업자의 개인정보 보호법 적용 안내서_국문_최종.pdf"

    md_pages = change_pdf_to_md(data_path)

    documents = []

    for i, md in enumerate(md_pages):
        doc = Document(text=md["text"], metadata=md["metadata"])
        documents.append(doc)

    return documents