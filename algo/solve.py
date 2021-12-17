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
        elif w == target[len(w):]:
            head = target[:len(w)]
            # if its head is already found, then return
            if head in found:
                return (head, w)
            # else mark the tail as found
            found[w] = True

    return None


def main():
    word_list = input('Type input words separated by space (ie. ab bc cd): ')
    target = input('Type the target word: ')
    print('Answer:', solve(word_list.split(), target))


if __name__ == '__main__':
    main()
