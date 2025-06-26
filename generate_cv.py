import openai
import pdfcrowd
import os
import json
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cv_json(kurzprofil):
    prompt = f"""
    Du bist ein professioneller Lebenslauf-Generator.

    Aufgabe:
    Erstelle aus dem folgenden Kurzprofil einen vollständigen, realistisch ausgeschmückten Lebenslauf im JSON-Format.

    Vorgaben:
    - Gib das Ergebnis ausschließlich als JSON-Objekt zurück, kein Freitext.
    - Das JSON-Objekt soll folgende Felder enthalten:
        - "name": String (immer "Anonymisiert")
        - "birth_year": String (ungefähr 30 Jahre alt)
        - "location": "Bremen"
        - "family_status": "Ledig"
        - "nationality": "Deutsch"
        - "email": Optional (lasse leer)
        - "phone": Optional (lasse leer)
        - "salary": Gehaltswunsch aus der Eingabe oder leer
        - "availability": Verfügbarkeit aus der Eingabe oder leer
        - "career_goal": 3-4 Sätze, zusammenhängender Fließtext
        - "work_experience": Liste von mindestens 2 Stationen, jeweils:
            - "position": String
            - "company": String
            - "period": String
            - "tasks": Liste mit 4-5 Aufgaben
        - "education": Liste von Bildungsabschlüssen, jeweils:
            - "degree": String
        - "skills": Enthält:
            - "fachkompetenz": Liste
            - "software": Liste
            - "languages": Liste
            - "personal_strengths": Liste

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

        # JSON parsen
        cv_json = json.loads(content)
        return cv_json

    except Exception as e:
        print(f"Fehler: {e}")
        return None


def generate_pdf(cv_data, output_path="generated_cv.pdf"):
    username = os.getenv("PDFCROWD_USERNAME")
    api_key = os.getenv("PDFCROWD_API_KEY")

    # HTML Template laden
    with open("cv_template.html", "r", encoding="utf-8") as file:
        template_str = file.read()

    template = Template(template_str)
    html_content = template.render(cv=cv_data)

    client = pdfcrowd.HtmlToPdfClient(username, api_key)

    with open(output_path, "wb") as f:
        client.convertStringToFile(html_content, f)

    return output_path
