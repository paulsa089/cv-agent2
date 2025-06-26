import openai
import pdfcrowd
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cv_text(kurzprofil):
    prompt = f"""
    Du bist ein professioneller Lebenslauf-Generator.

    Aufgabe:
    Erstelle aus dem folgenden Kurzprofil einen vollständigen, realistisch ausgeschmückten Lebenslauf im Stil eines anonymisierten Bewerberprofils.

    Vorgaben:
    - Verwende fiktive, aber plausible Daten für Name, Geburtsjahr (ca. 30 Jahre alt), Wohnort (Bremen), Familienstand (ledig) und Staatsangehörigkeit (deutsch).
    - Baue den Lebenslauf sinnvoll und ansprechend auf.
    - Schreibe in vollständigen Sätzen.
    - Strukturiere den Lebenslauf in folgende Abschnitte:
        1. Persönliche Angaben
        2. Berufsziel
        3. Berufserfahrung (2 Stationen mit Zeiträumen, Firmen und realistisch ausgeschmückten Aufgaben)
        4. Ausbildung
        5. Kenntnisse & Fähigkeiten (Fachkenntnisse, Software, Sprachen, Persönliche Stärken)
        6. Rahmenbedingungen (Gehaltswunsch und Verfügbarkeit)

    - Der Ton soll professionell und authentisch sein.
    - Verwende keine Bulletpoints in den persönlichen Angaben.
    - Die Tätigkeitsbeschreibungen sollen jeweils 4–5 Aufgaben umfassen.
    - Verwende als Standort Bremen.

    Eingabe:
    {kurzprofil}

    Gib den vollständigen Lebenslauf jetzt als zusammenhängenden Fließtext aus. Keine zusätzlichen Erklärungen.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )

    return response.choices[0].message.content

def generate_pdf(html_content, output_path="generated_cv.pdf"):
    username = os.getenv("PDFCROWD_USERNAME")
    api_key = os.getenv("PDFCROWD_API_KEY")

    client = pdfcrowd.HtmlToPdfClient(username, api_key)

    with open(output_path, "wb") as f:
        client.convertStringToFile(html_content, f)

    return output_path
