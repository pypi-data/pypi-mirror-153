from functools import partial
import random
from typing import List, Union, Optional

from .utils import bpm_to_time


def _random_chance(prob):
    return random.randint(1, 100) <= prob


def _oddeven(notes, even_first=False, **kwargs):
    odd = []
    even = []
    for i, n in enumerate(notes, start=1):
        if i % 2:
            even.append(n)
        else:
            odd.append(n)
    if even_first:
        return even + odd
    return odd + even


def oddeven(notes: List[int], **kwargs) -> List[int]:
    """
    odd indexed notes followed by even indexed notes
    """
    return _oddeven(notes)


def evenodd(notes: List[int], **kwargs) -> List[int]:
    """
    even indexed notes followed by odd indexed notes
    """
    return _oddeven(notes, even_first=True)


def _shift_n(notes: List[int], n: int = 1, **kwargs) -> List[int]:
    """
    switch the last n notes with the first n notes
    """
    n = min(n, len(notes))
    return notes[n:] + notes[:n]


def thumb_up(notes: List[int], **kwargs) -> List[int]:
    """
    alternate between the lowest note and an ascending scale
    """
    sorted_notes = list(sorted(notes))
    ordered_notes = []
    for note in sorted_notes[1:]:
        ordered_notes.extend([sorted_notes[0], note])
    return ordered_notes


def thumb_down(notes: List[int], **kwargs) -> List[int]:
    """
    alternate between the lowest note and a descending scale
    """
    sorted_notes = list(reversed(sorted(notes)))
    ordered_notes = []
    for note in sorted_notes[:-1]:
        ordered_notes.extend([sorted_notes[-1], note])
    return ordered_notes


def thumb_updown(notes: List[int], **kwargs) -> List[int]:
    """
    thumb up then down, without repeating highest and lowest notes.
    """
    return thumb_up(notes, **kwargs) + thumb_down(notes, **kwargs)[2:-2]


def thumb_downup(notes: List[int], **kwargs) -> List[int]:
    """
    thumb down then up, without repeating lowest and highest notes
    """
    return thumb_down(notes, **kwargs) + thumb_up(notes, **kwargs)[2:-2]


def pinky_up(notes: List[int], **kwargs) -> List[int]:
    """
    alternate between the highest note and an ascending scale
    """
    sorted_notes = list(sorted(notes))
    ordered_notes = []
    for note in sorted_notes[:-1]:
        ordered_notes.extend([sorted_notes[-1], note])
    return ordered_notes


def pinky_down(notes: List[int], **kwargs) -> List[int]:
    """
    alternate between the highest note and a descending scale
    """
    sorted_notes = list(reversed(sorted(notes)))
    ordered_notes = []
    for note in sorted_notes[1:]:
        ordered_notes.extend([sorted_notes[-1], note])
    return ordered_notes


def pinky_updown(notes: List[int], **kwargs) -> List[int]:
    """
    pinky up then down, without repeating highest and lowest notes.
    """
    return pinky_up(notes, **kwargs) + pinky_down(notes, **kwargs)[2:-2]


def pinky_downup(notes: List[int], **kwargs) -> List[int]:
    """
    pinky down then up, without repeating lowest and highest notes
    """
    return pinky_down(notes, **kwargs) + pinky_up(notes, **kwargs)[2:-2]


def _random(notes: List[int], **kwargs) -> List[int]:
    """
    randomly shuffle notes
    """
    random.shuffle(notes)
    return notes


def random_octaves(
    notes: List[int], octaves: List[int], prob_octave: int = 25, **kwargs
) -> List[int]:
    """
    randomly apply octaves to a sequence
    """
    new_notes = []
    for note in notes:
        if _random_chance(prob_octave):
            octave = random.choice(octaves)
            note += octave * 12
        new_notes.append(note)
    return new_notes


def random_silence(notes, prob_silence: int = 33, **kwargs) -> List[int]:
    """
    randomly remove notes from a sequence
    """
    new_notes = []
    for note in notes:
        if _random_chance(prob_silence):
            note = 0
        new_notes.append(note)
    return new_notes


