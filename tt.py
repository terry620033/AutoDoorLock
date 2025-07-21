#!/usr/bin/env python3

import time

t = time.time()

print(time.strftime('%Y%m%d-%H%M%Z', time.localtime(t)))

print((time.strftime('%Y%m%d-%H%M%p')+'_tls.log'))


