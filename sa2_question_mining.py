# %%
import paperdecoding
import numpy as np
import pandas as pd
import glob
import re

# %% [markdown]
# # All papers and reports to text #

# %%
for path in glob.glob('sa2papers/*.pdf'):
    pages = paperdecoding.gettextpages(path)
    pages = [page for page in pages if page is not None]
    outpath = path.replace('\\','_txt\\').replace('pdf','txt')
    paperdecoding.pages_totext(pages,outpath)

# %% [markdown]
# # Parse and tidy questions #

# %%
all_papers = [paperdecoding.pagesfromtext(x) for x in glob.glob('sa2papers_txt/*[0-9].txt')]

# %%
paperdates = [x[14:20] for x in glob.glob('sa2papers_txt/*[0-9].txt')]

# %% [markdown]
# Regex out the questions - I'm not sure if sa2 has any single-part questions (ie. questions that don't have a [total x] at the end).

# %%
qs = [re.findall('\n\d .+?\[Total \d+\]', '\n'.join(['']+p[1:]), re.DOTALL) for p in all_papers]
qs[25].pop(3)
qs[25].pop(1)
marks = [[float(re.findall('\[Total (\d+?)\]',q)[0]) for q in q_i] for q_i in qs]
qs[13].append(re.findall('\n3 .+?\[\d+\]', '\n'.join(['']+all_papers[13][1:]), re.DOTALL)[0])
marks[13].append(10)
bd = [[[float(mark) for mark in re.findall('\[(\d+?)\]',q)] for q in q_i] for q_i in qs]
bd[26][0]=[3.0, 6.0, 10.0, 8.0, 7.0, 6.0, 8.0]
qnos = [[int(s[1]) for s in q_i] for q_i in qs]

# %%
q_dictlist = [{'full_date': paperdates[i],
'question_no': qnos[i][j],
'total_marks': marks[i][j],
'breakdown': bd[i][j],
'question_text': q_ij} for i, q_i in enumerate(qs) for j, q_ij in enumerate(qs[i])]

# %%
qdf = pd.DataFrame(q_dictlist)

# %% [markdown]
# # Parse and tidy answers

# %%
all_reports = [paperdecoding.pagesfromtext(x) for x in glob.glob('sa2papers_txt/*[0-9]report.txt')]


# %%
reportdates = [x[14:20] for x in glob.glob('sa2papers_txt/*[0-9]report.txt')]
# %%
rqnos = [re.split(r'\nQ?(\d) ', ''.join(report))[1::2] for report in all_reports]
rqs = [re.split(r'\nQ?(\d) ', ''.join(report))[2::2] for report in all_reports]

# %%
def answerglue(i,j,n=1):
    """Utility function that glues answers back together where they have been incorrectly split up by the RE"""
    for dummy in range(n):
        rqs[i][j] = rqs[i][j] + '\n' + rqnos[i][j+1] + ' ' + rqs[i][j+1]
        rqnos[i].pop(j+1)
        rqs[i].pop(j+1)
answerglue(0,1,3)
answerglue(6,1)
answerglue(9,0)
answerglue(11,0,2)
answerglue(14,0)
answerglue(15,0)
answerglue(17,0,2)
answerglue(30,0)
answerglue(32,0,2)

# %%
r_dictlist = []
for i, rdt in enumerate(reportdates):
    for j,q in enumerate(rqnos[i]):
        r_dictlist.append({'full_date': rdt,
        'question_no': int(q),
        'answer_text': rqs[i][j]})
adf = pd.DataFrame(r_dictlist)
#adf

# %%
fulldf = pd.merge(qdf,adf)
fulldf[:7]

# %%
fulldf.to_csv('fulldf.csv')
