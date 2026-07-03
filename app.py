import os
import streamlit as st
from document_processor import translate_file
from translator import LANGUAGE_CODES

st.set_page_config(
    page_title="Offline Document Translator",
    layout="centered"
)

st.title("Offline AI Document Translator")

st.write(
    "Translate DOCX, PDF, and Excel documents using an offline machine learning model."
)

uploaded_file = st.file_uploader(
    "Upload document",
    type=["docx", "pdf", "xlsx"]
)

languages = list(LANGUAGE_CODES.keys())

source_language = st.selectbox(
    "Source language",
    languages,
    index=languages.index("English")
)

target_language = st.selectbox(
    "Target language",
    languages,
    index=languages.index("Hindi")
)

if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    input_path = os.path.join("uploads", uploaded_file.name)

    with open(input_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    output_name = "translated_" + uploaded_file.name
    output_path = os.path.join("outputs", output_name)

    if st.button("Translate Document"):

        if source_language == target_language:
            st.warning("Source and target languages are the same.")
        else:
            with st.spinner("Translating document. Please wait..."):
                try:
                    translate_file(
                        input_path,
                        output_path,
                        source_language,
                        target_language
                    )

                    st.success("Translation completed successfully.")

                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="Download translated document",
                            data=file,
                            file_name=output_name,
                            mime="application/octet-stream"
                        )

                except Exception as error:
                    st.error("Translation failed.")
                    st.exception(error)

st.markdown("---")

st.subheader("Project Information")

st.write(
    """
    This application uses an offline neural machine translation model to translate documents.
    It supports DOCX, XLSX, and PDF files. DOCX and Excel files preserve formatting as much
    as possible. PDF translation is currently basic due to layout limitations.
    """
)

st.subheader("Technologies Used")

st.write(
    """
    Python, Streamlit, Hugging Face Transformers, PyTorch, NLLB-200,
    python-docx, openpyxl, and PyMuPDF.
    """
)