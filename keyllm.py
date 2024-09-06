import openai
from keybert.llm import OpenAI
from keybert import KeyLLM
import httpx
import os

proxy_url = os.environ.get("PROXY_URL")
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), http_client=httpx.Client(proxy=proxy_url)
)
openai_llm = OpenAI(client)
kw_model = KeyLLM(openai_llm)


def extract_keywords_keyllm(text: str, check_vocab: bool = False):
    docs = [text]
    keywords = kw_model.extract_keywords(docs, check_vocab=check_vocab)
    return keywords[0]
