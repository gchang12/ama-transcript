from os import mkdir, walk
from os.path import sep, exists

from reddit_scraper.link_fetcher import get_link_compendium
from reddit_scraper.comment_fetcher import get_qa

def filename_maker(crew_member,username):
    filename=sep.join([crew_member,username])+'.txt'
    return filename

def get_dir_len(author):
    for x,y,filelist in walk(author):
        return len(filelist)

def save_comment(url,username,crew_member):
    filename=filename_maker(crew_member,username)
    make_header=lambda x: '%s\n===\n'%x
    src=get_qa(url)
    header1=make_header(username)
    header2=make_header(crew_member)
    if not src:
        return
    elif len(src) == 1:
        write_list=header1,'\n'*3,header2,src[0]
    else: # possibility of more comments than the initial Q&A handled in line 15 of comment_fetcher.py
        write_list=header1,src[0]+'\n'*3,header2,src[1]
    with open(filename,'w') as wfile:
        for val in write_list:
            wfile.write(val)

def get_data_len(author):
    data=get_link_compendium()[author]
    return len(data)

def compare_lengths(n=None):
    if n is None:
        castcrew=(
            'Daron Nefcy',\
            'Adam McArthur',\
            'Dominic Bisignano',\
            'Aaron Hammersley'
            )
        key=castcrew[n]
    else:
        key=n
    n=get_dir_len(key)
    m=get_data_len(key)
    if n < m:
        msg='There are %d/%d comment(s) that need to be gathered'%((m-n),m)
    else:
        msg='All data is compiled'
    message='\n'+msg+' for %s.'%key
    print(message)

def compile_all_comments():
    data_src=get_link_compendium()
    message=lambda x,y,n: "Current scraping %s's question for %s on try %d.\n"%(x,y,n)
    for author_name,data in data_src.items():
        author_name=author_name.replace(':','')
        if not exists(author_name):
            mkdir(author_name)
        for username,url in data.items():
            filename=filename_maker(author_name,username)
            count=1
            while not exists(filename):
                save_comment(url,username,author_name)
                if exists(filename):
                    compare_lengths(author_name)
                else:
                    x=message(username,author_name,count)
                    count+=1
                    print(x)

if __name__ == '__main__':
    compile_all_comments()
