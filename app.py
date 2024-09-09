import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from extract_keywords import extract_keywords, extract_few_shot_keywords, extract_keywords_cot
import json



def show_pdf(file_url):
    pdf_js = f"""
    <iframe src="https://mozilla.github.io/pdf.js/web/viewer.html?file={url}" width=None height="600" style="border: none;"></iframe>
    """
    st.markdown(pdf_js, unsafe_allow_html=True)


st.set_page_config(layout="wide")
st.title("Keyword Extractor")

with open("data/product_enriched.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
    df = pd.DataFrame(json_data)
    df = df.set_index("id")


grouped_ids = df.groupby("produkt").groups

product_id_dict = {product: list(ids) for product, ids in grouped_ids.items()}

col1, col2, col3 = st.columns(3)

with col1:
    selected_product = st.selectbox("Select Product", list(product_id_dict.keys()))

with col2:
    selected_id = st.selectbox("Select ID", product_id_dict[selected_product])

with col3:
    run_extraction = st.button("Extract Keywords")

if run_extraction:
    if selected_id:
        data = df.loc[int(selected_id)]

        if isinstance(data, pd.Series) and "content" in data:
            url = data["url"]
            details_text = data["content"]

            message, keywords = extract_keywords(details_text)
            message_few_shot, keywords_few_shot = extract_few_shot_keywords(details_text)
            message_cot, keywords_cot = extract_keywords_cot(details_text)

            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.write(url)

                st.subheader("Extracted Keywords")
                st.write(", ".join(keywords))

                st.subheader("Extracted Keywords Few Shot")
                st.write(", ".join(keywords_few_shot))

                st.subheader("Extracted Keywords COT")
                st.write(", ".join(keywords_cot))

                st.subheader("Thought process: ")
                st.write(message_cot)
                
                st.subheader("Original Text")
                st.write(details_text)
            
            with result_col2:
                st.subheader("Webpage")
                if url.lower().endswith('.pdf'):
                    show_pdf(url)
                else:
                    st.components.v1.iframe(url, width=None, height=600, scrolling=True)
        else:
            st.error("Invalid data format or 'details' column not found.")
    else:
        st.warning("Please enter an ID.")

