# -*- coding: utf-8 -*-
import json
import re
import nltk


class Node(dict):

    def __init__(self):
        dict.__init__(self)

    def add_node(self, nid, name, children=[]):
        self[nid] = {'name': name, 'children': list(children)}

    def add_child(self, nid, child):
        self[nid]['children'].append(child)


def occupation_to_json():
    '''parse occupation data structure'''
    with open('Data/occupations.txt') as f:
        lines = f.readlines()
    f.close()
    occupation_structure = Node()
    for l in lines:
        id_title_list = l.split("\t")
        if len(id_title_list) < 2:  # skip empty lines
            continue
        nid = id_title_list[0]
        name = id_title_list[1].rstrip()
        occupation_structure.add_node(nid, name)
        len_id = len(nid)
        while len_id > 1:
            parent_id = nid[0:len_id - 1]
            occupation_structure.add_child(parent_id, nid)
            len_id -= 1
    with open('Data/occupations_structure.json', 'w') as f:
        json.dump(occupation_structure, f)
    f.close()
    return occupation_structure


if __name__ == '__main__':
    occupation_structure = occupation_to_json()
