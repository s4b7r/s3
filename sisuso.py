# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython


# %%
from math import sqrt
import pprint
import copy


# %%
FIELD_SIDE_LEN = 9
MAX_NUM = FIELD_SIDE_LEN
SQUARE_SIDE_LEN = int(sqrt(FIELD_SIDE_LEN))


# %%
def empty_field():
    field = [[0] * FIELD_SIDE_LEN for _ in range(FIELD_SIDE_LEN)]
    return field


# %%
def the_field():
    field = [
        [0, 7, 0, 5, 0, 4, 0, 1, 0],
        [4, 0, 0, 0, 3, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 0, 0, 8, 0, 0, 9],
        [0, 2, 0, 0, 0, 0, 0, 3, 0],
        [3, 0, 0, 6, 0, 0, 0, 0, 8],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [9, 0, 0, 0, 8, 0, 0, 0, 6],
        [0, 5, 0, 7, 0, 2, 0, 8, 0]
    ]
    return field


# %%
def check_line(line):
    #print(f'checking line {line}')
    found_numbers = {}
    for elem in line:
        if elem != 0 and found_numbers.get(elem, None):
            #print(f'found wrong elem {elem}')
            return False
        found_numbers[elem] = True
    return True


# %%
def assert_field(field):
    assert len(field) == FIELD_SIDE_LEN
    for line in field:
        assert len(line) == FIELD_SIDE_LEN


# %%
def check(field):
    #assert_field(field)
    for evalidx, line in enumerate(field):
        if not check_line(line):
            #print(f'eval to {False} after line {evalidx}')
            return False
    transposed_field = list(map(list, zip(*field)))
    assert_field(transposed_field)
    for evalidx, col in enumerate(transposed_field):
        if not check_line(col):
            #print(f'eval to {False} after col {evalidx}')
            return False
    for square_location_down in range(SQUARE_SIDE_LEN):
        for square_location_right in range(SQUARE_SIDE_LEN):
            square = []
            for square_line_index in range(SQUARE_SIDE_LEN):
                square_line = field[square_location_down * SQUARE_SIDE_LEN + square_line_index][square_location_right * SQUARE_SIDE_LEN : square_location_right * SQUARE_SIDE_LEN + SQUARE_SIDE_LEN]
                square += square_line
            if not check_line(square):
                evalidx = square_location_down * SQUARE_SIDE_LEN + square_location_right
                #print(f'eval to {False} after square {evalidx}')
                return False
    return True


# %%
def solve(field):
    given = copy.deepcopy(field)
    field_index = 0
    backtracking = False
    while field_index < FIELD_SIDE_LEN ** 2:
        #print(f'field index {field_index}')
        field_line_index = field_index // FIELD_SIDE_LEN
        field_col_index = field_index % FIELD_SIDE_LEN
        if given[field_line_index][field_col_index] == 0:
            backtracking = False
            start_trial_number = field[field_line_index][field_col_index] + 1
            trial_is_good = False
            for trial_number in range(start_trial_number, MAX_NUM+1):
                #print(f'trial number {trial_number}')
                field[field_line_index][field_col_index] = trial_number
                trial_is_good = check(field)
                if trial_is_good:
                    #print(f'field [{field_line_index}][{field_col_index}] = {field[field_line_index][field_col_index]}')
                    field_index += 1
                    break
            else:
                field[field_line_index][field_col_index] = 0
                field_index -= 1
                backtracking = True
        else:
            if not backtracking:
                field_index += 1
            else:
                field_index -= 1


# %%
field = the_field()
get_ipython().magic('timeit -n1 -r1 solve(field)')
pprint.pprint(field)


