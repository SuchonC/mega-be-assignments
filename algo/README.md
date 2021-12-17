# Algorithm Programming

## How to run the program

Clone the repository onto your local machine

```sh
git clone https://github.com/SuchonC/mega-be-assignments
cd ./mega-be-assignments/algo
```

Then you should be able to execute the program, using the command

```sh
python solve.py
```

The program will then prompt for input words and target word

```txt
Type input words separated by space (ie. ab bc cd): ab bc cd
Type the target word: abcd
Answer: ('ab', 'cd')
```

## How the algorithm works

```python
# a dict containing founded parts of the target
found = {}

# for each word 'w' in the word list
for w in word_list:
    # check if w is the head of the target
    if w == target[:len(w)]:
        # if it is, extract the tail
        tail = target[len(w):]
        # if its tail is already found, then return
        if tail in found:
            return (w, tail)
        # else mark the head as found
        found[w] = True
    # if w is not the head
    # check if w is the tail of the target
    elif w == target[-len(w):]:
        # if it is, extract the head
        head = target[:-len(w)]
        # if its head is already found, then return
        if head in found:
            return (head, w)
        # else mark the tail as found
        found[w] = True

# return None if no word pair is found
return None
```

## Complexity Analysis