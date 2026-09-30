def evaluate(rule:dict,state:dict)->bool:
 op=rule.get("op")
 if op=="equals": return state.get(rule.get("field"))==rule.get("value")
 if op=="exists": return rule.get("field") in state
 if op=="and": return all(evaluate(x,state) for x in rule.get("conditions",[]))
 if op=="or": return any(evaluate(x,state) for x in rule.get("conditions",[]))
 raise ValueError("unsupported signal operator")
