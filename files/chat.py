import warnings

warnings.filterwarnings(
    "ignore", 
    category=UserWarning,
    message="None of PyTorch, TensorFlow >= 2.0, or Flax have been found.*"
)

# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()
embeddings = OpenAIEmbeddings()

db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings
)
retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    chain_type="stuff"
)

result = chain.invoke("What is a normal equation?")
print(result)
