def generate_cv_text(kurzprofil):
    prompt = f"""
    Du bist ein professioneller Lebenslauf-Generator.

    Deine Aufgabe: Erstelle aus dem folgenden Kurzprofil einen vollständigen, strukturierten Lebenslauf im **korrekten JSON-Format**.

    ⚠️ Regeln:
    - Gib **ausschließlich ein gültiges JSON-Objekt** aus. Keine Einleitung, keine Erklärung, keine Kommentare.
    - Beachte: Alle Texte müssen als Strings in Anführungszeichen stehen.
    - Es dürfen keine leeren Felder oder fehlende Anführungszeichen enthalten sein.
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

    ⚠️ Gib jetzt **ausschließlich das vollständige JSON** aus. Keine zusätzlichen Erklärungen oder Texte.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,  # Pflicht, damit kein Fließtext generiert wird
        max_tokens=2000,  # Falls Lebenslauf länger wird
        response_format="json"  # Nur bei aktueller OpenAI-Version möglich
    )

    return response.choices[0].message.content
