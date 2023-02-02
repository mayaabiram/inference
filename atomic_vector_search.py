import sys
import pandas as pd
import torch
import transformers

sys.path.insert(0,"../../")

import faiss #faiss-cpu
from tqdm import tqdm
from sentence_transformers import SentenceTransformer # sentence-transformers
import numpy as np
from assertion import Assertion



def first_level_relation(sentence):
    model = SentenceTransformer('all-mpnet-base-v2')
    model = model.to("mps")
    sentence_assertions = []
    data = pd.read_csv("./train.tsv", on_bad_lines='skip', sep="\t")
    print(data)

    count = 0
    for fact in tqdm(data.iloc, total=data.shape[0]):
        assertion = Assertion()
        assertion.subject = str(fact["subject"])
        assertion.relation = str(fact["relation"])
        assertion.object = str(fact["object"])
        sentence_assertions.append(" ".join([assertion.subject, assertion.relation, assertion.object]))
        count+=1
        if count == 5000:
            break
    print("Encoding.")
    # pool = model.start_multi_process_pool(target_devices=[0])
    # encoded = model.encode_multi_process(sentence_assertions, pool)
    encoded = model.encode(sentence_assertions,show_progress_bar=True)

    print("Done")
    index = faiss.IndexFlatIP(768) #dim of sent transf
    print(index)
    index.add(encoded.astype(np.float32))  # add vectors to the index

    queries = [sentence]
    query = model.encode(queries)

    k = 5
    q = np.ascontiguousarray(query.astype(np.float32))

    tot = []

    # q = np.expand_dims(q,0)
    D, I = index.search(q, k)  # Story level alignment, need to do sentence level alignment after this
    # print(I)
    print("Total:")
    print(I.shape)
    nearest_neightbor = []
    for j, i in enumerate(I):
        nearest_neightbor.append([])
        for sub_i in i:
            nearest_neightbor[j].append(sentence_assertions[sub_i])

        tot.append(nearest_neightbor[j])
    return tot