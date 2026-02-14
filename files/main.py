# from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()
embeddings = OpenAIEmbeddings()
# emb = embeddings.embed_query("I love data science!")
# print(emb)

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=100
)

# loader = TextLoader("facts.txt")
loader = PyPDFLoader("sample.pdf")

# docs = loader.load()
# print(docs)

docs = loader.load_and_split(
    text_splitter=text_splitter
)

# for doc in docs:
#     print(doc.page_content)
#     print("\n")

db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="emb"
)

# results = db.similarity_search_with_score( # or similarity_search
#     "What are generalized linear models?",
#     k=3 # default is 4
# )

# for result in results:
#     # print(result.page_content) # if using similarity_search
#     # print("---" * 10)
#     # print(result.metadata)
#     # print("---" * 10)
#     print(result[1])
#     print("---" * 10)
#     print(result[0].page_content)
#     print("\n")

results = db.similarity_search(
    "What are generalized linear models?"
)

for result in results:
    print("\n")
    print(result.page_content)
