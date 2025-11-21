import sys
import sre_parse
from typing import Set, Dict, Optional

# ------- AST Node Classes ------
class AstNode:
    pass

class LiteralNode(AstNode):
    def __init__(self, char):
        self.char = char
        
class ConcatNode(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class UnionNode(AstNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class StarNode(AstNode):
    def __init__(self, child):
        self.child = child
        
class PlusNode(AstNode):
    def __init__(self, child):
        self.child = child
        
        
        
# ------ NFA Classes ------
class State:
    def __init__(self, is_accept=False):
        self.is_accept = is_accept
        self.transitions: Dict[Optional[str], Set['State']] = {}
        self.state_id = id(self)

    def add_transition(self, symbol: Optional[str], state: 'State'):
        if symbol not in self.transtions:
            self.transtions[symbol] = set()
        self.transitions[symbol].add(state)

class NFA:
    start: State
    accept: State
    

        
        
        

# ------- Regex Validation and Parsing ---------

def parseRegex(regex):
    print("We have entered parseRegex")

    reggy = repr(regex)
    parse = sre_parse.parse(reggy)
    print(parse)

    #print("Adding concat symbols in prep for AST")
    #i = 0
    #while i < len(regex):
    #    if regex[i] == 'a' or regex[i] == 'b' or regex[i] == 'Z' or regex[i] == '*' or regex[i] == '+' or regex[i] == ')':
    #        if (i+1) < len(regex):
    #            if regex[i+1] == 'a' or regex[i+1] == 'b' or regex[i+1] == '(' or regex[i+1] == 'Z':
    #                r1 = regex[:i+1] + '.'
    #                r2 = regex[i+1:]
    #                regex = r1 + r2
    #    i += 1
     
    print(regex)
    print("Finished Adding '.'\n")  
    return parse
        
    # ------ AST CONSTRUCTION GOES HERE ------

    return 1

def validRegex(content):
    print("We have entered validity checker")
    
    # Valid Regex Check
    if len(content) == 0:
        print("Error: Empty file")
        sys.exit(1)
    stack = []
    for i in range(len(content)):
        #Checks Proper Symbol use
        if content[i] != 'Z' and content[i] != 'a' and content[i] != 'b' and content[i] != '+' and content[i] != '*' and content[i] != '|' and content[i] != '(' and content[i] != ')':
            print("Error: Erroneous Characters used, only valids are a,b,Z,+,*,|,(,)")
            sys.exit(1)

        # Checks that parenthesis are correct
        if content[i] == '(':
            stack.append('x')
        elif content[i] == ')':
            if stack:
                stack.pop()
            else:
                print("Error: Unmatched Parenthesis")
                sys.exit(1)

        # Checks that No invalid placed operators
        if i == 0 and (content[i] ==  '*' or content[i] ==  '|' or content[i] ==  '+'):
            print("Error: Regex Starts with invalid operater")
            sys.exit(1)
        if i == len(content) - 1 and content[i] == '|':
            print("Error: Can't end with union operator")
            sys.exit(1)

        # Checking for doubles
        if i + 1 < len(content):
            if content[i] == '+' or content[i] == '*':
                if content[i+1] == '+' or content[i+1] == '*':
                    print("Error: Improper Ajacent operators")
                    sys.exit(1)
            if content[i] == '|':
                if content[i+1] == '+' or content[i+1] == '*' or content[i+1] == '|':
                    print("Error: Improper Ajacent operators")
                    sys.exit(1)

        # Checking that no wrong operators next to parenthesis
        if i + 1 < len(content):
            if content[i] == '(':
                if content[i+1] == '+' or content[i+1] == '*' or content[i+1] == '|':
                    print("Error: Improper Ajacent operators")
                    sys.exit(1)

    if stack:
            print("Error: Unmatched Parenthesis")
            sys.exit(1)
    # Finished Checks
    print("No Erroneous regex elements")
                

def constructPieces(pRegex):
    nfa = None

    for op, av in pRegex:
        current_nfa = None
        if op == sre_parse.LITERAL:
            start = State()
            accept = State(is_accept=True)
            start.add_transition(chr(av), accept)
            current_nfa = NFA(start, accept)

        elif op == sre_parse.SUBPATTERN:
            subby = av[-1]
            current_nfa = constructPieces(subby)

        elif op == sre_parse.BRANCH:
            alternatives = av[1]

            if not alternatives:
                continue

            alt_nfas = [constructPieces(alt) for alt in alternatives]

            new_start = State()
            new_accept = State(is_accept=True)

            for alt_nfa in alt_nfas:
                new_start.add_transition(None, alt_nfa.start)
                alt_nfa.accept.is_accept = False
                alt_nfa.accept.add_transition(None, new_accept)

            current_nfa = NFA(new_start, new_accept)

        elif op == sre_parse.MAX_REPEAT or op == sre_parse.MIN_REPEAT:
            min_repeat, max_repeat, sub_pattern = av

            sub_nfa = constructPieces(sub_pattern)

            if min_repeat == 0 and max_repeat == 1:
                # ?
                new_start = State()
                new_accept = State(is_accept=True)

                new_start.add_transition(None, sub_nfa.start)
                new_start.add_transition(None, new_accept)

                sub_nfa.accept.is_accept = False
                sub_nfa.accept.add_transition(None, new_accept)

                current_nfa = NFA(new_start, new_accept)

            elif min_repeat == 0 and max_repeat == sre_parse.MAXREPEAT:
                # *
                new_start = State()
                new_accept = State(is_accept=True)

                new_start.add_transition(None, sub_nfa.start)
                new_start.add_transition(None, new_accept)

                sub_nfa.accept.is_accept = False
                sub_nfa.accept.add_transition(None, sub_nfa.start)
                sub_nfa.accept.add_transition(None, new_accept)

                current_nfa = NFA(new_start, new_accept)

            elif min_repeat == 1 and max_repeat == sre_parse.MAXREPEAT:
                # +
                new_start = State()
                new_accept = State(is_accept=True)

                new_start.add_transition(None, sub_nfa.start)

                sub_nfa.accept.is_accept = False
                sub_nfa.accept.add_transition(None, sub_nfa.start)
                sub_nfa.accept.add_transition(None, new_accept)

                current_nfa = NFA(new_start, new_accept)
            else:
                current_nfa = sub_nfa

        elif op == sre_parse.ANY:
            start = State()
            accept = State(is_accept=True)

            for c in range(32, 127):
                if chr(c) != '\n':
                    start.add_transtition(chr(c), accept)

            current_nfa = NFA(start, accept)

        else:
            raise ValueError(f"Unsupported regex operation: {op}")
        
        if current_nfa:
            if nfa is None:
                nfa = current_nfa
            else:
                nfa.accept.is_accept = False
                nfa.accept.add_transition(None, current_nfa.start)
                nfa = NFA(nfa.start, current_nfa.accept)

    return nfa if nfa else NFA(State(), State(is_accept=True))

def combinePieces():

    return 1

def textFormatting():

    return 1

if __name__ == "__main__":
    # Checks that has more then just script, if not tells you to add then fails
    if len(sys.argv) < 2:
        print("To use please add file: python regexToNFA <filename.txt>")
        sys.exit(1)

    # Getting file name
    filename = sys.argv[1]

    # Extract contents, if not there or other errors fail
    try:
        with open(filename, 'r') as file:
            content = file.read()
            #print(f"File contents of '{filename}': \n")
            print(content)
            print("\n")

            # Various Checks to make sure regex is valid
            validRegex(content)

            result = parseRegex(content)
            nfa = constructPieces(result)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")



    # If all goes well we now have a string that contains our file contents
