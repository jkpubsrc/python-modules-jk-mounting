#!/usr/bin/env python3



import os
import sys

import jk_mounting






mounter = jk_mounting.Mounter()

mo = jk_mounting.MountOptions()
mo.noatime = True
mo.nodiratime = True
print(mo)

mounter.mount("/dev/xyzabc", "/mnt", options=mo)

#mounter.unmount("/mnt")





