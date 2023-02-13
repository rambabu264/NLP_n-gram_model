suggested_words = []

class TrieNode():
    # Initialising one node for trie
    def __init__(self):
        self.children = {}
        self.last = False
        self.word = None
        self.count = 0
        if self.last:
            self.count = 1
            
    def increment_count(self):
        self.count += 1


class Trie():
    def __init__(self):
        self.root = TrieNode()


    def formTrie(self, keys):
        for key in keys:
            self.insert(key) 

    def insert(self, key):
        node = self.root

        for a in key:
            if not node.children.get(a):
                node.children[a] = TrieNode()

            node = node.children[a]

        node.last = True
        node.word = key
        if node.last:
            node.increment_count()

    def suggestionsRec(self, node, word):
        if node.last:
            suggested_words.append([word, node.count])

        for a, n in node.children.items():
            self.suggestionsRec(n, word + a)

    def printAutoSuggestions(self, key):
        node = self.root

        for a in key:
            if not node.children.get(a):
                return (0, suggested_words)
            node = node.children[a]

        if not node.children:
            return (-1, suggested_words)

        self.suggestionsRec(node, key)
        return (1, suggested_words)

