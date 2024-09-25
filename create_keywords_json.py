from dotenv import load_dotenv

from tqdm import tqdm
import json
import pandas as pd
import os
load_dotenv()
from extract_keywords import extract_keywords, extract_keywords_cot

def main():
    """
    Create keywords for all products in data/products_enriched.json
    Result is stored in data/keywords.json

    Combines the detected keywords from `extract_keywords` and `extract_keywords_cot`
    """
    with open("data/product_enriched.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        df = pd.DataFrame(json_data)
        df = df.set_index("id")
    data = []
    if os.path.exists("data/keywords_intermediate.json"):
        with open("data/keywords_intermediate.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        known_idx = [element['id'] for element in data]
    try:
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            if idx in known_idx:
                 continue
            text = row["content"]
            # cut off text due to TPM limit
            tpm = 25_000
            if len(text) > tpm:
                 print(len(text))
                 text = text[:tpm]
            _, keywords = extract_keywords(text)
            _, cot_keywords = extract_keywords_cot(text)
            keywords += cot_keywords
            keywords = [keyword.strip().replace('\n', '') for keyword in keywords]
            data.append({
                'id': idx,
                'keywords': list(set(keywords))
            })
    except Exception as e:
        with open("data/keywords_intermediate.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        raise e
    with open("data/keywords.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

if __name__ == '__main__':
    main()