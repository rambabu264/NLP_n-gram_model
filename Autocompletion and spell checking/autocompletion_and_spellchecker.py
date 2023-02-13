from trie_data_structure import Trie
import json
import nltk
nltk.download('punkt')

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search(node, word, maxCost ):

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in node.children:
        searchRecursive( node.children[letter], letter, word, currentRow, 
            results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in range( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:                
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append( (node.word, currentRow[-1] ) )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow, 
                results, maxCost )


def word_spellcheck(word, trie):
     
    for i in range(1, len(word)):
        results = search(trie.root, word, i)
        if len(results) > 0:
            break
    return results
        


def word_suggestion(key, trie):
 
    # autocompleting the given key using
    # our trie structure.
    flag, comp = trie.printAutoSuggestions(key)

    if flag == 1:
        # Sorting the suggested words with the number of frequencies and 
        # listing out top 5 frequet words 
        return sorted(comp, key = lambda x: x[1], reverse= True)[:5]
    elif flag == -1:
        return [key]
    else:
        return word_spellcheck(key, trie)

path = "D:\College\Packages\Wikipedia_scraping\wiki_scraper\extract_100.json"
def trie_build(path):
    with open(path) as file:
        data= json.load(file)

    sent = ""
    for d in data:
        sent += '.'.join(d[list(d.keys())[0]])

    keys = nltk.word_tokenize(sent)

    # creating trie object
    t = Trie()

    # creating the trie structure with the
    # given set of strings.
    t.formTrie(keys)

    return t

# if __name__ == "__main__":
#     file_path = "D:\College\Packages\Wikipedia_scraping\wiki_scraper\extract_100.json"
#     trie =  trie_build(file_path)
#     print(word_suggestion("biis", trie))
    # print(word_spellcheck("biis", trie))