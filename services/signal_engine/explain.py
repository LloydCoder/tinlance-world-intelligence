def explain(rule:dict,state:dict)->str:
 if rule.get("op") in {"equals","exists"}: return f"{rule['op']} {rule.get('field')} => {evaluate(rule,state)}"
 if rule.get("op") in {"and","or"}: return f"{rule['op']}({', '.join(explain(x,state) for x in rule['conditions'])})"
 raise ValueError("unsupported signal operator")
from .evaluate import evaluate
