def waitUntil(condition):
    print("helo")
    while True:
        if condition.loadIsComplete:
            print(condition.loadIsComplete)
            return True
