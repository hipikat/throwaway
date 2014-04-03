
import argparse
from functools import partial
import sys


# Define accepted command-line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('start_color', type=str,
                    help="Starting color (in hex) to generate step-colors from.")
parser.add_argument('end_color', type=str,
                    help="Ending color (in hex) to generate step-colors from.")
parser.add_argument('steps', type=int,
                    help="Number of step colors to calculate between start and end.")


def get_hex_triplet(color_string, hash_prefix=False):
    """
    Return a normalised six-hex-character color string, optionally with a
    `hash_prefix`. Expands shorthand form, i.e. `get_hex_triplet('#c0b')`
    returns 'cc00bb'.
    """
    letters = color_string[1:] if color_string.startswith('#') else color_string
    if len(letters) == 3:
        letters = letters[0] * 2 + letters[1] * 2 + letters[2] * 2
    return ('#' if hash_prefix else '') + letters


def get_triplet_magnitudes(hex_triplet):
    """
    Return a 3-tuple of hex character-pairs from a hex triplet string. This
    function cleans its input with `get_hex_triplet()`, so you don't have to.
    """
    clean_triplet = get_hex_triplet(hex_triplet)
    hex_pairs = clean_triplet[0:2], clean_triplet[2:4], clean_triplet[4:6]
    hex_to_int = partial(int, base=16)
    int_pairs = map(hex_to_int, hex_pairs)
    return map(lambda m: float(m) / 255, int_pairs)


def get_magnitudes_triplet(magnitudes_triplet, hash_prefix=False):
    """
    Given a 3-tuple of magnitudes from 0 to 1, return a hex triplet.
    """
    byte_magnitudes = map(lambda m: int(m * 255), magnitudes_triplet)
    hex_values = map(lambda b: hex(b)[2:], byte_magnitudes)
    padded_hexes = map(lambda h: h if len(h) == 2 else '0' + h, hex_values)
    return ('#' if hash_prefix else '') + ''.join(padded_hexes)


def get_color_steps(hex_start, hex_end, steps):
    """Return `steps` colors between `hex_start` and `hex_end`."""
    if not steps:
        return []
    start_mags, end_mags = map(get_triplet_magnitudes, (hex_start, hex_end))
    increments = []
    for start, end in zip(start_mags, end_mags):
        if end >= start:
            increments.append((end - start) / (steps+1))
        else:
            increments.append(-((start - end) / (steps+1)))
    step_colors = []
    for step in range(1, steps+1):
        step_color_magnitudes = (start_mags[0] + step * increments[0],
                                 start_mags[1] + step * increments[1],
                                 start_mags[2] + step * increments[2])
        step_colors.append(get_magnitudes_triplet(step_color_magnitudes))
    return step_colors


def main(*argv, **kwargs):
    """Entry-point for command-line invocation of the `color_steps` module."""
    args = parser.parse_args()

    print(args.start_color)
    for color in get_color_steps(args.start_color, args.end_color, args.steps):
        print(color)
    print(args.end_color)


if __name__ == '__main__':
    main(sys.argv)
