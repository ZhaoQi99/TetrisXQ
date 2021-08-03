from config import SHAPES


def _get_shape(pos):
    for i, shape in enumerate(SHAPES):
        for j, state in enumerate(shape):
            if state == pos:
                return (i, j)
    return None, None


def convert(pos):
    shape, state = _get_shape(pos)
    if shape == 0:  # ----
        return [[1, 1, 1, 1]], state
    elif shape == 1:  # L
        return [[1, 1, 1], [1, 0, 0]], 1 + state
    elif shape == 2:  # _｜
        return [[1, 1, 1], [0, 0, 1]], 3 + state
    elif shape == 3:  # T
        return [[1, 1, 1], [0, 1, 0]], 0
    elif shape == 4:  # O
        return [[1, 1], [1, 1]], 0
    elif shape == 5:  # S
        return [[0, 1, 1], [1, 1, 0]], 0
    elif shape == 6:
        return [[1, 1, 0], [0, 1, 1]], 0


def convert_to_answer(y, x, rotate):
    rotate = rotate % 4
    res = ['N']
    res += ['C' for i in range(rotate)]
    res.append(f'D{y-1}')
    if x < 4 - 1:
        res.append(f'L{3-x}')
    if x > 4 - 1:
        res.append(f'R{x-3}')
    return res


if __name__ == '__main__':
    a = [
        [0, 0],
        [0, -1],
        [-1, 1],
        [-1, 0],
    ]
    res = convert(a)
    print(res)
