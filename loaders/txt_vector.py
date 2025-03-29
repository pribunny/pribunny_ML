import os
import re
from langchain_core.documents import Document
from utils.chromaDB_client import get_vectorstore

# 1. 파일명 불러오기
# 2. 불러온 파일을 청킹 -> 그런데, 이미 손수 데이터를 잘랐다. 내가.
# 3. 청킹 데이터에 메타데이터 추가 -> source_name(파일이름),type(판례/기타), page_number, date(판례만)
# 4. 생성된 최종 데이터를 합쳐서 반환
# 5. 청킹한 데이터를 Document 형태로 저장

def get_file_list(docs):

    text_file_list = {}
    for i in docs:
        print(f"파일명 확인중 : {i}")
        base_name = get_base_name(i)
        if base_name in text_file_list:
            print(f"새로운 파일명 확인 : {base_name}")
            text_file_list[base_name] += 1
        else:
            print(f"기존 파일명 확인 : {base_name}")
            text_file_list[base_name] = 1
        print(f"현재 파일명 딕셔너리 : {text_file_list}")
        print("="*10)
    return text_file_list


def get_base_name(filename):
    filename = re.sub(r'\.txt$','',filename) #먼저 확장자 지우기 -> 숫자가 없는 파일을 위해
    return re.sub(r'\(\d+\)$','',filename) #이후에, 숫자 지우기

def get_date(filename):
    match = re.search(r'\d{4}\. ?\d{1,2}\. ?\d{1,2}\.', filename)
    if match:
        return match.group().strip()
    return None

def add_metadata(source_name, num_of_files):
    chunk_data_list = []
    for num in range(num_of_files):

        if num_of_files == 1: #파일이 하나만 존재할때
            chunk_name =  source_name

        else : #파일이 여러 개
            chunk_name = f'{source_name}({num+1})'
        with open(f'../data/txt/{chunk_name}.txt', encoding='utf-8') as c : #파일 내용 불러오기
            chunk = c.read()

        date = get_date(source_name) #날짜 데이터 넣기

        source_type = "" #데이터 종류 선택
        if "선고" in source_name:
            source_type = '판례'

        else:
            source_type = 'Q&A'

        chunk_data = {
            "metadata" : {
                "source": source_name,
                "type": source_type,
                "page_number": num+1,
            },
            "text" : chunk,
        }

        if date is not None:
            chunk_data["metadata"]["date"] = date

        chunk_data_list.append(chunk_data)

    return chunk_data_list


# 여기서부터 시작
path = '../data/txt'
docs = [f for f in os.listdir(path) if f.endswith('.txt')] #각 파일명이 들어있는 리스트

base_name_list = get_file_list(docs)

vectorstore=get_vectorstore(collection_name="test")

for key in base_name_list.keys():
    print("="*20)
    print(f'{key}파일의 메타데이터를 넣는 중')
    raw_chunks = add_metadata(key, base_name_list[key])

    for i in raw_chunks:
        print(i)

    chunks = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in raw_chunks
    ]
    vectorstore.add_documents(chunks)

print("완료!")
