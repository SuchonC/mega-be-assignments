def solve(word_list, target):
    if len(word_list) == 0:
        return None

    answer = None
    for i in range(len(word_list)):
        if len(word_list[i]) >= len(target):
            continue
        for j in range(i+1, len(word_list)):
            if len(word_list[j]) >= len(target):
                continue
            if word_list[i] + word_list[j] == target:
                answer = (word_list[i], word_list[j])
            elif word_list[j] + word_list[i] == target:
                answer = (word_list[j], word_list[i])
    print(answer)


if __name__ == "__main__":
    solve(["ab", "bc", "cd"], "abcd")
    solve(["ab", "bc", "cd"], "cdab")
    solve(["ab", "bc", "cd"], "abab")
