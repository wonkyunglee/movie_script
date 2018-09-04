import os
from tokenizer import Tokenizer
from parser import Parser
from processor import Processor


FILENAME = 'guardians_of_the_galaxy'
#FILENAME = 'doctor_strange'
def main():
    with open(os.path.join('original_scripts', FILENAME + '.srt'), 'r') as f:
        string = f.read()

    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(string)
    parser = Parser()
    script = parser.take_script(tokens)
    processor = Processor()
    processor.write_sentences(script, os.path.join('processed_scripts', FILENAME+'.txt'))


if __name__=='__main__':
    main()
