'''
# EBNF
SCRIPT=UTF8BOM, {SUBTITLE};
SUBTITLE=INDEX, TIMEINDICATOR, DESCRIPTION|SENTENCE, NEWLINE;
INDEX={DIGIT}, NEWLINE;
TIMEINDICATOR=TIME, RIGHTARROW, TIME, NEWLINE;
TIME=DIGIT, DIGIT, COLON, DIGIT, DIGIT, COLON, DIGIT, DIGIT, REST, DIGIT, DIGIT, DIGIT;
DESCRIPTION=LPAREN, DESC_TEXT, RPAREN, NEWLINE;
SENTENCE={SENT_TEXT,NEWLINE}
DESC_TEXT={ANY, NEWLINE};
TAG_TEXT={ANY};
SENT_TEXT={SENT_ITEM|TAG};
TAG = LTAG, TAG_TEXT, RTAG;
SENT_ITEM={ANY|DIGIT|LPAREN|RPAREN|REST|COLON};


# tokens
UTF8BOM="\ufeff1";
DIGIT="1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"0";
NEWLINE="\n";
RIGHTARROW=" --> "
COLON=":"
REST=","
LPAREN="(";
RPAREN=")";
ANY=a character except above

# Output Filetype
script = {'UTF8BOM':str, 'SUBTITLE':list}
script['SUBTITLE'][0] = {'INDEX':int, 'TIMEINDICATOR':dict, 'DESCRIPTION':str, 'SENTENCE':str}
script['SUBTITLE'][0]['TIMEINDICATOR']={'STARTTIME':str, 'ENDTIME':str}
'''
        
