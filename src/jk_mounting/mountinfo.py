#!/usr/bin/python
# -*- coding: utf-8 -*-




import re
import os
import sys
import codecs
import collections

import jk_simpleexec







class MountInfo(object):

	def __init__(self, device:str, mountPoint:str, fsType:str, options:dict):
		self.__device = device
		self.__mountPoint = mountPoint
		self.__fsType = fsType
		self.__options = options
	#

	@property
	def isRegularDevice(self):
		return self.__device.startswith("/")
	#

	@property
	def device(self) -> str:
		return self.__device
	#

	@property
	def mountPoint(self) -> str:
		return self.__mountPoint
	#

	@property
	def fsType(self) -> str:
		return self.__fsType
	#

	@property
	def options(self) -> dict:
		return self.__options
	#

	def toJSON(self):
		return {
			"device": self.__device,
			"mountPoint": self.__mountPoint,
			"fsType": self.__fsType,
			"options": self.__options,
		}
	#

	@staticmethod
	def _parseFromMountLine(line):
		assert isinstance(line, str)

		elements = line.split(' ')
		while len(elements) > 6:
			elements[1] = elements[1] + elements[2]
			del elements[2]
		options = dict()
		for optionLine in elements[3].split(","):
			pos = optionLine.find("=")
			if pos < 0:
				options[optionLine] = None
			else:
				options[optionLine[0:pos]] = optionLine[pos + 1:]
		return MountInfo(elements[0], elements[1], elements[2], options)
	#

	def __str__(self):
		return "MountInfo(device=" + self.__device + ", mountPoint=" + self.__mountPoint + ", fsType=" + self.__fsType + ", options=" + str(self.__options) + ")"
	#

	def __repr__(self):
		return "MountInfo(device=" + self.__device + ", mountPoint=" + self.__mountPoint + ", fsType=" + self.__fsType + ", options=" + str(self.__options) + ")"
	#

#





