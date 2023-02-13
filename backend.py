from flask import Flask, jsonify, request
from Autocompletion_and_spell_checking.autocompletion_and_spellchecker import trie_build, word_suggestion
from N_Gram import N_Gram_pred
app = Flask(__name__)

file_path = "D:\College\Packages\Wikipedia_scraping\wiki_scraper\extract_100.json"


# @app.route("/home/<string:word>", methods=['GET'])
# def autocomplete_spellchecker(word):
#     if request.method == 'GET':

#         # word = request.args.get('word')
#         trie =  trie_build(file_path)

#         return jsonify( {"words": word_suggestion(word, trie)} )
@app.route("/home", methods=['GET'])
def autocomplete_spellchecker():
    if request.method == 'GET':
        sent = request.args.get('sent')
        word_to_suggest = sent.split(" ")[-1]
        trie = trie_build(file_path)

        return jsonify({"words": word_suggestion(word_to_suggest, trie)})

@app.route("/ngram", methods=['GET'])
def n_gram_model():
    if request.method == 'GET':
        sent = request.args.get('sent')

        file = "extracted.json"
        corpus = N_Gram_pred.refresh_models(file)

        txt = N_Gram_pred.get_prediction(sent)

        return jsonify({"Prediction:", txt})