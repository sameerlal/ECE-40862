# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu

import random

num = random.randint(0, 10)
print(num)
for i in range(3):
	x = int(input("Enter your guess:"))
	if x == num:
		print("You win!")
		break
	elif i == 2:
		print("You lose!")
		break
