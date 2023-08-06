"""The MIDAS runtime config (adapted from the palaestrAI runtime
config).

"""
from __future__ import annotations

from copy import deepcopy
from io import TextIOWrapper
from os import getcwd
from pathlib import Path
from typing import Any, Dict, TextIO, Union

import appdirs
import ruamel.yaml

from . import LOG

CONFIG_FILE_NAME = "midas-runtime-conf.yml"
CONFIG_FILE_PATHS = [
    f"{appdirs.site_config_dir('midas', 'OFFIS')}/{CONFIG_FILE_NAME}",
    f"{appdirs.user_config_dir('midas', 'OFFIS')}/{CONFIG_FILE_NAME}",
    f"{getcwd()}/{CONFIG_FILE_NAME}",
]
DATA_FOLDER_NAME = "midas_data"
DEFAULT_BASE_CONFIG = {
    "paths": {
        "data_path": (
            f"{appdirs.user_config_dir('midas', 'OFFIS')}/midas_data"
        ),
        # "output_path": f"{getcwd()}/_outputs",
        "output_path": "_outputs",
        "scenario_path": (
            f"{appdirs.user_config_dir('midas', 'OFFIS')}/midas_scenarios"
        ),
    },
    "data": {
        "commercials": [
            {
                "name": "CommercialsRefTMY3.hdf5",
                "load_on_start": True,
                "base_url": "https://openei.org/datasets/files/961/pub/",
                "loc_url": (
                    "COMMERCIAL_LOAD_DATA_E_PLUS_OUTPUT/USA_NY_Rochester-"
                    "Greater.Rochester.Intl.AP.725290_TMY3/RefBldg"
                ),
                "post_fix": "New2004_v1.3_7.1_5A_USA_IL_CHICAGO-OHARE.csv",
                "data_urls": [
                    ["FullServiceRestaurant", "FullServiceRestaurant"],
                    ["Hospital", "Hospital"],
                    ["LargeHotel", "LargeHotel"],
                    ["LargeOffice", "LargeOffice"],
                    ["MediumOffice", "MediumOffice"],
                    ["MidriseApartment", "MidriseApartment"],
                    ["OutPatient", "OutPatient"],
                    ["PrimarySchool", "PrimarySchool"],
                    ["QuickServiceRestaurant", "QuickServiceRestaurant"],
                    ["SecondarySchool", "SecondarySchool"],
                    ["SmallHotel", "SmallHotel"],
                    ["SmallOffice", "SmallOffice"],
                    ["Stand-aloneRetail", "StandaloneRetail"],
                    ["StripMall", "StripMall"],
                    ["SuperMarket", "SuperMarket"],
                    ["Warehouse", "Warehouse"],
                ],
                "el_cols": [
                    "Electricity:Facility [kW](Hourly)",
                    "Fans:Electricity [kW](Hourly)",
                    "Cooling:Electricity [kW](Hourly)",
                    "Heating:Electricity [kW](Hourly)",
                ],
            },
        ],
        "default_load_profiles": [
            {
                "name": "DefaultLoadProfiles.hdf5",
                "load_on_start": True,
                "base_url": "https://www.bdew.de/media/documents/Profile.zip",
                "filename": "Repräsentative Profile VDEW.xls",
                "sheet_names": [
                    "H0",
                    "G0",
                    "G1",
                    "G2",
                    "G3",
                    "G4",
                    "G5",
                    "G6",
                    "L0",
                    "L1",
                    "L2",
                ],
                "seasons": [
                    ["Winter", "winter"],
                    ["Sommer", "summer"],
                    ["Übergangszeit", "transition"],
                ],
                "days": [
                    ["Samstag", "saturday"],
                    ["Sonntag", "sunday"],
                    ["Werktag", "weekday"],
                ],
            }
        ],
        "generator_timeseries": [
            {
                "base_url": "https://ds.50hertz.com/api/",
                "pv_url": "PhotovoltaicActual",
                "wind_url": "WindPowerActual",
                "postfix": "/DownloadFile?fileName=",
                "name": "GenWindPV50Hertz.hdf5",
                "load_on_start": True,
                "first_year": 2019,
                "last_year": 2019,
            }
        ],
        "simbench": [
            {
                "name": "1-LV-rural3--0-sw.hdf5",
                "load_on_start": True,
            }
        ],
        "smart_nord": [
            {"name": "SmartNordProfiles.hdf5", "load_on_start": True}
        ],
        "weather": [
            {
                "name": "WeatherBre2009-2020.hdf5",
                "load_on_start": True,
                "base_url": (
                    "https://opendata.dwd.de/climate_environment/CDC/"
                    "observations_germany/climate/hourly/"
                ),
                "air_url": (
                    "air_temperature/historical/stundenwerte_TU_00691_"
                    "19490101_"
                ),
                "wind_url": (
                    "wind/historical/stundenwerte_FF_00691_19260101_"
                ),
                "sun_url": ("sun/historical/stundenwerte_SD_00691_19510101_"),
                "cloud_url": (
                    "cloudiness/historical/stundenwerte_N_00691_19490101_"
                ),
                "solar_url": "solar/stundenwerte_ST_00691_row.zip",
                "post_fix": "20211231_hist.zip",
                "start_date": "2009-01-01 00:00:00",
            }
        ],
    },
    "modules": {
        "default_modules": [
            ["store", "midas.modules.store.module:DatabaseModule"],
            ["timesim", "midas.modules.timesim.module:TimeSimModule"],
            ["powergrid", "midas.modules.powergrid.module:PowergridModule"],
            ["sbdata", "midas.modules.sbdata.module:SimbenchDataModule"],
            ["sndata", "midas.modules.sndata.module:SmartNordDataModule"],
            ["comdata", "midas.modules.comdata.module:CommercialDataModule"],
            ["dlpdata", "midas.modules.dlpdata.module:DLPDataModule"],
            ["pwdata", "midas.modules.pwdata.module:PVWindDataModule"],
            ["weather", "midas.modules.weather.module:WeatherDataModule"],
            ["der", "pysimmods.mosaik.midas_module:PysimmodsModule"],
            ["goa", "midas.modules.goa.module:GridOperatorModule"],
        ],
        "custom_modules": [],
    },
    "misc": {"seed_max": 1_000_000, "use_pprint": False},
    "logging": {
        "version": 1,
        "formatters": {
            "simple": {
                "format": ("%(asctime)s [%(name)s][%(levelname)s] %(message)s")
            },
            "debug": {
                "format": (
                    "%(asctime)s [%(name)s (%(process)d)][%(levelname)s] "
                    "%(message)s (%(module)s.%(funcName)s in %(filename)s"
                    ":%(lineno)d)"
                )
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "console-debug": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "debug",
                "stream": "ext://sys.stdout",
            },
            "logfile": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "midas.log",
                "mode": "w",
            },
            "logfile-debug": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "debug",
                "filename": "midas_debug.log",
                "mode": "w",
            },
        },
        "loggers": {
            "midas.api": {"level": "WARNING"},
            "midas.modules": {"level": "WARNING"},
            "midas.scenario": {"level": "WARNING"},
            "midas.tools": {"level": "WARNING"},
            "midas.util": {"level": "WARNING"},
            "pysimmods": {"level": "WARNING"},
        },
        "root": {
            "level": "ERROR",
            "handlers": [
                "console",
                "logfile-debug",
            ],
        },
    },
}


