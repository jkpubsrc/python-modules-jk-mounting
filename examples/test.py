#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import sys

import jk_mounting
import jk_json



mounter = jk_mounting.Mounter()

for mi in mounter.getMountInfos(isRegularDevice = True):
	print()
	#print(mi)
	jk_json.prettyPrint(mi.toJSON())

print()

#mo = jk_mounting.MountOptions()
#mo.noatime = True
#mo.nodiratime = True
#print(mo)

#mounter.mount("/dev/xyzabc", "/mnt", options=mo)

#mounter.unmount("/mnt")





