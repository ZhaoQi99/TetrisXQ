from Settings import Settings
from environment.AutoPlayEnvironment import AutoPlayEnvironment
from graphics.GraphicModule import GraphicModule
import json
from convert import convert, convert_to_answer

settings = Settings(20, 20)


def generate_tetromino(pos):
    shape, state = convert(pos)
    return settings.TETROMINO.build_tetromino().index(shape), state


TETROMINO_AGENT = generate_tetromino

if __name__ == '__main__':

    graphic_interface = GraphicModule(settings)

    env_model = AutoPlayEnvironment(settings, graphic_interface)

    turns = 0
    ans = list()
    with open("data.json", "r") as f:
        data = json.load(f)
    while True and turns < len(data):
        action, origin_rotate = TETROMINO_AGENT(data[turns])
        state, _, end, chosen = env_model.action(action)
        turns += 1
        print(turns)
        # print(state)
        _, y, x, rotate, _, _ = chosen
        # print(y, x, rotate)
        # input('aa')
        ans += convert_to_answer(y, x, rotate + origin_rotate)
        if end:
            print("Turns: " + str(turns))
            turns = 0
        # save answer
        with open("ac.txt", 'w') as f:
            f.write(','.join(ans))
