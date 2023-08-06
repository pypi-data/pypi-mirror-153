import logging
import os
from pathlib import Path

from .configuration import Config
from .utils import Singleton, create_directories


class EnvironmentNames(object, metaclass=Singleton):
	__var_name: str = 'ENVIRONMENT'
	__local_env_name: str = 'local'
	__developement_env_name: str = 'dev'
	__testing_env_name: str = 'test'
	__staging_env_name: str = 'stage'
	__production_env_name: str = 'prod'

	def __init__(self, var_name: str = 'ENVIRONMENT', local_env: str = 'local',
	             dev_env: str = 'dev', test_env: str = 'test',
	             stage_env: str = 'stage', prod_env: str = 'prod'
	             ):
		self.__local_env_name = local_env.lower().strip()
		self.__staging_env_name = stage_env.lower().strip()
		self.__production_env_name = prod_env.lower().strip()
		self.__testing_env_name = test_env.lower().strip()

	@property
	def local(self):
		return self.__local_env_name

	@property
	def developement(self):
		return self.__developement_env_name

	@property
	def staging(self):
		return self.__staging_env_name

	@property
	def testing(self):
		return self.__testing_env_name

	@property
	def production(self):
		return self.__production_env_name

	@property
	def var_name(self):
		return self.__var_name


class Environment(object,metaclass=Singleton):
	__config_filetype: str = '.env'

	__resource_dir: str = ''

	__base_env_file: str = ''

	__config_file: str = ''

	__current_env_name: str = ''

	__environment_names: EnvironmentNames

	__root_dir: Path = None

	__config: Config = None

	__required_dir_list: list = []

	def __str__(self):
		return dict(
			type=self, name=self.name, base_file=self.__base_env_file,
			config_file=self.__config_file
		).__str__()

	def __load_base_env_file(self):
		try:
			if not self.name:
				from dotenv import load_dotenv
				load_dotenv(self.__base_env_file)
				self.__current_env_name = os.environ.get(self.env_names.var_name, default=None)


		except Exception as e:
			logging.exception(e)
			exit()

	def set_environment_name(self, env_name: str = None):
		if self.name not in [None, '']:
			self.__current_env_name = env_name
		return self

	def __init__(self,
	             root: Path = '', src_dir: str = 'resource',
	             filename: str = '', config_filetype: str = '.env',
	             env_names: EnvironmentNames = EnvironmentNames()
	             ):
		try:
			self.__environment_names = env_names
			self.__config_filetype = config_filetype

			if not os.path.isdir(root):
				raise Exception(f"Parameter 'root' in Environment.__init__(), cannot be empty.")

			self.__root_dir = root
			self.__resource_dir = os.path.join(self.root_dir, src_dir)

			if not os.path.isdir(self.resource_dir):
				self.__required_dir_list.append(self.resource_dir)

			self.__base_env_file = os.path.join(self.resource_dir, filename,
			                                    self.__config_filetype)

			if not os.path.isfile(self.__base_env_file):
				raise Exception(f"Base environment file '{self.__base_env_file}' doesn't Exists")

		except Exception as e:
			logging.error(e)
			exit()

	def add_required_dirs(self, dirs: list = None):
		self.__required_dir_list.extend([] if dirs is None else dirs)
		return self

	def setup(self):
		try:
			self.__load_base_env_file()

			if self.name:
				self.__config_file = os.path.join(
					self.resource_dir, f"{self.name}{self.__config_filetype}"
				)
				self.__config = Config(config_file=self.__config_file).load()

				if self.config and self.config.get('REQUIRED_DIRS') is not None:
					self.__required_dir_list.extend(self.config.get('REQUIRED_DIRS').as_list())

				create_directories(self.__required_dir_list)

		except Exception as e:
			logging.exception(e)
			exit()
		return self

	@property
	def root_dir(self):
		return self.__root_dir.__str__()

	@property
	def resource_dir(self):
		return self.__resource_dir

	@property
	def env_names(self):
		return self.__environment_names

	@property
	def config(self):
		return self.__config

	@property
	def name(self):
		return self.__current_env_name.strip()

	@property
	def is_local(self):
		return self.__current_env_name == self.env_names.local

	@property
	def is_dev(self):
		return self.__current_env_name == self.env_names.developement

	@property
	def is_stage(self):
		return self.__current_env_name == self.env_names.staging

	@property
	def is_test(self):
		return self.__current_env_name == self.env_names.testing

	@property
	def is_prod(self):
		return self.__current_env_name == self.env_names.production