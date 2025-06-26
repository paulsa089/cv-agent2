import streamlit as st
from generate_cv import generate_cv_json, generate_pdf

st.set_page_config(page_title="CV Generator", layout="wide")

st.title("💼 Lebenslauf-Generator")

kurzprofil = st.text_area("Gib hier das Kurzprofil ein:", height=250)

if st.button("Lebenslauf generieren"):
    st.write("Button gedrückt!")
    if kurzprofil.strip() == "":
        st.error("Bitte gib ein Kurzprofil ein.")
    else:
        with st.spinner("Lebenslauf wird generiert..."):
            cv_data = generate_cv_json(kurzprofil)
            st.write("cv_data:", cv_data)

            if cv_data is None:
                st.error("Fehler bei der Generierung des Lebenslaufs.")
            else:
                st.subheader("📄 Generierter Lebenslauf")
                st.json(cv_data)

                # PDF-Erstellung testweise auskommentiert, wenn du nur JSON testen willst:
                # pdf_path = generate_pdf(cv_data)
                # st.write(f"PDF gespeichert unter: {pdf_path}")

                # with open(pdf_path, "rb") as file:
                #     st.download_button(
                #         label="📥 PDF herunterladen",
                #         data=file,
                #         file_name="Lebenslauf.pdf",
                #         mime="application/pdf"
                #     )
