import nltk
import re

class RelationalEntity(object):

    def __init__(self, subj_type, obj_type, subj, obj):
        self.subj_type  = subj_type
        self.obj_type   = obj_type
        self.subj       = subj
        self.obj        = obj
    
    def __repr__(self):
        return repr('sub_type={0}, obj_type={1}, sub={2}, obj={3}'.format(self.subj_type, self.obj_type, self.subj, self.obj))

def findrelations(text):
    entities = [];
    
    IN                      = re.compile(r'.*\bin\b(?!\b.+ing)')
    
    sentences               = nltk.sent_tokenize(text)
    tokenized_sentences     = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences        = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    
    chunked_sentences       = nltk.ne_chunk_sents(tagged_sentences)    
    
    sub                     = 'ORGANIZATION'
    obj                     = 'GPE'      
    for doc in chunked_sentences:
        for rel in nltk.sem.extract_rels(sub, obj, doc, corpus='ace', pattern=IN):
            raw_entity = nltk.sem.clause(rel, '')
            entities.append(RelationalEntity(sub, obj, raw_entity[2:(raw_entity.find('\'',2))], raw_entity[(raw_entity.find('\'',2)+4):(len(raw_entity)-2)]))
    return entities