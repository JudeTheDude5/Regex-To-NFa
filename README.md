Regex to NFA Converter

A Python implementation of Thompson's Construction algorithm that converts regular expressions into Non-deterministic Finite Automata (NFAs) with formal descriptions.

INPUT:
Takes a single .txt file that contains a properly formatted regex.

What is the proper format?
- only using a's or b's
- using | for union
- using Z for sigma
- *, +, and () work as usual

Step 1: Read file
- checks that file is inputted
- opens file and passes content to validRegex()

Step 2: Validate regex is in proper form
- checks proper symbol use
- checks proper parenthesis 
- checks for no invalidly placed operators
- checks for double operators
- checks for proper operator parenthesis order
- then main moves to parseRegex()

Step 3: Parse regex into Abstract Syntax Tree (AST)
- called pythons built in library
* library will be removed eventually so depreciation warning ignored * 
- then main moves to constructPieces()

Step 4: Constructing NFA from the AST
- checks for certain parse operand and adds correct part into NFA class
- returns NFA which has start and accept states that are of state type and have the attributes: is_accept, transitions, state_id, visited
- then main moves to combinePieces()

Step 5: Combine the NFA pieces into a formal description
- get all the states in the NFA 
- rename states to "prettier" names
- create a set of all the states
- create delta using dict
- find start state
- find all accept states (most likely only one due to Thompson's   Construction)
- return formal description
- then main moves to __str__() in the formalDescription class

Step 6: Turn formal description into string
- create a lines var
- organize formal description into separate parts 
- call method that organizes delta table
- add parts to lines as they are made
- return lines

Step 7: Write to file
- take passed in string and write to file "NFA_formal_description.txt"

OUTPUT:
Writes the formal description for the NFA to a file titled "NFA_formal_description.txt"


Example command line entry:

python3 ./regexToNFA.py regexFile.txt
