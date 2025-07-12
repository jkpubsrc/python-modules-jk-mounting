

import jk_logging

import jk_mounting









with jk_logging.wrapMain() as log:

	m = jk_mounting.Mounter()
	for mi in m.getMountInfos2(isFuseDevice=True, isRegularDevice=False):
		print(mi)

