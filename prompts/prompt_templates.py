from llama_index.core.prompts import PromptTemplate

# 커스텀 프롬프트
test_prompt = PromptTemplate(
    "You are a helpful assistant. Only use the following context to answer the question.\n"
    "Only use the provided context and cite sources if relevant.\n\n"
    "Context:\n{context_str}\n\n"
    "Question: {query_str}\n\n"
    "Answer:"
)