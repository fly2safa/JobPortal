"""
Extract text from PDF and DOCX files.
"""
from pathlib import Path
from typing import Optional
import PyPDF2
from docx import Document
from app.core.logging import get_logger

logger = get_logger(__name__)


class TextExtractor:
    """Extract text from various file formats."""
    
    @staticmethod
    def extract_text(file_path: str) -> Optional[str]:
        """
        Extract text from file based on extension.
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text or None if extraction fails
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        
        try:
            if ext == '.pdf':
                return TextExtractor._extract_from_pdf(file_path)
            elif ext in ['.doc', '.docx']:
                return TextExtractor._extract_from_docx(file_path)
            else:
                logger.warning(f"Unsupported file type: {ext}")
                return None
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return None
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()

