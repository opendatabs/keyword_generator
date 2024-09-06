import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from mrvn import extract_keywords_marvin
from llamaindex import extract_keywords_llama_index
from keyllm import extract_keywords_keyllm
import json

def show_pdf(file_url):
    pdf_js = f"""
    <iframe src="https://mozilla.github.io/pdf.js/web/viewer.html?file={url}" width=None height="600" style="border: none;"></iframe>
    """
    st.markdown(pdf_js, unsafe_allow_html=True)

load_dotenv()
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

            # keyllm_keywords = extract_keywords_keyllm(details_text)
            # marvin_keywords = extract_keywords_marvin(details_text)
            llama_index_keywords = extract_keywords_llama_index(details_text)

            result_col1, result_col2 = st.columns(2)
            
            with result_col1:
                st.write(url)

                # st.subheader("Extracted Keywords KeyLLM")
                # st.write(", ".join(keyllm_keywords))

                # st.subheader("Extracted Keywords Marvin")
                # st.write(", ".join(marvin_keywords))

                st.subheader("Extracted Keywords")
                st.write(", ".join(llama_index_keywords))
                
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

