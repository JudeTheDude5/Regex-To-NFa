import sys

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
            print("File contents of '{filename}': \n")
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")

    # If all goes well we now have a string that contains our file contents

def parseRegex():

    return 1

def constructPieces():

    return 1

def combineePieces():

    return 1

def textFormatting():

    return 1