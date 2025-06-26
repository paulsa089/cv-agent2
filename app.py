import streamlit as st
from generate_cv import generate_cv_json, generate_pdf

st.title("💼 Lebenslauf-Generator")

kurzprofil = st.text_area("Gib hier das Kurzprofil ein:", height=250)

if st.button("Lebenslauf generieren"):
    if not kurzprofil.strip():
        st.error("Bitte gib ein Kurzprofil ein.")
    else:
        with st.spinner("Lebenslauf wird generiert..."):
            cv_data = generate_cv_json(kurzprofil)
            if cv_data is None:
                st.error("Fehler bei der Generierung des Lebenslaufs.")
            else:
                st.json(cv_data)
                pdf_path = generate_pdf(cv_data)
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 PDF herunterladen",
                        data=file,
                        file_name="Lebenslauf.pdf",
                        mime="application/pdf"
                    )
