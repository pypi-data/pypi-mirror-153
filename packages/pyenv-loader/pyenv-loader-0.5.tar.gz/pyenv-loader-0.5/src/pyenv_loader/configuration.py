import logging
import os
from dotenv import load_dotenv, dotenv_values
from .utils import Singleton


# Env variable class
class ConfigVar(object):
	_key = None

	_value = None

	def __init__(self, key: str = '', default=None):
		self._key = key
		self._value = os.environ.get(key=key, default=default)

	def __str__(self):
		return str(self.__dict__)

	@property
	def key(self):
		return self._key

	@property
	def value(self):
		return self._value

	def as_str(self, default: str = '') -> str:
		return default if self._value is None else self._value

	def as_int(self, default: int = 0) -> int:
		return default if self._value is None else int(self._value)

	def as_float(self, default: float = 0.0) -> float:
		return default if self._value is None else float(self._value)

	def as_bool(self, default: bool = False) -> bool:
		if self._value is not None:
			return (int(self._value) > 0) if self._value.isnumeric() \
				else self._value.lower() in ['yes', 'true', '1']
		else:
			return default

	def as_list(self, sep='|', default: list = None) -> list:
		default = default if default is not None else []
		return default if self._value is None else self._value.split(sep=sep)

	def as_tuple(self, sep='|', default: tuple = None) -> tuple:
		default = default if default is not None else tuple()
		return tuple(self.as_list(sep=sep, default=list(default)))

	def as_dict(self, sep='|', kv_sep: str = '=', default: dict = None) -> dict:
		default = default if default is not None else dict()
		lst = self.as_list(sep=sep)
		if len(lst) > 0:
			return {
				str(item).strip().split(kv_sep)[0]:
					str(item).strip().split(kv_sep)[1]
				for item in lst}

	def as_path(self, default='', joinpath: str = None):
		if joinpath is not None:
			return os.path.join(joinpath, self.as_str(default=default))
		return self.as_str(default=default)


class Config(object, metaclass=Singleton):
	__config_file: str = ''

	__is_loaded = False

	_is_debug = False

	def __str__(self):
		return dict(obj=self, is_loaded=self.is_loaded, file=self.file).__str__()

	def __load_config_from_env_file(self, force=False):
		if not self.__is_loaded or force:
			self.__load_config_from_env_file()
			self.__is_loaded = True
		return self

	def __init__(self, config_file: str = None):
		try:
			if os.path.isfile(config_file):
				self.__config_file = config_file
			else:
				raise Exception(f"Config file '{self.__config_file}' doesn't exists.")

		except Exception as e:
			logging.error(e)
			exit()

	def load(self, force=False):
		try:
			if (not self.is_loaded) or force:
				load_dotenv(self.file)
				self.__is_loaded = True
		except Exception as e:
			logging.error(e)
		return self

	def get(self, key: str = '', default=None) -> ConfigVar:
		self.load()
		return ConfigVar(key=key, default=default)

	def all(self, as_dict=True):
		self.load()
		config = dotenv_values(self.file)
		return config if as_dict else {key: ConfigVar(key=key) for key in config}

	@property
	def file(self):
		return self.__config_file

	@property
	def name(self):
		return os.path.basename(self.file)

	@property
	def debug(self):
		return self._is_debug or self.get('DEBUG').as_bool(default=False)

	@property
	def is_loaded(self):
		return self.__is_loaded