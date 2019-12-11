







class MountInfo(object):

	def __init__(self, device:str, mountPoint:str, fsType:str, options:dict):
		self.__device = device
		self.__mountPoint = mountPoint
		self.__fsType = fsType
		self.__options = options
	#

	#
	# Is this a regular device like "/dev/sda1" or "/dev/nvme0n1p3" or is this something like "proc" or "udev"?
	#
	@property
	def isRegularDevice(self) -> bool:
		return self.__device.startswith("/")
	#

	#
	# The device. This is something like "/dev/sda", "/dev/nvme0n1p3", "proc" or "udev".
	#
	@property
	def device(self) -> str:
		return self.__device
	#

	#
	# The mount point. This is something like "/", "/sys/fs/cgroup/perf_event" or "/snap/core/8213".
	#
	@property
	def mountPoint(self) -> str:
		return self.__mountPoint
	#

	#
	# The type of the file system used. This is something like "cgroup", "tmpfs", "proc", "squashfs" or "ext4".
	#
	@property
	def fsType(self) -> str:
		return self.__fsType
	#

	#
	# THe mount options. This is something like "rw,nodev,relatime,fd=32,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=1140" converted to a dictionary. The dictionary keys are the individual options, the dictionary values the values of the mount options. If no values are assigned for a key `None` is used for the value.
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

	#
	# This method is invoked by `Mounter` to parse a mount information text line.
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












