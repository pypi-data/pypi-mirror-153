import random,os,inspect
def middle(min: int,max: int):
 return (min+max)/2
def change(number: int,change: int):
    return number+random.randint(-change,change)
def find_path():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))