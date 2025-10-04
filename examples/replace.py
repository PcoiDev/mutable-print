from mutable_print import mutable_print
import time

line = mutable_print("Loading modules... fail")
time.sleep(1)

# Replace part of the content then convert to uppercase
line.replace("fail", "done ✅").upper()
time.sleep(1)

line2 = mutable_print("Task #42 failed in 3.2s")
time.sleep(1)

# replace duration dynamically
line2.regex_replace(r"\d+\.\ds", "2.9s")
