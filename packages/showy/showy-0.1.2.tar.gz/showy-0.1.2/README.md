
# showy


``showy`` is a helper for matplotlib subplots.



## Usage


``showy`` can be used in a script-like manner. 

Let's first define the layout:

```python
layout = {
    "title": "Example",
    "graphs": [
        {
            "curves": [{"var": "sine_10"}],
            "x_var": "time",
            "y_label": "Fifi [mol/m³/s]",
            "x_label": "Time [s]",
            "title": "Sinus of frequency *"
        },
        {
            "curves": [{"var": "sine_30"}],
            "x_var": "time",
            "y_label": "Riri [Hz]",
            "x_label": "Time [s]",
            "title": "Second graph"
        },
        {
            "curves": [
                {
                    "var": "sine_100",
                    "legend": "origin",
                },
                {
                    "var": "sine_100p1",
                    "legend": "shifted",
                }
            ],
            "x_var": "time",
            "y_label": "Loulou [cow/mug]",
            "x_label": "Time [s]",
            "title": "Third graphg"
        }
    ],
    "figure_structure": [3, 1],
    "figure_dpi": 92.6
}
```

Now, let's create dummy data:

```python
import numpy as np

data = dict()
data["time"] = np.linspace(0, 0.1, num=256)

data["sine_10"] = np.cos(data["time"] * 10 * 2 * np.pi)
data["sine_30"] = np.cos(data["time"] * 30 * 2 * np.pi)
data["sine_100"] = np.cos(data["time"] * 100 * 2 * np.pi)
data["sine_100p1"] = 1. + np.cos(data["time"] * 100 * 2 * np.pi)
```

Finally, we just have to display it:

```python
from showy import showy

showy(layout, data)
```


**Tip**: Define the layout in a ``yaml`` or ``json`` file in order to it across applications.

If you define it in a ``yaml`` file, then load it with (need to install [``pyyaml``](https://pypi.org/project/PyYAML/):

```python
import yaml

with open(filename, 'r') as file:
  layout = yaml.load(file, Loader=yaml.SafeLoader)
```

If you define it in a ``json`` file, then load it with:

```python
import json

with open(filename, 'r') as file:
  layout = json.load(filename)

```



### Using wildcard `*`

A neat feature of ``showy`` is the wild card usage to simplify layout creation. For example, if you have 3 variables called ``var_1``, ``var_2``, ``var_3``, you only need to define the graph layout for a variable ``var_*``.

The example above reduces to:


```python
layout = {
    "title": "Example",
    "graphs": [{
        "curves": [{"var": "sine_*"}],
        "x_var": "time",
        "y_label": "Sine [mol/m³/s]",
        "x_label": "Time [s]",
        "title": "Sinus of frequency *"
    }],
    "figure_structure": [3, 3],
    "figure_dpi": 92.6
}
```


## json-schema standard

``showy`` is based on a json-schema standard defined [here](https://gitlab.com/cerfacs/showy/raw/master/src/showy/schema.yaml). Check [this](https://cerfacs.fr/coop/json-schema-for-sci-apps) out to learn more about the usage of the json-schema standard. (For your daily usage of ``showy`` you just need to ensure your layout respects the schema)



