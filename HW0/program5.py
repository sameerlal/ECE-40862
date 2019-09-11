# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu

class TwoSumClass:
	def __init__(self):
		self.nums = [10,20,10,40,50,60,70]
		num = int(input("What is your target number? "))
		ind1, ind2 = self.twoSum(num)
		print("index1=" + str(ind1), "index2=" + str(ind2))

	def twoSum(self, target):
		numDict = dict()
		for index, value in enumerate(self.nums):
			m = target - value
			if m in numDict:
				return [numDict[m], index]
			else:
				numDict[value] = index
		return "", ""

x = TwoSumClass()



