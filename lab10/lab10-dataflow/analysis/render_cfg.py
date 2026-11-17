from pathlib import Path
import json, subprocess, csv, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
p=Path(__file__).resolve().parents[1]
w=json.loads((p/'analysis/witnesses.json').read_text())
# Each edge is rendered individually as a source/target arrow with its actual method label.
# Full adjacency is explicit through repeated source-line identifiers.
edges=sorted(w['edges'],key=lambda e:(int(re.sub('[^0-9]','',e[0])),e[0],e[1]))
fig,ax=plt.subplots(figsize=(20,len(edges)*.63+15));ax.set_xlim(0,10);ax.set_ylim(-1,len(edges)+24);ax.axis('off')
labels={'31':'parameters','32a':'attendance == null','32b':'threshold < 0','33':'throw / exit','35':'present = 0','36':'streak = 0','37':'best = 0','38c':'has next attendance?','38d':'a = next element','39':'a > 0','40':'present++','41':'streak++','42':'streak > best','43':'best = streak','46':'streak = 0','49':'score = 0','50':'present >= threshold','51':'score = 5','53':'best >= 5','54':'score += 3','56':'return score / exit'}

positions={'31': (5, 22), '32a': (5, 20.5), '32b': (5, 19), '33': (8.5, 20), '35': (5, 17.5), '36': (5, 16), '37': (5, 14.5), '38c': (5, 13), '38d': (2, 11.5), '39': (2, 10), '40': (1, 8.5), '41': (1, 7), '42': (1, 5.5), '43': (1, 4), '46': (3.4, 8.5), '49': (7, 11.5), '50': (7, 10), '51': (8.6, 8.5), '53': (7, 7), '54': (8.6, 5.5), '56': (7, 4)}
for node,(x,y) in positions.items():
 ax.text(x,len(edges)+y,f'{node}: {labels[node]}',ha='center',va='center',fontsize=9,bbox=dict(boxstyle='round',fc='#edf4ff',ec='#2c5282'),zorder=5)
for idx,(a,b,names) in enumerate(edges,1):
 x,y=positions[a];xx,yy=positions[b]; yy+=len(edges);y+=len(edges)
 rad=.28 if b=='38c' else 0
 ax.add_patch(FancyArrowPatch((x,y),(xx,yy),connectionstyle=f'arc3,rad={rad}',arrowstyle='->',mutation_scale=14,shrinkA=20,shrinkB=20,color='#526477'))
 ax.text((x+xx)/2+(1 if rad else .15),(y+yy)/2,f'E{idx}',fontsize=7,color='#8b2300')

for i,(a,b,names) in enumerate(edges):
 y=len(edges)-i-1
 branch=''
 if a in ('32a','32b','38c','39','42','50','53'):
  true={'32a':'33','32b':'33','38c':'38d','39':'40','42':'43','50':'51','53':'54'}
  branch='T' if true[a]==b else 'F'
 for x,node in ((1.4,a),(8.6,b)):
  ax.text(x,y,f'{node}: {labels[node]}',ha='center',va='center',fontsize=10,bbox=dict(boxstyle='round',fc='#edf4ff',ec='#2c5282'))
 ax.add_patch(FancyArrowPatch((2.8,y),(7.15,y),arrowstyle='->',mutation_scale=13))
 ax.text(5,y+.12,f'E{i+1}  '+branch+'  '+min(names,key=len),ha='center',fontsize=9)
ax.set_title('bonus CFG and annotated edge detail\nIdentical line IDs denote the same node; T/F = predicate result.\n38c: iteration condition; 38d: element definition. Every feasible edge has an actual test method.',fontsize=14,pad=25)
fig.savefig(p/'cfg-bonus.png',dpi=150,bbox_inches='tight');plt.close(fig)
