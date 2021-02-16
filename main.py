# lispy
# https://stopa.io/post/265
from collections.abc import Hashable
from collections import defaultdict

instruction = [
    'do',
    [
        'draw_point',
        {
            'x': 2,
            'y': 2
        },
    ],
    [
        'def', 'shape',
        [
            'draw_line',
            {
                'x': 0,
                'y': 0
            },
            {
                'x': 1,
                'y': 1
            },
            'blue',
        ]
    ],
    ['rotate', 'shape'],
    # user-defined function
    [
        'def', 'draw_triangle',
        [
            'fn', ['left', 'top', 'right', 'color'],
            [
                'do',
                ['draw_line', 'left', 'top', 'color'],
                ['draw_line', 'left', 'right', 'color'],
                ['draw_line', 'top', 'right', 'color'],
            ]
        ]
    ],
    [
        'draw_triangle',
        {
            'x': 0,
            'y': 0
        },
        {
            'x': 1,
            'y': 1
        },
        {
            'x': 0,
            'y': 1
        },
        'blue',
    ]
]

#_def('draw_triangle', v=parse_instruction(['fn', ['l', 't',...], ['do', ['draw_line', 'l', 't']]]))
#... v=parse_fn_instruction([['l', 't',...], ['do', ['draw_line', 'l', 't']]], variables)
#_def('draw_triangle', v=newfn)

# Support definitions of variables and functions
variables = {}


def do(*args):
    # hmmm
    return args


def _def(name, v):
    global variables
    variables[name] = v


def draw_point(a):
    return 'a point'


def draw_line(a, b, color):
    print('drawing line')
    return 'a line'


def rotate(line):
    print('rotating')
    return line + ' rotated'


functions = defaultdict(
    lambda: None, {
        'do': do,
        'def': _def,
        'draw_point': draw_point,
        'draw_line': draw_line,
        'rotate': rotate
    })


def map_args_with_values(args, values):
    # When this is executed, args is the list of function parameters, # e.g.
    # ['left', 'top', ...]
    # and values is the list of arguments for
    # a call of the function, e.g.
    # [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}, ...]
    return {a: v for a, v in zip(args, values)}


def parse_fn_instruction(args, body):

    def newfn(*values):
        global variables
        variables = {**variables, **map_args_with_values(args, values)}
        return parse_instruction(body)

    return newfn


def parse_instruction(ins):
    # First check if ins is a variable
    if isinstance(ins, Hashable) and ins in variables:
        return variables[ins]
    elif not isinstance(ins, list):
        # must be an argument... so args must not be lists?
        return ins
    else:
        fname, *args = ins
        print(fname)

        if fname == 'fn':
            # args is a list with two elements: first one is the list
            # of arguments, second is the 'body': a do instruction
            return parse_fn_instruction(*args)
        else:
            # use a defaultdict with None for variables and functions
            fn = functions[fname] or variables[fname]
            return fn(*map(parse_instruction, args))


print('hi')
print(parse_instruction(instruction))
