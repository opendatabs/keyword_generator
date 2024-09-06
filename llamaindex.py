import os
import openai
import httpx
from llama_index.llms.openai import OpenAI
from llama_index.core.extractors import (
    QuestionsAnsweredExtractor,
    KeywordExtractor,
)
from llama_index.core import Document
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.ingestion import IngestionPipeline

MAX_TOKENS = 4096 

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=MAX_TOKENS, chunk_overlap=128
)


proxy_url = os.environ.get("PROXY_URL")
model = "gpt-4o" # "gpt-4o-mini"
llm = OpenAI(temperature=0.7, model=model,api_key=os.getenv("OPENAI_API_KEY"), http_client=httpx.Client(proxy=proxy_url), max_tokens=MAX_TOKENS)

KEYWORD_EXTRACT_TEMPLATE = """\
{context_str}. Give {keywords} unique keywords for this \
document. The keywords should match with search queries of users to find this document. Do not copy terms from the document. For each keyword propose synonyms in simple language. Do not include numbers, years and Basel-Stadt in your keyword proposal. Only German keywords. Think very hard. Format as comma separated. Keywords: """

extractors = [
    # QuestionsAnsweredExtractor(questions=3, llm=llm),
    KeywordExtractor(keywords=30, llm=llm, prompt_template=KEYWORD_EXTRACT_TEMPLATE),
]

transformations = [text_splitter] + extractors

pipeline = IngestionPipeline(transformations=transformations)


def extract_keywords_llama_index(text: str):
    docs = [Document(text=text)]
    stata_nodes = pipeline.run(documents=docs)

    keywords = stata_nodes[0].metadata
    keywords = keywords["excerpt_keywords"].split(",")
    return keywords