def three_two(notes, **kwargs) -> List[int]:
    """
    3 notes then 2 of silence
    """
    breaks = range(0, len(notes), 5)
    for b in breaks[1:]:
        notes[b - 2 : b] = [0, 0]
    return notes


def two_three(notes, **kwargs) -> List[int]:
    """
    2 notes then 3 of silence
    """
    breaks = range(0, len(notes), 5)
    for b in breaks[1:]:
        notes[b - 3 : b] = [0, 0, 0]
    return notes


def even_off(notes, prob_even_off: int = 33, **kwargs) -> List[int]:
    """
    turn even notes randomly off
    """
    new_notes = []
    for i, note in enumerate(notes, 1):
        if i % 2 == 0 and _random_chance(prob_even_off):
            note = 0
        new_notes.append(note)
    return new_notes


def odd_off(notes, prob_odd_off: int = 29, **kwargs) -> List[int]:
    """
    turn odd notes randomly off
    """
    new_notes = []
    for i, note in enumerate(notes, 1):
        if i % 2 != 0 and _random_chance(prob_odd_off):
            note = 0
        new_notes.append(note)
    return new_notes


STYLES = {
    "down": lambda x: reversed(sorted(x)),
    "up": lambda x: sorted(x),
    "downup": lambda x: list(reversed(sorted(x))) + list(sorted(x))[1:-1],
    "updown": lambda x: list(sorted(x)) + list(reversed(sorted(x)))[1:-1],
    "oddeven": oddeven,
    "evenodd": evenodd,
    "shift_1": partial(_shift_n, n=1),
    "shift_2": partial(_shift_n, n=2),
    "shift_3": partial(_shift_n, n=3),
    "shift_4": partial(_shift_n, n=4),
    "shift_5": partial(_shift_n, n=5),
    "shift_6": partial(_shift_n, n=6),
    "shift_7": partial(_shift_n, n=7),
    "shift_8": partial(_shift_n, n=8),
    "thumb_up": thumb_up,
    "thumb_down": thumb_down,
    "thumb_updown": thumb_updown,
    "thumb_updown": thumb_downup,
    "pinky_up": pinky_up,
    "pinky_down": pinky_down,
    "pinky_updown": pinky_updown,
    "pinky_downup": pinky_downup,
    "random": _random,
    "random_octaves": random_octaves,
    "random_silence": random_silence,
    "three_two": three_two,
    "two_three": two_three,
    "odd_off": odd_off,
    "even_off": even_off,
}


def apply_style(notes: List[int], style: str = "down", **kwargs) -> List[int]:
    return STYLES.get(style)(notes, **kwargs)


def apply_styles(notes: List[int], styles: List[str], **kwargs):
    # apply multiple styles, in order
    for style in styles:
        notes = apply_style(notes, style, **kwargs)
    return notes


def midi_arp(
    chord_notes: List[int],  # list of notes to arpeggiate
    bpm: float = 120.0,  # bpm
    count: Union[float, int, str] = "1/16",
    time_sig: str = "4/4",  # time signature
    octaves: List[int] = [0],  # a list of octaves to add to the chord (eg: [-1, 2])
    loops: int = 4,  # The number of times to loop the pattern
    styles: List[str] = ["down"],  # TODO: implement different styles
    retrigger: Optional[int] = None,  # number of notes after which to restart pattern.
    # if None, the pattern will loop over and over again
    **kwargs
):
    """
    Given a list of chord notes, a style name (eg: up, down), and a note count, generate an arpeggiated sequence of notes.
    """
    # create list of notes including octaves
    chord_notes = list(
        set(chord_notes + [o * 12 + n for o in octaves for n in chord_notes])
    )
    note_duration = bpm_to_time(bpm, count, time_sig)
    velocity = 100
    total_duration = 0
    n_loops = 0
    n_steps = 0
    while True:
        # apply the style /  order

        for note in apply_styles(chord_notes, styles, **kwargs):
            n_steps += 1
            total_duration += note_duration
            yield {
                "note": note,
                "type": "note" if note != 0 else "silence",
                "duration": note_duration,  # TODO: shorter notes?
                "velocity": velocity,
            }

        n_loops += 1
        if n_loops >= loops:
            break
