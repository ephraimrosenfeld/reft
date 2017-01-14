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


def get_rel(tokens, tree, sub_precedes_obj):
    if len(tokens) == 0 or len(tree) == 0 or (len(tree) < len(tokens)) :
        return None
    sub_type, obj_type, sub, obj = '', '', '', ''    
    token_index = 0    
    subj_found, obj_found    = False, False
    for i in range((len(tree) - len(tokens))):
        val = ''
        print(str(i) + ': ' + str(type(tree[i])))
        if isinstance(tree[i], nltk.tree.Tree):
            print(str(tree[i]) + ' is a tree')
            val = tree[i].label()
        else :#tuple    
            val = str(tree[i][1])
        print('val: ' + val)    
        if tokens[token_index].lower() == val.lower():
            if isinstance(tree[i], nltk.tree.Tree):
                if sub_precedes_obj:
                    if subj_found == False :
                        subj_found     = True
                        sub_type     = tokens[i]
                        sub            = ' '.join([x[0] for x in tree[i].leaves()])
                    else:
                        obj_found    = True
                        obj_type     = tokens[i]
                        obj            = ' '.join([x[0] for x in tree[i].leaves()])
                else:
                    if obj_found == False :
                        obj_found     = True
                        obj_type     = tokens[i]
                        obj            = ' '.join([x[0] for x in tree[i].leaves()])
                    else:
                        subj_found     = True
                        sub_type          = tokens[i]
                        sub            = ' '.join([x[0] for x in tree[i].leaves()])
            token_index = token_index + 1
            if subj_found and obj_found: #match found
                return RelationalEntity(sub_type, obj_type, sub, obj)
        elif subj_found or obj_found:
            return None
        else :
            continue
    return None   

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
        print(doc)
        for rel in nltk.sem.extract_rels(sub, obj, doc, corpus='ace', pattern=IN):
            raw_entity = nltk.sem.clause(rel, '')
            print(raw_entity)
            entities.append(RelationalEntity(sub, obj, raw_entity[2:(raw_entity.find('\'',2))], raw_entity[(raw_entity.find('\'',2)+4):(len(raw_entity)-2)]))
    print('entities retrieved: '+ str(len(entities)))
    return entities