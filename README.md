# movie_scripts

## TL;DR
Remove useless parts of a movie script file(.srt) and save it to the text file.

## What does it do?
1. Parse the script file.
1. Remove indices of the sentence.
1. Remove start time and end time of each sentence.
1. Remove descriptions which are parenthesized.
1. Remove HTML tags which are encosed with <>.


## Example
>  '\ufeff1\n',   
 '00:00:12,440 --> 00:00:14,249\n',   
 '(MELLOW POP SONG\n',   
 'PLAYING ON WALKMAN)\n',   
 '\n',   
 '2\n',   
 '00:00:36,920 --> 00:00:37,967\n',   
 'Peter.\n',   
 '\n',   
 '3\n',   
 '00:00:39,480 --> 00:00:42,563\n',   
 'Your momma wants to speak with you.\n',   
 '\n',    
 ...   
    
to   

>  'Peter.'    
 'Your momma wants to speak with you.'   
 ...   
    

## How to Parse it?
I used LL parser to parse .srt file. 
Of course english sentences are not following CFG.
But .srt file has a strict format and i made following EBNF rules up.

### EBNF

> SCRIPT=UTF8BOM, {SUBTITLE};   
SUBTITLE=INDEX, TIMEINDICATOR, DESCRIPTION|SENTENCE, NEWLINE;   
INDEX={DIGIT}, NEWLINE;   
TIMEINDICATOR=TIME, RIGHTARROW, TIME, NEWLINE;   
TIME=DIGIT, DIGIT, COLON, DIGIT, DIGIT, COLON, DIGIT, DIGIT, REST, DIGIT, DIGIT, DIGIT;   
DESCRIPTION=LPAREN, DESC_TEXT, RPAREN, NEWLINE;   
SENTENCE={SENT_TEXT,NEWLINE};   
DESC_TEXT={ANY, NEWLINE};   
TAG_TEXT={ANY};   
SENT_TEXT={SENT_ITEM|TAG};   
TAG = LTAG, TAG_TEXT, RTAG;   
SENT_ITEM={ANY|DIGIT|LPAREN|RPAREN|REST|COLON};   
   
### Tokens   

> UTF8BOM="\ufeff1";   
DIGIT="1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"0";   
NEWLINE="\n";   
RIGHTARROW=" --> ";   
COLON=":";   
REST=",";   
LPAREN="(";   
RPAREN=")";   
ANY=any character except above.;   



 
 
