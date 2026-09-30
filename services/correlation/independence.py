def independent_count(source_id:str,supporting_sources:set[str],dependencies:set[tuple[str,str]])->int:
 return sum(1 for s in supporting_sources if s!=source_id and (s,source_id) not in dependencies and (source_id,s) not in dependencies)
