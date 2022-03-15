from bs4 import BeautifulSoup
from requests import get

def get_qa(url):
    kw={
        'name':'div',\
        'data-testid':'comment',\
        'class':'_3cjCphgls6DH-irkVaA0GM'
    }
    soup=BeautifulSoup(get(url).text,'html.parser')
    comments=soup.find_all(**kw)
    kw={'name':'p','class':'_1qeIAgB0cPwnLhDF9XSiJM'}
    qa=list()
    for n,comment in enumerate(comments):
        if n > 1:
            with open('overfull-qa.txt','a') as afile:
                afile(url+'\n')
            return qa
        text=str()
        count=1
        for p in comment.find_all(**kw):
           if p.parent.name == 'li':
                text+=str(count)+'. '
                count+=1
           text+=p.text+'\n'
        qa.append(text)
        count=1
    return qa
