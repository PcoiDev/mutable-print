
    
    MutablePrint._instances.clear()
    
    print("\n=== Test 3: Loading spinner ===")
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
            
        mutable.set(f"{DOTS[i % len(DOTS)]} {current_text}")
        time.sleep(0.1)
    
    print("\nDone!")