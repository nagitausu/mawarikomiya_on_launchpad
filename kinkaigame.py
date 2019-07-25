import time
import launchpad
import random

TRAJ_SPEED = 0.1

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
        while msg == None:
            msg = LP.ReadXY()
            time.sleep(0.01)
        msg = None
        while msg == None:
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
    for i in range(1,8):
        if x - i < 0 or field[x - i][y] != 1:
            break
        traj.insert(0, [x - i, y])
        taken.append([x - i, y])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Right
    traj = []
    for i in range(1,8):
        if y - i < 0 or field[x][y - i] != 1:
            break
        traj.insert(0, [x, y - i])
        taken.append([x, y - i])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Down
    traj = []
    for i in range(1,8):
        if x + i > 7 or field[x + i][y] != 1:
            break
        traj.insert(0, [x + i, y])
        taken.append([x + i, y])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    # Take Left
    traj = []
    for i in range(1,8):
        if y + i > 7 or field[x][y + i] != 1:
            break
        traj.insert(0, [x, y + i])
        taken.append([x, y + i])
        draw_traj(LP, traj, TRAJ_SPEED)
        time.sleep(0.1)
    return taken


def blink(pos, color, post_color):
    for i in range(3):
        LP.LedCtrlXY(pos[0], pos[1], color[0], color[1], color[2])
        time.sleep(0.2)
        LP.LedCtrlXY(pos[0], pos[1], 0, 0, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(pos[0], pos[1], post_color[0], post_color[1], post_color[2])
    return

def winning(LP, player_pos):
    x = player_pos[0]
    y = player_pos[1]
    for i in range(3):
        LP.LedCtrlXY(x, y, 50, 30, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(x, y, 0, 0, 0)
        time.sleep(0.2)
    LP.LedScrollText("YOU WIN!!")
    exit()

def losing(LP, mawari_pos):
    x = mawari_pos[0]
    y = mawari_pos[1]
    for i in range(3):
        LP.LedCtrlXY(x, y, 60, 0, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(x, y, 0, 0, 0)
        time.sleep(0.2)
    LP.LedScrollText("YOU LOSE...")
    exit()

def finish(LP, gold):
    time.sleep(1)
    LP.midi_out.send_sysex(0, 32, 41, 2, 4, 20, 109, 0, 4, \
                           89, 79, 85, 32, \
                           ord("G"), ord("O"), ord("T"), \
                           ord(str(gold // 10)), ord(str(gold % 10)), \
                           ord("G"), ord("O"), ord("L"), ord("D"), ord("!"))
    print(gold)
    exit()

field = [[1] * 8 for _ in range(8)]
machines = []
machine_num = 5
for _ in range(machine_num):
    machine = [random.randint(0, 7), random.randint(0, 7), 0]
    while machine in machines:
        machine = [random.randint(0, 7), random.randint(0, 7), 0]
    machines.append(machine)
    field[machine[0]][machine[1]] = -1

LP = launchpad.Launchpad()
for i in range(8):
    for j in range(8):
        if field[i][j] == 1:
            LP.LedCtrlXY(i, j, 50, 30, 0)
        elif field[i][j] == -1:
            LP.LedCtrlXY(i, j, 0, 0, 60)

used = 0
gold = 0
while True:
    msg = read_player_motion(LP, field)
    blink(msg, [0, 0, 60], [0, 0, 60])
    taken = machine_work(LP, field, msg)
    gold += len(taken)
    for x, y in taken:
        field[x][y] = 0
    LP.LedCtrlXY(msg[0], msg[1], 0, 0, 10)
    field[msg[0]][msg[1]] = 0
    used += 1
    if used == machine_num:
        finish(LP, gold)
