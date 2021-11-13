# %%
import requests
import glob
import zipfile
import os

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

sa2_download()
sa2_unpacker()
sa2_tidy()