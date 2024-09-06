import os

import marvin
import openai
from llama_index.core import Document
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.extractors.marvin import MarvinMetadataExtractor
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, Field

marvin.settings.openai.api_key = os.environ["OPENAI_API_KEY"]
marvin.settings.openai.chat.completions.model = "gpt-4o" # "gpt-4o-mini" 


num_keywods = 20

class StatAMetaData(BaseModel):
    keywords: str = Field(
        ...,
        description=f"Eine Liste der {num_keywods} wichtigsten Suchbegriffen und Synonimen um den Text besser zu Indexieren. Keine Zahlen.",
    )


node_parser = TokenTextSplitter(separator=" ", chunk_size=512, chunk_overlap=128)


metadata_extractor = MarvinMetadataExtractor(marvin_model=StatAMetaData)
pipeline = IngestionPipeline(transformations=[node_parser, metadata_extractor])


def extract_keywords_marvin(text: str):
    documents = [Document(text=text)]
    nodes = pipeline.run(documents=documents, show_progress=True)
    keywords = nodes[0].metadata["marvin_metadata"]["keywords"].split(",")
    return keywords
