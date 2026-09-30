def contradiction(a:dict,b:dict)->bool:
 return a.get("subject_ref")==b.get("subject_ref") and a.get("predicate")==b.get("predicate") and a.get("object_value")!=b.get("object_value")
