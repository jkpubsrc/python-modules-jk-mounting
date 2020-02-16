#!/usr/bin/env python3





import os
import sys

import jk_mounting
import jk_json






mounter = jk_mounting.Mounter()

mi = mounter.getMountInfoByFilePath("/etc/init.d")

print(mi)




