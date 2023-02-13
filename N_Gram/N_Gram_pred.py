import N_Gram
import json
import pprint as pp

def refresh_models(filename):
    with open(filename) as file:
        data= json.load(file)
    sent = []
    for d in data:
        sent.append(d[list(d.keys())[0]])
    corpus  = [element for innerList in sent for element in innerList]
    bigram = N_Gram.N_Grams(corpus, 2)
    unigram = N_Gram.N_Grams(corpus, 1)
    trigram = N_Gram.N_Grams(corpus, 3)
    quadgram = N_Gram.N_Grams(corpus, 4)
    N_Gram.save_model(bigram, "bigram.json")
    print("Created & Stored Bigram")
    N_Gram.save_model(unigram, "unigram.json")
    print("Created & Stored Unigram")
    N_Gram.save_model(trigram, "trigram.json")
    print("Created & Stored Trigram")
    N_Gram.save_model(quadgram, "quadgram.json")
    print("Created & Stored Quadgram")

def get_prediction(sent):
    length = len(sent.split(' '))
    ngram = {}
    n = length
    if length == 1:
        ngram = N_Gram.open_model("unigram.json")
    elif length == 2:
        ngram = N_Gram.open_model("bigram.json")
    elif length == 3:
        ngram = N_Gram.open_model("trigram.json")
    elif length < 1:
        return "CANNOT DO PREDICTION!"
    else:
        n = 4
        ngram = N_Gram.open_model("quadgram.json")
    pred = N_Gram.generate_text(ngram, sent, n)
    return pred

if __name__ == "__main__":
    file = "extracted.json"
    corpus = refresh_models(file)
    #pp.pprint(corpus)
    pr = "hello there"
    txt = get_prediction(pr)
    print("text:", pr)
    print("Prediction:", txt)
