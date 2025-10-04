from mutable_print import mutable_print
import time

DOTS = ["⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽", "⣾"]
TEXTS = {
    0: "Deleting some stuff...",
    12: "Doing this...",
    30: "Doing that...",
    36: "Publishing results...",
    47: "Finishing..."
}

mutable = mutable_print(DOTS[0])
current_text = ""

for i in range(50):
    text = TEXTS.get(i)
    
    if text:
        current_text = text
        
    bar = mutable.set(f"{DOTS[(i) % len(DOTS)]} {current_text}")
    time.sleep(0.1)