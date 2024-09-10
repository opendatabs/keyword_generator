import os
from openai import OpenAI
import httpx

MAX_TOKENS = 4096

proxy_url = os.environ.get("PROXY_URL")
model = "gpt-4o"  # "gpt-4o-mini"
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(proxy=proxy_url),
)

SYSTEM_PROMPT = """You are a SEO expert and your goal is to improve the meta data for the given document. \
                Come up with at most 20 unique keywords for this document. \
                The keywords should match with search queries of potential users that are trying to find this document. \
                Do not copy terms from the document. \
                For each proposed keyword include synonyms using simple A2 level language. \
                Include the synonyms directly in your output list. \
                Do not include numbers, years and Basel-Stadt or Basel in your keyword proposal. \
                Only German keywords. \
                Use Swiss German writing, i.e. use ss instead of ß. \
                Do not number the keywords. \
                Synonyms should also be seperated by a comma from the initial keyword. \
                Format keywords as comma separated list at the end of your answer after 'Keywords:'"""


SYSTEM_PROMPT_FEW_SHOT = """You are a SEO expert and your goal is to improve the meta data for the given document. \
                Come up with at most 20 unique keywords for this document. \
                The keywords should match with search queries of potential users that are trying to find this document. \
                Do not copy terms from the document. \
                For each proposed keyword include synonyms using simple A2 level language. \
                Include the synonyms directly in your output list. \
                Do not include numbers, years and Basel-Stadt or Basel in your keyword proposal. \
                Only German keywords. \
                Use Swiss German writing, i.e. use ss instead of ß. \
                Do not number the keywords. \
                Synonyms should also be seperated by a comma from the initial keyword. \
                Format keywords as comma separated list at the end of your answer after 'Keywords:' \
                Document: '''Teuerungsrechner 05 Preise Basler Index der Konsumentenpreise Mit dieser Anwendung können Sie mit dem Basler Index indexierte Beträge (z.B. Alimentenzahlungen, Renten, usw.) oder die Teuerungsrate für einen beliebigen Zeitraum berechnen. Sie haben die Möglichkeit, die Indexreihen mit jahresdurchschnittlichen (ab 1915) oder monatlichen (ab 1940) Werten für die Berechnung zu verwenden.'''  \
                Keywords: Inflation berechnen, Preisindex Schweiz, Konsumentenpreisindex, Teuerungsrate Schweiz, Lebenshaltungskosten Schweiz, Indexierte Beträge berechnen, Inflationsrechner, Preisentwicklung Schweiz, Preisveränderung Schweiz, Teuerung Schweiz, Kostensteigerung Schweiz, Preissteigerung, Inflationsrate, Preisvergleich, Konsumentenpreise, Preisstatistik, Preisänderung, Kosten, Lohnentwicklung \
                Document: '''Grenzwertüberschreitungen Ozon \n Anzahl Überschreitungen des Stunden-Grenzwertes pro Jahr, Region Basel \n Im Jahr 2023 lagen in Basel-Stadt 304 Stunden-Mittelwerte über dem Grenzwert für Ozon. Laut Luftreinhalte-Verordnung dürfte der Grenzwert höchstens einmal pro Jahr überschritten werden. \n Anzahl Stunden-Mittelwerte pro Jahr, welche über dem in der Luftreinhalte-Verordnung (LRV) gesetzlich festgelegten Grenzwert von 120 μg/m<sup>3</sup> liegen, unterschieden nach Art der Lage der Messstationen: Ländliche Höhenlagen (Chrischona, Brunnersberg, Chaumont (NABEL)), Agglomeration (Binningen (NABEL), Dornach (SO)), Stadt Basel (Basel St.Johanns-Platz).<br>Ozon ist ein sekundärer Luftschadstoff, es wird bei intensiver Sonneneinstrahlung aus den Vorläuferschadstoffen Stickstoffoxiden und flüchtigen organischen Verbindungen in Kombination mit Sauerstoff gebildet. In städtischen Gebieten ist die Ozonkonzentration in der Regel tiefer als in ländlichen, da Stickstoffmonoxid aus Autoabgasen mit Ozon reagiert und dieses so abgebaut wird.''' \
                Keywords: Ozonbelastung, Ozonwerte, Luftverschmutzung, Luftqualität, Luftreinhalte-Verordnung, Grenzwertüberschreitung, Luftschadstoffe, städtische Luftqualität, ländliche Luftqualität, Messstationen, Ozonbildung, Stickstoffoxide, Abgas, Autoabgase, Luftüberwachung, Umweltverschmutzung, Luftreinheit, Schadstoffmessung, Luftschutz, Verschmutzung Vororte \
                """

SYSTEM_PROMPT_COT = """You are a SEO expert and your goal is to improve the meta data for the given document. \
                Come up with at most 20 unique keywords for this document. \
                The keywords should match with search queries of potential users that are trying to find this document. \
                Do not copy terms from the document. \
                The keywords should be relevant for the document and highlight the unique characteristics of this document. \
                For each proposed keyword include synonyms using simple A2 level language. \
                Include the synonyms directly in your output list. \
                Do not include numbers, years and Basel-Stadt or Basel in your keyword proposal. \
                Do not use generic terms such as Zeit, Zeitspanne, Monat, Software, Summe, Durchschnitt, Berichte. \
                Only German keywords. \
                Use Swiss German writing, i.e. use ss instead of ß. \
                Do not number the keywords. \
                Synonyms should also be seperated by a comma from the initial keyword. \
                Format keywords as comma separated list at the end of your answer after Keywords: \
                Let's think step by step. """

KEYWORD_EXTRACT_TEMPLATE = """\
<document> {context_str} </document>. \
You are a SEO expert and your goal is to improve the meta data for the given document. \
Come up with at most {keywords} unique keywords for this document. \
The keywords should match with search queries of potential users that are trying to find this document. \
Do not copy terms from the document. \
For each keyword propose synonyms using simple A2 language. \
Do not include numbers, years and Basel-Stadt in your keyword proposal. \
Only German keywords. \
Use Swiss German writing, i.e. use ss instead of ß. \
Format keywords as comma separated at the end of your anser. \
Let's think step by step. """
# Keywords: """

def extract_keywords(text: str):
    response = llm.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "system",
            "content": SYSTEM_PROMPT
            },
            {
            "role": "user",
            "content": f'"""{text}"""'
            }
        ],
        temperature=0.5,
        max_tokens=MAX_TOKENS,
        top_p=1
        )
    message = response.choices[0].message.content
    keywords = message.split("Keywords:")[-1]
    keywords = keywords.split(",")
    return message, keywords

def extract_few_shot_keywords(text: str):
    response = llm.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "system",
            "content": SYSTEM_PROMPT_FEW_SHOT
            },
            {
            "role": "user",
            "content": f"""Document: '''{text}''' \
                Keywords: """
            }
        ],
        temperature=0.5,
        max_tokens=MAX_TOKENS,
        top_p=1
        )
    message = response.choices[0].message.content
    keywords = message.split("Keywords:")[-1]
    keywords = keywords.split(",")
    return message, keywords

def extract_keywords_cot(text: str):
    response = llm.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "system",
            "content": SYSTEM_PROMPT_COT
            },
            {
            "role": "user",
            "content": f'Dokument: """{text}"""'
            }
        ],
        temperature=0.5,
        max_tokens=MAX_TOKENS,
        top_p=1
        )
    message = response.choices[0].message.content
    keywords = message.split("Keywords:")[-1]
    keywords = keywords.split(",")
    return message, keywords