'''
    StanfordCoreNLP wrapper.
    Need to start StanfordCoreNLP server manually by running the command:
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000
    in your folder where the unzipped StanfordCoreNLP is located.
'''

from stanfordcorenlp import StanfordCoreNLP
import logging
import json

class StanfordNLP:
    """
        Python StanfordNLP Wrapper.

        Connect to localhost:9000.
    """

    def __init__(self, host="http://localhost", port=9000):
        self.nlp = StanfordCoreNLP(host, port = port, timeout = 30000)
        self.props = {
            "annotators": "tokenize, split, pos, lemma, ner, parse, depparse, dcoref, relation",
            "pipelineLanguage": "en",
            "outputFormat": "json"
        }

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))

    @staticmethod
    def tokens_to_dict(_tokens):
        tokens = defaultdict(dict)
        for token in _tokens:
            tokens[int(token['index'])] = {
                'word': token['word'],
                'lemma': token['lemma'],
                'pos': token['pos'],
                'ner': token['ner']
            }
        return tokens


if __name__ == "__main__":
    nlp = StanfordNLP()
    text = "A blog post using Stanford CoreNLP Server. Visit www.khalidalnajjar.com for more details."
    # print("Annotate:", nlp.annotate(text))
    print("POS:", nlp.pos(text))
    print("Tokens:", nlp.word_tokenize(text))
    print("NER:", nlp.ner(text))
    print("Parse:",  nlp.parse(text))
    print("Dep Parse:", nlp.dependency_parse(text))
