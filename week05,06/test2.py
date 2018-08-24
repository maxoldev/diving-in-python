from threading import Thread
import time
import time


def count(n):
    while n > 0:
        n -= 1


# series run
t0 = time.time()
#count(50_000_000)
#count(50_000_000)
#print(time.time() - t0)

# parallel run
t0 = time.time()
th1 = Thread(target=count, args=(50_000_000,))
th2 = Thread(target=count, args=(50_000_000,))

th1.start();
print("th1.start");
th2.start();
print("th2.start")
#th1.join();
print("th1.join");
#time.sleep(2)
th2.join();
print("th2.join")
print("before time")
print(time.time() - t0)
print("after time")
