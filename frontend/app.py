import os
import requests
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# =========================================================
# BACKEND
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"


# =========================================================
# LOGO
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "backend",
        "assets",
        "logo.png"
    )
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .warning {
        padding: 15px;
        border-radius: 8px;
        background-color: #fff3cd;
        border: 1px solid #ffe69c;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOGO
# =========================================================

if os.path.exists(LOGO_PATH):

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            LOGO_PATH,
            width=180
        )

else:

    st.warning(
        "Logo not found: " + LOGO_PATH
    )


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="title">LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)


# =========================================================
# WARNING
# =========================================================

st.markdown(
    """
    <div class="warning">
    ⚠️ <b>Important:</b> LegalEase creates AI-assisted drafts.
    It does not provide legal advice. Review the document with
    a qualified legal professional before using it.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Settings")

    brand_name = st.text_input(
        "Brand Name",
        value="LegalEase"
    )

    st.divider()

    st.write("Backend URL")

    st.code(BACKEND_URL)

    # -----------------------------------------------------
    # TEST BACKEND
    # -----------------------------------------------------

    if st.button(
        "🔎 Test Backend",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{BACKEND_URL}/health",
                timeout=5
            )

            if response.status_code == 200:

                st.success("Backend connected!")

                st.json(
                    response.json()
                )

            else:

                st.error(
                    f"Backend returned status "
                    f"{response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Backend connection timed out."
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )


# =========================================================
# DOCUMENT CREATION
# =========================================================

st.header("📄 Create Legal Document")


# =========================================================
# DOCUMENT TYPE
# =========================================================

document_type = st.selectbox(
    "Document Type",
    [
        "Freelance Work Contract",
        "Legal Agreement",
        "Service Agreement",
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Business Agreement",
        "Custom Legal Document"
    ]
)


# =========================================================
# PARTIES
# =========================================================

parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Client: ABC Technologies Pvt. Ltd.\n"
        "Freelancer: Arun Kumar"
    ),
    height=120
)


# =========================================================
# TERMS
# =========================================================

terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "The freelancer will provide website development services; "
        "The total project fee is Rs. 25,000; "
        "The client will pay 50% in advance and 50% after completion; "
        "The freelancer will complete the work within 30 days; "
        "Both parties agree to maintain confidentiality."
    ),
    height=180
)


# =========================================================
# EFFECTIVE DATE
# =========================================================

effective_date = st.text_input(
    "Effective Date",
    placeholder="1 October 2026"
)


# =========================================================
# GENERATE DOCUMENT
# =========================================================

if st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    elif not effective_date.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        # -------------------------------------------------
        # IMPORTANT:
        # Backend expects "effective_date"
        # -------------------------------------------------

        request_data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date
        }

        # -------------------------------------------------
        # SEND TO FASTAPI
        # -------------------------------------------------

        with st.spinner(
            "Generating legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=request_data,
                    timeout=120
                )

                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    st.session_state[
                        "document_text"
                    ] = data["content"]

                    st.session_state[
                        "document_type"
                    ] = data["document_type"]

                    st.success(
                        "✅ Document generated successfully!"
                    )

                # -----------------------------------------
                # BACKEND ERROR
                # -----------------------------------------

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        error_message = response.text

                    st.error(
                        "Generation failed:\n"
                        + str(error_message)
                    )

            # ---------------------------------------------
            # CONNECTION ERROR
            # ---------------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to LegalEase backend.\n\n"
                    "Make sure FastAPI is running at:\n"
                    "http://127.0.0.1:8000"
                )

            # ---------------------------------------------
            # TIMEOUT
            # ---------------------------------------------

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ Backend request timed out."
                )

            # ---------------------------------------------
            # OTHER ERROR
            # ---------------------------------------------

            except Exception as e:

                st.error(
                    f"Unexpected error: {e}"
                )


# =========================================================
# DOCUMENT PREVIEW
# =========================================================

if "document_text" in st.session_state:

    st.divider()

    st.header("📝 Generated Document")

    edited_text = st.text_area(
        "Edit your document",
        value=st.session_state["document_text"],
        height=600
    )

    st.session_state[
        "document_text"
    ] = edited_text


    # =====================================================
    # EXPORT SECTION
    # =====================================================

    st.divider()

    st.header("📥 Export Document")

    col1, col2, col3 = st.columns(3)


    # =====================================================
    # TXT
    # =====================================================

    with col1:

        if st.button(
            "📄 Export TXT",
            use_container_width=True
        ):

            try:

                export_data = {
                    "text": edited_text,
                    "document_type": document_type,
                    "terms": terms,
                    "brand_name": brand_name
                }

                response = requests.post(
                    f"{BACKEND_URL}/export/txt",
                    json=export_data,
                    timeout=30
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download TXT",
                        data=response.content,
                        file_name="legalease_document.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                else:

                    st.error(
                        f"TXT export failed: "
                        f"{response.text}"
                    )

            except Exception as e:

                st.error(
                    f"TXT export error: {e}"
                )


    # =====================================================
    # DOCX
    # =====================================================

    with col2:

        if st.button(
            "📘 Export DOCX",
            use_container_width=True
        ):

            try:

                export_data = {
                    "text": edited_text,
                    "document_type": document_type,
                    "terms": terms,
                    "brand_name": brand_name
                }

                response = requests.post(
                    f"{BACKEND_URL}/export/docx",
                    json=export_data,
                    timeout=30
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download DOCX",
                        data=response.content,
                        file_name="legalease_document.docx",
                        mime=(
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),
                        use_container_width=True
                    )

                else:

                    st.error(
                        f"DOCX export failed: "
                        f"{response.text}"
                    )

            except Exception as e:

                st.error(
                    f"DOCX export error: {e}"
                )


    # =====================================================
    # PDF
    # =====================================================

    with col3:

        if st.button(
            "📕 Export PDF",
            use_container_width=True
        ):

            try:

                export_data = {
                    "text": edited_text,
                    "document_type": document_type,
                    "terms": terms,
                    "brand_name": brand_name
                }

                response = requests.post(
                    f"{BACKEND_URL}/export/pdf",
                    json=export_data,
                    timeout=30
                )

                if response.status_code == 200:

                    st.download_button(
                        "⬇️ Download PDF",
                        data=response.content,
                        file_name="legalease_document.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            response.text
                        )

                    except Exception:

                        error_message = response.text

                    st.error(
                        "PDF export failed:\n"
                        + str(error_message)
                    )

            except Exception as e:

                st.error(
                    f"PDF export error: {e}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LegalEase | AI-assisted legal document drafting | "
    "Not legal advice"
)