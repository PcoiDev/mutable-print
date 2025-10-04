from mutable_print import mutable_print
import time

message = mutable_print("Starting")
time.sleep(1)

# "Starting - please wait"
message.append(" - please wait") 
time.sleep(1)

# "🔄 Starting - please wait"
message.prepend("🔄 ")
message.replace("please wait", "takes longer than expected...")
time.sleep(1)
