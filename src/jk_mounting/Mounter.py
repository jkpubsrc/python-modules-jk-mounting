



import os
import sys
import codecs
# import time

import jk_simpleexec


from .MountInfo import MountInfo
from .MountOptions import MountOptions










class Mounter(object):

	def __init__(self):
		self.__lastRefresh = 0
		self.refresh()
	#

	def refresh(self):
		# dt = time.time() - self.__lastRefresh
		self.__mountInfos = self.__retrieveMountInfos()
	#

	def getMountInfos(self, fsTypeIncl = None, fsTypeExcl = None, isRegularDevice = None):
		if (fsTypeIncl is None) and (fsTypeExcl is None) and (isRegularDevice is None):
			return list(self.__mountInfos)

		if isRegularDevice is None:
			pass
		elif isinstance(isRegularDevice, bool):
			pass
		else:
			raise Exception("isRegularDevice is not of type boolean!")

		if fsTypeIncl is None:
			pass
		elif isinstance(fsTypeIncl, str):
			fsTypeIncl = [ fsTypeIncl ]
		elif isinstance(fsTypeIncl, list):
			for fsTypeInclItem in fsTypeIncl:
				assert isinstance(fsTypeInclItem, str)
		else:
			raise Exception("fsTypeIncl is not of type string or string list!")

		if fsTypeExcl is None:
			pass
		elif isinstance(fsTypeExcl, str):
			fsTypeExcl = [ fsTypeExcl ]
		elif isinstance(fsTypeExcl, list):
			for fsTypeExclItem in fsTypeExcl:
				assert isinstance(fsTypeExclItem, str)
		else:
			raise Exception("fsTypeExcl is not of type string or string list!")

		ret = []
		for mi in self.__mountInfos:
			if isRegularDevice is not None:
				if isRegularDevice:
					if not mi.isRegularDevice:
						continue
				else:
					if mi.isRegularDevice:
						continue
			if fsTypeExcl is not None:
				if mi.fsType in fsTypeExcl:
					continue
			if fsTypeIncl is not None:
				if mi.fsType not in fsTypeIncl:
					continue
			ret.append(mi)
		return ret
	#

	def isMounted(self, path):
		for mi in self.__mountInfos:
			if mi.device == path:
				return True
			if mi.mountPoint == path:
				return True
		return False
	#

	def __retrieveMountInfos(self):
		mountInfos = []
		with codecs.open("/proc/mounts", "r", "utf-8") as f:
			for line in f.readlines():
				line = line[:-1]
				mountInfos.append(MountInfo._parseFromMountLine(line))
		return mountInfos
	#

	#
	# Mount a device.
	#
	# @param	str device						The device to mount. Specify the device path here.
	# @param	str mountPoint					The location where to mount the specified device. Specify an existing empty directory here.
	# @param	mixed options					Mount options. Specify a mount options string here as you would if you invoke "mount" directly,
	#											a list of strings to concatenate or a dictionary with key-value pairs containing all mount options.
	#											Additionally you can specify a <c>MountOptions</c> object, which then get's converted to a suitable
	#											option string automatically.
	# @param	bool raiseExceptionIfMounted	Before mounting a device a check is performed if the device is already mounted (by invoking
	#											<c>self.isMounted(...)</c>. If <c>True</c> is specified here an exception is raised if
	#											the device in question is already mounted (or the path in question is already used as a
	#											mount point).
	#
	def mount(self, device:str, mountPoint:str, options = None, raiseExceptionIfMounted = True):
		assert isinstance(device, str)
		assert isinstance(mountPoint, str)
		assert isinstance(options, (type(None), str, list, dict, MountOptions))
		assert isinstance(raiseExceptionIfMounted, bool)

		if self.isMounted(device):
			if raiseExceptionIfMounted:
				raise Exception("Device " + device + " already mounted!")
			else:
				return False

		if self.isMounted(mountPoint):
			if raiseExceptionIfMounted:
				raise Exception("Path " + mountPoint + " already mounted!")
			else:
				return False

		if isinstance(options, MountOptions):
			options = str(options)
		elif isinstance(options, list):
			s = ""
			bNeedsComma = False
			for option in options:
				if bNeedsComma:
					s += ","
				else:
					bNeedsComma = True
				s += option
			options = s
		elif isinstance(options, dict):
			s = ""
			bNeedsComma = False
			for optionName in options:
				optionValue = options[optionName]
				if bNeedsComma:
					s += ","
				else:
					bNeedsComma = True
				s += optionName
				if optionValue is not None:
					s += "=" + optionValue
			options = s

		args = []
		if (options is not None) and (len(options) > 0):
			args.append("-o")
			args.append(options)
		args.append(device)
		args.append(mountPoint)

		result = jk_simpleexec.invokeCmd("/bin/mount", args)
		if len(result.stdErrLines) > 0:
			for s in result.stdErrLines:
				if s.find(": WARNING:") >= 0:
					continue
				else:
					raise Exception(s)
		if result.returnCode != 0:
			raise Exception("Failed to mount " + device + " at " + mountPoint + "!")
		return True
	#

	def unmount(self, deviceOrMountPoint:str, raiseExceptionIfNotMounted = True):
		assert isinstance(deviceOrMountPoint, str)
		assert isinstance(raiseExceptionIfNotMounted, bool)

		if not self.isMounted(deviceOrMountPoint):
			if raiseExceptionIfNotMounted:
				raise Exception(deviceOrMountPoint + " is not mounted!")

		result = jk_simpleexec.invokeCmd("/bin/umount", [ deviceOrMountPoint ])
		if len(result.stdErrLines) > 0:
			for s in result.stdErrLines:
				if s.find(": WARNING:") >= 0:
					continue
				else:
					raise Exception(s)
		if result.returnCode != 0:
			raise Exception("Failed to unmount " + deviceOrMountPoint + "!")
		return True
	#



#






















