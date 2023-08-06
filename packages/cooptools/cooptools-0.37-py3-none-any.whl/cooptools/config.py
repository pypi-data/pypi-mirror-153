from configparser import ConfigParser, NoOptionError, NoSectionError
import os
import logging
from typing import Dict, Any, Tuple, Union, Callable, Optional
import cooptools.os_manip as osm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ConfigStateException(Exception):
    def __init__(self, txt: str = None):
        logger.error(txt)
        super().__init__(txt)


class ConfigStateFactory:

    def __init__(self,
                 config_definition_dict: Dict[str, Dict[str, Any]],
                 config_file_path_provider: Optional[Union[str, Callable[[], str]]] = None,
                 make_file_if_missing: bool = False):

        if config_definition_dict is None:
            raise ConfigStateException(f"config_definition_dict cannot be None")

        if make_file_if_missing and config_file_path_provider is None:
            raise ConfigStateException(f"config_file_path_provider cannot be None when make_file_if_missing flag is set to True")

        self.make_file_if_missing = make_file_if_missing

        self._config_definition_dict = config_definition_dict
        self.parser = ConfigParser()

        self._config_file_path_provider: Optional[Union[str, Callable[[], str]]] = None
        self.current_file_path = None

        self.set_file(config_file_path_provider)

    def __getitem__(self, item: Tuple[str, str]):
        return self.get_config(item[0], item[1])

    def _try_resolve_config_file_path(self):
        if self._config_file_path_provider is None:
            return None

        if type(self._config_file_path_provider) == str:
            return self._config_file_path_provider

        try:
            return self._config_file_path_provider()
        except Exception as e:
            logger.error(f"Unable to resolve the config file path: {e}")
            return None

    def set_file(self, file_path_provider: Union[str, Callable[[], str]]):
        self._config_file_path_provider = file_path_provider
        self.current_file_path = self._try_resolve_config_file_path()

        self.reload()

    def reload(self):
        self._verify_file()
        self._try_load_pass(self.current_file_path)


    def _verify_file(self):
        if not self.make_file_if_missing or self._config_file_path_provider is None:
            return

        if self.current_file_path is not None \
                and not os.path.isfile(self.current_file_path) \
                and not self.make_file_if_missing:
            raise ConfigStateException(f"config_file_path {self.current_file_path} does not exist.")
        elif self.current_file_path is not None \
                and not os.path.isfile(self.current_file_path):
            osm.create_file(self.current_file_path,
                            file_type=osm.FileType.INI)

        self._verify_headers_in_file()

    def _verify_headers_in_file(self):
        verification_parser = ConfigParser()
        verification_parser.read(self.current_file_path)

        for header, values in self._config_definition_dict.items():
            if not verification_parser.has_section(header):
                with open(self.current_file_path, 'a') as file:
                    lines = []
                    lines.append(f'\n\n[{header}]')
                    lines += [f'\n{k}={v}' for k, v in values.items() if not callable(v)]
                    file.writelines(lines)


    def _try_load_pass(self, config_file_path: str):
        try:
            self.load_from_file(config_file_path=config_file_path)
        except:
            pass
        finally:
            # set attributes
            for header, vals in self._config_definition_dict.items():
                for k, v in vals.items():
                    setattr(self, f"{header}_{k}", self._try_access_parser_default(header, k, v))

    def load_from_file(self, config_file_path: str = None):
        if config_file_path is not None:
            self.current_file_path = config_file_path

        if not os.path.isfile(self.current_file_path):
            issue = f"Unable to load config from directory: \"{self.current_file_path}\" does not exist"
            raise ConfigStateException(issue)

        try:
            self.parser.read(self.current_file_path)
            logger.info(f"Config set from directory: {self.current_file_path}")
        except Exception as e:
            issue = f"Unable to load config from directory: {self.current_file_path}" \
                    f"\n{e}"
            raise ConfigStateException(issue) from e

    def _try_access_parser_default(self, header, name, default):
        try:
            return self.parser.get(header, name)
        except (NoSectionError, NoOptionError):
            pass

        try:
            return default()
        except TypeError as e:
            pass

        return default

    def get_config(self, header, name):
        if header not in self._config_definition_dict.keys():
            raise ConfigStateException(f"Requested header [\"{header}\"] was not defined")
        if name not in self._config_definition_dict[header].keys():
            raise ConfigStateException(f"Requested config [\"{name}\"] was not defined")
        default = self._config_definition_dict[header][name]
        val = self._try_access_parser_default(header, name, default)
        logger.debug(f"Value for {header}|{name}: {val}")
        return val

    @property
    def config_dir(self):
        return os.path.dirname(self.current_file_path)

    @property
    def config_file_path(self):
        return self.current_file_path

    @property
    def sections(self):
        return self.parser.sections()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    _def = "def"
    my_dict = {_def: {
                   "a": None,
                   "b": 2,
                   "c": "TRYIT",
                   "d": lambda: 123}
    }

    con = ConfigStateFactory(my_dict, config_file_path_provider=r'C:\Users\tburns\AppData\Local\coopazureutils\config2.ini')

    print(con.get_config(_def, "a"), con.get_config(_def, "b"), con.get_config(_def, "c"))

    print(con.def_a, con.def_b, con.def_c, con.def_d)
    print(con[(_def, "b")])

    print(con.sections)
