# == Python Modules ==
import yaml
from pathlib import Path
from typing import Dict

# === Function to Retrieve the Prompts ===
def load_prompt(
        name: str,
        path: Path = Path("config/prompts.yaml")
) -> str:
    """
    Loads a specific prompt definition from the YAML registry.

    Args:
        name (str): The key of the prompt inside the registry.
        path (Path, optional): Path to the prompts.yaml file.

    Returns:
        str: The prompt definition corresponding to the provided name.
    """

    ## === Calling the Whole YAML Registry ===
    data = yaml.safe_load(
        path.read_text(encoding = "utf-8")
    )

    ## === Returning a Specific Prompt ===
    return data["Prompts"][name]

# === Function to Render a Prompt with Variables ===
def render_prompt(
        prompt_name: str,
        path: Path = Path("config/prompts.yaml"),
        **kwargs
) -> Dict[str, str]:
    """
    Retrieves and renders a specific prompt by filling in variables.

    Args:
        prompt_name (str): Name of the prompt to load.
        path (Path, optional): Path to the prompts.yaml file.
        **kwargs: Variable substitutions for the prompt template.

    Returns:
        Dict[str, str]: Dictionary containing system message,
                        user message, output schema, and few_shots.
    """

    ## === Loading the Full Prompt Definition ===
    prompt_def = load_prompt(
        name = prompt_name,
        path = path
    )

    ## === Extracting the Template String ===
    template = prompt_def["template"]

    ## === Collecting Variables Needed by the Template ===
    var_values = {
        k: v for k, v in kwargs.items()
    }

    ## === Filling the Variables into the Template ===
    filled_prompt = template.format(
        **var_values
    )

    ## === Returning the Rendered Prompt Package ===
    return {
        "system": prompt_def["system"],
        "user": filled_prompt,
        "output_schema": prompt_def["output_schema"]
    }