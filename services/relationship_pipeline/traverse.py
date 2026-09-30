from collections import defaultdict
def traverse(edges:list[tuple[str,str,str]],start:str,max_depth:int=2)->set[str]:
 if max_depth<0: raise ValueError("max_depth must be non-negative")
 graph=defaultdict(set)
 for a,p,b in edges: graph[a].add(b)
 seen={start}; frontier={start}
 for _ in range(max_depth):
  frontier={n for x in frontier for n in graph[x]}-seen
  seen|=frontier
 return seen
