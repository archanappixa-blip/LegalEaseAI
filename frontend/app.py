import html
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8001"


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background: #f4f6f9;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 25px;
        padding-bottom: 40px;
    }

    .hero {
        background: linear-gradient(135deg, #111827, #263449);
        color: white;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 19px;
        opacity: 0.9;
    }

    .hero-small {
        margin-top: 12px;
        font-size: 14px;
        opacity: 0.7;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .card-title {
        font-size: 21px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 8px;
    }

    .card-text {
        color: #6b7280;
        line-height: 1.6;
    }

    .feature {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        text-align: center;
        min-height: 120px;
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 8px;
    }

    .feature-title {
        font-weight: 700;
        color: #111827;
    }

    .feature-text {
        color: #6b7280;
        font-size: 14px;
        margin-top: 5px;
    }

    .preview-box {
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 14px;
        padding: 25px;
        line-height: 1.8;
        min-height: 250px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        padding-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "document" not in st.session_state:
    st.session_state["document"] = ""

if "document_type" not in st.session_state:
    st.session_state["document_type"] = ""

if "terms" not in st.session_state:
    st.session_state["terms"] = ""


# ---------------------------------------------------------
# Hero
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">⚖️ LegalEase</div>

        <div class="hero-subtitle">
            AI-Powered Legal Document Drafting Platform
        </div>

        <div class="hero-small">
            Draft • Review • Edit • Export
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Introduction
# ---------------------------------------------------------

st.markdown(
    """
    <div class="card">
        <div class="card-title">
            Welcome to LegalEase
        </div>

        <div class="card-text">
            LegalEase helps users create AI-assisted first drafts
            of common legal documents. Enter the document details,
            generate a draft, review and edit it, then export it
            as TXT, DOCX, or PDF.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Features
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Drafting</div>
            <div class="feature-text">
                Generate legal document drafts
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">✏️</div>
            <div class="feature-title">Easy Editing</div>
            <div class="feature-text">
                Review and edit generated content
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Multiple Formats</div>
            <div class="feature-text">
                Export TXT, DOCX and PDF
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="feature">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Simple Workflow</div>
            <div class="feature-text">
                Draft, review and export
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")


# ---------------------------------------------------------
# New Document button
# ---------------------------------------------------------

if st.session_state["document"]:

    if st.button(
        "🆕 Create New Document",
        use_container_width=True,
    ):
        st.session_state["document"] = ""
        st.session_state["document_type"] = ""
        st.session_state["terms"] = ""

        st.rerun()


# ---------------------------------------------------------
# Document Information
# ---------------------------------------------------------

st.markdown(
    """
    <div class="card-title">
        📋 Create Legal Document
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    document_type = st.selectbox(
        "Document Type",
        [
            "Freelance Work Contract",
            "Employment Agreement",
            "Non-Disclosure Agreement",
            "Service Agreement",
            "Rental Agreement",
            "Partnership Agreement",
            "Consulting Agreement",
            "Loan Agreement",
            "Business Contract",
        ],
    )


with col2:

    effective_date = st.text_input(
        "Effective Date",
        placeholder="Example: 24 September 2026",
    )


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example: Jane Doe (Service Provider), "
        "TechNova Inc. (Client)"
    ),
    height=100,
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Example: Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),
    height=150,
)


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

generate_clicked = st.button(
    "✨ Generate Legal Document",
    type="primary",
    use_container_width=True,
)


if generate_clicked:

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

        request_data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=request_data,
                    timeout=120,
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state["document"] = data.get(
                    "content",
                    "",
                )

                st.session_state["document_type"] = (
                    document_type
                )

                st.session_state["terms"] = terms

                st.success(
                    "✅ Legal document generated successfully!"
                )

            else:

                try:
                    error = response.json().get(
                        "detail",
                        response.text,
                    )

                except Exception:
                    error = response.text

                st.error(
                    f"Backend error ({response.status_code}): {error}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to LegalEase backend. "
                "Make sure FastAPI is running on "
                "http://127.0.0.1:8000"
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏳ The request took too long. Please try again."
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )


# ---------------------------------------------------------
# Generated document
# ---------------------------------------------------------

if st.session_state["document"]:

    st.divider()

    st.markdown(
        """
        <div class="card-title">
            📝 Generated Legal Document
        </div>
        """,
        unsafe_allow_html=True,
    )

    edited_document = st.text_area(
        "Review and edit your document",
        value=st.session_state["document"],
        height=600,
    )

    st.session_state["document"] = edited_document


    # -----------------------------------------------------
    # Preview
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="card-title">
            👁️ Document Preview
        </div>
        """,
        unsafe_allow_html=True,
    )

    safe_document = html.escape(
        edited_document
    ).replace(
        "\n",
        "<br>",
    )

    st.markdown(
        f"""
        <div class="preview-box">
            {safe_document}
        </div>
        """,
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # Downloads
    # -----------------------------------------------------

    st.divider()

    st.markdown(
        """
        <div class="card-title">
            ⬇️ Download Document
        </div>
        """,
        unsafe_allow_html=True,
    )


    export_data = {
        "text": edited_document,
        "document_type": st.session_state.get(
            "document_type",
            document_type,
        ),
        "terms": st.session_state.get(
            "terms",
            terms,
        ),
        "brand_name": "LegalEase",
    }


    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        try:

            response = requests.post(
                f"{BACKEND_URL}/export/txt",
                json=export_data,
                timeout=30,
            )

            if response.status_code == 200:

                st.download_button(
                    "📄 Download TXT",
                    response.content,
                    "legalease_document.txt",
                    "text/plain",
                    use_container_width=True,
                )

            else:

                st.error(
                    "TXT export failed."
                )

        except Exception as error:

            st.error(
                f"TXT export error: {error}"
            )


    # DOCX
    with col2:

        try:

            response = requests.post(
                f"{BACKEND_URL}/export/docx",
                json=export_data,
                timeout=30,
            )

            if response.status_code == 200:

                st.download_button(
                    "📝 Download DOCX",
                    response.content,
                    "legalease_document.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

            else:

                st.error(
                    "DOCX export failed."
                )

        except Exception as error:

            st.error(
                f"DOCX export error: {error}"
            )


    # PDF
    with col3:

        try:

            response = requests.post(
                f"{BACKEND_URL}/export/pdf",
                json=export_data,
                timeout=30,
            )

            if response.status_code == 200:

                st.download_button(
                    "📕 Download PDF",
                    response.content,
                    "legalease_document.pdf",
                    "application/pdf",
                    use_container_width=True,
                )

            else:

                st.error(
                    "PDF export failed."
                )

        except Exception as error:

            st.error(
                f"PDF export error: {error}"
            )


# ---------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------

st.divider()

st.warning(
    "⚠️ LegalEase generates AI-assisted first drafts. "
    "Documents should be reviewed by a qualified legal "
    "professional before use."
)


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        ⚖️ <b>LegalEase</b><br>
        AI-Powered Legal Document Drafting Platform<br>
        Final Year Project
    </div>
    """,
    unsafe_allow_html=True,
)