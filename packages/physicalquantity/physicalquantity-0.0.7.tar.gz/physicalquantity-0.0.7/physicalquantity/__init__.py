#!/usr/bin/python3
"""Simple library for working with physical quantities"""
import json
from datetime import datetime
from dateutil import parser
import pytz

ISO_UNITS = {
  "one":       {},
  "metre":     {"dimensions": {"length": 1}},
  "kg":        {"dimensions": {"mass": 1}},
  "second":    {"dimensions": {"time": 1}},
  "ampere":    {"dimensions": {"current": 1}},
  "kelvin":    {"dimensions": {"temperature": 1}},
  "mole":      {"dimensions": {"substance": 1}},
  "candela":   {"dimensions": {"intensity": 1}},
  "hertz":     {"dimensions": {"time": -1}},
  "newton":    {"dimensions": {"length": 1, "mass": 1, "time": -2}},
  "pascal":    {"dimensions": {"length": -1, "mass": 1, "time": -2}},
  "joule":     {"dimensions": {"length": 2, "mass": 1, "time": -2}},
  "watt":      {"dimensions": {"length": 2, "mass": 1, "time": -3}},
  "coulomb":   {"dimensions": {"current": 1, "time": 1}},
  "volt":      {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -1}},
  "ohm":       {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -2}},
  "siemens":   {"dimensions": {"length": -2, "mass": -1, "time": 3, "current": 2}},
  "farad":     {"dimensions": {"length": -2, "mass": -1, "time": 4, "current": 2}},
  "tesla":     {"dimensions": {"mass": 1, "time": -2, "current": -1}},
  "weber":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -1}},
  "henry":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -2}},
  "lux":       {"dimensions": {"intensity": 1, "length": -2}},
  "grey":      {"dimensions": {"length": 2, "time": -2}},
  "m2":        {"dimensions": {"length": 2}},
  "m3":        {"dimensions": {"length": 3}},
}

NONAME_UNITS = {
  "velocity":       {"dimensions": {"length": 1, "time": -1}},
  "acceleration":   {"dimensions": {"length": 1, "time": -2}},
  "wavenumber":     {"dimensions": {"length": -1}},
  "density":        {"dimensions": {"mass": 1, "length": -3}},
  "surfacedensity": {"dimensions": {"mass": 1, "length": -2}},
  "specificvolume": {"dimensions": {"mass": -1, "length": 3}},
  "currentdensity": {"dimensions": {"current": 1, "length": -2}},
  "magneticfieldstrength": {"dimensions": {"current": 1, "length": -1}},
  "concentration":  {"dimensions": {"substance": 1, "length": -3}},
  "massconcentration": {"dimensions": {"mass": 1, "length": -3}},
  "luminance": {"dimensions": {"intensity": 1, "length": -2}},
}

TRANSPOSED_UNITS = {
  "degrees":   {"scale": 0.017453292},
  "coordinate": {"scale": 0.017453292},
  "foot":      {"dimensions": {"length": 1}, "scale": 0.3048},
  "inch":      {"dimensions": {"length": 1}, "scale": 0.0254},
  "mile":      {"dimensions": {"length": 1}, "scale": 1609.344},
  "yard":      {"dimensions": {"length": 1}, "scale": 0.9144},
  "au":        {"dimensions": {"length": 1}, "scale": 149597870700},
  "lightyear": {"dimensions": {"length": 1}, "scale": 9460730472580000},
  "parsec":    {"dimensions": {"length": 1}, "scale": 30856775812799588},
  "gram":      {"dimensions": {"mass": 1}, "scale": 0.001},
  "pound":     {"dimensions": {"mass": 1}, "scale": 0.45359},
  "ounce":     {"dimensions": {"mass": 1}, "scale": 0.02835},
  "stone":     {"dimensions": {"mass": 1}, "scale": 6.3502934},
  "minute":    {"dimensions": {"time": 1}, "scale": 60},
  "hour":      {"dimensions": {"time": 1}, "scale": 3600},
  "day":       {"dimensions": {"time": 1}, "scale": 86400},
  "year":      {"dimensions": {"time": 1}, "scale": 31557600},
  "celcius":   {"dimensions": {"temperature": 1}, "offset": 273.15},
  "fahrenheit":{"dimensions": {"temperature": 1}, "offset": 255.3722, "scale": 0.5555555556},
  "are":       {"dimensions": {"length": 2}, "scale": 100},
  "hectare":   {"dimensions": {"length": 2}, "scale": 10000},
  "acre":      {"dimensions": {"length": 2}, "scale": 4046.86},
  "barn":      {"dimensions": {"length": 2}, "scale": 0.0000000000000000000000000001},
  "litre":     {"dimensions": {"length": 3}, "scale": 0.001},
  "barrel":    {"dimensions": {"length": 3}, "scale": 0.158987294928},
  "gallon":    {"dimensions": {"length": 3}, "scale": 0.003785411784},
  "pint":      {"dimensions": {"length": 3}, "scale": 0.000473176473},
  "radianpersecond": {"dimensions": {}, "scale": 3.14159265358979323846}
}

