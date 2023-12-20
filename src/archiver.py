#!/usr/bin/python3
"""
"""

ROOT_URL = 'https://www.reddit.com/r/StarVStheForcesofEvil/comments/cll9u5/star_vs_the_forces_of_evil_ask_me_anything'
# All source URLs are of the form: 
# - ROOT_URL/{url_id}/?context=3

import sqlite3
import re

from pathlib import Path

def list_content_creators():
    cc_list=list()
    with open('content-creators.txt') as rfile:
        for line in rfile.readlines():
            line=line.strip()
            cc_list.append(line)
    return cc_list

def fix_line_quotes(line):
# Fixes the quotes for TeX
    pattern='(?<=\s)"|^"'
    line=re.sub(pattern,'``',line)
    return line


def parse_file(filename):
    # Extracts contents of web-scraped file into two files:
    # - one for the question, and one for the answer
    question=list()
    answer=list()
    # Collect question first
    l=question
    cc_list=list_content_creators()
    with open(filename) as rfile:
        for N,line in enumerate(rfile.readlines()):
            line=line.strip()
            # Skip header and equals-sign delimiter
            if N < 2:
                continue
            elif not line:
                if N == 2:
                    # When the original commentor deleted his comment
                    line='(message deleted)'
                else:
                    # If not 3rd line and the line is blank, then switch to collecting contents of answer
                    l=answer
                    continue
            elif line in cc_list:
                # Skip name of content-creator
                continue
            elif line == '===':
                # Skip the delimiter
                continue
            line=fix_line_quotes(line)
            # Append line to whichever list is set to `l'
            l.append(line)
    return question,answer

if __name__ == '__main__':
    url_getter = lambda url_id: f'https://www.reddit.com/r/StarVStheForcesofEvil/comments/cll9u5/star_vs_the_forces_of_evil_ask_me_anything/{url_id}/?context=3'
    con = sqlite3.connect("output/ama_archive.db")
    try:
        cur = con.execute("CREATE TABLE ama_session(content_creator TEXT, fan_name TEXT, question_text TEXT, answer_text TEXT, url_id TEXT)")
    except sqlite3.OperationalError:
        print("table exists already. skipping")
        cur = con.cursor()
        pass
    record_list = []
    for cc_dir in Path("output").iterdir():
        if not cc_dir.is_dir():
            # skip database file
            continue
        for query_file in cc_dir.iterdir():
            # content_creator
            content_creator = query_file.parts[1]
            fan_name = query_file.parts[2].replace('.txt', '')
            #print(query_file)
            question_lines, answer_lines = parse_file(query_file)
            question_text = "\n".join(question_lines)
            answer_text = "\n".join(answer_lines)
            # links/{cc_dir}/{fan_name}.txt
            url_file = Path("links", content_creator, fan_name + ".txt")
            url_id = url_file.read_text().strip().split("/")[-2]
            record = {
                "content_creator": content_creator,
                "fan_name": fan_name,
                "question_text": question_text,
                "answer_text": answer_text,
                "url_id": url_id,
                }
            record_list.append(record)
    cur.executemany("INSERT INTO ama_session VALUES(:content_creator, :fan_name, :question_text, :answer_text, :url_id)", record_list)
    con.commit()
