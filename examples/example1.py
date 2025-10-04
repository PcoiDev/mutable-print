from mutable_print import mutable_print
import time
   
mutable2 = mutable_print("Hello", "World! 2")
mutable = mutable_print("Hello", "World!")
time.sleep(1)

print("This is a normal print")
time.sleep(1)

mutable("Updated text")
time.sleep(1)

mutable.replace("Updated", "Modified")
time.sleep(1)

print("Another normal print")
time.sleep(1)

mutable.append(" - Extra!")
time.sleep(1)

mutable.upper()
time.sleep(1)

mutable.set("Final text")
mutable("Final text 2")
mutable2.set("Hello", "World! 3")