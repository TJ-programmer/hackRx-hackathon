import requests
import os
from bs4 import BeautifulSoup
from app.logging_config import setup_logger
from io import BytesIO

logger = setup_logger(__name__)


def _extract_pdf_text(content: bytes) -> str:
    try:
        import PyPDF2
    except Exception:
        logger.error("PyPDF2 not installed. Please add it to requirements to parse PDFs.")
        return ""

    try:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n".join(pages).strip()
    except Exception as e:
        logger.exception(f"[ERROR] Failed to read PDF: {e}")
        return ""


def parse_document(url: str) -> str:
    try:
        logger.info(f"Fetching document from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logger.info("Parser fetched document successfully")

        content_type = response.headers.get("Content-Type", "").lower()
        is_pdf = url.lower().endswith(".pdf") or "application/pdf" in content_type

        if is_pdf:
            text = _extract_pdf_text(response.content)
            if text:
                logger.info("Extracted text from PDF document")
                return text
            logger.warning("PDF detected but no text extracted; falling back to HTML parsing if possible.")

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n')
        logger.info(f"Successfully parsed the url {url}")
        return text.strip()

    except requests.exceptions.RequestException as e:
        logger.exception(f"[ERROR] Failed to fetch the url: {e}")
        return ""

    except Exception as e:
        logger.exception(f"[ERROR] An unexpected error occurred while parsing: {e}")
        return ""
