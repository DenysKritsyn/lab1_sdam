import sys
from parameters.average import *

if len(sys.argv) < 2:
    print("Pass arguments")
    sys.exit(1)

# NODE_TLS_REJECT_UNAUTHORIZED=0 antigravity
def main():

    avg=getAverage(1,2,3,4)

    print(avg)

    return 0

main()