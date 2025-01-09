"""
 @author Jenna Makin - B00903304
"""
import os


## This class checks if the inputted string is valid in the language JSON
class DFA:
    ## constructor
    def __init__ (self):
        # initial state is q0
        self.state = 'q0'

    def reset(self):
        # reset to initial state
        self.state = 'q0'

    """
    This checks if an input_string char is valid.
    If the char is accepted by any state, then the current state of the DFA changes. If the character is not valid
    then the DFA goes to an invalid state. This method cannot check if it is a valid number
    """
    def transition (self, char):
        # state transitions
        # start state
        if self.state == 'q0':
            if char in [',', '{', '}', '[', ']', ':']:
                # q1 is final state
                self.state = 'q1'
            elif char.isspace():
                self.state = 'white_space'

            elif char == '"':
                # q2 is inside string
                self.state = 'q2'
            elif char == 't':
                self.state = 'q5'
            elif char == 'f':
                self.state = 'q9'
            elif char == 'n':
                self.state = 'q12'
        # q2 is string
        elif self.state == 'q2':
            if char == '"':
                self.state = 'q4'
            else:
                self.state = 'q2'

        elif self.state == 'q5' and char == 'r':
                self.state = 'q6'

        elif self.state == 'q9' and char == 'a':
                self.state = 'q10'

        elif self.state == 'q10' and char == 'l':
                self.state = 'q11'
        elif self.state == 'q11' and char == 's':
                self.state = 'q7'

        elif self.state == 'q6' and char == 'u':
                self.state = 'q7'
        elif self.state == 'q7' and char == 'e':
                self.state = 'q8'

        elif self.state == 'q12' and char == 'u':
                self.state = 'q13'
        elif self.state == 'q13' and char == 'l':
                self.state = 'q14'

        elif self.state == 'q14' and char == 'l':
                self.state = 'q15'

        else:
            self.state = 'invalid'

    ## checks if the DFA is in a final state.
    # Returns true if it is. Returns false if not
    def is_accepting(self):
        if (self.state == 'q1' or self.state == 'q4' or self.state == 'q8' or self.state == 'q15' or self.state == 'num'
                or self.state == 'exponent_num' or self.state == 'double' or self.state == 'negative_num'
                or self.state == 'zero'):
            return True
        else:
            return False

    ## checks if the input_string is a valid string in the langauge and if it is in a final state.
    def process_string(self, input_string):
        ## reset DFA
        self.reset()
        """
        if it is one character, then in needs to be in a final state
        if the input_string is a sequence of characters then the last character in the sequence 
        needs to be in a final state
        """
        for char in input_string:
            ## takes char through DFA
            self.transition(char)
            if self.state == 'invalid':
                return False

        return self.is_accepting()

"""
Token class which keeps track of the token type and the value
"""
class Token:
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def get_type(self):
        return self.type

    def get_value(self):
        return self.value
"""
This class takes the JSON strings and tokenizes them if they are valid tokens by using the DFA
"""
class Tokenizer:
    def __init__(self):
        self.tokens = []

    def reset(self):
        self.tokens = []
    """
    prints out the tokens
    """
    def print(self, file_name):
        for t in self.tokens:
            if t.get_value() is None:
                print(f"<{t.get_type()}>")
            else:
                print(f"<{t.get_type()},{t.get_value()}>")
        print()
    """    
    Reads every individual character as one to tokenize. Uses the DFA to check if it is valid before adding to
    the list of Tokens.
    If it could be a STRING, BOOLEAN or null value, it validates it with the DFA as a whole entity
    before it tokenizes it as one
    If they are not valid, it prints lexical error at the character and then returns nothing
    """
    def tokenize(self, input_string):
        token_string = ""
        token_num = ""
        bool_null = ""
        is_num = False
        quote_count = 0
        dfa = DFA()

        for char in input_string:
            # checks if it is a number, and it is not inside a string
            if (char.isdigit() or char in ['-', '.', '+']) and is_num == False and quote_count % 2 == 0:
                is_num = True
                token_num += char
            # checks if it is still one continuous number
            elif is_num and (char.isdigit() or char in ['-','.','e','E','+']):
                token_num += char

            elif char == '"':
                quote_count += 1
                # if the string is closed
                if quote_count % 2 == 0:
                    token =  Token("STRING", token_string)
                    self.tokens.append(token)
                    dfa.reset()
                    token_string = ""
            # if string is closed, and it is a character, then it checks if it is a valid boolean or null value
            elif char.isalpha() and quote_count % 2 == 0:
                bool_null += char
                if len(bool_null) >= 4 and dfa.process_string(bool_null):
                    if bool_null == "null":
                        token = Token("NULL", bool_null)
                        self.tokens.append(token)
                    else:
                        token = Token("BOOLEAN", bool_null)
                        self.tokens.append(token)
                    bool_null = ""
                    dfa.reset()

            else:
                # adds numbers to list of tokens
                if token_num:
                    token = Token("NUMBER", token_num)
                    self.tokens.append(token)
                    dfa.reset()
                    token_num = ""
                    is_num = False

                # if it is not "inside" a string
                if quote_count % 2 != 0:
                    token_string += char
                # uses DFA to check if it is a valid token
                elif dfa.process_string(char):
                    token = Token(char, None)
                    self.tokens.append(token)
                    dfa.reset()
                elif char.isspace():
                    is_num = False
                    valid = dfa.process_string(bool_null)
                    if valid and bool_null != "":
                        token = Token("BOOLEAN", bool_null)
                        self.tokens.append(token)
                        bool_null = ""
                        dfa.reset()
                    elif not valid and bool_null != "":
                        print(f"lexical error at {bool_null}")
                        dfa.reset()
                        return
                    continue
                else:
                    if char.isspace():
                        char = 'blank'
                    print(f"lexical error at {char}")
                    return

        # if there are numbers to be added it adds them
        if token_num:
            token = Token("NUMBER", token_num)
            self.tokens.append(token)

"""
main function that uses the tokenizer to check if the text files contain valid JSON strings
If they are valid, then it prints out all the valid tokens in list format
"""
def main():
    lexer = Tokenizer()
    files = input("How many files are there? ")
    for i in range(1, int(files) + 1):
        file_name = f"test{i}.txt"
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                input_string = file.read().strip()
                print(f"File: {file_name}")
                lexer.tokenize(input_string)
                lexer.print(file_name)
                lexer.reset()

        else:
            print(f"{file_name}: File not found")


if __name__ == "__main__":
    main()