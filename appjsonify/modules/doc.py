from pathlib import Path

class Token:
    """Token definition."""
    def __init__(
        self, 
        token: str, 
        pos: tuple,
        font_size: float,
        font_name: str,
        meta: dict = {}
    ):
        self.token: str = token
        self.pos: tuple = pos
        self.font_size: float = font_size
        self.font_name: str = font_name
        self.meta: dict = meta


class Line:
    """Line definition."""
    def __init__(
        self, 
        line: str, 
        pos: tuple,
        font_size: float,
        font_name: str,
        tokens: list[Token],
        meta: dict = {}
    ):
        self.line: str = line
        self.pos: tuple = pos
        self.font_size: float = font_size
        self.font_name: str = font_name
        self.tokens: list[Token] = tokens
        self.meta: dict = meta


class Paragraph:
    """Paragraph definition."""
    def __init__(
        self, 
        paragraph: str,
        pos: tuple,
        font_size: float,
        font_name: str,
        lines: list[Line],
        meta: dict = {}
    ):
        self.paragraph: str = paragraph
        self.pos: tuple = pos
        self.font_size: float = font_size
        self.font_name: str = font_name
        self.lines: list[Line] = lines
        self.meta: dict = meta


class Page:
    """Page definition."""
    def __init__(
        self,
        paragraphs: list[Paragraph],
        lines: list[Line],
        tokens: list[Token], 
        meta: dict = {}
    ):
        self.paragraphs: list[Paragraph] = paragraphs
        self.lines: list[Line] = lines
        self.tokens: list[Token] = tokens
        self.meta: dict = meta


class Document:
    """Document definition."""
    def __init__(
        self, 
        input_path: Path, 
        pages: list[Page] = [],
        formatted_paragraphs: list[Paragraph] = [],
        meta: dict = {}
    ):
        self.input_path: Path = input_path
        self.pages: list[Page] = pages
        self.formatted_paragraphs: list[Paragraph] = formatted_paragraphs
        self.meta: dict = meta
