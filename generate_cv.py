import streamlit as st
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import pdfcrowd
import openai
import json

# Umgebungsvariablen laden
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDFCROWD_USERNAME = os.getenv("PDFCROWD_USERNAME")
PDFCROWD_API_KEY = os.getenv("PDFCROWD_API_KEY")

openai.api_key = OPENAI_API_KEY

st.title("Lebenslauf Generator mit KI-Unterstützung")

st.header("Kurzprofil eingeben")

kurzprofil_text = st.text_area("Beschreibe das Kurzprofil", height=200)

def generate_cv_text(kurzprofil):
    prompt = f"""
    Du bist ein erfahrener Karriereberater und Bewerbungsexperte. Erstelle aus folgendem Kurzprofil einen vollständig formulierten, professionellen Lebenslauf in deutscher Sprache.

    Bitte erstelle den Lebenslauf mit den folgenden Abschnitten:
    - Persönliche Daten (Name, Geburtsjahr, Wohnort)
    - Berufsziel
    - Berufserfahrung (mit Position, Firma, Zeitraum und Aufgaben – in vollständigen Sätzen)
    - Ausbildung (mit Abschluss, Schule/Firma, Zeitraum)
    - Kenntnisse & Fähigkeiten (mit Fachkompetenzen, Soft Skills, Software, Sprachen – in Stichpunkten)

    Bitte gib den Lebenslauf als gut strukturierten Text mit Überschriften aus – nicht als JSON oder Aufzählung von Rohdaten.

    Kurzprofil:
    {kurzprofil}

    Erstelle den Lebenslauf so, dass er direkt in eine Bewerbung eingefügt werden kann.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500,
    )

    return response.choices[0].message.content


if st.button("Lebenslauf generieren"):
    if not kurzprofil_text.strip():
        st.error("Bitte gib zuerst ein Kurzprofil ein.")
    else:
        with st.spinner("KI-generierter Lebenslauf wird erstellt..."):
            cv_json_str = generate_cv_text(kurzprofil_text)
            st.text_area("KI-generierter Lebenslauf (JSON)", cv_json_str, height=300)

            try:
                cv_data = json.loads(cv_json_str)
            except json.JSONDecodeError:
                st.error("Der von der KI erzeugte Lebenslauf konnte nicht als JSON geparst werden.")
                cv_data = {}

            if cv_data:
                env = Environment(loader=FileSystemLoader('.'))
                template = env.get_template('cv_template.html')
                html_content = template.render(cv=cv_data)

                try:
                    client = pdfcrowd.HtmlToPdfClient(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
                    pdf_bytes = client.convertString(html_content)
                    output_file = f"{cv_data.get('name', 'Lebenslauf').replace(' ', '_')}_Lebenslauf.pdf"

                    st.success("PDF erfolgreich erstellt!")
                    st.download_button("PDF herunterladen", data=pdf_bytes, file_name=output_file, mime="application/pdf")
                except pdfcrowd.Error as e:
                    st.error(f"Fehler bei der PDF-Erstellung: {e}")
