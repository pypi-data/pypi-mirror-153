# Physical Quantity library for Python

A simple library for working with physical quantities. 
Implements basic dimensional decomposition of physical quantities and provides
basic operations (addition, subtraction, multiplication, division, comparison) 
for working with these quantities.

Support for non-SI units is available but most operations will result in 
implicit conversions to SI units. Use the *as_absolute*() or *as_relative*()
methods to convert back to the desired non-SI units.

Note that while this library supports a wide range of the dimentional analysis
and related integrity artifacts of working with physical quantities, the prime 
goal of this library isn't the dimentional integrity of code, but instead the
unified serialization or rather serializisability of physical quantities.

## install

```
pip install physicalquantity
```


## constructor

The PhysicalQuantity (in normal use) takes up to two arguments. The first argument (defaulting to zero) is a numeric value for the physical quantity, the second argument (defaulting to "one") is the name of the units or physical phenonemon the physical quantity refers to. This name can be prefixed with any of the metric prefixes from yotta down to yocto.

We distinguish between:

* si units
* no-name units
* transposed units
* aliasses
* prefixes

The following SI units (with aliasses) are currently defined.
* one
  * number
  * dimentionless
  * radians
  * steradian
* metre
  * meter
  * meters
  * length
  * m
* kg
  * weight
* second
  * seconds
  * sec
  * time
* ampere
  * current
  * amp
* kelvin
  * temperature
* mole
* candela
  * intencity
  * lumen
  * illuminance
* hertz
  * frequency
  * becquerel
  * hz
* newton
  * force
* pascal
  * stress
  * pressure
  * pa
* joule
  * energy
  * work
  * heat
* watt
  * power
* coulomb
  * charge
* volt
  * potential
* ohm
  * resistance
* siemens
* farad
  * capacitance
* tesla
  * fluxdensity
* weber
  * flux
* henry
  * inductance
* lux
  * illuminance
* grey
  * absorbedradiation
  * sievert
* m2
  * squaremetre
* m3
  * cubicmetre

```python
from physicalquantity import PhysicalQuantity as PQ

force1 = PQ(40, "newton")
```

Next to these SI units we have a set of nameless units for what quantities are constructed using the name of the physical phenonemon.

* velocity
* acceleration
* wavenumber
* density
* surfacedensity
* specificvolume
* currentdensity
* magneticfieldstrength
* concentration
* massconcentration
* luminance

```python
from physicalquantity import PhysicalQuantity as PQ

acc1 = PQ(9.8, "acceleration") 
```

An other set of units are the transposed and/or scaled units. Note that when quantoties of these units are used with operators, the result will get normalized to their coresponding SI units.

* degrees
* foot
  * feet
  * ft
* inch
* mile
* yard
* au
  * astronomicalunit
* lightyear
* parsec
* gram
  * g
* pound
  * pounds
  * lbs
  * lb
* ounce
  * oz
* stone
  * stones
  * st
* minute
  * minutes
  * min
* hour
  * hr
* day
  * dy
* year
  * yr
* celcius
* fahrenheit
* are
* hectare
* acre
* barn
* litre
  * liter
* barrel
* gallon
* pint

```python
from physicalquantity import PhysicalQuantity as PQ

vol1 = PQ(22, "litre")   
```

Each of the units and their aliases may be prefixed with one of the metric prefixes

* yotta
* zetta
* exa
* peta
* tera
* giga
* mega
* kilo
* hecto
* deca
* deci
* centi
* milli
* micro
* nano
* pico
* femto
* atto
* zepto
* yocto

```python
from physicalquantity import PhysicalQuantity as PQ

res1 = PQ(2.4, "megaohm")   
```

# normalized

While many operations will return an SI normalized result, it is possible to do so explicitly

```
from physicalquantity import PhysicalQuantity as PQ

temperature = PQ(79, "fahrenheit").normalized()  # normalize to Kelvin
```

# as\_absolute / as\_relative

The reverse of normalization comes in two variants. An absolute and a relative variant. 

```python
from physicalquantity import PhysicalQuantity as PQ

temperature = (PQ(76,"fahrenheit") + PQ(19,"celcius") / PQ(2, "one")).as_absolute("fahrenheit")
``` 

```python
from physicalquantity import PhysicalQuantity as PQ

temperature = (PQ(76,"fahrenheit") - PQ(19,"celcius")).as_relative("fahrenheit")
```

For quantities without an implied offset the two operations are equivalent.

```python
from physicalquantity import PhysicalQuantity as PQ

distance = PQ(1,"attoparsec").as_absolute("centiinch").as_dict()

```

# dimensions check

Often you will want to check if a wuantity has the expected dimensions

```python
assert temperature.same_dimensions("temperature")
```

# operators

The following operators are supported:

* \* : multiplication
* \/ : division
* \+ : addition
* \- : subtraction
* \*\* : power 

Impossible operations will throw an RuntimeError, If the operation succeed, the result will always have a normalized value.
It is important to note that not all resulting values will have a *unit_name* value. The *dimensions* value of the PhysicalQuantity though
will always uniquely identify the units used.

```python
voltage1 = PQ(20,"milliampere") * PQ(15,"kiloohm")

voltage2 = PQ(100, "watt") / PQ(6, "ampere")

voltage3 = voltage1 - voltage2

voltage4 = (voltage1 + voltage2) / PQ(2)

volume = PQ(0.15, "metre") ** PQ(3)
```

# comparison

All the comparison operators work on PhysicalQuantity objects

```python
if voltage2 > voltage1:
    ...
```

# serialization

While PhysicalQuantity has a *json* method for serializing a single PhysicalQuantity as JSON, the expected usage would be the use of a serializable PhysicalQuantity structure as part of a larger structure.


A sample of serialization:
```python
import json
from physicalquantity import PhysicalQuantity as PQ

collection = {}
collections["temperature"] = PQ(94, "fahrenheit").normalized().as_dict()
collections["distance"] = PQ(1,"attoparsec").normalized().as_dict()
collections["timestamp"] = PQ(datetime.datetime.now().timestamp(), "sec").as_dict(use_iso8601=True)
serialized = json.dumps(collection)
```

And deserialization:

```python
import json
from physicalquantity import PhysicalQuantity as PQ
from physicalquantity import from_dict as pq_from_dict

collection = json.loads(serialized)
temperature = pq_from_dict(collection["temperature"])
```

A serialized version of a PhysicalQuantity can look something like this for values that map to units:

```json
{
  "value": 0.03085677581279959,
  "unit": "metre"
}
```

Or if there is no unit name to map to, a more verbose representation, here for acceleration:

```json
{
  "value": 17.0,
  "unit": {
    "dimensions": {
      "length": 1, 
      "time": -2
    }
  }
}
```

Note that even a PhysicalQuantity that doesn't make any sense that is a result of operations with PhysicalQuantity units is still serializable:

```json
{
  "value": 8.0,
  "unit": {
    "dimensions": {
      "length": 3,
      "mass": 1,
      "time": -5,
      "current": -1,
      "substance": -1
    }
  }
}
```
