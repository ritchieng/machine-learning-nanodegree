"""Count words."""

s = "How are you doing how is are"

words = s.lower().split()
my_dict = {}
for word in words:
    if word in my_dict:
        my_dict[word] += 1
    else:
        my_dict[word] = 1

my_tuples = my_dict.items()
n_sort = sorted(my_tuples, key=lambda x: (-x[1],x[0]))

print(n_sort)