UNIT_ALIAS = {
    "one": [
        "number",
        "radians",
        "one-radian",
        "dimentionless",
        "steradian",
        "watt-db",
        "one-db",
        "one-undef",
        "one-percentage",
        "one-ppb"
    ],
    "metre": ["meter", "meters","metres", "length", "m"],
    "foot": ["feet","ft"],
    "candela": ["intencity", "lumen", "illuminance"],
    "au": ["astronomicalunit"],
    "gram": ["g"],
    "kg": ["weight"],
    "pound": ["lbs", "lb", "pounds"],
    "ounce": ["oz"],
    "second": ["time", "seconds", "sec"],
    "minute": ["minutes","min"],
    "hour": ["hr"],
    "day": ["dy"],
    "year": ["yr"],
    "ampere": ["current", "amp"],
    "kelvin": ["temperature"],
    "hertz": ["frequency","becquerel", "hz"],
    "newton": ["force"],
    "pascal": ["stress", "pressure", "pa"],
    "joule": ["energy", "work", "heat"],
    "watt": ["power"],
    "coulomb": ["charge"],
    "volt": ["potential"],
    "ohm": ["resistance"],
    "farad": ["capacitance"],
    "tesla": ["fluxdensity"],
    "weber": ["flux"],
    "henry": ["inductance"],
    "lux": ["illuminance"],
    "grey": ["absorbedradiation", "sievert"],
    "m2": ["squaremetre"],
    "m3": ["cubicmetre"],
    "litre": ["liter"],
    "stone": ["stones","st"]
}

ISO_PREFIX = {
  "yotta": 1000000000000000000000000,
  "zetta": 1000000000000000000000,
  "exa":   1000000000000000000,
  "peta":  1000000000000000,
  "tera":  1000000000000,
  "giga":  1000000000,
  "mega":  1000000,
  "kilo":  1000,
  "hecto": 100,
  "deca":  10,
  "deci":  0.1,
  "centi": 0.01,
  "milli": 0.001,
  "micro": 0.000001,
  "nano":  0.000000001,
  "pico":  0.000000000001,
  "femto": 0.000000000000001,
  "atto":  0.000000000000000001,
  "zepto": 0.000000000000000000001,
  "yocto": 0.000000000000000000000001
}

def _name_to_unit(name):
    # pylint: disable = too-many-statements, too-many-branches, too-many-locals
    offset = 0.0
    scale = 1.0
    rescale = 1.0
    unit_name = name
    full_prefix = ""
    fullname = name
    for prefix,mscale in ISO_PREFIX.items():
        if name.startswith(prefix):
            name = name[len(prefix):]
            rescale *= mscale
            full_prefix += prefix
    if name in ISO_UNITS:
        unit = ISO_UNITS[name].copy()
        unit_name = fullname
    elif name in TRANSPOSED_UNITS:
        unit = TRANSPOSED_UNITS[name].copy()
        unit_name = fullname
    else:
        unit = None
        for key, value in UNIT_ALIAS.items():
            if name in value:
                if key in ISO_UNITS:
                    unit = ISO_UNITS[key].copy()
                    unit_name = full_prefix + key
                elif key in TRANSPOSED_UNITS:
                    unit = TRANSPOSED_UNITS[name].copy()
                    unit_name = full_prefix + key
                else:
                    raise RuntimeError("Invalid unit name for physical quantity")
    if unit is None:
        if fullname in NONAME_UNITS:
            unit = NONAME_UNITS[fullname]
            unit_name = None
        else:
            raise RuntimeError("Invalid unit name for physical quantity")
    if "scale" in unit:
        scale = unit["scale"] * rescale
    else:
        scale = rescale
    if "offset" in unit:
        offset = unit["offset"]
    dimensions = []
    dims = {}
    if "dimensions" in unit:
        dims = unit["dimensions"]
    for dimension in ["length",
                      "mass",
                      "time",
                      "current",
                      "temperature",
                      "substance",
                      "intensity"]:
        if dimension in dims:
            dimensions.append(dims[dimension])
        else:
            dimensions.append(0)
    unit["dim_array"] = dimensions
    unit["unit_name"] = unit_name
    unit["offset"] = offset
    unit["scale"] = scale
    return unit

