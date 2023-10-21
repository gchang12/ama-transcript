def list_content_creators():
    cc_list=list()
    with open('content-creators.txt') as rfile:
        for line in rfile.readlines():
            line=line.strip()
            cc_list.append(line)
    return cc_list
