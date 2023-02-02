import spacy
import requests

possible_rels = {'RelatedTo' : ' is related to ', 
'FormOf' : ' is a form of ',
'IsA': ' is a ',
'PartOf' : ' is a part of ',
'HasA' : ' has a ',
'UsedFor': ' is used for ',
'CapableOf': ' is capable of ',
'AtLocation': ' is located at ',
'Causes': ' causes ',
'HasSubevent': ' has a sub-event, ',
'HasFirstSubevent': ' starts with ',
'HasLastSubevent': ' ends with ',
'HasPrerequisite': ' requires first, ',
'HasProperty': ' has the property ',
'MotivatedByGoal': ' is motivated by the goal of ',
'ObstructedBy': ' is obstructed by ',
'Desires': ' desires ',
'CreatedBy': ' is created by ',
'Synonym': ' is synonymous with ',
'Antonym': ' is antonyms with ',
'DistinctFrom': ' is distinct from ',
'DerivedFrom': 'is derived from ',
'SymbolOf': ' is a symbol of ',
'DefinedAs': ' is defined as ',
'MannerOf': ' is a manner of ',
'LocatedNear': ' is located near ',
'HasContext': ' has the context, ',
'SimilarTo': ' is similar to ',
'EtymologicallyRelatedTo': ' is etymologically related to ',
'EtymologicallyDerivedFrom': ' is etymologically derived from ',
'CausesDesire': ' causes desire to ',
'MadeOf': ' is made of ',
'ReceivesAction': ' receives the action of '}

def make_sentence(rel):
  subj = rel[0]
  relation = rel[1]
  dobj = rel[2]
  return str(subj) + possible_rels[str(relation)] + str(dobj)



def get_subj(input_sentence):
  sent = input_sentence
  doc=nlp(sent)

  sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
  word = sub_toks[0]
  return word

def subj_prop(input_sentence):
  sent = input_sentence
  doc=nlp(sent)

  sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
  word = sub_toks[0]
  obj = requests.get('http://api.conceptnet.io/c/en/' + str(word)).json()

  for item in obj["edges"]:
    if item["rel"]["label"] == "AtLocation":
      print(str(word) + " is located at " + str(item["@id"].split('/')[-2]))
    if item["rel"]["label"] == "HasProperty":
      print(str(word) + " has property " + str(item["@id"].split('/')[-2]))
    if item["rel"]["label"] == "RelatedTo":
      print(str(word) + " has property " + str(item["@id"].split('/')[-2]))
    if item["rel"]["label"] == "IsA":
      print(str(word) + " has property " + str(item["@id"].split('/')[-2]))

def subj_loc(input_sentence):
  sent = input_sentence
  doc=nlp(sent)
  locations = []
  sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
  word = sub_toks[0]
  obj = requests.get('http://api.conceptnet.io/c/en/' + str(word)).json()

  for item in obj["edges"]:
    if item["rel"]["label"] == "AtLocation":
      locations.append(str(item["@id"].split('/')[-2]))
  return locations


def get_dobj(input_sentence):
  sent = input_sentence
  doc=nlp(sent)

  sub_toks = [tok for tok in doc if (tok.dep_ == "dobj") ]
  if (sub_toks):
    word = sub_toks[0]
  else:
    word = ''
  return word

def dobj_prop(input_sentence):
  sent = input_sentence
  doc=nlp(sent)

  sub_toks = [tok for tok in doc if (tok.dep_ == "dobj") ]
  if (sub_toks):
    word = sub_toks[0]
  else:
    word = ''
  print("Direct object: " + str(word))
  obj = requests.get('http://api.conceptnet.io/c/en/' + str(word)).json()


def location_dobj(input_sentence):
  dobj = get_dobj(input_sentence)
  print(dobj)
  for item in subj_loc(input_sentence):
    print(str(dobj) + ' located at ' + str(item))

def get_edges(word):
  rels = []
  obj = requests.get('http://api.conceptnet.io/c/en/' + str(word)).json()["edges"]
  for item in obj:
    typerel = item["rel"]["label"]
    rels.append((word, typerel, str(item["@id"].split('/')[-2])))
  return rels


def get_rels(sentence):
  subj = get_subj(sentence)
  rels = get_edges(subj)
  for rel in rels:
    print(make_sentence(rel))




if __name__ == '__main__':
  nlp = spacy.load("en_core_web_sm")
  print("Input sentence")
  sentence = input()
  get_rels(sentence)
  