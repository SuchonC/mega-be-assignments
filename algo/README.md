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
How many input words ? : 2   
Enter word #1 : ab
Enter word #2 : bc
Enter the target word : abbc
Answer : ('ab', 'bc')
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

### Time Complexity

Let _n_ be the length of the input word list

For each word in the list, at most one dictionary look up will occur and its _O(1)_ for each look up

So the time complexity is **O(n)**

### Space Complexity

Let _n_ be the length of the inport word list

In the worst case where no solution pair exists but each word is always either a head or a tail portion of the target word, the found dictionary will have _n_ keys, that's _O(n)_

And in average case, the dictionary keys still grows by the order of n, that's also _O(n)_

Combined with the space of input list _O(n)_

So the space complexity is also **O(n)**

