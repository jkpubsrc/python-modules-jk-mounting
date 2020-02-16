#!/usr/bin/env python3





import os
import sys

import jk_mounting
import jk_json






mounter = jk_mounting.Mounter()

for mi in mounter.getMountInfos(isRegularDevice = True):
	print()
	print(mi)
	jk_json.prettyPrint(mi.toJSON())

print()






