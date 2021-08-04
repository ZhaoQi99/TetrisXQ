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
        return [[1, 1, 1, 1]], shape, state + 1
    elif shape == 1:  # L
        return [[1, 1, 1], [1, 0, 0]], shape,state
    elif shape == 2:  # _｜
        return [[1, 1, 1], [0, 0, 1]], shape, 1 + state
    elif shape == 3:  # T
        return [[1, 1, 1], [0, 1, 0]], shape,state
    elif shape == 4:  # O
        return [[1, 1], [1, 1]], shape,state
    elif shape == 5:  # S
        return [[0, 1, 1], [1, 1, 0]], shape,state
    elif shape == 6: # Z
        return [[1, 1, 0], [0, 1, 1]], shape, state


def convert_to_answer(y, x, rotate, shape):
    rotate = rotate % 4
    res = ['N']
    if rotate > 0:
        res.append(f'C{rotate}')
    if x < 4 - 1:
        if 3 - x > 0:
            t = min(3, 3 - x)
            if shape == 0:
                t += 1
            res.append(f'L{t}')
    if x > 4 - 1:
        if x - 3 > 0:
            t = min(x-3,5)
            if shape == 1:
                t += 1
            res.append(f'R{t}')
    t = min(y+1,19)
    if shape == 0:
        t += 1
    res.append(f'D{t}')
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
