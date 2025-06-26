import streamlit as st
import openai
import pdfcrowd
import json
import os
from dotenv import load_dotenv
from jinja2 import Template

# .env laden
load_dotenv()

# pdfcrowd API-Daten aus .env lesen
PDFCROWD_USERNAME = os.getenv("PDFCROWD_USERNAME")
PDFCROWD_API_KEY = os.getenv("PDFCROWD_API_KEY")

# OpenAI API-Key aus .env lesen
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cv_text(kurzprofil):
    prompt = f"""
Du bist ein professioneller Lebenslauf-Generator.

Deine Aufgabe: Erstelle aus dem folgenden Kurzprofil einen vollständigen, strukturierten Lebenslauf im korrekten JSON-Format.

⚠️ Regeln:
- Gib ausschließlich ein gültiges JSON-Objekt aus. Keine Einleitung, keine Erklärung, keine Kommentare.
- Das JSON muss exakt dieser Struktur entsprechen:

{{
    "name": "Vorname Nachname",
    "birth_year": "Geburtsjahr",
    "location": "Wohnort",
    "marital_status": "Familienstand",
    "nationality": "Staatsangehörigkeit",
    "contact": {{
        "email": "E-Mail",
        "phone": "Telefonnummer"
    }},
    "career_goal": "Berufsziel",
    "work_experience": [
        {{
            "position": "Position",
            "company": "Firma",
            "period": "Zeitraum (z.B. seit 05/2019 oder 07/2017 - 04/2019)",
            "tasks": [
                "Aufgabe 1",
                "Aufgabe 2",
                "Aufgabe 3"
            ]
        }}
    ],
    "education": [
        {{
            "degree": "Abschluss",
            "institution": "Institution",
            "period": "Zeitraum"
        }}
    ],
    "salary_expectation": "Gehaltsvorstellung (z.B. 50.000 € brutto/Jahr)",
    "availability": "Verfügbarkeit (z.B. 1 Monat Kündigungsfrist)",
    "skills": {{
        "fachkompetenz": ["Fachkenntnis 1", "Fachkenntnis 2"],
        "personal_strengths": ["Stärke 1", "Stärke 2"],
        "software": ["Software 1", "Software 2"],
        "languages": ["Sprache 1", "Sprache 2"]
    }}
}}

Verwende folgende Eingabe als Basis für den Lebenslauf:
{kurzprofil}

Gib jetzt ausschließlich das vollständige JSON aus. Keine zusätzlichen Erklärungen oder Texte.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=2000,
    )

    text_response = response.choices[0].message.content.strip()

    if text_response.startswith("```json"):
        text_response = text_response.strip("```json").strip("```").strip()

    try:
        cv_json = json.loads(text_response)
    except json.JSONDecodeError as e:
        st.error(f"JSON Parsing Fehler: {e}")
        st.write("Antwort von GPT-4:")
        st.code(text_response)
        return None

    return cv_json

def render_cv_html(cv_json, template_path="template.html"):
    with open(template_path, "r", encoding="utf-8") as file:
        template_str = file.read()
    template = Template(template_str)
    return template.render(cv=cv_json)

def convert_html_to_pdf(html_content):
    client = pdfcrowd.HtmlToPdfClient(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
    pdf_bytes = client.convertString(html_content)
    return pdf_bytes

# Streamlit UI
st.title("Lebenslauf-Generator mit GPT-4 & PDF-Erstellung (pdfcrowd)")

kurzprofil = st.text_area("Kurzprofil eingeben", height=200)

if st.button("Lebenslauf generieren") and kurzprofil.strip():
    with st.spinner("Erzeuge Lebenslauf..."):
        cv_json = generate_cv_text(kurzprofil)
        if cv_json:
            st.success("Lebenslauf JSON erzeugt!")
            st.json(cv_json)

            html_output = render_cv_html(cv_json)
            st.markdown("---")
            st.markdown("### Vorschau Lebenslauf (HTML gerendert)")
            st.components.v1.html(html_output, height=800, scrolling=True)

            with st.spinner("Generiere PDF..."):
                try:
                    pdf_bytes = convert_html_to_pdf(html_output)
                    st.download_button(
                        label="📄 Lebenslauf als PDF herunterladen",
                        data=pdf_bytes,
                        file_name="lebenslauf.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"PDF-Erstellung fehlgeschlagen: {e}")
