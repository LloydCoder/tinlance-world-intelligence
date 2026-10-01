"""Small deterministic signal DSL; unsupported operators fail closed."""
def evaluate(rule:dict,state:dict)->bool:
    op=rule.get("op")
    if op=="equals": return state.get(rule.get("field"))==rule.get("value")
    if op=="exists": return rule.get("field") in state
    if op=="gt": return state.get(rule.get("field")) is not None and state[rule["field"]] > rule.get("value")
    if op=="gte": return state.get(rule.get("field")) is not None and state[rule["field"]] >= rule.get("value")
    if op=="in": return state.get(rule.get("field")) in rule.get("values",[])
    if op=="and": return all(evaluate(x,state) for x in rule.get("conditions",[]))
    if op=="or": return any(evaluate(x,state) for x in rule.get("conditions",[]))
    if op=="not": return not evaluate(rule.get("condition",{}),state)
    raise ValueError("unsupported signal operator")
