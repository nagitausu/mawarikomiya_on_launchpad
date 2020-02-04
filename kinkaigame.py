import time
import launchpad
import kinkaigame_solver
import random

TRAJ_SPEED = 0.05
MACHINE_NUM = 5


def random_init():
    field = [[1] * 8 for _ in range(8)]
    lines = [item for item in range(8)]
    random.shuffle(lines)
    cols = lines[:MACHINE_NUM]
    random.shuffle(lines)
    rows = lines[:MACHINE_NUM]

    machines = []
    for x, y in zip(cols, rows):
        machines.append((x, y))
        field[x][y] = -1
    ans = kinkaigame_solver.solve(field, machines)
    return field, ans


def colorize_launchpad(LP, field):
    for i in range(8):
        for j in range(8):
            if field[i][j] == 1:
                LP.LedCtrlXY(i, j, 50, 30, 0)
            elif field[i][j] == -1:
                LP.LedCtrlXY(i, j, 0, 0, 60)


def draw_traj(LP, traj, speed):
    for i, (x, y) in enumerate(traj):
        LP.LedCtrlXY(x, y, 50, 30, 0)
        time.sleep(speed)
        LP.LedCtrlXY(x, y, 0, 0, 0)
    LP.LedCtrlXY(x, y, 0, 0, 0)


# Take LaunchPad Object and field[8][8]
# Returns msg[2]
def read_player_motion(LP, field):
    while True:
        msg = None
        while msg is None:
            msg = LP.ReadXY()
            time.sleep(0.01)
        msg = None
        while msg is None:
            msg = LP.ReadXY()
            time.sleep(0.01)
        if field[msg[0]][msg[1]] == -1:
            break
    return msg


def machine_work(LP, field, pos):
    x, y, _ = pos
    taken = []
    # Take Up
    traj = []
    for i in range(1, 8):
        if x - i < 0 or field[x - i][y] != 1:
            break
        traj.insert(0, [x - i, y])
        taken.append([x - i, y])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Right
    traj = []
    for i in range(1, 8):
        if y - i < 0 or field[x][y - i] != 1:
            break
        traj.insert(0, [x, y - i])
        taken.append([x, y - i])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Down
    traj = []
    for i in range(1, 8):
        if x + i > 7 or field[x + i][y] != 1:
            break
        traj.insert(0, [x + i, y])
        taken.append([x + i, y])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Left
    traj = []
    for i in range(1, 8):
        if y + i > 7 or field[x][y + i] != 1:
            break
        traj.insert(0, [x, y + i])
        taken.append([x, y + i])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    return taken


def blink(pos, color):
    for _ in range(3):
        LP.LedCtrlXY(pos[0], pos[1], *color)
        time.sleep(0.2)
        LP.LedCtrlXY(pos[0], pos[1], 0, 0, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(pos[0], pos[1], *color)


def finalize(LP, gold, ans):
    time.sleep(1)
    if gold == ans:
        message = "OPTIMUM!! " + str(gold) + "/" + str(ans)
        LP.LedScrollText(message, 109)
    else:
        message = "NOT OPTIMUM... " + str(gold) + "/" + str(ans)
        LP.LedScrollText(message, 81)
    print(gold)
    exit()

if __name__ == "__main__":
    LP = launchpad.Launchpad()
    field, ans = random_init()
    colorize_launchpad(LP, field)

    used = 0
    gold = 0
    while True:
        msg = read_player_motion(LP, field)
        blink(msg, [0, 0, 60])
        taken = machine_work(LP, field, msg)
        gold += len(taken)
        for x, y in taken:
            field[x][y] = 0
        LP.LedCtrlXY(msg[0], msg[1], 10, 10, 10)
        field[msg[0]][msg[1]] = 0
        used += 1
        if used == MACHINE_NUM:
            finalize(LP, gold, ans)
