from __future__ import annotations
import unicodedata
from datetime import datetime,timezone
def normalize_text(value:str)->str: return " ".join(unicodedata.normalize("NFKC",value).split())
def normalize_predicate(value:str)->str: return normalize_text(value).casefold().replace(" ","_")
def normalize_datetime(value:datetime)->datetime:
 if value.tzinfo is None: raise ValueError("datetime must be timezone-aware")
 return value.astimezone(timezone.utc)
