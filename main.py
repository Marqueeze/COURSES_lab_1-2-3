import sys
from logic import tokenize, digits_indicies, foreign_indicies

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Expected 1 argument which is directory path")
    else:
        path = sys.argv[1]
        print(tokenize(path))
        print(digits_indicies(path))
        print(foreign_indicies(path))
