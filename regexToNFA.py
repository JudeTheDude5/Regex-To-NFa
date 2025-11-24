import sys
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sre_parse
# ^ Used for regex parsing will eventually be removed from python hence the warning ignore
from dataclasses import dataclass
from typing import Set, Dict, Optional
        
        
# ------ NFA Classes ------
class State:
    """Represents a state in the NFA."""
    def __init__(self, is_accept=False):
        self.is_accept = is_accept
        self.transitions: Dict[Optional[str], Set['State']] = {}
        self.state_id = id(self)
        self.visited = False

    def add_transition(self, symbol: Optional[str], state: 'State'):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)

class NFA:
    """Represents a Non-deterministic Finite Automaton (NFA)."""
    def __init__(self, start, accept):
        self.start: State = start
        self.accept: State = accept
        
# ------- Formal Description Class -------
@dataclass
class formalDescription:
    """Dataclass to hold the formal description of an NFA."""
    
    Q: Set[str]
    Sigma: Set[str]
    Q0: str
    Delta: Dict[tuple[str, Optional[str]], Set[str]] 
    F: Set[str]
    state_mapping: Dict[State, str] 
    
    def __str__(self, regex) -> str:
        """Returns the formal string description of the NFA."""
        #print("Entered __str__")
        return self.toString(regex)
    
    def toString(self, regex) -> str:
        """Generates a formal string description of the NFA."""
        #print("Entered createStringDescription")
        
        lines = []  
        
        lines.append("=" * 70)
        lines.append("Formal Description of NFA for regex: " + regex)
        lines.append("=" * 70)
        
        lines.append("\n1.  States (Q):")
        lines.append("\n    Q = {" + ", ".join(sorted(self.Q)) + "}")
        lines.append("    |Q| = " + str(len(self.Q)))
        
        lines.append("\n2.  Alphabet (Σ):")
        lines.append("\n    Σ = {" + ", ".join(sorted(self.Sigma)) + "}")
        
        lines.append("\n3.  Transition Table (Δ):")
        lines.append("\n" + self.formatDelta())
        
        lines.append("\n4.  Start State (Q0):")
        lines.append("\n    q₀ = " + "".join(self.Q0))
        
        lines.append("\n5.  Accept States (F):")
        lines.append("\n    F = {" + ", ".join(sorted(self.F)) + "}\n")
        
        lines.append("=" * 70)
        
        formalDescriptionStr = "\n".join(lines)
        
        writeToFile(formalDescriptionStr)
        
        return formalDescriptionStr
    
    def formatDelta(self):
        """Formats the transition function Δ into a readable table."""
        
        lines = []
        allSymb = sorted(self.Sigma)
        has_epsilon = any(symbol is None for (_, symbol) in self.Delta.keys())
        
        # Create header
        header  = ["State"] + [repr(s) for s in allSymb]
        if has_epsilon:
            header.append("ε")
        
        # Determine column widths
        colWidths = [max(len(h), 8) for h in header]
        for state in sorted(self.Q):
            
            colWidths[0] = max(colWidths[0], len(state) + 1)
            
            for i, symbol in enumerate(allSymb):
                key = (state, symbol)
                if key in self.Delta:
                    dest_states = "{" + ",".join(sorted(self.Delta[key])) + "}"
                    colWidths[i + 1] = max(colWidths[i + 1], len(dest_states))
            
            if has_epsilon:    
                key = (state, None)
                if key in self.Delta:
                    dest_states = "{" + ",".join(sorted(self.Delta[key])) + "}"
                    colWidths[-1] = max(colWidths[-1], len(dest_states))
                    
        lines.append("  " + " | ".join(h.ljust(w) for h, w in zip(header, colWidths)))
        lines.append("  " + "-+-".join('-' * w for w in colWidths))
        
        for state in sorted(self.Q):
            row = []
            
            row.append(state.ljust(colWidths[0]))
            
            for i, symbol in enumerate(allSymb):
                key = (state, symbol)
                if key in self.Delta:
                    dest_states = sorted(self.Delta[key])
                    cell = "{" + ", ".join(dest_states) + "}"
                else:
                    cell = "∅"
                row.append(cell.ljust(colWidths[i + 1]))
                
            if has_epsilon:
                key = (state, None)
                if key in self.Delta:
                    dest_states = sorted(self.Delta[key])
                    cell = "{" + ", ".join(dest_states) + "}"
                else:
                    cell = "∅"
                row.append(cell.ljust(colWidths[-1]))
            
            lines.append("  " + " | ".join(row))
            

        return "\n".join(lines)


# ------- Regex Validation and Parsing ---------

def parseRegex(regex):
    """Parses the regex string into an AST using sre_parse."""
    #print("We have entered parseRegex")

    #reggy = repr(regex)
    parse = sre_parse.parse(regex)
    #print(parse)
     
    #print(regex)
    #print("Finished Adding '.'\n")  
    return parse


