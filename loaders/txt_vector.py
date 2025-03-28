import os
from langchain_core.documents import Document
from utils.chromaDB_client import get_chroma_client

# 1. 파일명 불러오기
path = '../data/txt'

docs = [f for f in os.listdir(path) if f.endswith('.txt')] #각 파일명이 들어있는 리스트

### 첫 번째부터, 해당 파일과 동일한 이름 파일 수 확인 -> 파일명과 함께 수 저장
text_file_list = {}
for i in docs:
    base_name = i.split('(')[0]
    if base_name in text_file_list:
        text_file_list[base_name] += 1
    else:
        text_file_list[base_name] = 1

# 2. 불러온 파일을 청킹 -> 그런데, 이미 손수 데이터를 잘랐다. 내가.
# 3. 청킹 데이터에 메타데이터 추가 -> source_name(파일이름),type(판례/기타), page_number, date(판례만)
def add_metadata(source_name, num_of_files):
    chunk_data_list = []
    for num in range(num_of_files):

        chunk_name = f'{source_name}({num+1})'
        with open(f'../data/txt/{chunk_name}.txt', encoding='utf-8') as c : #파일 내용 불러오기
            chunk = c.read()

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
        chunk_data_list.append(chunk_data)

    return chunk_data_list

##  판례데이터는 임의로 잘린데이터를 페이지로 구분하도록 함. (토큰 수 맞게 잘랐으니까)
# 4. 생성된 최종 데이터를 합쳐서 반환
# 5. 청킹한 데이터를 Document 형태로 저장
vectorstore = get_chroma_client(collection_name="test")

for key in text_file_list.keys():
    print("="*20)
    print(f'{key}파일의 메타데이터를 넣는 중')
    raw_chunks = add_metadata(key, text_file_list[key])

    for i in raw_chunks:
        print(i)

    chunks = [
        Document(page_content=chunk["text"], metadata=chunk["metadata"])
        for chunk in raw_chunks
    ]
    vectorstore.add_documents(chunks)
