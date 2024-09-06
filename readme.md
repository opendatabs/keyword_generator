# Automatically create keywords for stata.bs.ch

Create keywords for indicators, tables, articles, applications, grafics, datasets, dashboards and so on to enrich the meta data used to find products on stata.bs.ch

## Setup

Execute those commands to setup the project:

1. `python -m virtualenv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt --no-build-isolation`
4. Create a copy of `.env.example` and name it `.env`
5. Add your OpenAI API key to `.env` file under `OPENAI_API_KEY=`
6. Add your proxy credentials to `.env` `PROXY_URL=`
