class Trie:
    def __init__(self):
        self.root = {}

    def add_word(self, word):
        current = self.root
        for char in word:
            if char not in current:
                current[char] = {}
            current = current[char]
        current["__leaf__"] = True

    def find_node(self, prefix):
        current = self.root
        for char in prefix:
            if not char in current:
                return False
            current = current[char]
        return current

    def match_prefix(self, prefix):
        node = self.find_node(prefix)
        if not node:
            return False
        return self._leaves(node, prefix, [])

    # This could be cleaner with a node object, but I don't want to have to
    # serialize a python object for every node, so I'm living with passing the
    # state
    def _leaves(self, node, prefix, result=[]):
        if "__leaf__" in node:
            result.append(prefix)

        for child in node:
            if child == "__leaf__":
                continue
            self._leaves(
                node[child],
                prefix + child,
                result
            )

        return result
