from src.metrics import basic


class Manager:
    def __init__(self, filename):
        self.text = open(filename, "r").read()

    def preprocess(self, text):
        pass

    def analyse(self):
        return basic.avg_sentence_length(self.text)

    def postprocess(self, text, previous_results):
        pass
