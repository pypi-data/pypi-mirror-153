import logging, os


def singleton(class_):
	instances = {}

	def getinstance(*args, **kwargs):
		if class_ not in instances:
			instances[class_] = class_(*args, **kwargs)
		return instances[class_]

	return getinstance


class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


def create_directories(dir_list: list):
	for directory in dir_list:
		try:
			if not os.path.isdir(directory):
				os.mkdir(directory, mode=0o777)
		except Exception as e:
			logging.error(f"Exception occurred while creating directory[{directory}] :\n {e}")