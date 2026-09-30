from packages.contracts.replay import BacktestResult
def backtest(rule_id:str,predicted:set[str],expected:set[str],total:int)->BacktestResult:
 return BacktestResult(rule_id,total,len(predicted),len(predicted&expected),len(predicted-expected),len(expected-predicted))
