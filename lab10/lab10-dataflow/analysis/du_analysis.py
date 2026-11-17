"""Source-level trace ledger; binary attendance represents the a>0 partition.
Enumerates witnesses, not a replacement for static def-clear review.
"""
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def trace(a,t):
    defs={}; pairs={}; path=[]; edges=[]
    def step(line, uses=(), writes=()):
        if path: edges.append((str(path[-1]),str(line)))
        path.append(line)
        for v,kind in uses:
            d,idx=defs[v]; pairs[(v,d,line,kind)]=path[idx:].copy()
        for v in writes: defs[v]=(line,len(path)-1)
    step(31,writes=('attendance','threshold'))
    step('32a', [('attendance','p-'+('T' if a is None else 'F'))])
    if a is None: step(33);return pairs,path,edges,None
    step('32b',[('threshold','p-'+('T' if t<0 else 'F'))])
    if t<0: step(33);return pairs,path,edges,None
    step(35,writes=('present',));step(36,writes=('streak',));step(37,writes=('best',))
    present=streak=best=0
    for x in a:
        step('38c',[('attendance','p-T')]);step('38d',writes=('a',))
        step(39,[('a','p-'+('T' if x>0 else 'F'))])
        if x>0:
            step(40,[('present','c')],('present',));present+=1
            step(41,[('streak','c')],('streak',));streak+=1
            step(42,[(v,'p-'+('T' if streak>best else 'F')) for v in ('streak','best')])
            if streak>best:step(43,[('streak','c')],('best',));best=streak
        else:step(46,writes=('streak',));streak=0
    step('38c',[('attendance','p-F')]);step(49,writes=('score',));score=0
    step(50,[(v,'p-'+('T' if present>=t else 'F')) for v in ('present','threshold')])
    if present>=t:step(51,writes=('score',));score=5
    step(53,[('best','p-'+('T' if best>=5 else 'F'))])
    if best>=5:step(54,[('score','c')],('score',));score+=3
    step(56,[('score','c')]);return pairs,path,edges,score

def main():
    seeds=[('BD1_allDefs_score49to54',[1,1,1,1,1,0,1],8),('BD2_allDefs_score51to56',[0,1],1)]
    candidates=[(list(a),t) for n in range(9) for a in product((0,1),repeat=n) for t in sorted({0,n,n+1})]+[(None,0),([], -1),(None,-1)]
    universe=set().union(*(set(trace(a,t)[0]) for a,t in candidates))
    chosen=seeds.copy();covered=set().union(*(set(trace(a,t)[0]) for _,a,t in chosen))
    while universe-covered:
        a,t=max(candidates,key=lambda c:len(set(trace(*c)[0])-covered))
        chosen.append((f'BD{len(chosen)+1}_duWitness',a,t));covered.update(trace(a,t)[0])
    chosen += [('BX_nullAndNegative',None,-1),('BB_longerThanFive',[2,2,2,2,2,2],0),('BB_negativeMeansAbsent',[-1,1],1)]
    ledger={}; edge_tests={};body=[]
    for name,a,t in chosen:
        pairs,path,edges,score=trace(a,t)
        for k,p in pairs.items():ledger.setdefault(k,[]).append((name,p))
        for edge in edges:edge_tests.setdefault(edge,set()).add(name)
        arr='null' if a is None else 'new int[]{'+','.join(map(str,a))+'}'
        call=f'DataFlowTargets.bonus({arr},{t})'
        assertion=f'assertThrows(IllegalArgumentException.class, () -> {call});' if score is None else f'assertEquals({score}, {call});'
        body.append(f' @Test void {name}() {{ {assertion} }}')
    (ROOT/'src/test/java/mn/edu/must/sqat/BonusTest.java').write_text('package mn.edu.must.sqat;\nimport org.junit.jupiter.api.Test;\nimport static org.junit.jupiter.api.Assertions.*;\nclass BonusTest {\n'+'\n'.join(body)+'\n}\n')
    lines=['| Variable | Def | Use | Kind | Def-clear witness | Test IDs | Covered |','|---|---|---|---|---|---|---|']
    for (v,d,u,k),hits in sorted(ledger.items(),key=lambda x:tuple(map(str,x[0]))):
        lines.append(f'| {v} | {d} | {u} | {k} | '+ ' → '.join(map(str,hits[0][1]))+' | '+', '.join(n for n,_ in hits)+' | Yes |')
    (ROOT/'analysis/bonus-du.md').write_text('\n'.join(lines)+'\n')
    (ROOT/'analysis/witnesses.json').write_text(json.dumps({'tests':chosen,'edges':[(a,b,sorted(ns)) for (a,b),ns in edge_tests.items()]},indent=2))
    print(len(ledger),'feasible branch-specific pairs;',len(chosen),'bonus tests')
if __name__=='__main__': main()
