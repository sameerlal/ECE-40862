# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu

numList = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
x = int(input('Enter number: '))
newList = list()
for num in numList:
	if num < x:
		newList.append(num)
print("The new list is ", newList)
