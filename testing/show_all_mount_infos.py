

import jk_logging

import jk_mounting









with jk_logging.wrapMain() as log:

	fsTypes = set()

	m = jk_mounting.Mounter()
	for mi in m.getMountInfos():
		mi.dump()
		fsTypes.add(mi.fsType)

	print()

	for fs in sorted(fsTypes):
		print(fs)

	print()

	for mi in m.getMountInfos2(isSnapDevice=False):
		print(mi)
		fsTypes.add(mi.fsType)

	print()

