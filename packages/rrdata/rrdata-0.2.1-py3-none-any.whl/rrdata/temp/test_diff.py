
list1 = ['2022-05-20']

list2 = ['2022-05-18', '2022-05-19', '2022-05-20']

list_diff = [x for x in list2 if x not in list1]

print(list_diff)
print(type(list1[0]))
print(list(set(list2).difference(set(list1))))