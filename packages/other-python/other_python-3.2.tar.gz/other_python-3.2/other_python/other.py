import random
def middle(min: int,max: int):
 return (min+max)/2
def change(number: int,change: int):
    return number+random.randint(-change,change)
def ListToInt(List:list) :
    result = 0
    for x in List:
         result += x
    return result