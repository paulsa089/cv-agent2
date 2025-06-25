import streamlit as st
import pdfcrowd
from jinja2 import Environment, FileSystemLoader
import random

# PDFCrowd Zugangsdaten
PDFCROWD_USERNAME = 'paulsa'
PDFCROWD_API_KEY = 'e0bd4b588648bfc431efcd2c0df245a2'

st.title("Fiktiven Lebenslauf aus Kurzprofil erstellen")

st.header("Kurzprofil eingeben")

# Kurzprofil-Eingabe
short_profile = st.text_area("Bitte gib dein Kurzprofil ein:", height=250)

if st.button("Fiktiven Lebenslauf erstellen"):
    if not short_profile.strip():
        st.error("Bitte ein Kurzprofil eingeben.")
    else:
        # Sehr einfache Logik zur Extraktion – kann später mit KI verbessert werden
        if "Finanzbuchhaltung" in short_profile or "Buchhaltung" in short_profile:
            job_title = "Finanzbuchhalter"
            skills = ["Buchhaltung", "Monatsabschlüsse", "Umsatzsteuer-Voranmeldungen"]
            career_goal = "Engagierter Finanzbuchhalter mit umfassender Erfahrung in der Buchhaltung."
        elif "Vertrieb" in short_profile or "Sales" in short_profile:
            job_title = "Vertriebsmitarbeiter"
            skills = ["Kundenakquise", "Vertriebsstrategien", "CRM-Systeme"]
            career_goal = "Zielorientierter Vertriebsmitarbeiter mit Leidenschaft für den Verkauf."
        else:
            job_title = "Kaufmännischer Mitarbeiter"
            skills = ["Organisation", "Kundenbetreuung", "Kommunikation"]
            career_goal = "Strukturierter kaufmännischer Mitarbeiter mit vielfältigen Erfahrungen."

        # Fiktive Basisdaten
        name = "Max Mustermann"
        birth_year = str(random.randint(1985, 1995))
        location = "Berlin"
        family_status = "Ledig"
        nationality = "Deutsch"

        # Fiktive Arbeitserfahrung
        work_experience = [
            {
                "position": job_title,
                "period": "01/2021 - heute",
                "company": "Musterfirma GmbH, Berlin",
                "tasks": [
                    f"Verantwortung für {skills[0]}",
                    f"Optimierung von {skills[1]}-Prozessen",
                    f"Zusammenarbeit mit internen Abteilungen und externen Partnern"
                ]
            },
            {
                "position": "Sachbearbeiter",
                "period": "06/2018 - 12/2020",
                "company": "Beispielfirma AG, Berlin",
                "tasks": [
                    "Administrative Aufgaben",
                    "Erstellung von Berichten",
                    "Kundenbetreuung"
                ]
            }
        ]

        # Fiktive Ausbildung
        education = [
            {"degree": "Weiterbildung zum Finanzbuchhalter (IHK)", "period": "2017 - 2018", "institution": "IHK Berlin"},
            {"degree": "Ausbildung zum Industriekaufmann", "period": "2014 - 2017", "institution": "Beispielunternehmen GmbH"}
        ]

        # Skills
        cv_skills = {
            "fachkompetenz": skills,
            "personal_strengths": ["Zuverlässig", "Teamfähig", "Analytisch"],
            "software": ["MS Office", "DATEV"],
            "languages": ["Deutsch", "Englisch"]
        }

        # CV-Daten zusammenstellen
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
            "skills": cv_skills,
            "salary": "",
            "availability": "",
            "email": "",
            "phone": "",
            "kursprofil": short_profile
        }

        # Lebenslauf generieren
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
