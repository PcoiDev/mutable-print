from mutable_print import mutable_print
import time

mutable = mutable_print("Hello", "World! 2", end=" | ")
mutable2 = mutable_print("Hello", "World!")
time.sleep(1)

print("This is a normal print")
time.sleep(1)

mutable2("Updated text")
time.sleep(1)

mutable2.replace("Updated", "Modified")
time.sleep(1)

print("Another normal print")
time.sleep(1)

mutable2.append(" - Extra!")
time.sleep(1)

mutable2.upper()
time.sleep(1)

mutable2.set("Final text")
mutable("Hello", "World! 3")