"""
FreeCAD macro to get dimensions for wind turbines using default values.

To filter output by table name, you can use jq.

For example:
jq '.[] | select(.children[0].children[0].children[0].properties.textContent | ascii_downcase | contains("frame dimensions"))'
"""

import json

from openafpm_cad_core.app import (
    WindTurbineShape,
    exec_turbine_function,
    get_default_parameters,
    load_dimension_tables,
)


def print_dimension_tables(turbine_shape: WindTurbineShape) -> str:
    parameters = get_default_parameters(turbine_shape)

    return json.dumps(
        load_dimension_tables(
            parameters["magnafpm"], parameters["furling"], parameters["user"]
        ),
        indent=2,
    )


if __name__ == "__main__":
    exec_turbine_function(
        "Get dimensions for wind turbine(s) using default values.",
        print_dimension_tables,
    )
