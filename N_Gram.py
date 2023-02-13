import nltk
import re
import pprint as pp
import numpy as np
import json

dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])

def N_Grams(text, n):
    
    ngrams, n1gram = [], []
    for txt in text:
        for i in range(0,n-1):
            txt = '<s> ' + txt
            txt = txt + ' </s>'
        ngrams += list(nltk.ngrams(txt.split(), n))
        n1gram += list(nltk.ngrams(txt.split(), n - 1))
    #pp.pprint(ngrams)
    #pp.pprint(n1gram)
    ngram_freq = {x[0]: x[1] for x in [x for x in nltk.FreqDist(ngrams).items()]}
    #print(ngram_freq)
    
    n1gram_freq = {x[0]: x[1] for x in [x for x in nltk.FreqDist(n1gram).items()]}
    #print(n1gram_freq)
    
    ngram_prob = {}
    for k,v in ngram_freq.items():
        ngram = k
        if ngram[:-1] in n1gram:
            prob = v / n1gram_freq[ngram[:-1]]
            ngram_prob[k] = prob
    
    return ngram_prob

def generate_text(prob, prompt, n):

    if len(prompt.split(' ')) < (n - 1):
        return 'TEXT CANNOT BE GENERATED'
    #pp.pprint(prob)
    #print("prompt:", prompt.split(' '))
    text = ['<s>']
    text.extend(prompt.split(' '))
    #print("text:", text)
    pref_tup = tuple(text[-(n-1):])    
    cnt = 0
    while (pref_tup[-1] != '</s>') and (cnt < 3):
        #print("Pref Tuple:", pref_tup)
        #print([tup[:-1] for tup in prob.keys()])
        keys = [tup for tup in prob.keys() if pref_tup == tup[:-1]]
        if keys == None:
            return " ".join(text[1:])
        #print("keys:",keys)
        prob_keys = dictfilt(prob, keys)
        #print(prob_keys)
        max_key = max(prob_keys, key=prob_keys.get)[-1]
        #print("word:", max_key)
        pref_tup = list(pref_tup)
        pref_tup.append(max_key)
        pref_tup = tuple(pref_tup[1:])
        text.append(max_key)
        cnt += 1
        #text.append(word)
    #print(text[1:])
    pred = ' '.join(text[1:])
    pred = pred.replace("</s>", "")
    return pred

def preprocess(txt):

    txt = re.sub(r'\n{2,}|^\n', '', txt)
    txt = re.sub(r'^\d+\s|\s\d+\s|\s\d+$', ' ', txt)
    txt = re.sub(r'\.', '', txt)
    txt = re.sub(r',', '', txt)
    return txt
    
def save_model(dict, filename="ngram-model.json"):
    dict = {','.join(list(k)):v for k,v in dict.items()}
    with open(filename, "w") as outfile:
        json.dump(dict, outfile)

def open_model(filename="ngram-model.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    data = {tuple(k.split(',')):v for k,v in data.items()}
    return data

if __name__ == "__main__":

    text = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 
            'Sed massa felis, fermentum et tortor sit amet, semper imperdiet orci.']
    text = [preprocess(x) for x in text]
    n = 2
    prob = N_Grams(text, n)
    #print(prob)
    save_model(prob)
    prob = open_model()
    sent = generate_text(prob, 'lorem ipsum dolor', n)
    sent = re.sub(r'\,|\.', '', sent)
    print(sent)