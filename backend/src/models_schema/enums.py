from enum import Enum


class DocumentType(str, Enum):
    PDF = "PDF"
    IMAGE = "IMAGE"
    TEXT = "TEXT"
