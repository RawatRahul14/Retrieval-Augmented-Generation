# == Python Modules ==
import yaml
from typing import Dict
from pathlib import Path

# === Class for Handling Model Configurations ===
class ModelConfig:
    def __init__(
            self,
            yaml_path: Path = Path("config/models.yaml")
    ):
        """
        Initialize the ModelConfig class.

        Args:
            yaml_path (Path, optional): Path to the models.yaml file.
                                        Defaults to config/models.yaml.
        """

        ## === Reading the YAML File ===
        with open(yaml_path, "r") as f:
            self.config = yaml.safe_load(f)

    # === Function to Get Full Model Details by Alias ===
    def get_model(
            self,
            alias: str
    ) -> dict:
        """
        Get the full model details for a given alias.

        Args:
            alias (str): The alias of the model.

        Returns:
            dict: Model details corresponding to the alias.
        """
        return self.config["llm_models"][alias]

    # === Function to Get Model Assigned to a Specific Agent ===
    def get_agent_model(
            self,
            agent_name: str
    ) -> Dict[str, str]:
        """
        Get the model alias assigned to a specific agent.

        Args:
            agent_name (str): The name of the agent.

        Returns:
            str: The full model details mapped to the agent.
        """

        ## === Retrieving Alias for the Agent ===
        alias = self.config["agent_model_mapping"].get(agent_name)

        ## === Returning the Model Details if Found ===
        return self.get_model(alias) if alias else None