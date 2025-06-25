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
    Du bist ein erfahrener Karriereberater. Erstelle aus folgendem Kurzprofil einen strukturierten Lebenslauf mit Abschnitten zu Ausbildung, Berufserfahrung, Fähigkeiten und Sprachkenntnissen.
    
    Kurzprofil:
    {kurzprofil}
    
    Bitte formatiere den Lebenslauf als JSON mit folgenden Feldern:
    - name
    - birth_year
    - location
    - education: Liste von Einträgen mit degree, institution, period
    - work_experience: Liste von Einträgen mit position, company, period, tasks (Liste)
    - skills: fachkompetenz, personal_strengths, software, languages (jeweils Listen)
    - career_goal
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800,
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
