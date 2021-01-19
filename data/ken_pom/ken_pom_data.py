import os

from ast import literal_eval

NUM_ROWS = 1000
ACTUAL_SPREAD = 3
PREDICTED_SPREAD = 4
PERCENT_COLUMN = 5
CORRECT_TEAM_COLUMN = 6
COVERED_COLUMN = 7


def favorite_over_percent(percent: int) -> tuple:
    f = get_ken_pom_file()

    correct = 0
    wrong = 0
    total = 0
    money = 0

    for line in f:
        obj = literal_eval(line)

        if obj["percentage"] != "ERROR" and int(obj["percentage"]) >= percent:
            if obj["actual"] < 0:
                correct += 1
                money += 100
            else:
                wrong += 1
                money -= 110

            total += 1

    print(
        "correct: {}, incorrect: {}, total: {}, money: {}".format(
            correct, wrong, total, money
        )
    )
    return correct, total, correct / total * 100, money


def dog_under_percent(percent: int) -> tuple:
    f = get_ken_pom_file()

    correct = 0
    wrong = 0
    total = 0
    money = 0

    for line in f:
        obj = literal_eval(line)

        if obj["percentage"] != "ERROR" and int(obj["percentage"]) <= percent:
            if obj["actual"] > 0:
                correct += 1
                money += 100
            else:
                wrong += 1
                money -= 110

            total += 1

    print(
        "correct: {}, incorrect: {}, total: {}, money: {}".format(
            correct, wrong, total, money
        )
    )
    return correct, total, correct / total * 100, money


def get_ken_pom_file():
    return open(os.getcwd() + "/../data/KenPomPredictions.txt", "r")
