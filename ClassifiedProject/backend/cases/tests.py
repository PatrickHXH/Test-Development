import re

# line = "Cats are smarter than dogs"
# s = "http://${Host}/get"
# re.search('(?<=\${).+(?=})', s)
# matchObj = re.match(r'(.*) are (.*)', line)
# print(matchObj.group())
#
# if matchObj:
#     print("matchObj.group() : ", matchObj.group())
#     print("matchObj.group(1) : ", matchObj.group(1))
#     print("matchObj.group(2) : ", matchObj.group(2))
# else:
#     print
#     ("No match!!")

    # , re.M | re.I
s = "http://${Host}/get"
aa = re.search('(?<=\${).{1,4}(?=})', s)
# aa = re.search(r'\?=}', s)
print(aa.group())