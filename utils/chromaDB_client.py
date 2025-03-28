import os

import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import Optional, List

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # 상위 폴더
persist_path = os.path.join(project_root, "chroma_db")

def get_chroma_client(
    persist_dir: str = persist_path,
    embedding_model: Optional[OpenAIEmbeddings] = None,
    collection_name: Optional[str] = None
) -> Chroma:
    """
    Chroma 벡터스토어 클라이언트를 반환
    
    :param persist_dir: Chroma 저장 경로
    :param embedding_model: 사용할 임베딩 모델
    :param collection_name: 컬렉션 이름
    :return: 
    """

    api_key = os.environ.get("OPENAI_API_KEY")

    if embedding_model is None:
        embedding_model = OpenAIEmbeddings(openai_api_key=api_key)

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model,
        collection_name=collection_name
    )

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")