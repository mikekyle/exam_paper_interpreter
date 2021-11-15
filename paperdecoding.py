# %%
import pdfplumber
import re
import numpy as np
import pandas as pd

def gettextpages(path):
    with pdfplumber.open(path) as pdf:
        text_pages = [page.extract_text() for page in pdf.pages]
    return text_pages

def pages_totext(pages,path):
    pages = [re.sub(r'[^\x00-\x7F]+',' ', page) for page in pages]
    with open(path, 'w') as f:
        f.write('--page--'.join(pages))

def pagesfromtext(path):
    with open(path) as f:
        pages = f.read().split('--page--')
    return pages

def getdatefrompaper(pages):
    return re.findall('[a-zA-Z]*? \d\d\d\d',pages[0])[0]

def split_combiq(combiq):
    """Takes a question text, splits after the first [d] mark number"""
    split_by_marks = re.split('(\[\d+?\])',combiq)
    short_q = ''.join(split_by_marks[:2])
    remainder = ''.join(split_by_marks[2:])
    next_q = re.findall('\n\d .+?\[Total \d+\]', remainder, re.DOTALL)[0]
    return (short_q,next_q)

def pdftodf(path):
    pages = gettextpages(path)
    pages = [page for page in pages if page]
    qs = re.findall('\n\d .+?\[Total \d+\]', '\n'.join(['']+pages[1:]), re.DOTALL)
    marks = [float(re.findall('\[Total (\d+?)\]',q)[0]) for q in qs]
    bd = [[float(mark) for mark in re.findall('\[(\d+?)\]',q)] for q in qs]
    qnos = [int(s[1]) for s in qs]
    q_dictlist = []
    for i, q in enumerate(qs):
        if marks[i] == sum(bd[i]):
            q_dictlist.append({'question_no': qnos[i],
                               'total_marks': marks[i],
                               'breakdown': bd[i],
                               'question_text': q})
        elif marks[i] == sum(bd[i][1:]):
            q_a,q_b = split_combiq(q)
            q_dictlist.append({'question_no': qnos[i],
                               'total_marks': bd[i][0],
                               'breakdown': bd[i][0:1],
                               'question_text': q_a})
            q_dictlist.append({'question_no': (qnos[i]+1),
                               'total_marks': marks[i],
                               'breakdown': bd[i][1:],
                               'question_text': q_b})
        elif marks[i] == sum(bd[i][2:]):
            q_a,q_b = split_combiq(q)
            q_b,q_c = split_combiq(q_b)
            q_dictlist.append({'question_no': qnos[i],
                               'total_marks': bd[i][0],
                               'breakdown': bd[i][0:1],
                               'question_text': q_a})
            q_dictlist.append({'question_no': (qnos[i]+1),
                               'total_marks': bd[i][1],
                               'breakdown': bd[i][1:2],
                               'question_text': q_b})
            q_dictlist.append({'question_no': (qnos[i]+2),
                               'total_marks': marks[i],
                               'breakdown': bd[i][2:],
                               'question_text': q_c})
        elif marks[i] == sum(bd[i][3:]):
            q_a,q_b = split_combiq(q)
            q_b,q_c = split_combiq(q_b)
            q_c,q_d = split_combiq(q_c)
            q_dictlist.append({'question_no': qnos[i],
                               'total_marks': bd[i][0],
                               'breakdown': bd[i][0:1],
                               'question_text': q_a})
            q_dictlist.append({'question_no': (qnos[i]+1),
                               'total_marks': bd[i][1],
                               'breakdown': bd[i][1:2],
                               'question_text': q_b})
            q_dictlist.append({'question_no': (qnos[i]+2),
                               'total_marks': bd[i][2],
                               'breakdown': bd[i][2:3],
                               'question_text': q_c})
            q_dictlist.append({'question_no': (qnos[i]+3),
                               'total_marks': marks[i],
                               'breakdown': bd[i][3:],
                               'question_text': q_d})
        else:
            print(f'looks like something weird at qs[{i}]')
    qdf = pd.DataFrame(q_dictlist)
    return qdf

command_verbs = ['describe',
                'suggest',
                'discuss',
                'state',
                'list',
                'calculate',
                'outline',
                'determine',
                'explain',
                'comment',
                'show']

key_words = ['regulation',
            'tax',
            'mutual',
            'hedge',
            'fundamental',
            'budget',
            'budgetting']
# %%
