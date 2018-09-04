class Processor(object):
    
    def __init__(self):
        pass
    
    def collect_sentences(self, script):
        sentences = []
        for subtitle in script['SUBTITLE']:
            sentences.append(subtitle['SENTENCE'])
        return sentences
    
    def write_sentences(self, script, filepath):
        sentences = self.collect_sentences(script)
        with open(filepath, 'w') as f:
            for sentence in sentences:
                f.write(sentence + '\n')
        