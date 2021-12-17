def solve(word_list, target):
    if len(word_list) == 0:
        return None
    if len(target) == 0:
        return None

    found = {}

    for w in word_list:
        # if w is the head of the target
        if w == target[:len(w)]:
            tail = target[len(w):]
            # if its tail is already found, then return
            if tail in found:
                return (w, tail)
            # else mark the head as found
            found[w] = True
        # if w is the tail of the target
        elif w == target[-len(w):]:
            head = target[:-len(w)]
            # if its head is already found, then return
            if head in found:
                return (head, w)
            # else mark the tail as found
            found[w] = True

    return None


def main():
    n = int(input('How many input words ? : '))
    word_list = [input(f'Enter word #{i} : ') for i in range(1, n+1)]
    target_word = input('Enter the target word : ')
    print('Answer :', solve(word_list, target_word))

if __name__ == '__main__':
    main()
