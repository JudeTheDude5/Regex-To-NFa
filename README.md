# Regex-To-NFa
Ok so I have an idea on how to do this pipeline

we'll have functions 

parseRegex: Check for all expressions, put into expanding list then we can look through and add them to next function

constructPieces: build list full of DFA datastrucures for indivudal constructions, for all of this Im thinking recursive for parentehesis? to insure proper order and since we don't know how far into it it goes

combinePieces: go through each piece and add it to the next, list should just be in order

textFormatting: Format it into text and return

then text should be output.

nned to look through the book to review


parsing ideas:

cases:
a     just a letter we'll check to it's right for * and + and ^(then to the right to see a number)
sigma    check for stuff to the right
parenthesis     if open left error, if open right note location of left move to right until we find right take note of location then we can take everything from the middle plus look to right, perhaps have *,+,^ be toggles within the data? like a struct that include a string and a character, each of those has own character that will be read for structure, plus parenthesis since we have to look inside those recursively for more stuff.

I just have to start implementing will be easier once I've started.

just realized theres also empty string and set, U, and dot, ugh this'll be annoying, I'm sure theres a better way to parse the string I'm just not sure what


Alphabet is constrained to a and b

we will have special characters to represent certain symbols

Sigma = Z
Union = |
Concat = .
Star = *
E = empty Set
S = empty String
Plus = +
K power equals = number