#
# This class represents various common mount options. <c>__str__()</c> is invoked by <c>Mounter.mount(...)</c> during a mount attempt in order to derive valid
# mount options from an instance of this class.
#
class MountOptions(object):

	def __init__(self):
		self._async = True
		self._atime = True
		self._diratime = True
		self._rw = True
		self._dev = True
		self._suid = True
		self._exec = True
		self._relatime = True
		self._dirsync = False
		self._uid = None
		self._gid = None
		self._remount = False

		"""
		# cifs
		self._user = None
		self._password = None
		self._credentials = None
		self._forceuid = False
		self._forcegid = False
		self._port = None
		self._netbiosname = None
		self._file_mode = None
		self._dir_mode = None
		self._domain = None
		"""

	def __repr__(self):
		return "MountOptions(" + self.__str__() + ")"

	def __str__(self):
		s = ""

		if self._uid != None:
			s += ",uid=" + str(self._uid)
		if self._gid != None:
			s += ",gid=" + str(self._gid)
		if self._remount:
			s += ",remount"
		if not self._async:
			s += ",sync"
		if not self._atime:
			s += ",noatime"
		if not self._diratime:
			s += ",nodiratime"
		if not self._rw:
			s += ",ro"
		if not self._dev:
			s += ",nondev"
		if not self._suid:
			s += ",nosuid"
		if not self._exec:
			s += ",noexec"
		if not self._relatime:
			s += ",norelatime"
		if self._dirsync:
			s += ",dirsync"

		if len(s) > 0:
			return s[1:]
		else:
			return ""
	#

	#
	# Attempt to remount an already-mounted filesystem. This is commonly used to change the mount flags for a filesystem, especially to make a readonly filesystem writeable. It does not change device or mount point.
	#
	@property
	def remount(self):
		return self._remount

	@remount.setter
	def remount(self, value):
		assert isinstance(value, bool)
		self._remount = value

	#
	# Allow set-user-identifier or set-group-identifier bits to take effect.
	#
	@property
	def suid(self):
		return self._suid

	@suid.setter
	def suid(self, value):
		assert isinstance(value, bool)
		self._suid = value

	#
	# Do not allow set-user-identifier or set-group-identifier bits to take effect. (This seems safe, but is in fact rather unsafe if you have suidperl(1) installed.)
	#
	@property
	def nosuid(self):
		return not self._suid

	@nosuid.setter
	def nosuid(self, value):
		assert isinstance(value, bool)
		self._suid = not value

	#
	# Update inode access times relative to modify or change time. Access time is only updated if the previous access time was earlier than the current modify or change time. (Similar to noatime, but doesn't break mutt or other applications that need to know if a file has been read since the last time it was modified.)
	#
	@property
	def relatime(self):
		return self._relatime

	@relatime.setter
	def relatime(self, value):
		assert isinstance(value, bool)
		self._relatime = value

	#
	# Do not use relatime feature. See also the strictatime mount option.
	#
	@property
	def norelatime(self):
		return not self._relatime

	@norelatime.setter
	def norelatime(self, value):
		assert isinstance(value, bool)
		self._relatime = not value

	#
	# All I/O to the filesystem should be done asynchronously. (See also the sync option.)
	#
	@property
	def async(self):
		return self._async

	@async.setter
	def async(self, value):
		assert isinstance(value, bool)
		self._async = value

	#
	# All I/O to the filesystem should be done synchronously. In case of media with limited number of write cycles (e.g. some flash drives) "sync" may cause life-cycle shortening.
	#
	@property
	def sync(self):
		return not self._async

	@sync.setter
	def sync(self, value):
		assert isinstance(value, bool)
		self._async = not value

	#
	# Do not update inode access times on this filesystem (e.g, for faster access on the news spool to speed up news servers).
	#
	@property
	def noatime(self):
		return not self._atime

	@noatime.setter
	def noatime(self, value):
		assert isinstance(value, bool)
		self._atime = not value

	#
	# Do not use noatime feature, then the inode access time is controlled by kernel defaults. See also the description for strictatime and relatime mount options.
	#
	@property
	def atime(self):
		return self._atime

	@atime.setter
	def atime(self, value):
		assert isinstance(value, bool)
		self._atime = value

	#
	# Do not interpret character or block special devices on the file system.
	#
	@property
	def nodev(self):
		return not self._dev

	@nodev.setter
	def nodev(self, value):
		assert isinstance(value, bool)
		self._dev = not value

	#
	# Interpret character or block special devices on the filesystem.
	#
	@property
	def dev(self):
		return self._dev

	@dev.setter
	def dev(self, value):
		assert isinstance(value, bool)
		self._dev = value

	#
	# Update directory inode access times on this filesystem. This is the default.
	#
	@property
	def diratime(self):
		return self._rw

	@diratime.setter
	def diratime(self, value):
		assert isinstance(value, bool)
		self._diratime = value

	#
	# Do not update directory inode access times on this filesystem.
	#
	@property
	def nodiratime(self):
		return not self._diratime

	@nodiratime.setter
	def nodiratime(self, value):
		assert isinstance(value, bool)
		self._diratime = not value

	#
	# All directory updates within the filesystem should be done synchronously. This affects the following system calls: creat, link, unlink, symlink, mkdir, rmdir, mknod and rename.
	#
	@property
	def dirsync(self):
		return self._dirsync

	@dirsync.setter
	def dirsync(self, value):
		assert isinstance(value, bool)
		self._dirsync = value

	#
	# Permit execution of binaries.
	#
	@property
	def exec(self):
		return self._exec

	@exec.setter
	def exec(self, value):
		assert isinstance(value, bool)
		self._exec = value

	#
	# Do not allow direct execution of any binaries on the mounted filesystem. (Until recently it was possible to run binaries anyway using a command like /lib/ld*.so /mnt/binary. This trick fails since Linux 2.4.25 / 2.6.0.)
	#
	@property
	def noexec(self):
		return not self._exec

	@noexec.setter
	def noexec(self, value):
		assert isinstance(value, bool)
		self._exec = not value

	#
	# Mount the filesystem read-write.
	#
	@property
	def rw(self):
		return self._rw

	@rw.setter
	def rw(self, value):
		assert isinstance(value, bool)
		self._rw = value

	#
	# Set the owner of all files. (Default: the uid and gid of the current process.)
	#
	@property
	def uid(self):
		return self._uid

	@uid.setter
	def uid(self, value):
		assert isinstance(value, (type(None), int, str))
		self._uid = value

	#
	# Set the group of all files. (Default: the uid and gid of the current process.)
	#
	@property
	def gid(self):
		return self._gid

	@gid.setter
	def gid(self, value):
		assert isinstance(value, (type(None), int, str))
		self._gid = value

	# ----------------

	"""
	def user(self):
		return self._user

	@user.setter
	def user(self, value):
		assert isinstance(value, (type(None), str))
		self._user = value

	def password(self):
		return self._password

	@password.setter
	def password(self, value):
		assert isinstance(value, (type(None), str))
		self._password = value

	def credentials(self):
		return self._credentials

	@credentials.setter
	def credentials(self, value):
		assert isinstance(value, (type(None), str))
		self._credentials = value

	def forceuid(self):
		return self._forceuid

	@forceuid.setter
	def forceuid(self, value):
		assert isinstance(value, (type(None), str, int))
		self._forceuid = value

	def forcegid(self):
		return self._forcegid

	@forcegid.setter
	def forcegid(self, value):
		assert isinstance(value, (type(None), str, int))
		self._forcegid = value

	def port(self):
		return self._port

	@port.setter
	def port(self, value):
		assert isinstance(value, (type(None), int))
		self._port = value

	def netbiosname(self):
		return self._netbiosname

	@netbiosname.setter
	def netbiosname(self, value):
		assert isinstance(value, (type(None), str))
		self._netbiosname = value

	def file_mode(self):
		return self._file_mode

	@file_mode.setter
	def file_mode(self, value):
		assert isinstance(value, (type(None), int))
		self._file_mode = value

	def dir_mode(self):
		return self._dir_mode

	@dir_mode.setter
	def dir_mode(self, value):
		assert isinstance(value, (type(None), int))
		self._dir_mode = value

	def domain(self):
		return self._domain

	@domain.setter
	def domain(self, value):
		assert isinstance(value, (type(None), str))
		self._domain = value
	"""