class _RuntimeConfig:
    """Application-wide runtime configuration.

    This singleton class provides an application-wide runtime configuration
    and transparently hides all sources from the rest of the application.
    """

    DEFAULT_CONFIG = deepcopy(DEFAULT_BASE_CONFIG)

    _instance = None

    def __init__(self):
        self._config_file_path = None
        self.config_search_path = CONFIG_FILE_PATHS

        # The loaded configuration is what RuntimeConfig.load gave us.
        # It remeains immutable after loading.
        self._loaded_configuration = dict()

    def _get(self, key: str, default=None, exception=None) -> Any:
        """Retrieves a config key.

        Retrieves any config key; if not set, it queries the config
        dictionary; if it isn't present there, it returns the given
        default value. It also sets the value in the current object
        as side-effect.

        """
        lkey = f"_{key}"
        if lkey not in self.__dict__:
            try:
                self.__dict__[lkey] = self._loaded_configuration[key]
            except KeyError:
                if default:
                    self.__dict__[lkey] = default
                else:
                    self.__dict__[lkey] = _RuntimeConfig.DEFAULT_CONFIG[key]
                if exception:
                    raise KeyError(exception)
        return self.__dict__[lkey]

    def reset(self):
        """Resets the runtime configuration to empty state."""
        for key in list(self._loaded_configuration.keys()) + list(
            _RuntimeConfig.DEFAULT_CONFIG.keys()
        ):
            try:
                del self.__dict__[f"_{key}"]
            except KeyError:
                pass
        self._loaded_configuration = dict()
        self._config_file_path = None

    @property
    def logging(self) -> Dict:
        """Configuration of all subsystem loggers.

        Returns
        -------
        dict
            A logging configuration that can be fed into
            `logging.DictConfig`.

        """
        return self._get(
            "logging", exception="Sorry, no logging config in the config file."
        )

    # TODO: Add more properties
    @property
    def paths(self) -> Dict:
        """Return the configured paths."""
        return self._get("paths", exception="Sorry, not paths configured.")

    @property
    def data(self) -> Dict:
        """Return the configured datasets."""
        data = self._get("data", exception="Sorry, no datasets configured.")
        for key, values in DEFAULT_BASE_CONFIG["data"].items():
            data.setdefault(key, values)
        return data

    @property
    def modules(self) -> Dict:
        return self._get("modules", exception="Sorry, no modules configured.")

    @property
    def misc(self) -> Dict:
        """Return miscellaneous options."""
        return self._get(
            "misc", exception="Sorry, no miscellaneous options configured."
        )

    def load(
        self, stream_or_dict: Union[dict, TextIO, str, Path, None] = None
    ):
        """Load the configuration from an external source.

        The runtime configuration is initialized from the default
        configuration in ::`_RuntimeConfig.DEFAULT_CONFIG`. This method
        then iterates through the list in
        ::`_RuntimeConfig.CONFIG_FILE_PATHS`, subsequently updating the
        existing configuration with new values found. Finally, the
        given ::`stream_or_dict` parameter is used if present,
        ultimately taking preference over all other values.

        That means that each config file can contain only a portion of
        the overall configuration; it gets updated subsequently.

        Parameters
        ----------
        stream_or_dict: Union[dict, TextIO, str, Path, None]
            Loads the runtime configuration directly from a dictionary
            or as YAML-encoded stream. If no stream is given, the
            default files in ::`.CONFIG_FILE_PATHS` will be tried as
            described.

        """
        if not isinstance(self._loaded_configuration, dict):
            self._loaded_configuration = dict()
        if stream_or_dict is None and self._loaded_configuration:
            # if not stream_or_dict and len(self._loaded_configuration) > 0:
            # Don't load a default config if we already have something;
            # use reset() instead.
            return

        # yml = ruamel.yaml.YAML(typ="safe")
        has_seen_nondefault_config = False
        self._loaded_configuration.update(_RuntimeConfig.DEFAULT_CONFIG)
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        for fil in CONFIG_FILE_PATHS:
            try:
                LOG.debug("Trying to open configuration file: '%s'", fil)
                with open(fil, "r") as fp:
                    deserialized = yaml.load(fp)
                    if not isinstance(deserialized, dict):
                        LOG.warning(
                            "The contents of '%s' coult not be deserialized"
                            " to dict, skipping it.",
                            fil,
                        )
                        continue
                    self._loaded_configuration.update(deserialized)
                    self._config_file_path = fil
                    has_seen_nondefault_config = True
            except IOError:
                continue

        if isinstance(stream_or_dict, dict):
            self._loaded_configuration.update(stream_or_dict)
            self._config_file_path = "(dict)"
            return

        if isinstance(stream_or_dict, str):
            stream_or_dict = Path(stream_or_dict)
        if isinstance(stream_or_dict, Path):
            try:
                stream_or_dict = open(stream_or_dict, "r")
            except OSError:
                LOG.warning(
                    "Failed to load runtime configuration from file at"
                    " '%s', ignoring",
                    stream_or_dict,
                )
        if stream_or_dict is not None:
            try:
                deserialized = yaml.load(fp)
                if not isinstance(deserialized, dict):
                    raise TypeError
                self._loaded_configuration.update(deserialized)
                try:
                    self._config_file_path = stream_or_dict.name
                except AttributeError:
                    self._config_file_path = str(stream_or_dict)
                has_seen_nondefault_config = True
            except TypeError:
                LOG.warning(
                    "Failed to load runtime configuration from stream"
                    " at '%s', ignoring it",
                    repr(stream_or_dict),
                )
            finally:
                if isinstance(stream_or_dict, TextIOWrapper):
                    stream_or_dict.close()

        if not has_seen_nondefault_config:
            LOG.info(
                "No runtime configuration given, loaded built-in default."
            )
            self._config_file_path = "(DEFAULT)"

    def to_dict(self) -> Dict:
        return {key: self._get(key) for key in _RuntimeConfig.DEFAULT_CONFIG}

    def __str__(self):
        return f"<RuntimeConfig id=0x{id(self)}> at {self._config_file_path}"

    def __repr__(self):
        return str(self.to_dict())


def RuntimeConfig():
    if _RuntimeConfig._instance is None:
        _RuntimeConfig._instance = _RuntimeConfig()
        try:
            _RuntimeConfig._instance.load()
        except FileNotFoundError:
            from copy import deepcopy

            _RuntimeConfig._instance._loaded_configuration = deepcopy(
                _RuntimeConfig.DEFAULT_CONFIG
            )
    return _RuntimeConfig._instance
