import unicodedata
def normalize_identifier(value:str)->str: return " ".join(value.strip().casefold().split())
def normalize_alias(value:str)->str: return " ".join(unicodedata.normalize("NFKC",value).casefold().split())
