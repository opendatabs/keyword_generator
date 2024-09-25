from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from extract_keywords import extract_keywords, extract_keywords_cot, extract_few_shot_keywords

app = Flask(__name__)

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_api():
    data = request.get_json()
    text = data['text']

    _, keywords = extract_keywords(text)
    _, few_shot_keywords = extract_few_shot_keywords(text)
    _, cot_keywords = extract_keywords_cot(text)
    keywords += cot_keywords
    keywords += few_shot_keywords
    keywords = [keyword.strip().replace('\n', '') for keyword in keywords]
    unique_keywords = list(set(keywords))

    return jsonify({'keywords': unique_keywords})

if __name__ == '__main__':
    app.run(debug=False) 
