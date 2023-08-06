# midi-utils 

`midi-utils` is a lightweight, pure-python utility for generating scales of midi notes.

## installation 

You can install `midi-utils` from PyPI:

```
pip install midi-utils
```

## usage

`midi-utils` includes a couple of useful function called `midi_scale` for generating lists of midi notes in particular scales (you can see a full list of provided scales in [`midi_utils.constants`](midi_utils/constants.py))

```python
from midi_utils import midi_scale

midi_scale('C', 'MAJOR', 'C3', 'E5')
# >>> [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86, 88]
```

It also provides a function for mapping arbitrary values to a midi scale. This is useful for generating data sonifications. For instance, you could map an RGB value (which can range from 0-255) to a midi note in a particular scale:

```python
from midi_utils import midi_scale, map_to_midi_scale

c_min_scale = midi_scale('C', 'MINOR', 'C3', 'Eb5')
map_to_midi_scale(155, c_min_scale, 0, 255)
# >>> 77
```

## tests

A simple test suite is provided which you can run via `pytest`:

```
git clone git@gitlab.com:gltd/midi-utils.git
cd midi-utils
pip install -e . 
pytest
```
