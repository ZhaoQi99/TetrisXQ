from Settings import Settings
from environment.AutoPlayEnvironment import AutoPlayEnvironment
from graphics.GraphicModule import GraphicModule
import json
from convert import convert, convert_to_answer

settings = Settings(20, 10)


def generate_tetromino(pos):
    t, shape,state = convert(pos)
    return settings.TETROMINO.build_tetromino().index(t), shape, state


TETROMINO_AGENT = generate_tetromino

if __name__ == '__main__':

    graphic_interface = GraphicModule(settings)

    env_model = AutoPlayEnvironment(settings, graphic_interface)

    turns = 0
    ans = list()
    with open("data.json", "r") as f:
        data = json.load(f)
    while turns < len(data):
        action, shape, origin_rotate = TETROMINO_AGENT(data[turns])
        state, _, end, chosen = env_model.action(action)
        turns += 1
        # print(turns)
        # print(state)
        print(chosen)
        if not chosen:
            with open("ac1.txt", 'w') as f:
                f.write(','.join(ans))

        _, y, x, rotate, _, _ = chosen
        print(shape, y, x, rotate)
        # input('aa')
        ans += convert_to_answer(y, x, rotate + origin_rotate, shape)
        if end:
            print("Turns: " + str(turns))
            # turns = 0
        # save answer
        with open("ac.txt", 'w') as f:
            f.write(','.join(ans))
