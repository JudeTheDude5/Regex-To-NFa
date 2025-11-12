import sys

def parseRegex(regex):
    print("We have entered parseRegex")

    i = 0
    while i < len(regex):
        if regex[i] == 'a' or regex[i] == 'b' or regex[i] == 'Z' or regex[i] == '*' or regex[i] == '+' or regex[i] == ')':
            if (i+1) < len(regex):
                if regex[i+1] == 'a' or regex[i+1] == 'b' or regex[i+1] == '(' or regex[i+1] == 'Z':
                    r1 = regex[:i+1] + '.'
                    r2 = regex[i+1:]
                    regex = r1 + r2

                    print(r1)
                    print(r2)
                    print("\n")
        i += 1

    

    print("\n")
    print(regex)
    return 1

def constructPieces():

    return 1

def combineePieces():

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

            result = parseRegex(content)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")



    # If all goes well we now have a string that contains our file contents