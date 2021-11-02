#!/usr/bin/env python3

from datetime import datetime
from defusedxml import ElementTree
from pathlib import Path
import json

DATA_DIR = Path('../data')

def parse_date(xml_data):
    raw = xml_data.findall(".//ElectionDate")[0].text
    return datetime.strptime(raw, "%m/%d/%Y")

def write_dir(p, id_to_info):
    with open(p.joinpath('directory.json'), 'w') as f:
        json.dump(id_to_info, f)

def process_choice_data(contest_path, choice):
    res = {}
    for vote_type in choice.findall(".//VoteType"):
        for precinct in vote_type.findall(".//Precinct"):
            p = res.setdefault(precinct.attrib['name'], {})
            p[vote_type.attrib['name']] = int(precinct.attrib['votes'])
    for k in res:
        res[k]['Total'] = sum(res[k].values())
    with open(contest_path.joinpath('%s.json' % choice.attrib['key']), 'w') as f:
        json.dump(res, f)

def process_contest_data(election_path, contest):
    contest_path = election_path.joinpath(contest.attrib['key'])
    contest_path.mkdir(exist_ok=True)
    id_to_name = {}
    for choice in contest.findall(".//Choice"):
        id_to_name[choice.attrib['key']] = choice.attrib['text']
        process_choice_data(contest_path, choice)
    write_dir(contest_path, id_to_name)

def process_scytl_tree(data):
    election_date = parse_date(data)
    election_path = DATA_DIR.joinpath(
        datetime.strftime(election_date, '%Y-%m-%d'))
    election_path.mkdir(exist_ok=True)
    id_to_name = {}
    for contest in data.findall(".//Contest"):
        id_to_name[contest.attrib['key']] = contest.attrib['text']
        process_contest_data(election_path, contest)
    write_dir(election_path, id_to_name)

if __name__ == '__main__':
    xs = ElementTree.parse('detail.xml')
    process_scytl_tree(xs)
