from bs4 import BeautifulSoup, NavigableString
from os.path import sep, exists
from os import mkdir

def get_link_compendium():
    kw={'name':'p','class':'_1qeIAgB0cPwnLhDF9XSiJM'}

    with open('compendium.html') as rfile:
        soup=BeautifulSoup(rfile,'html.parser')

    link_dict=dict()

    done=False

    for n,tag in enumerate(soup.find_all(**kw)):
        if not n:
            continue
        elif done:
            break
        for k,t in enumerate(tag.descendants):
            if type(t) == NavigableString:
                continue
            elif t.name == 'a':
                val=t.text,t['href']
                subkey=t.text
                subval=t['href']
                link_dict[key][subkey]=subval
                if subkey == 'SailorRose23':
                    done=True
            elif t.name == 'strong':
                key=t.text.replace(':','')
                link_dict[key]=dict()
    return link_dict

def write_links():
    lc=get_link_compendium()
    root=['links',None,'']
    if not exists('links'):
        mkdir('links')
    for cc,dobject in lc.items():
        root[1]=cc
        root_dir=sep.join(root)
        if not exists(root_dir):
            mkdir(root_dir)
        for fan,url in dobject.items():
            root[2]=fan+'.txt'
            filename=sep.join(root)
            root[2]=''
            with open(filename,'w') as wfile:
                wfile.write(url)

if __name__ == '__main__':
    write_links()
