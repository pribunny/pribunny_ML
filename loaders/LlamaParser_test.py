#pip install llama-parse

import os
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import nest_asyncio
from dotenv import load_dotenv

load_dotenv(".env")
nest_asyncio.apply()

api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
#파서 설정
parser = LlamaParse(
    api_key = api_key,
    result_type="markdown",
    num_workers=4, #worker의 수 -> worker가 뭔데?
    verbose=True,
    language= "ko",
)

# #SimpleDirectoryReader를 사용해 파싱
# file_extractor = {".pdf" : parser}
#
# #LlamaParse로 파일 파싱
# documents = SimpleDirectoryReader(
#     input_files=["test.pdf"],
#     file_extractor=file_extractor,
# ).load_data()

documents = parser.load_data("test.pdf") #data 경로 넣어주기
print(documents[1].text)