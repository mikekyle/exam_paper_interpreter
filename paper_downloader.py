# %%
import requests
import glob
import zipfile
import os
import paperdecoding

def sa2_download():
    SA2urllist = [
        #'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-specialist-advanced-exam-paper-september-2021',
        'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-specialist-advanced-exam-paper-and-examiners-report-april-2021',
        'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-advanced-exam-paper-and-examiners-report-september-2020',
        'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-advanced-exam-paper-and-examiners-report-april-2020',
        'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-advanced-exam-paper-september-2019',
        'https://www.actuaries.org.uk/documents/subject-sa2-life-insurance-advanced-exam-paper-and-examiners-report-april-2019',
        'https://www.actuaries.org.uk/documents/subject-sa2-past-exam-papers-and-examiners-reports-2005-2018',
    ]

    filenames = ['sa2papers/'+url.split('/')[-1]+'.zip' for url in SA2urllist]

    reqs = [requests.get(url) for url in SA2urllist]

    for filename, req in zip(filenames,reqs):
        open(filename,'wb').write(req.content)

def sa2_unpacker():
    for zpath in glob.glob('sa2papers/*.zip'):
        with zipfile.ZipFile(zpath) as z:
            z.extractall('sa2papers/')

def sa2_tidy():
    fullpaths = glob.glob('sa2papers/**/*.pdf',recursive=1)
    targets = ['sa2papers\\'+p.split('\\')[-1] for p in fullpaths]
    for p,n in zip(fullpaths,targets):
        os.renames(p,n)
    for p in glob.glob('sa2papers/*.zip'):
        os.remove(p)
# maybe rename files 
# could do yyyymm and yyyymmreport

def sa2_rename():
    fullpaths = glob.glob('sa2papers/*.pdf')
    reportflags = [s.__contains__('Report') for s in fullpaths]
    targets = [s[20:26] for s in fullpaths]
    for p,n,f in zip(fullpaths,targets,reportflags):
        if f:
            os.renames(p,'sa2papers/'+n+'report.pdf')
        else:
            os.renames(p,'sa2papers/'+n+'.pdf')
    os.rename('sa2papers/AM.pdf.pdf','sa2papers/202104.pdf')

def sa2_totxt():
    fullpaths = glob.glob('sa2papers/*.pdf')
    outpaths = [p.replace('sa2papers','sa2papers_txt').replace('pdf','txt'
    )
    for p in fullpaths]
    for p,o in zip(fullpaths,outpaths):
        pages = paperdecoding.gettextpages(p)
        pages = [x for x in pages if x is not None]
        paperdecoding.pages_totext(pages,o)


sa2_download()
sa2_unpacker()
sa2_tidy()
sa2_rename()
sa2_totxt()
# %%