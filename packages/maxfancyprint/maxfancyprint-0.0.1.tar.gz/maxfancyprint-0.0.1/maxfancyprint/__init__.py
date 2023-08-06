def fPrint(str1, delay):
    ###############################
    import string, random, os, time
    alphabet = list(string.ascii_letters)
    others = [" ", "!", "?", "-", "_", ".", ","]
    alphabet.extend(others)
    current = ""
    ###############################
    for c in str1:
        letters = alphabet.copy()
        l = ""
        while l != c:
            l = random.choice(letters)
            letters.remove (l)
            print(current + l)
            time.sleep(delay)
        current += l