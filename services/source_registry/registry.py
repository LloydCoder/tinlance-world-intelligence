"""Reference source registry with stable identity and uniqueness semantics."""
from __future__ import annotations
from packages.contracts import Source

class SourceRegistryError(ValueError):
    pass

class SourceRegistry:
    def __init__(self)->None:
        self._by_id:dict[str,Source]={}
        self._id_by_uri:dict[str,str]={}

    def register(self, source:Source)->Source:
        if not source.id.strip() or not source.name.strip():
            raise SourceRegistryError("source id and name are required")
        if source.canonical_uri in self._id_by_uri and self._id_by_uri[source.canonical_uri] != source.id:
            raise SourceRegistryError("canonical URI is already registered")
        if source.id in self._by_id and self._by_id[source.id] != source:
            raise SourceRegistryError("source id already exists")
        self._by_id[source.id]=source
        self._id_by_uri[source.canonical_uri]=source.id
        return source

    def get(self, source_id:str)->Source|None:
        return self._by_id.get(source_id)

    def list_enabled(self)->tuple[Source,...]:
        return tuple(s for s in self._by_id.values() if s.enabled)
