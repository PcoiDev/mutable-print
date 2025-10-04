from mutable_print import mutable_print
import time

line = mutable_print("Temporary log message", end="\n\n")
time.sleep(1)

line.clear() # remove text
time.sleep(1)

print("This is a normal print")
line.set("Message restored") # replace cleared text
