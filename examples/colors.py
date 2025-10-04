from mutable_print import mutable_print
import rich_style, time

TEXT = "This is a rainbow message! As you can see, colors are supported. This is useful for highlighting important information. Enjoy using mutable-print with colors!"
mutable = mutable_print("")

for i in range(0, TEXT.__len__() + 1):
    time.sleep(0.025)
    
    # Display rainbow text up to the i-th character
    mutable.set(rich_style.rainbow_text(TEXT[:i]))