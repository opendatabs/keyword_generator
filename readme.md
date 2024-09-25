# Keyword Enhancer for stata.bs.ch 

**Boost search discoverability on stata.bs.ch!**

This project aims to automatically generate relevant keywords for various content types on stata.bs.ch (indicators, tables, articles, etc.), enhancing the platform's search functionality and making it easier for users to find what they need.

## Features

* **Automated keyword extraction:** Leverages OpenAI's language models for intelligent keyword generation.
* **Flexible API:**  Provides a simple API for keyword extraction on-demand.
* **Streamlit App:**  Offers an interactive interface for keyword generation from StatApp data dumps.
* **Dockerized deployment:** Supports easy deployment using Docker for streamlined setup.

## Getting Started

### Prerequisites

* Python (3.9 or higher)
* An OpenAI API key
* (Optional) A StatApp products dump in JSON format (`data/products.json`) if you plan to use the Streamlit app or generate `keywords.json`.

### Installation

1. **Clone the repository:** `git clone https://github.com/opendatabs/keyword_generator.git`
2. **Create a virtual environment:** `python -m venv venv`
3. **Activate the environment:** 
    * Windows: `.\venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`
4. **Install dependencies:** `pip install -r requirements.txt --no-build-isolation`
5. **Configure the environment:**
    * Copy `.env.example` to `.env`
    * Add your OpenAI API key: `OPENAI_API_KEY=<your-key>`
    * (Optional) Add your proxy credentials if needed: `PROXY_URL=<your-proxy-url>`

## Usage

### API

1. **Start the API server:** `python keywords_apy.py`
2. **Test with cURL:**

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"text": "Your sample text here"}' http://127.0.0.1:5000/extract_keywords

3. Integrate the API: Use the `/extract_keywords` endpoint in your applications to generate keywords dynamically.

### Streamlit App (Optional)

1. **Prepare data:**
    * Place a dump of the StatApp products at `data/products.json`.
    * Run python `utils.py` to generate `data/products_enriched.json`.
2. **Launch the app:** `streamlit run app.py`
3. **Interact:** Use the app's interface to explore and generate keywords from your data.

### Docker Deployment (Optional)

1. **Build the image:** `docker-compose up --build`
2. **Access the API:** The API will be available at `http://localhost:5000/extract_keywords.`
