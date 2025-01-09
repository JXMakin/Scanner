# Scanner for JSON
## Grammar:
**value:** dict | list | STRING | NUMBER | _true_ | _false_ | _null_
<br/>**list:** [ value, value* ]
<br/>**dict:** { pair, pair* }
<br/>**pair:** STRING : value

### Rules:
+ All boolean values are lowercase as well as null
+ Strings are tokenized with their parenthesis (ex. "hello")
+ Strings do not accept double quotes inside the String (ex. "hello" Bob" is not valid)
+ Numbers accept e (ex. 23e4 and 23.4e5)
  + Does accept 23e-34

## Using The Code
The Scanner reads from any number of txt files that are named test and some number
<br/>(ex. _test2.txt_). At the start, it will ask the user for the number of files that are being tested.
The test files have to start from 1. It will then tokenize the strings. If there is a lexical error
anywhere in a file, it will return lexical error and what character might've caused it. Even
if the other strings are valid in the file, it will still return an error.

## Key Parts of The Code
- **DFA:** Checks if the characters are valid words in the JSON (valid symbols or STRINGS)
- **DFA for numbers:** Checks if the numbers are valid numbers in JSON
- **Tokenizer:** Tokenizes the string.
  - Iterates through each line in the file. For each line, it will then iterate through each 
      character in the string. 
  - It then gives it to the DFA. If the DFA returns true, then it is a valid token. It will
then add it to it's list of tokens for that file.
    - If it recognizes it as a NUMBER, STRING, BOOLEAN or _null_ value, it will group the characters together.
      It will then send the group of characters to the DFA to be recognized as a token as a whole 
- **Main:** reads in the files and executes the Scanner. Number of files being read comes from keyboard input. Once the program finishes with one file, the list of tokens from that file is then printed.