import os
import json
import openai
import pdfcrowd
from jinja2 import Template

# API-Keys aus Streamlit Secrets lesen, wenn verfügbar (Cloud)
try:
    import streamlit as st
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    pdfcrowd_username = st.secrets["PDFCROWD_USERNAME"]
    pdfcrowd_api_key = st.secrets["PDFCROWD_API_KEY"]
except ImportError:
    # Fallback lokale Entwicklung (z.B. .env)
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pdfcrowd_username = os.getenv("PDFCROWD_USERNAME")
    pdfcrowd_api_key = os.getenv("PDFCROWD_API_KEY")

def generate_cv_json(kurzprofil):
    prompt = f"""
    Du bist ein professioneller Lebenslauf-Generator.
    ...
    Eingabe:
    {kurzprofil}
    Gib nur das JSON-Objekt zurück, keine weiteren Erklärungen.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=2000
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print(f"Fehler: {e}")
        return None

def generate_pdf(cv_data, output_path="generated_cv.pdf"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(BASE_DIR, "cv_template.html")

    with open(template_path, "r", encoding="utf-8") as file:
        template_str = file.read()

    template = Template(template_str)
    html_content = template.render(cv=cv_data)

    client = pdfcrowd.HtmlToPdfClient(pdfcrowd_username, pdfcrowd_api_key)

    with open(output_path, "wb") as f:
        client.convertStringToFile(html_content, f)

    return output_path
