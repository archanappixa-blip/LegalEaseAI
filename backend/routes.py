from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import Response

from backend.schemas import (
    DocumentRequest,
    ExportRequest
)

from backend.services.exporters import (
    make_docx,
    make_pdf,
    make_txt
)

from backend.services.gemini_generator import (
    GeminiDocumentGenerator
)


router = APIRouter()


generator = GeminiDocumentGenerator()


@router.get("/")
def root():

    return {

        "name": "LegalEase API",

        "version": "1.0.0",

        "status": "running",

        "docs": "/docs"
    }


@router.get("/health")
def health():

    return {

        "status": "ok",

        "service": "legalease-backend"
    }


@router.post("/generate")
def generate_document(
    request: DocumentRequest
):

    try:

        generated = (
            generator
            .generate_document(
                request
            )
        )

        return {

            "success": True,

            "document_type":
                request.document_type,

            "content":
                generated
        }

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "Document generation failed: "
                f"{exc}"
            )
        ) from exc


@router.post("/export/txt")
def export_txt(
    request: ExportRequest
):

    content = make_txt(
        request.text
    )

    return Response(

        content=content,

        media_type=(
            "text/plain; charset=utf-8"
        ),

        headers={
            "Content-Disposition":
                'attachment; filename="legalease_document.txt"'
        }
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest
):

    try:

        content = make_docx(

            request.text,

            request.document_type,

            request.terms,

            request.brand_name
        )

        return Response(

            content=content,

            media_type=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            headers={
                "Content-Disposition":
                    'attachment; filename="legalease_document.docx"'
            }
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                f"DOCX export failed: {exc}"
            )

        ) from exc


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest
):

    try:

        content = make_pdf(

            request.text,

            request.document_type,

            request.terms,

            request.brand_name
        )

        return Response(

            content=content,

            media_type="application/pdf",

            headers={
                "Content-Disposition":
                    'attachment; filename="legalease_document.pdf"'
            }
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                f"PDF export failed: {exc}"
            )

        ) from exc