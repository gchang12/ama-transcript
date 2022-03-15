from os import walk, sep, mkdir, system
from os.path import exists

def list_content_creators():
    cc_list=list()
    with open('content-creators.txt') as rfile:
        for line in rfile.readlines():
            line=line.strip()
            cc_list.append(line)
    return cc_list

def parse_file(filename):
    question=list()
    answer=list()
    l=question
    cc_list=list_content_creators()
    with open(filename) as rfile:
        for N,line in enumerate(rfile.readlines()):
            line=line.strip()
            if N < 2:
                continue
            elif not line:
                if N == 2:
                    # When the original commentor deleted his comment
                    line='(message deleted)'
                else:
                    l=answer
                    continue
            elif line in cc_list:
                continue
            elif line == '===':
                continue
            l.append(line)
    return question,answer

def get_emo_dict():
    emo_dict=dict()
    with open('emo-dict.csv') as rfile:
        for line in rfile.readlines():
            line=line.strip()
            line=line.split(',')
            emo_dict[line[0]]=line[1]
    return emo_dict

def replace_emo(line):
    ed=get_emo_dict()
    rstring=lambda s: '\\includesvg[width=9pt,height=9pt]{emoticons/%s}'%s
    for emo,code in ed.items():
        code=rstring(code)
        line=line.replace(emo,code)
    others={
        '’':'\'',\
        '“':'``',\
        '…':'...',\
        '”':'\'\'',\
        '‍':''
        }
    for key, val in others.items():
        line=line.replace(key,val)
    return line

def write_from_list(filename,wlist):
    characters='{','}','$','&','#','^','_','%'
    math_chars='<','>'
    with open(filename,'w') as wfile:
        for w in wlist:
            w=w.replace('\\','\\textbackslash')
            for c in characters:
                rtext='\\'+c
                if c == '^':
                    rtext+='{}'
                w=w.replace(c,rtext)
            for mc in math_chars:
                w=w.replace(mc,'$'+mc+'$')
            w=replace_emo(w)
            wfile.write(w+'\n')

def save_qa():
    src=['src',None]
    cc_list=list_content_creators()
    if not exists('qa'):
        mkdir('qa')
    for cc in cc_list:
        src[1]=cc
        folder=sep.join(src)
        cc='qa'+sep+cc
        dest=[cc,None]
        if not exists(cc):
            mkdir(cc)
        for x,y,filelist in walk(folder):
            for file in filelist:
                file=sep.join([folder,file])
                question,answer=parse_file(file)
                dest[1]='q-'+file.split(sep)[-1]
                destQ=sep.join(dest)
                dest[1]='a-'+file.split(sep)[-1]
                destA=sep.join(dest)
                write_from_list(destQ,question)
                write_from_list(destA,answer)

if __name__ == '__main__':
    save_qa()
