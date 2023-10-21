from os import sep, walk, mkdir
from os.path import exists
from reddit_scraper.cc_lister import list_content_creators

def list_emo(filename):
    linelist=set()
    with open(filename) as rfile:
        for line in rfile.readlines():
            line=line.strip()
            if line.isascii():
                continue
            linelist.add(line)
    emolist=set()
    for line in linelist:
        for c in line:
            if c.isascii():
                continue
            emolist.add(c)
    return emolist

def find_emoticons(cc):
    user_emo=dict()
    all_emos=set()
    for x,y,filelist in walk(cc):
        for file in filelist:
            filename=sep.join([x,file])
            emo=list_emo(filename)
            if not emo:
                continue
            user_emo[file[:-4]]=emo
            all_emos.update(emo)
    return user_emo,all_emos

def get_all_emos():
    cc_list=list_content_creators()
    emo_compendium=set()
    emo_dict=dict()
    for cc in cc_list:
        user_emo,all_emos=find_emoticons(cc)
        emo_compendium.update(all_emos)
        emo_dict[cc]=user_emo
    return emo_dict,emo_compendium

def write_emos():
    emo_dict,emo_compendium=get_all_emos()
    with open('emo-list.txt','w') as wfile:
        for emo in emo_compendium:
            wfile.write(emo+'\n')
    if not exists('emo-locs'):
        mkdir('emo-locs')
    for cc,dobject in emo_dict.items():
        filename=sep.join(['emo-locs',cc+'.txt'])
        with open(filename,'w') as wfile:
           for user,line in dobject.items():
                wfile.write(user+':')
                for emo in line:
                    wfile.write(emo+',')
                wfile.write('\n')

write_emos()
