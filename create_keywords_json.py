from dotenv import load_dotenv
load_dotenv()
from tqdm import tqdm
import time
import json
import pandas as pd
from extract_keywords import extract_keywords, extract_few_shot_keywords, extract_keywords_cot

def main():
    with open("data/product_enriched.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        df = pd.DataFrame(json_data)
        df = df.set_index("id")
    data = []
    try:
        for idx, row in tqdm(df.iterrows(), total=len(df)):
            text = row["content"]
            _, keywords = extract_keywords(text)
            # _, few_shot_keyword = extract_few_shot_keywords(text)
            # keywords += few_shot_keyword
            _, cot_keywords = extract_keywords_cot(text)
            keywords += cot_keywords
            keywords = [keyword.strip().replace('\n', '') for keyword in keywords]
            data.append({
                'id': idx,
                'keywords': list(set(keywords))
            })
            # Prevent TPM limit :(
            time.sleep(5)
    except:
        with open("data/keywords_intermediate.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
    with open("data/keywords.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

if __name__ == '__main__':
    main()