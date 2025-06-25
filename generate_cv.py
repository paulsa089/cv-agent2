import streamlit as st
import pdfcrowd
from jinja2 import Environment, FileSystemLoader
import openai
from docx import Document

# PDFCrowd Zugangsdaten
PDFCROWD_USERNAME = 'paulsa'
PDFCROWD_API_KEY = 'e0bd4b588648bfc431efcd2c0df245a2'

# OpenAI API-Key
openai.api_key = "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"

st.title("Lebenslauf Generator (Cloud PDF)")

st.header("Kurzprofil eingeben")

input_type = st.radio("Kurzprofil eingeben oder Datei hochladen?", ("Freitext", "Datei hochladen"))

kurzprofil_text = ""

if input_type == "Freitext":
    kurzprofil_text = st.text_area("Kurzprofil eingeben", height=200)

elif input_type == "Datei hochladen":
    uploaded_file = st.file_uploader("Lade dein Kurzprofil hoch (.txt oder .docx)", type=['txt', 'docx'])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            kurzprofil_text = uploaded_file.read().decode('utf-8')
            st.text_area("Inhalt der Datei", kurzprofil_text, height=200)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            kurzprofil_text = "\n".join([p.text for p in doc.paragraphs])
            st.text_area("Inhalt der Datei", kurzprofil_text, height=200)
        else:
            st.error("Dateityp nicht unterstützt")

st.header("Optional: Lebenslauf-Daten manuell eingeben")

job_title = st.text_input("Berufsbezeichnung", "")
name = st.text_input("Name", "")
birth_year = st.text_input("Geburtsjahr", "")
location = st.text_input("Wohnort", "")
family_status = st.text_input("Familienstand", "")
nationality = st.text_input("Staatsangehörigkeit", "")
career_goal = st.text_area("Berufsziel", "")

education_input = st.text_area("Ausbildung (Einträge mit Semikolon trennen)", "")
skills_professional = st.text_area("Fachliche Kenntnisse (Semikolon getrennt)", "")
skills_personal = st.text_area("Persönliche Eigenschaften (Semikolon getrennt)", "")
languages_input = st.text_area("Sprachen (Semikolon getrennt)", "")

if st.button("Lebenslauf generieren"):
    with st.spinner("Generiere Lebenslauf..."):

        if kurzprofil_text:
            # Sende das Kurzprofil an GPT, um strukturierten Lebenslauf zu erstellen
            prompt = f"""
            Erstelle auf Basis des folgenden Kurzprofils einen vollständigen Lebenslauf.
            Nutze realistische Daten für Name, Berufserfahrung, Ausbildung und Fähigkeiten.
            Struktur: Name, Berufsbezeichnung, Geburtsjahr, Wohnort, Familienstand, Staatsangehörigkeit, Berufsziel, Ausbildung, Berufserfahrung, Fachliche Kenntnisse, Persönliche Eigenschaften, Sprachen.

            Kurzprofil:
            {kurzprofil_text}
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            cv_text = response.choices[0].message['content']

            # Zeige den generierten Text an
            st.subheader("Generierter Lebenslauf (Rohtext)")
            st.text(cv_text)

            # Hier wäre der Schritt, den Text in cv_data zu parsen (kann ich dir bauen, wenn du möchtest)

            st.info("Den automatisierten Parser baue ich dir gern, aktuell musst du noch die Daten manuell übertragen.")

        # Wenn manuelle Eingabe genutzt wurde
        # (Hier machen wir ein einfaches Fallback, Parser folgt)

        # Parse education entries
        education = []
        for edu_str in education_input.split(";"):
            edu_str = edu_str.strip()
            if edu_str:
                education.append({"degree": edu_str, "period": "", "institution": ""})

        languages = [l.strip() for l in languages_input.split(";") if l.strip()]

        skills = {
            "fachkompetenz": [s.strip() for s in skills_professional.split(";") if s.strip()],
            "personal_strengths": [s.strip() for s in skills_personal.split(";") if s.strip()],
            "software": [],
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
            "work_experience": [],
            "education": education,
            "skills": skills,
            "salary": "",
            "availability": "",
            "email": "",
            "phone": "",
            "kursprofil": kurzprofil_text
        }

        # PDF erstellen
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('cv_template.html')
        html_content = template.render(cv=cv_data)

        try:
            client = pdfcrowd.HtmlToPdfClient(PDFCROWD_USERNAME, PDFCROWD_API_KEY)
            pdf_bytes = client.convertString(html_content)
            output_file = f"{(name or 'Lebenslauf').replace(' ', '_')}.pdf"

            st.success("PDF erfolgreich erstellt!")
            st.download_button("PDF herunterladen", data=pdf_bytes, file_name=output_file, mime="application/pdf")

        except pdfcrowd.Error as e:
            st.error(f"Fehler bei der PDF-Erstellung: {e}")
