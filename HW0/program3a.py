# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu

def fib(n):
	fibs = list()
	i = 0
	a, b = 1, 1
	while i < n:
		i += 1
		fibs.append(str(a))
		a, b = b, a + b
	return fibs

x = int(input('How many Fibonacci numbers would you like to generate: '))
print("The Fibonacci sequence is", ', '.join(fib(x)))
