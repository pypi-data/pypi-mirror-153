"""MIDAS base upgrade module for dataset simulators."""
import logging

from .upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class BaseDataModule(UpgradeModule):
    def __init__(
        self,
        module_name,
        default_scope_name,
        default_sim_config_name,
        default_import_str,
        default_cmd_str,
        log=LOG,
    ):
        super().__init__(
            module_name=module_name,
            default_scope_name=default_scope_name,
            default_sim_config_name=default_sim_config_name,
            default_import_str=default_import_str,
            default_cmd_str=default_cmd_str,
            log=log,
        )

        self.models = {}
        self._scaling_key = "scaling"

    def check_module_params(self, module_params):
        """Check the module params and provide default values"""

        module_params.setdefault("start_date", self.scenario.base.start_date)
        module_params.setdefault("data_path", self.scenario.base.data_path)
        module_params.setdefault("cos_phi", self.scenario.base.cos_phi)
        module_params.setdefault("interpolate", False)
        module_params.setdefault("noise_factor", 0.2)

        if module_params["no_rng"]:
            module_params["randomize_data"] = False
            module_params["randomize_cos_phi"] = False
        else:
            module_params.setdefault("randomize_data", False)
            module_params.setdefault("randomize_cos_phi", False)

    def check_sim_params(self, module_params):
        """Check the params for a certain scope/simulator instance."""

        self.sim_params.setdefault("grid_name", self.scope_name)
        self.sim_params.setdefault("start_date", module_params["start_date"])
        self.sim_params.setdefault("data_path", module_params["data_path"])
        self.sim_params.setdefault("cos_phi", module_params["cos_phi"])
        self.sim_params.setdefault("interpolate", module_params["interpolate"])
        self.sim_params.setdefault(
            "randomize_data", module_params["randomize_data"]
        )
        self.sim_params.setdefault(
            "randomize_cos_phi", module_params["randomize_cos_phi"]
        )
        self.sim_params.setdefault(
            "noise_factor", module_params["noise_factor"]
        )
        self.sim_params.setdefault("seed_max", self.scenario.base.seed_max)
        self.sim_params.setdefault("seed", self.scenario.create_seed())

    def start_models(self):
        """Start models of a certain simulator."""

        for model in self.models:
            mapping_key = f"{model}_mapping"

            self.start_models_from_mapping(mapping_key, model, "load")

    def start_models_from_mapping(self, mapping_key, model, mtype):
        """Iterate over a mapping and start models."""

        self.sim_params.setdefault(mapping_key, self.create_default_mapping())
        if not self.sim_params[mapping_key]:
            # No mappings configure
            return

        mapping = self.scenario.create_shared_mapping(
            self, self.sim_params["grid_name"], mtype
        )
        model_name = model
        for bus, entities in self.sim_params[mapping_key].items():
            mapping.setdefault(bus, [])
            for eidx, (name, scale) in enumerate(entities):
                if model is None:
                    model_name = name

                model_key = self.scenario.generate_model_key(
                    self, model_name, bus, eidx
                )
                scaling = scale * float(self.sim_params[f"{mtype}_scaling"])
                params = {self._scaling_key: scaling}
                full_id = self.start_model(model_key, model_name, params)

                info = self.scenario.get_sim(self.sim_key).get_data_info()
                mapping[bus].append(
                    (
                        model_name,
                        info[full_id.split(".")[-1]]["p_mwh_per_a"] * scaling,
                    )
                )

    def connect_to_grid(self, mapping_key, model, mtype, attrs=None):
        if attrs is None:
            attrs = ["p_mw", "q_mvar"]

        model_name = model
        for bus, entities in self.sim_params[mapping_key].items():
            for eidx, (name, _) in enumerate(entities):
                if model is None:
                    model_name = name

                model_key = self.scenario.generate_model_key(
                    self, model_name, bus, eidx
                )
                grid_entity_key = self.get_grid_entity(mtype, bus)
                self.connect_entities(model_key, grid_entity_key, attrs)

    def connect_to_db(self):
        """Connect the models to db."""
        for model in self.models:
            mapping_key = f"{model}_mapping"
            self._connect_to_db(mapping_key, model)

    def _connect_to_db(self, mapping_key, model, attrs=None):
        if attrs is None:
            attrs = ["p_mw", "q_mvar"]

        db_key = self.scenario.find_first_model("store", "database")[0]
        model_name = model
        for bus, entities in self.sim_params[mapping_key].items():
            for eidx, (name, _) in enumerate(entities):
                if model is None:
                    model_name = name

                model_key = self.scenario.generate_model_key(
                    self, model_name, bus, eidx
                )

                self.connect_entities(model_key, db_key, attrs)

    def get_grid_entity(self, mtype, bus):
        models = self.scenario.find_grid_entities(
            self.sim_params["grid_name"], mtype, endswith=f"_{bus}"
        )
        if models:
            for key in models:
                # Return first match
                return key

        self.logger.info(
            "Grid entity for %s, %s at bus %d not found",
            self.sim_params["grid_name"],
            mtype,
            bus,
        )
        raise ValueError(
            f"Grid entity for {self.sim_params['grid_name']}, {mtype} "
            f"at bus {bus} not found!"
        )

    def create_default_mapping(self):
        default_mapping = dict()

        return default_mapping