#






class Mounter(object):

	def __init__(self):
		self.refresh()
	#

	def refresh(self):
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
			if isRegularDevice != None:
				if isRegularDevice:
					if not mi.isRegularDevice:
						continue
				else:
					if mi.isRegularDevice:
						continue
			if fsTypeExcl != None:
				if mi.fsType in fsTypeExcl:
					continue
			if fsTypeIncl != None:
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
	def mount(self, device, mountPoint, options = None, raiseExceptionIfMounted = True):
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
				if optionValue != None:
					s += "=" + optionValue
			options = s

		args = []
		if (options != None) and (len(options) > 0):
			args.append("-o")
			args.append(options)
		args.append(device)
		args.append(mountPoint)

		result = jk_simpleexec.invokeCmd("/bin/mount", args)
		if len(result.stdErrLines) > 0:
			for s in result.stdErrLines:
				if s.startswith("WARNING:"):
					continue
				else:
					raise Exception(s)
		if result.returnCode != 0:
			raise Exception("Failed to mount " + device + " at " + mountPoint + "!")
		return True
	#

	def unmount(self, deviceOrMountPoint, raiseExceptionIfNotMounted = True):
		assert isinstance(deviceOrMountPoint, str)
		assert isinstance(raiseExceptionIfNotMounted, bool)

		if not self.isMounted(deviceOrMountPoint):
			if raiseExceptionIfNotMounted:
				raise Exception(deviceOrMountPoint + " is not mounted!")

		result = jk_simpleexec.invokeCmd("/bin/umount", [ deviceOrMountPoint ])
		result.dump()
		if len(result.stdErrLines) > 0:
			for s in result.stdErrLines:
				if s.startswith("WARNING:"):
					continue
				else:
					raise Exception(s)
		if result.returnCode != 0:
			raise Exception("Failed to unmount " + deviceOrMountPoint + "!")
		return True
	#



#






















