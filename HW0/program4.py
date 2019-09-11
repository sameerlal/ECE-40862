# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu

nameDay = dict()
nameDay["Albert Einstein"] = "4/14/1879"
nameDay["Ada Lovelace"] = "12/10/1815"
nameDay["Benjamin Franklin"] = "01/17/1706"
print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in nameDay.keys():
	print(name)
print("Who’s birthday do you want to look up?")
x = input()
if x in nameDay:
	print(x + "'s birthday is", nameDay[x])
else:
	print(x + " is not in the dictionary")
