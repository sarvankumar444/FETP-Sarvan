word = "FORMULAQSOLUTIONSFORMULAQSOLUTIONS"
l = [letter for letter in word]
size = int(input("Enter No of lines for design"))
num = size // 2

for i in range(num + 1):
    spaces = " " * (size - i - 1)
    character = "".join(l[i:(i * 3) + 1])
    print(spaces + character)

ch = list(character)
try:
    for i in range(num, -1, -1):
        if ch != []:
            spaces = " " * (size - i - 1)

            if ch != []:
                ch.pop(0)
                ch.pop(-1)

            character = "".join(ch)
            print(f"", spaces + (character))
except IndexError:
    pass