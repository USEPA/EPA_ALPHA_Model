import threading


def gfg():
    print("GeeksforGeeks\n")
    timer1 = threading.Timer(1.0, gfg)
    timer1.start()


timer = threading.Timer(2.0, gfg)
timer.start()
print("Exit\n")