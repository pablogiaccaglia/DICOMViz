def waitUntil(condition):
    print("helo")
    while True:
        if condition.loadIsComplete:
            print(condition.loadIsComplete)
            return True


import threading, time

def my_threaded_func(arg, arg2):
    print("Running thread! Args:", (arg, arg2))
    time.sleep(10)
    print("Done!")



if __name__ == '__main__':
    thread = threading.Thread(target = my_threaded_func, args = ("I'ma", "thread"))
    thread.start()
    print("Spun off thread")
