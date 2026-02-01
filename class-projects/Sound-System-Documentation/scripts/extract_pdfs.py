#!/usr/bin/env python3
import pdfplumber, os, sys
BASE='/Users/mitchell/code/projects/class-projects/Sound-System-Documentation'
files=[
    os.path.join(BASE,'Sound Guildelines 2008.pdf'),
    os.path.join(BASE,'USITT TSDCA Sound Documentation Recommendations_April_2022_APPROVED.pdf')
]
for f in files:
    print('---')
    print('Processing:', os.path.basename(f))
    if not os.path.exists(f):
        print('MISSING:', f)
        continue
    try:
        with pdfplumber.open(f) as pdf:
            texts=[]
            empty_pages=[]
            for i,page in enumerate(pdf.pages, start=1):
                t=page.extract_text()
                if t and t.strip():
                    texts.append(t)
                else:
                    empty_pages.append(i)
            out=f[:-4]+'.txt'
            with open(out,'w',encoding='utf-8') as fh:
                fh.write('\n\n'.join(texts))
            chars=sum(len(s) for s in texts)
            print('Pages:', len(pdf.pages))
            print('Extracted characters:', chars)
            print('Empty pages (first 10):', empty_pages[:10])
            if texts:
                sample = texts[0][:1000].replace('\n','\n')
                print('Sample (first 1000 chars):\n')
                print(sample)
            else:
                print('No textual content extracted from any page.')
    except Exception as e:
        print('ERROR processing', f, e)
print('Done')
