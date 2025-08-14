from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.mistralai import MistralAI
from llama_index.core import Settings


pc = Pinecone(api_key="pcsk_6PUmzH_58RKsC3EDHpGHL5nFX6dfNfRBZz9vQKzYKUfjrQSJcSU4m8CQxkZnjsKdqw6FEf")
index_name = "paper-summarizer"
index = pc.Index(index_name)

vector_store = PineconeVectorStore(pc.Index(index_name))
storage_context = StorageContext.from_defaults(vector_store=vector_store)
llm = MistralAI(model="open-mistral-7b", api_key = "OAaFT0jM8jGshHiF2jUste5tX61rTSOP", max_tokens=1024)
embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.llm = llm
Settings.embed_model = embedding_model


index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

def answer_question(query):
    response = query_engine.query(query)
    return response


# if __name__ == "__main__":
#     print("Ask me anything! (type 'exit' to quit)\n")
#     while True:
#         query = input("Your question: ")
#         if query.lower() in ["exit", "quit"]:
#             print("Goodbye! 👋")
#             break
#         result = answer_question(query)
#         print("Answer:", result["answer"])
#         print("-" * 50)