class Parser(object):
    
    def __init__(self, allow_tag=False):
        self.allow_tag = allow_tag
    
    # SCRIPT=UTF8BOM, {SUBTITLE};
    def take_script(self, tokens):
        tokens = tokens.copy()
        script = dict()
        utf8bom = self.return_token_or_raise(tokens, 'UTF8BOM')
        script.update({'UTF8BOM':utf8bom})
        script['SUBTITLE'] = []
        while(len(tokens) > 0):
            subtitle = self.return_term_or_raise(tokens, self.take_subtitle)
            script['SUBTITLE'].append(subtitle)
        return script
    
    # SUBTITLE=INDEX, TIMEINDICATOR, DESCRIPTION|SENTENCE, NEWLINE;
    def take_subtitle(self, tokens):
        subtitle = dict()
        index = self.return_term_or_raise(tokens, self.take_index)
        subtitle.update({'INDEX':index})
        timeindicator = self.return_term_or_raise(tokens, self.take_timeindicator)
        subtitle.update({'TIMEINDICATOR':timeindicator})
        try:
            description = self.take_description(tokens)
            subtitle.update({'DESCRIPTION':description})
        except Exception as e:
            pass
        try:
            sentence = self.take_sentence(tokens)
            subtitle.update({'SENTENCE':sentence})
        except Exception as e:
            pass
        newline = self.return_token_or_raise(tokens, 'NEWLINE')
        return subtitle

    # INDEX={DIGIT}, NEWLINE;      
    def take_index(self, tokens):
        index = []
        index_value = ''
        while(True):
            try:
                digit = self.return_token_or_raise(tokens, 'DIGIT')
                index_value += digit
            except:
                break            
        newline = self.return_token_or_raise(tokens, 'NEWLINE')
        index.append({'INDEX':int(index_value)})
        return index

    # TIMEINDICATOR=TIME, RIGHTARROW, TIME, NEWLINE;
    def take_timeindicator(self, tokens):
        timeindicator = dict()
        
        starttime = self.return_term_or_raise(tokens, self.take_time)
        rightarrow = self.return_token_or_raise(tokens, 'RIGHTARROW')
        endtime = self.return_term_or_raise(tokens, self.take_time)
        newline = self.return_token_or_raise(tokens, 'NEWLINE')
        
        timeindicator.update({'STARTTIME':starttime, 'ENDTIME':endtime})
        return timeindicator
        
    # TIME=DIGIT, DIGIT, COLON, DIGIT, DIGIT, COLON, DIGIT, DIGIT, REST, DIGIT, DIGIT, DIGIT;
    def take_time(self, tokens):
        
        hour1 = self.return_token_or_raise(tokens, 'DIGIT')
        hour2 = self.return_token_or_raise(tokens, 'DIGIT')
        colon1 = self.return_token_or_raise(tokens, 'COLON')
        min1 = self.return_token_or_raise(tokens, 'DIGIT')
        min2 = self.return_token_or_raise(tokens, 'DIGIT')
        colon2 = self.return_token_or_raise(tokens, 'COLON')
        sec1 = self.return_token_or_raise(tokens, 'DIGIT')
        sec2 = self.return_token_or_raise(tokens, 'DIGIT')
        rest = self.return_token_or_raise(tokens, 'REST')
        ms1 = self.return_token_or_raise(tokens, 'DIGIT')
        ms2 = self.return_token_or_raise(tokens, 'DIGIT')
        ms3 = self.return_token_or_raise(tokens, 'DIGIT')
        
        time = hour1 + hour2 + colon1 + \
               min1 + min2 + colon2 + \
               sec1 + sec2 + rest + \
               ms1 + ms2 + ms3
        return time
    
    #DESCRIPTION=LPAREN, TEXT, RPAREN, NEWLINE;
    def take_description(self, tokens):
        
        lparen = self.return_token_or_raise(tokens, 'LPAREN')
        desctext = self.return_term_or_raise(tokens, self.take_desctext)
        rparen = self.return_token_or_raise(tokens, 'RPAREN')
        newline = self.return_token_or_raise(tokens, 'NEWLINE')
        
        description = lparen + desctext + rparen
        return description
    
    
    # SENTENCE={SENT_TEXT,NEWLINE}
    def take_sentence(self, tokens):
        sentence = ''
        while(True):
            try:
                text = self.return_term_or_raise(tokens, self.take_senttext)
                newline = self.return_token_or_raise(tokens, 'NEWLINE')
                sentence += text + ' '
            except Exception as e:
                break
        return sentence
    
    
    #SENT_TEXT={SENT_ITEM|TAG};
    def take_senttext(self, tokens):
        senttext = ''
        while(True):
            try:
                sentitem = self.return_term_or_raise(tokens, self.take_sentitem)
                #print(sentitem)
                senttext += sentitem
            except:
                try:
                    tag = self.return_term_or_raise(tokens, self.take_tag)
                    if self.allow_tag:
                        senttext += tag
                except:
                    break
        return senttext
            
    #TAG = LTAG, TAGTEXT, RTAG;
    def take_tag(self, tokens):
        ltag = self.return_token_or_raise(tokens, 'LTAG')
        tagtext = self.return_term_or_raise(tokens, self.take_tagtext)
        rtag = self.return_token_or_raise(tokens, 'RTAG')
        tag = ltag + tagtext + rtag
        return tag
        
    #SENT_ITEM={ANY|DIGIT|LPAREN|RPAREN|REST|COLON};
    def take_sentitem(self, tokens):
        text = ''
        while(True):
            if list(tokens[0].keys())[0] in ['ANY', 'DIGIT', 'LPAREN', 'RPAREN', 'COLON', 'REST']:
                text += list(tokens.pop(0).values())[0]
            else:
                break
        return text
    
    #DESCTEXT={ANY, NEWLINE}
    def take_desctext(self, tokens):
        text = ''
        while(True):
            if list(tokens[0].keys())[0] in ['ANY', 'NEWLINE']:
                text += list(tokens.pop(0).values())[0]
            else:
                break
        return text
    
    #TAGTEXT={ANY, DIGIT}
    def take_tagtext(self, tokens):
        text = ''
        while(True):
            if list(tokens[0].keys())[0] in ['ANY', 'DIGIT']:
                text += list(tokens.pop(0).values())[0]
            else:
                break
        return text
    
    def return_token_or_raise(self, tokens, token_name):
        if token_name in tokens[0].keys():
            return tokens.pop(0)[token_name]
        else:
            raise Exception('not expected token exception', tokens[0].keys(), token_name)
        
    def return_term_or_raise(self, tokens, take_term_func):
        term = take_term_func(tokens)
        if len(term) == 0:
            raise Exception('not expected term exception')
        else:
            return term
        
    