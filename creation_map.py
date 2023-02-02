import argparse
import json
import sys
from math import floor
from multiprocessing import Pool
from multiprocessing import Queue
import csv

sys.path.insert(0,"/u/pe25171/kbart/")
sys.path.insert(0,"../../")
from dataclasses import asdict

import pandas as pd
import torch
from tqdm import tqdm
from transformers import pipeline, RobertaTokenizer

from assertion import Assertion

# rels = ["oEffect","oReact","oWant","xAttr","xEffect",
#         "xIntent","xNeed","xReact","xWant"]
# text_rels = ["has the effect on others of [FILL]",
#              "makes others react [FILL]",
#              "makes others want to do [FILL]",
#              "described as [FILL]",
#              "has the effect [FILL]",
#              "causes the event because [FILL]",
#              "before needs to [FILL]",
#              "after feels [FILL]",
#              "after wants to [FILL]"]
rels = ["AtLocation",
 "CapableOf",
 "Causes",
 "CausesDesire",
 "CreatedBy",
 "Desires",
"HasA",
 "HasFirstSubevent",
 "HasLastSubevent",
 "HasPrerequisite",
 "HasProperty",
 "HasSubEvent",
 "HinderedBy",
 "InstanceOf",
 "isAfter",
"isBefore",
"isFilledBy",
"MadeOf",
 "MadeUpOf",
 "MotivatedByGoal",
 "NotDesires",
 "ObjectUse",
 "UsedFor",
 "oEffect",
"oReact",
"oWant",
"PartOf",
 "ReceivesAction",
 "xAttr",
"xEffect",
 "xIntent",
 "xNeed",
 "xReact",
 "xReason",
 "xWant"]

text_rels = ["located or found at/in/on",
             "is/are capable of",
"causes",
"makes someone want",
"is created by",
"desires",
"has, possesses or contains",
"begins with the event/action",
"ends with the event/action",
"to do this, one requires",
"can be characterized by being/having","includes the event/action",
"can be hindered by",
"is an example/instance of",
"happens after",
"happens before",
"blank can be filled by",
"is made of",
"made (up) of",
"is a step towards accomplishing the goal","do(es) not desire",
"used for","used for",
"has the effect on others of",
"makes others react",
"makes others want to do",
"is a part of",
"can receive or be affected by the action",
 "described as",
"has the effect",
"causes the event because",
"before needs to",
"after feels",
"because",
"after wants to"]
print(len(text_rels),len(rels))

if __name__ == '__main__':
    mydata = pd.read_csv("train.tsv",sep="\t").drop_duplicates().reset_index()
    all_atomic_data = []
    for data in tqdm(mydata.iloc):
        subject = ''
        relation = ''
        object = ''
        try:
            subject = data.values[1].split()[0]
        except:
            continue
        try:
            clause = data.values[1]
        except:
            continue
        try:
            relation = data.values[2]
        except:
            continue
        try:
            object = data.values[3]
        except:
            continue
        assertion = Assertion(clause, relation, object)
        all_atomic_data.append({"subject": subject, "clause": clause, "relation": relation, "object": object})
    print(len(all_atomic_data))
    query_subject = "cat"
    res = []
    for item in all_atomic_data:
        if query_subject == item["subject"]:
            res.append(item)


    print(len(res))
    with open('output.tsv', 'w', newline='') as f_output:
        for item in all_atomic_data:
            writer = csv.writer(f_output, delimiter=' ')
            print(item)
            json.dump(item, f_output)
            writer.writerow('')
