import time 

def delays(seconds, reason = ""):
    print("----- delays() -----")
    print("Waiting for %s seconds due to %s..." %(seconds, reason))
    seconds = int(seconds)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')