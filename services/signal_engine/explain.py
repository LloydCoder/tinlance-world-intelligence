from .evaluate import evaluate

def explain(rule:dict,state:dict)->str:
    if rule.get("op") in {"equals","exists","gt","gte","in"}:
        return f"{rule['op']} {rule.get('field')} => {evaluate(rule,state)}"
    if rule.get("op") in {"and","or"}:
        return f"{rule['op']}({', '.join(explain(x,state) for x in rule['conditions'])})"
    if rule.get("op")=="not":
        return f"not({explain(rule['condition'],state)})"
    raise ValueError("unsupported signal operator")
