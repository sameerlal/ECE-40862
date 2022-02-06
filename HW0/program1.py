# RTVIK SRIRAM BHARADWAJ
# bharadwr[AT]purdue[DOT]edu
from datetime import datetime
year = datetime.now().year

name = input('What is your name? ')
age = input('How old are you? ')
year = 100 - int(age) + year
print(f"{name} will be 100 years old in the year {year}")
