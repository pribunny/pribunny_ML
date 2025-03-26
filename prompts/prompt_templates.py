from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful assistant. Only use the following context to answer the question.\n"
        "Only use the provided context and cite sources if relevant.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )
)