def validRegex(content):
    """Validates the regex string for correctness."""
    #print("We have entered validity checker")
    
    # Valid Regex Check
    if len(content) == 0:
        print("Error: Empty file")
        sys.exit(1)
    stack = []
    for i in range(len(content)):
        #Checks Proper Symbol use
        if content[i] != 'Z' and content[i] != 'a' and content[i] != 'b' and content[i] != '+' and content[i] != '*' and content[i] != '|' and content[i] != '(' and content[i] != ')':
            print("Error: Erroneous Characters used, only valid ones are a,b,Z,+,*,|,(,)")
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
            print("Error: Regex Starts with invalid operator")
            sys.exit(1)
        if i == len(content) - 1 and content[i] == '|':
            print("Error: Can't end with union operator")
            sys.exit(1)

        # Checking for doubles
        if i + 1 < len(content):
            if content[i] == '+' or content[i] == '*':
                if content[i+1] == '+' or content[i+1] == '*':
                    print("Error: Improper Adjacent operators")
                    sys.exit(1)
            if content[i] == '|':
                if content[i+1] == '+' or content[i+1] == '*' or content[i+1] == '|':
                    print("Error: Improper Adjacent operators")
                    sys.exit(1)

        # Checking that no wrong operators next to parenthesis
        if i + 1 < len(content):
            if content[i] == '(':
                if content[i+1] == '+' or content[i+1] == '*' or content[i+1] == '|':
                    print("Error: Improper Adjacent operators")
                    sys.exit(1)

    if stack:
            print("Error: Unmatched Parenthesis")
            sys.exit(1)
    # Finished Checks
    #print("No Erroneous regex elements")
                

def constructPieces(pRegex):
    """Constructs NFA pieces from the parsed regex AST."""
    nfa = None

    for op, av in pRegex:
        current_nfa = None
        if op == sre_parse.LITERAL:
            if chr(av) == "'":
                continue
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
            
        elif op == sre_parse.IN:
            start = State()
            accept = State(is_accept=True)

            for itemOp, itemAv in av:
                if itemOp == sre_parse.LITERAL:
                    start.add_transition(chr(itemAv), accept)
                elif itemOp == sre_parse.RANGE:
                    for c in range(itemAv[0], itemAv[1] + 1):
                        start.add_transition(chr(c), accept)
                        
            current_nfa = NFA(start, accept)

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

            elif min_repeat == 0 and max_repeat == sre_parse.MAX_REPEAT:
                # *
                new_start = State()
                new_accept = State(is_accept=True)

                new_start.add_transition(None, sub_nfa.start)
                new_start.add_transition(None, new_accept)

                sub_nfa.accept.is_accept = False
                sub_nfa.accept.add_transition(None, sub_nfa.start)
                sub_nfa.accept.add_transition(None, new_accept)

                current_nfa = NFA(new_start, new_accept)

            elif min_repeat == 1 and max_repeat == sre_parse.MAX_REPEAT:
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
                    start.add_transition(chr(c), accept)

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

def combinePieces(nfa):
    """Combines NFA pieces into a formal description."""
    #print("entered combine pieces")

    all_states = getStates(nfa)

    state_mapping = {}
    for i, state in enumerate(sorted(all_states, key=lambda s: s.state_id)):
        state_mapping[state] = f"q{i}"

    Q = set(state_mapping.values())

    #print(Q)

    delta = {}
    for state in all_states:
        state_name = state_mapping[state]
        for symbol, dest_states in state.transitions.items():
            dest_names = {state_mapping[s] for s in dest_states}
            delta[(state_name, symbol)] = dest_names

    Q0 = state_mapping[nfa.start]

    #print(Q0)

    F = {state_mapping[s] for s in all_states if s.is_accept}

    #print(F)

    return formalDescription(Q, {"a", "b"}, Q0, delta, F, state_mapping)

def getStates(nfa: NFA):
    """Retrieves all states in the NFA using DFS."""
    #print("Entered getStates")
    visited = set()
    stack = [nfa.start]

    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)

        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                if next_state not in visited:
                    stack.append(next_state)

    return visited


def writeToFile(strDesc):
    """Writes the formal description string to a file."""
    
    #print("Entered writeToFile")
    
    print("Writing Formal Description to 'NFA_formal_description.txt'")
    
    try:
        with open("NFA_formal_description.txt", "w") as f:
            f.write(strDesc)
        print("Successfully wrote to 'NFA_formal_description.txt'")
    except Exception as e:
        print(f"An error occurred while writing to file: {e}")
    

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
            #print(content)
            #print("\n")

            # Various Checks to make sure regex is valid
            validRegex(content)

            # Parsing Regex into AST
            result = parseRegex(content)
            
            # Construct NFA from AST
            nfa = constructPieces(result)
            
            # Combine NFA pieces into formal description
            tx = combinePieces(nfa)
            
            tx.__str__(content)
            
            # Print Formal Description to console
            #print("\n")
            #print(tx)


    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



    # If all goes well we now have a string that contains our file contents
