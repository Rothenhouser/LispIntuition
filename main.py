# lispy

instruction = [
    'do',
    [
        'draw_point',
        {
            'x': 2,
            'y': 2
        },
    ],
    ['rotate', [
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
    ]],
]


def do(*args):
    # hmmm
    return args


def draw_point(a):
    return 'a point'


def draw_line(a, b, color):
    print('drawing line')
    return 'a line'


def rotate(line):
    print('rotating')
    return line + ' rotated'


functions = {
    'do': do,
    'draw_point': draw_point,
    'draw_line': draw_line,
    'rotate': rotate
}


def parse_instruction(ins):
    print('parsing ' + str(ins))
    if not isinstance(ins, list):
        # must be an argument... so args must not be lists?
        return ins
    else:
        fname, *args = ins
        print(fname)
        print(args)
        print(ins)
        return functions[fname](*map(parse_instruction, args))


print('hi')
print(parse_instruction(instruction))
