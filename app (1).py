import streamlit as st
import pdfcrowd
from jinja2 import Environment, FileSystemLoader

# pdfcrowd Zugangsdaten
PDFCROWD_USERNAME = 'paulsa'  # Hier deinen pdfcrowd Username eintragen
PDFCROWD_API_KEY = 'e0bd4b588648bfc431efcd2c0df245a2'    # Hier deinen pdfcrowd API Key eintragen

st.title("Lebenslauf Generator (Cloud PDF)")

st.header("Lebenslauf-Daten eingeben")

job_title = st.text_input("Berufsbezeichnung", "Finanzbuchhalter")
name = st.text_input("Name", "[Anonymisiert]")
birth_year = st.text_input("Geburtsjahr", "1996")
location = st.text_input("Wohnort", "Berlin")
family_status = st.text_input("Familienstand", "Ledig")
nationality = st.text_input("Staatsangehörigkeit", "Deutsch")
career_goal = st.text_area("Berufsziel", "Digitalaffiner Finanzbuchhalter...")

education = st.text_area("Ausbildung (Trenne Einträge mit Semikolon)", "")
skills_professional = st.text_area("Fachliche Kenntnisse", "")
skills_personal = st.text_area("Persönliche Eigenschaften", "")
languages = st.text_area("Sprachen (Trenne Einträge mit Semikolon)", "")

if st.button("Lebenslauf generieren"):
    cv_data = {
        "job_title": job_title,
        "name": name,
        "birth_year": birth_year,
        "location": location,
        "family_status": family_status,
        "nationality": nationality,
        "career_goal": career_goal,
        "education": [e.strip() for e in education.split(";") if e.strip()],
        "skills": {
            "professional": skills_professional,
            "personal": skills_personal
        },
        "languages": [l.strip() for l in languages.split(";") if l.strip()]
    }

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('cv_template.html')
    html_content = template.render(cv=cv_data)

    try:
        client = pdfcrowd.HtmlToPdfClient(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
        output_file = f"{cv_data['name'].replace(' ', '_')}_CV.pdf"

        pdf_bytes = client.convertString(html_content)

        st.success("PDF erfolgreich erstellt!")
        st.download_button("PDF herunterladen", pdf_bytes, file_name=output_file)

    except pdfcrowd.Error as why:
        st.error(f"Fehler bei der PDF-Erstellung: {why}")