def _find_si_name(dimarr):
    for key, val in ISO_UNITS.items():
        dimension_array = []
        dimensions = val.get("dimensions",{})
        for dimension in ["length",
                          "mass",
                          "time",
                          "current",
                          "temperature",
                          "substance",
                          "intensity"]:
            if dimension in dimensions:
                dimension_array.append(dimensions[dimension])
            else:
                dimension_array.append(0)
        if dimarr == dimension_array:
            return key
    return None

class PhysicalQuantity:
    """Single class for representing any type of physical unit"""
    def __init__(
            self,
            value=0.0,
            name="one",
            dimensions=None,
            scale=1.0,
            offset=0.0):
        """Constructor"""
        # pylint: disable=too-many-arguments
        self.value = value
        if name == "time" and isinstance(value, str):
            self.value = parser.parse(value).timestamp()
        elif not isinstance(value, (int, float)):
            raise RuntimeError("value should be a number")
        if name is None and dimensions is not None:
            self.dimensions = dimensions
            self.unit_name = None
            self.scale = scale
            self.offset = offset
            return
        unit = _name_to_unit(name)
        self.unit_name = unit["unit_name"]
        self.scale = unit["scale"]
        self.offset = unit["offset"]
        self.dimensions = unit["dim_array"]

    def normalized(self):
        """Normalize to ISO units"""
        si_name = _find_si_name(self.dimensions)
        if si_name is None:
            return PhysicalQuantity(self.value * self.scale + self.offset, None, self.dimensions)
        return PhysicalQuantity(self.value * self.scale + self.offset, si_name)

    def __mul__(self, other):
        """Multiplication"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only multiply with PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        result_dimensions = [x + y for (x, y) in zip(selfn.dimensions, othern.dimensions)]
        result_value = selfn.value * othern.value
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rmul__(self, other):
        """Something multiplied by self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in subtraction")
        return self * other

    def __truediv__(self, other):
        """Division"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only divide by PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        result_dimensions = [x - y for (x, y) in zip(selfn.dimensions, othern.dimensions)]
        result_value = selfn.value / othern.value
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rtruediv__(self, other):
        """Something divided by self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in division")
        return PhysicalQuantity(other) / self

    def __add__(self, other):
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only add a PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if selfn.dimensions != othern.dimensions:
            raise RuntimeError("Can't add up physical quantities with non-matching units")
        if selfn.unit_name is None:
            return PhysicalQuantity(selfn.value + othern.value, None, selfn.dimensions)
        return PhysicalQuantity(selfn.value + othern.value, selfn.unit_name)

    def __radd__(self, other):
        """Something plus self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in addition")
        return self + other

    def __sub__(self, other):
        """Subtract"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only subtract a PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if selfn.dimensions != othern.dimensions:
            raise RuntimeError("Can't add up physical quantities with non-matching units")
        if selfn.unit_name is None:
            return PhysicalQuantity(selfn.value - othern.value, None, selfn.dimensions)
        return PhysicalQuantity(selfn.value - othern.value, selfn.unit_name)

    def __rsub__(self, other):
        """Something minus self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in subtraction")
        return PhysicalQuantity(other) - self

    def __pow__(self, other):
        """To the power"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only exponentialize with PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if othern.dimensions != [0,0,0,0,0,0,0]:
            raise RuntimeError("Can only raise to a dimensionless power")
        result_dimensions = [x * othern.value for x in selfn.dimensions]
        result_value = selfn.value ** othern.value
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rpow__(self, other):
        """Something to the power of self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in exponentiation")
        return PhysicalQuantity(other) ** self

    def __eq__(self, other):
        """Equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value == othern.value and selfn.dimensions == othern.dimensions

    def __ne__(self, other):
        """Not Equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value != othern.value or selfn.dimensions != othern.dimensions

    def __lt__(self, other):
        """Less than"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value < othern.value and selfn.dimensions == othern.dimensions

    def __gt__(self, other):
        """Greater than"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value > othern.value and selfn.dimensions == othern.dimensions

    def __le__(self, other):
        """Less or equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value <= othern.value and selfn.dimensions == othern.dimensions

    def __ge__(self, other):
        """Greater or equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value >= othern.value and selfn.dimensions == othern.dimensions

    def as_absolute(self, name):
        """Cast to a value of a named unit,respecting offsets as to get an absolute value"""
        unit = _name_to_unit(name)
        if self.dimensions != unit["dim_array"]:
            raise RuntimeError("Unit mismatch for absolute cast")
        nself = self.normalized()
        return PhysicalQuantity((nself.value - unit["offset"]) / unit["scale"], name)

    def as_relative(self, name):
        """Cast to a value of a named unit, discarding offsets as to get a relative value"""
        unit = _name_to_unit(name)
        if self.dimensions != unit["dim_array"]:
            raise RuntimeError("Unit mismatch for absolute cast")
        nself = self.normalized()
        return PhysicalQuantity(nself.value / unit["scale"], name)

    def as_iso8601(self):
        """Get as iso8601 datetime string"""
        if not self.same_dimensions("time"):
            raise RuntimeError(
                "Only physical quanties with time dimensions can be fetched as iso8601"
            )
        tzone = pytz.timezone('UTC')
        return datetime.fromtimestamp(self.normalized().value, tzone).isoformat()

    def same_dimensions(self, name):
        """Check if a PhysicalQuantity has the same dimensions as a named unit"""
        unit = _name_to_unit(name)
        return self.dimensions == unit["dim_array"]

    def as_dict(self, use_iso8601=False):
        """Serializable dict of PhysicalQuantity"""
        result = {}
        result["value"] = self.value
        if self.unit_name is None:
            result["unit"] = {}
            result["unit"]["dimensions"] = {}
            for idx, name in enumerate(["length",
                                        "mass",
                                        "time",
                                        "current",
                                        "temperature",
                                        "substance",
                                        "intensity"]):
                if self.dimensions[idx] != 0:
                    result["unit"]["dimensions"][name]= self.dimensions[idx]
            if self.scale != 1.0:
                result["unit"]["scale"] = self.scale
            if self.offset != 0.0:
                result["unit"]["offset"] = self.offset
        else:
            result["unit"] = self.unit_name
            if use_iso8601 and result["unit"] in ["second", "time", "seconds", "sec"]:
                result["unit"] = "time"
                result["value"] = self.as_iso8601()
        return result

    def json(self, use_iso8601=False):
        """JSON serialzation of PhysicalQuantity"""
        return json.dumps(self.as_dict(use_iso8601), indent=4, sort_keys=True)

def from_dict(quantity_dict):
    """Re-create a PhysicalQuantity from a serializable dict"""
    if "value" not in quantity_dict:
        raise RuntimeError("No value key in dict")
    if "unit" not in quantity_dict:
        raise RuntimeError("No unit key in dict")
    if isinstance(quantity_dict["unit"],str):
        return PhysicalQuantity(quantity_dict["value"], quantity_dict["unit"])
    unit_dict = quantity_dict["unit"]
    offset = 0.0
    if "offset" in unit_dict:
        offset = unit_dict["offset"]
    scale = 1.0
    if "scale" in unit_dict:
        offset = unit_dict["scale"]
    dimension_array = []
    if "dimensions" in unit_dict:
        dimensions = unit_dict["dimensions"]
    else:
        raise RuntimeError("No dimensions in in dict")
    for dimension in ["length",
                      "mass",
                      "time",
                      "current",
                      "temperature",
                      "substance",
                      "intensity"]:
        if dimension in dimensions:
            dimension_array.append(dimensions[dimension])
        else:
            dimension_array.append(0)
    return PhysicalQuantity(quantity_dict["value"], None, dimension_array, scale, offset)
