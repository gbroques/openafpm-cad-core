"""
FreeCAD macro to print furl tranforms using default values.
"""
import json
from collections import OrderedDict
from multiprocessing import Pool
from typing import Union

from openafpm_cad_core.app import (WindTurbine, get_default_parameters,
                                   load_furl_transform)


def get_furl_transform(turbine: WindTurbine) -> dict:
    parameters = get_default_parameters(turbine)

    return load_furl_transform(
        parameters['magnafpm'],
        parameters['user'],
        parameters['furling'])


class CompactJSONEncoder(json.JSONEncoder):
    """
    A JSON Encoder that puts small containers on single lines.

    See:
        https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
    """

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 70
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 3
    """Maximum number of items in container that might be put on single line."""

    INDENTATION_CHAR = " "

    def __init__(self, *args, **kwargs):
        # using this class without indentation is pointless
        if kwargs.get("indent") is None:
            kwargs.update({"indent": 4})
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            if self._put_on_single_line(o):
                return "[" + ", ".join(self.encode(el) for el in o) + "]"
            else:
                self.indentation_level += 1
                output = [self.indent_str + self.encode(el) for el in o]
                self.indentation_level -= 1
                return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"
        elif isinstance(o, dict):
            if o:
                if self._put_on_single_line(o):
                    return "{ " + ", ".join(f"{self.encode(k)}: {self.encode(el)}" for k, el in o.items()) + " }"
                else:
                    self.indentation_level += 1
                    output = [
                        self.indent_str + f"{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()]
                    self.indentation_level -= 1
                    return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"
            else:
                return "{}"
        elif isinstance(o, float):  # Use scientific notation for floats, where appropiate
            return format(o, "g")
        elif isinstance(o, str):  # escape newlines
            o = o.replace("\n", "\\n")
            return f'"{o}"'
        else:
            return json.dumps(o)

    def iterencode(self, o, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(o)

    def _put_on_single_line(self, o):
        return self._primitives_only(o) and len(o) <= self.MAX_ITEMS and len(str(o)) - 2 <= self.MAX_WIDTH

    def _primitives_only(self, o: Union[list, tuple, dict]):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())

    @property
    def indent_str(self) -> str:
        return self.INDENTATION_CHAR*(self.indentation_level*self.indent)


def slugify_enum(enum: WindTurbine) -> str:
    return enum.value.lower().replace(' ', '-')


if __name__ == '__main__':
    turbines = [
        WindTurbine.T_SHAPE,
        WindTurbine.H_SHAPE,
        WindTurbine.STAR_SHAPE,
        WindTurbine.T_SHAPE_2F]
    with Pool(len(turbines)) as p:
        results = p.map(get_furl_transform, turbines)
        furl_transforms = OrderedDict()
        for result, turbine in zip(results, turbines):
            key = slugify_enum(turbine)
            furl_transforms[key] = result
        print(json.dumps(furl_transforms, cls=CompactJSONEncoder, indent=2))
