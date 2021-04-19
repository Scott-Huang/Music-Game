"""
"""
import random
from random import randint, choices

KEY_NUM = 8
GENERATE_SIZE = 60
PATTERN_NUMBER = 40
WEIGHT_DECAY = 0.04

def get_random_sequence(sequence):
    start_index = randint(0, len(sequence))
    return sequence[start_index:] + sequence[:start_index]

def get_left_sequence(seq_length, key_num=KEY_NUM):
    sequence = range(1, key_num // 2 + 1)
    if bool(random.getrandbits(1)):
        sequence = reversed(sequence)
    sequence = [(i+1,) for i in sequence]
    return get_random_sequence(sequence)[:seq_length]

def get_right_sequence(seq_length, key_num=KEY_NUM):
    sequence = range(key_num // 2 + 1, key_num + 1)
    if bool(random.getrandbits(1)):
        sequence = reversed(sequence)
    sequence = [(i+1,) for i in sequence]
    return get_random_sequence(sequence)[:seq_length]

def get_repetition(circle, repetition):
    if isinstance(circle, int):
        circle = (circle,)
    return [circle for _ in range(repetition)]

def get_random_repetition(repetition, key_num=KEY_NUM):
    circle = randint(1,key_num)
    return get_repetition(circle, repetition)

def get_repeted_sequence(sequence, repetition):
    temp_seq = []
    for _ in range(repetition):
        temp_seq += sequence
    return temp_seq

def get_empty_sequence(length):
    return [tuple()] * length

def get_random_spontaneous(circle_number, key_num=KEY_NUM):
    return tuple(random.sample(range(1,key_num+1), circle_number))

def combine_tuple(left, right):
    left = set(left)
    right = set(right)
    return tuple(left | right)

def combine_sequence(left_seq, right_seq):
    return [combine_tuple(left, right) for left,right in zip(left_seq, right_seq)]

GENERATION_FUNCTIONS = [get_left_sequence, get_right_sequence, get_random_repetition,
                        get_empty_sequence, get_random_spontaneous, combine_sequence]
GENERATION_WEIGHTS = [0.25, 0.25, 0.15, 0.1, 0.08, 0.17]

def generate_patterns(generate_size=GENERATE_SIZE, key_num=KEY_NUM):
    def __generate_patterns(size, weights, key_num):
        function = choices(GENERATION_FUNCTIONS, weights=weights)[0]
        if function == combine_sequence:
            weights[-1] = max(0, weights[-1]-WEIGHT_DECAY)
            weights[-2] = max(0, weights[-2]-WEIGHT_DECAY)
            return combine_sequence(__generate_patterns(size, weights, key_num), 
                                    __generate_patterns(size, weights, key_num))
        elif function == get_random_spontaneous:
            return [get_random_spontaneous(randint(2,key_num//2+1+1)) for _ in range(size)]
        return function(size)
    
    pattern = []
    while generate_size:
        step_size = min(randint(1,key_num//2), generate_size)
        generate_size -= step_size
        pattern += __generate_patterns(step_size, GENERATION_WEIGHTS, key_num)
    return pattern

PATTERNS = [generate_patterns() for _ in range(PATTERN_NUMBER)]