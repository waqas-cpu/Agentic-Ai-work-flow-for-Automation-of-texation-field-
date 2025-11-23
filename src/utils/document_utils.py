"""
Document processing utilities
"""

from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def load_text_file(file_path: str) -> str:
    """
    Load text from a file
    
    Args:
        file_path: Path to text file
        
    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Loaded text file: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Failed to load file {file_path}: {e}")
        return ""


def load_documents_from_directory(
    directory: str,
    extensions: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Load all documents from a directory
    
    Args:
        directory: Directory path
        extensions: List of file extensions to include (e.g., ['.txt', '.pdf'])
        
    Returns:
        List of document dictionaries
    """
    if extensions is None:
        extensions = ['.txt', '.md', '.pdf', '.docx']
    
    documents = []
    dir_path = Path(directory)
    
    if not dir_path.exists():
        logger.warning(f"Directory does not exist: {directory}")
        return documents
    
    for file_path in dir_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in extensions:
            try:
                if file_path.suffix == '.txt' or file_path.suffix == '.md':
                    content = load_text_file(str(file_path))
                else:
                    # Placeholder for other file types
                    content = f"[Content from {file_path.name}]"
                
                documents.append({
                    "path": str(file_path),
                    "name": file_path.name,
                    "extension": file_path.suffix,
                    "content": content
                })
            except Exception as e:
                logger.error(f"Failed to load document {file_path}: {e}")
    
    logger.info(f"Loaded {len(documents)} documents from {directory}")
    return documents


def extract_tax_year(text: str) -> int:
    """
    Extract tax year from document text
    
    Args:
        text: Document text
        
    Returns:
        Tax year (defaults to current year if not found)
    """
    import re
    from datetime import datetime
    
    # Look for 4-digit years in text
    years = re.findall(r'\b(20\d{2})\b', text)
    
    if years:
        return int(max(years))  # Return most recent year found
    
    return datetime.now().year


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    max_length = 255
    if len(sanitized) > max_length:
        if '.' in sanitized:
            name, ext = sanitized.rsplit('.', 1)
            available_length = max_length - len(ext) - 1  # -1 for the dot
            sanitized = name[:available_length] + '.' + ext
        else:
            sanitized = sanitized[:max_length]
    
    return sanitized
