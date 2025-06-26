import streamlit as st
from generate_cv import generate_cv_text, generate_pdf

st.set_page_config(page_title="CV Generator", layout="wide")

st.title("💼 Lebenslauf-Generator")

kurzprofil = st.text_area("Gib hier das Kurzprofil ein:", height=250)

if st.button("Lebenslauf generieren"):
    if kurzprofil.strip() == "":
        st.error("Bitte gib ein Kurzprofil ein.")
    else:
        with st.spinner("Lebenslauf wird generiert..."):
            cv_text = generate_cv_text(kurzprofil)

        st.subheader("📄 Generierter Lebenslauf")
        st.write(cv_text)

        html_content = f"""
        <html>
        <head><meta charset="utf-8"></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
        {cv_text.replace("\n", "<br><br>")}
        </body>
        </html>
        """

        pdf_path = generate_pdf(html_content)

        with open(pdf_path, "rb") as file:
            btn = st.download_button(
                label="📥 PDF herunterladen",
                data=file,
                file_name="Lebenslauf.pdf",
                mime="application/pdf"
            )
