UTF8BOM = '\ufeff'
DIGIT = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}
NEWLINE = '\n'
RIGHTARROW = ' --> '
COLON = ':'
REST = ','
LPAREN = '('
RPAREN = ')'
LTAG = '<'
RTAG = '>'

class Tokenizer(object):
    
    
    def __init__(self):
        pass
    
    def tokenize(self, string):
        stack = list(string)
        tokens = []
        while len(stack) > 0:
            any_check = True
            for pop_func in [self.pop_utf8bom, self.pop_digit, self.pop_newline, 
                             self.pop_rightarrow, self.pop_colon, self.pop_rest, 
                             self.pop_lparen, self.pop_rparen, 
                             self.pop_ltag, self.pop_rtag]:
                try:
                    token = pop_func(stack)
                    if token is not None:
                        tokens.append(token)
                        any_check = False
                except IndexError as e:
                    print(e)
                    break
            if any_check:
                tokens.append(self.pop_any(stack))
        return tokens
        
    def pop_utf8bom(self, stack):
        #print('hi', stack[0], 'bye', UTF8BOM)
        if stack[0] == UTF8BOM:
            popped = stack.pop(0)
            return {'UTF8BOM':popped}
        else:
            return None
    
    def pop_digit(self, stack):
        if stack[0] in DIGIT:
            popped = stack.pop(0)
            return {'DIGIT':popped}
        else:
            return None
    
    def pop_newline(self, stack):
        if stack[0] == NEWLINE:
            popped = stack.pop(0)
            return {'NEWLINE':popped}
        else:
            return None
    
    def pop_rightarrow(self, stack):
        if ''.join(stack[:len(RIGHTARROW)]) == RIGHTARROW:
            popped = ''.join([stack.pop(0) for _ in range(len(RIGHTARROW))])
            return {'RIGHTARROW':popped}
        else:
            return None
        

    def pop_colon(self, stack):
        if stack[0] == COLON:
            popped = stack.pop(0)
            return {'COLON':popped}
        else:
            return None
        
    def pop_rest(self, stack):
        if stack[0] == REST:
            popped = stack.pop(0)
            return {'REST':popped}
        else:
            return None
        
    def pop_lparen(self, stack):
        if stack[0] == LPAREN:
            popped = stack.pop(0)
            return {'LPAREN':popped}
        else:
            return None
        
    def pop_rparen(self, stack):
        if stack[0] == RPAREN:
            popped = stack.pop(0)
            return {'RPAREN':popped}
        else:
            return None
    
    def pop_ltag(self, stack):
        if stack[0] == LTAG:
            popped = stack.pop(0)
            return {'LTAG':popped}
        else:
            return None
    
    def pop_rtag(self, stack):
        if stack[0] == RTAG:
            popped = stack.pop(0)
            return {'RTAG':popped}
        else:
            return None
        
    def pop_any(self, stack):
        popped = stack.pop(0)
        return {'ANY':popped}
    