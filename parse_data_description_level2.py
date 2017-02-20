#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import json
import re
import collections

with open('Data/occupations_structure.json', 'r') as f:
    occupations = json.load(f)
    major_level = [nid for nid in occupations.keys() if len(nid) == 1]
    major_level.sort()
    parse_level = [nid for nid in occupations.keys() if len(nid) == 2]
    parse_level.sort()

    major_str_list = ["Major Group " + level for level in major_level]
    parse_str_list = ["Sub-major Group " + level for level in parse_level]

with open('Data/occupation_definition.txt') as f:
    lines = f.readlines()

flag = 0
description = []
group_list = []
job_description = []
for l in lines:
    text = l.rstrip()
    text = text.decode('utf-8')
    if len(text) < 20: # skip too long sentence
        if text in major_str_list:
            flag = 0
        if text in parse_str_list:
            group_list.append(text)
            print "parse string", text
            index = parse_str_list.index(text)
            if index != 0:
                job_description.append(" ".join(description))
            description = []
            flag = 1
    elif flag == 1:
        description = description + \
            re.findall(
                "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+", text)

# deal with the last one
job_description.append(" ".join(description))

job_title_list = []
for p in parse_level:
    job_title_list.append(occupations[p]["name"])

title_descrip_dict = collections.OrderedDict()
for idx, job_des in enumerate(job_description):
    title_descrip_dict[job_title_list[idx]] = job_des

with open("Data/job_description_level2.json", 'w') as f:
    json.dump(title_descrip_dict, f, indent=4)
