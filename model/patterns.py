"""Program Description

The patterns.py program is responsible for generating random patterns.
"""

import random
from random import randint, choices

# default key_num
KEY_NUM = 8
# default length of a pattern
GENERATE_SIZE = 60
# default number of patterns
PATTERN_NUMBER = 40
# the decaying factors of weight probability for random pattern generation
WEIGHT_DECAY = 0.04

def get_random_sequence(sequence):
    """Generate a sequence from a random position."""
    start_index = randint(0, len(sequence))
    return sequence[start_index:] + sequence[:start_index]

def get_left_sequence(seq_length, key_num=KEY_NUM):
    """Generate a random sequence in the left side."""
    sequence = range(1, key_num // 2 + 1)
    if bool(random.getrandbits(1)):
        sequence = reversed(sequence)
    sequence = [(i+1,) for i in sequence]
    return get_random_sequence(sequence)[:seq_length]

def get_right_sequence(seq_length, key_num=KEY_NUM):
    """Generate a random sequence in the right side."""
    sequence = range(key_num // 2 + 1, key_num + 1)
    if bool(random.getrandbits(1)):
        sequence = reversed(sequence)
    sequence = [(i+1,) for i in sequence]
    return get_random_sequence(sequence)[:seq_length]

def get_repetition(circle, repetition):
    """Repeat a circle for several times."""
    if isinstance(circle, int):
        circle = (circle,)
    return [circle for _ in range(repetition)]

def get_random_repetition(repetition, key_num=KEY_NUM):
    """Get a random repeating circles."""
    circle = randint(1,key_num)
    return get_repetition(circle, repetition)

def get_repeted_sequence(sequence, repetition):
    """Repeat a sequence for several times."""
    temp_seq = []
    for _ in range(repetition):
        temp_seq += sequence
    return temp_seq

def get_empty_sequence(length):
    """Get sequence of empty key pressing."""
    return [tuple()] * length

def get_random_spontaneous(circle_number, key_num=KEY_NUM):
    """Get a random keys pressing bundle."""
    return tuple(random.sample(range(1,key_num+1), circle_number))

def combine_tuple(left, right):
    """Combine two tuples into one."""
    left = set(left)
    right = set(right)
    return tuple(left | right)

def combine_sequence(left_seq, right_seq):
    """Combine two sequences in to one."""
    return [combine_tuple(left, right) for left,right in zip(left_seq, right_seq)]

# functions to generate patterns
GENERATION_FUNCTIONS = [get_left_sequence, get_right_sequence, get_random_repetition,
                        get_empty_sequence, get_random_spontaneous, combine_sequence]
# the probability distribution of the functions above
GENERATION_WEIGHTS = [0.25, 0.25, 0.15, 0.1, 0.08, 0.17]

def generate_patterns(generate_size=GENERATE_SIZE, key_num=KEY_NUM):
    """Generate a pattern randdomly.

    Arguments:
        generate_size: The size of the generated pattern.
        key_num: The number of keys in the keyset.
    Returns:
        The generated pattern as a sequence of tuples which represent
        the track indexes to have circles being added.
    """

    def __generate_patterns(size, weights, key_num):
        """Generate a part of patterns recursively.

        Arguments:
            size: The number of elements in the part of a pattern.
            weights: The probability distribution of gerating functions.
            key_num: The number of keys in the keyset.
        Returns:
            The generated partial pattern as a sequence of tuples which represent
            the track indexes to have circles being added.
        """

        function = choices(GENERATION_FUNCTIONS, weights=weights)[0]
        if function == combine_sequence:
            new_weights = weights.copy()
            new_weights[-1] = max(0, weights[-1]-WEIGHT_DECAY)
            new_weights[-2] = max(0, weights[-2]-WEIGHT_DECAY)
            return combine_sequence(__generate_patterns(size, new_weights, key_num), 
                                    __generate_patterns(size, new_weights, key_num))
        elif function == get_random_spontaneous:
            return [get_random_spontaneous(randint(2,key_num//2+1+1)) for _ in range(size)]
        return function(size)
    
    pattern = []
    while generate_size:
        step_size = min(randint(1,key_num//2), generate_size)
        generate_size -= step_size
        pattern += __generate_patterns(step_size, GENERATION_WEIGHTS, key_num)
    return pattern

# 40 generated random patterns
PATTERNS = [generate_patterns() for _ in range(PATTERN_NUMBER)]