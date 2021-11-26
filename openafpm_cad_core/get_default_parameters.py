"""Module for retrieving default values for wind turbine variants."""
import json
from pathlib import Path
from typing import TypedDict

from .parameter_groups import (FurlingParameters, MagnafpmParameters,
                               UserParameters)
from .wind_turbine import WindTurbine

__all__ = ['get_default_parameters', 'Parameters']


class Parameters(TypedDict):
    """Dictionary containing magnafpm, furling, and user parameters."""
    magnafpm: MagnafpmParameters
    furling: FurlingParameters
    user: UserParameters


def get_default_parameters(variant: WindTurbine) -> Parameters:
    """Get default parameter values for "T Shape", "H Shape", or "Star Shape" turbines.

    .. literalinclude:: ../../openafpm_cad_core/default_parameters.json
       :language: JSON
    """
    dir_path = Path(__file__).parent.resolve()
    parameters_path = dir_path.joinpath('default_parameters.json')

    with open(parameters_path) as f:
        parameters_by_variant = json.load(f)
    return parameters_by_variant[variant.value]
