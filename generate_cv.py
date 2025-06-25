import streamlit as st
import pdfcrowd
from jinja2 import Environment, FileSystemLoader
from docx import Document  # Für .docx Dateien

# PDFCrowd Zugangsdaten
PDFCROWD_USERNAME = 'paulsa'  # Deinen pdfcrowd Username eintragen
PDFCROWD_API_KEY = 'e0bd4b588648bfc431efcd2c0df245a2'  # Deinen pdfcrowd API Key eintragen

st.title("Lebenslauf Generator (Cloud PDF)")

st.header("Kursprofil eingeben")

# Kursprofil Input: Freitext oder Datei-Upload
input_type = st.radio("Kursprofil eingeben oder Datei hochladen?", ("Freitext", "Datei hochladen"))

kursprofil_text = ""

if input_type == "Freitext":
    kursprofil_text = st.text_area("Kursprofil beschreiben", height=200)

elif input_type == "Datei hochladen":
    uploaded_file = st.file_uploader("Lade dein Kursprofil hoch (.txt oder .docx)", type=['txt', 'docx'])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            kursprofil_text = uploaded_file.read().decode('utf-8')
            st.text_area("Inhalt der Datei", kursprofil_text, height=200)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            kursprofil_text = "\n".join([p.text for p in doc.paragraphs])
            st.text_area("Inhalt der Datei", kursprofil_text, height=200)
        else:
            st.error("Dateityp nicht unterstützt")

st.header("Lebenslauf-Daten eingeben")

job_title = st.text_input("Berufsbezeichnung", "Finanzbuchhalter")
name = st.text_input("Name", "Max Mustermann")
birth_year = st.text_input("Geburtsjahr", "1990")
location = st.text_input("Wohnort", "Berlin")
family_status = st.text_input("Familienstand", "Ledig")
nationality = st.text_input("Staatsangehörigkeit", "Deutsch")
career_goal = st.text_area("Berufsziel", "Motivierter Finanzbuchhalter mit Erfahrung...")

education_input = st.text_area("Ausbildung (Einträge mit Semikolon trennen)", "Weiterbildung zum Finanzbuchhalter (IHK); Ausbildung zum Industriekaufmann")
skills_professional = st.text_area("Fachliche Kenntnisse (Semikolon getrennt)", "Buchhaltung; Umsatzsteuer-Voranmeldungen; Monatsabschlüsse")
skills_personal = st.text_area("Persönliche Eigenschaften (Semikolon getrennt)", "Zuverlässig; Teamfähig; Lernbereit")
languages_input = st.text_area("Sprachen (Semikolon getrennt)", "Deutsch; Englisch")

# Beispiel: Fiktive Arbeitserfahrung (du kannst das erweitern oder per Formular auch dynamisch machen)
work_experience = [
    {
        "position": "Finanzbuchhalter",
        "period": "02/2021 - heute",
        "company": "Dienstleistungsunternehmen (KMU), Berlin",
        "tasks": [
            "Bearbeitung von Eingangs- und Ausgangsrechnungen",
            "Abstimmung von Konten und Unterstützung bei Monatsabschlüssen",
            "Erstellung von Umsatzsteuer-Voranmeldungen",
            "Nutzung von DATEV Unternehmen online und digitalen Buchhaltungslösungen",
            "Zusammenarbeit mit Steuerberatern und internen Abteilungen"
        ]
    },
    {
        "position": "Kaufmännischer Sachbearbeiter",
        "period": "09/2019 - 01/2021",
        "company": "Handelsunternehmen, Berlin",
        "tasks": [
            "Rechnungsprüfung und Bearbeitung des Zahlungsverkehrs",
            "Unterstützung in der vorbereitenden Buchhaltung",
            "Erstellung von Auswertungen in MS Excel"
        ]
    }
]

# Parse education entries
education = []
for edu_str in education_input.split(";"):
    edu_str = edu_str.strip()
    if edu_str:
        # Einfach mal alles in degree, keine weiteren Felder
        education.append({
            "degree": edu_str,
            "period": "",
            "institution": ""
        })

# Parse languages (optional)
languages = [l.strip() for l in languages_input.split(";") if l.strip()]

# Compose skills dict to match template
skills = {
    "fachkompetenz": [s.strip() for s in skills_professional.split(";") if s.strip()],
    "personal_strengths": [s.strip() for s in skills_personal.split(";") if s.strip()],
    "software": [],  # Optional, leer
    "languages": languages
}

cv_data = {
    "job_title": job_title,
    "name": name,
    "birth_year": birth_year,
    "location": location,
    "family_status": family_status,
    "nationality": nationality,
    "career_goal": career_goal,
    "work_experience": work_experience,
    "education": education,
    "skills": skills,
    "salary": "",         # Optional
    "availability": "",   # Optional
    "email": "",          # Optional
    "phone": "",          # Optional
    "kursprofil": kursprofil_text  # Hier kannst du das Kursprofil weiterverwenden
}

if st.button("Lebenslauf generieren"):
    # Template laden
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('cv_template.html')
    html_content = template.render(cv=cv_data)

    try:
        client = pdfcrowd.HtmlToPdfClient(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
        pdf_bytes = client.convertString(html_content)
        output_file = f"{name.replace(' ', '_')}_Lebenslauf.pdf"

        st.success("PDF erfolgreich erstellt!")
        st.download_button("PDF herunterladen", data=pdf_bytes, file_name=output_file, mime="application/pdf")

    except pdfcrowd.Error as e:
        st.error(f"Fehler bei der PDF-Erstellung: {e}")
