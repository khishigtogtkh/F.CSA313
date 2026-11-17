# Subsequent AI review (same assistant, not independent human analysis)

Baseline frozen at commit 91e08d4. Read source and enumerate reaching definitions independently of witness selection:

| Variable | Reaching-def → use combinations (T/F where feasible) |
|---|---|
|attendance|31→32a(T/F), 31→38c(T/F)|
|threshold|31→32b(T/F), 31→50(T/F)|
|a|38d→39(T/F)|
|present|35→40, 40→40, 35→50(T/F), 40→50(T/F)|
|streak|36→41, 41→41, 46→41, 41→42(T/F), 41→43|
|best|37→42(T), 43→42(T/F), 37→53(F), 43→53(T/F)|
|score|49→54, 49→56, 51→54, 51→56, 54→56|

33 branch-specific requirements; no missing or extra feasible pair compared with baseline.
Rejected tempting additions: best37→42F (first positive streak is 1 > initial best 0), best37→53T (initial best remains 0), streak36/46→42/43 (41 kills it first). Extra mutation-kill test adds value discrimination, not a new pair. No claim of independent reviewer or manual student baseline.
