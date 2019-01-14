import sys
import time
import math
def croupier(roll):

    s = .05
    for i in range (37):
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)

        
    for i in range (37):
        
        sys.stdout.write("\r%d " % i)

        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll):
        
        sys.stdout.write("\r%d " % i)
        sys.stdout.flush()
        time.sleep(s)
        
    for i in range(roll,37+roll):
        if (i > 36):
            sys.stdout.write("\r%d " % (i - 36))
        else:
            sys.stdout.write("\r%d " % i)
        sys.stdout.flush()
        s *= 1.05
        time.sleep(s)

croupier(int(raw_input('this is what will roll: ')))