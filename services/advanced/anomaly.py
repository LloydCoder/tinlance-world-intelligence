import math
def z_score(observed:float,baseline:float,stddev:float)->float:
 if stddev<=0: return 0.0 if observed==baseline else math.inf
 return (observed-baseline)/stddev
