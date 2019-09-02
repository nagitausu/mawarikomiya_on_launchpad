import time
import mawarikomiya
import launchpad
import random

def draw_traj(LP, traj, goal_pos, speed):
    for i, item in enumerate(traj):
        if i != 0:
            LP.LedCtrlXY(x, y, 0, 0, 0)
            if x == goal_pos[0] and y == goal_pos[1]:
                LP.LedCtrlXY(x, y, 30, 30, 0)
        x = item // 8
        y = item % 8
        LP.LedCtrlXY(x, y, 60, 0, 0)
        time.sleep(speed)

def read_player_motion(LP):
    msg = None
    while msg == None:
        msg = LP.ReadXY()
        time.sleep(0.01)
    msg = None
    while msg == None:
        msg = LP.ReadXY()
        time.sleep(0.01)
    return msg

def winning(LP, player_pos):
    x = player_pos[0]
    y = player_pos[1]
    for i in range(3):
        LP.LedCtrlXY(x, y, 30, 30, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(x, y, 0, 0, 0)
        time.sleep(0.2)
    LP.LedScrollText("YOU WIN!!", 79)
    exit()

def losing(LP, mawari_pos):
    x = mawari_pos[0]
    y = mawari_pos[1]
    for i in range(3):
        LP.LedCtrlXY(x, y, 60, 0, 0)
        time.sleep(0.2)
        LP.LedCtrlXY(x, y, 0, 0, 0)
        time.sleep(0.2)
    LP.LedScrollText("YOU LOSE...", 72)
    exit()

player_pos = [3,3]
goal_pos = [random.randint(0, 7), random.randint(0, 7)]
MK = mawarikomiya.Mawarikomiya(player_pos)
LP = launchpad.Launchpad()
LP.LedCtrlXY(player_pos[0], player_pos[1], 0, 0, 60)
LP.LedCtrlXY(goal_pos[0], goal_pos[1], 30, 30, 0)

cnt = 0
speed = 0.1
while True:
    if cnt % 5 == 0 and cnt != 0:
        speed /= 2.0
    msg = read_player_motion(LP)
    LP.LedCtrlXY(player_pos[0], player_pos[1], 0, 0, 0)
    LP.LedCtrlXY(msg[0], msg[1], 0, 0, 60)
    player_pos[0] = msg[0]
    player_pos[1] = msg[1]
    if player_pos[0] == goal_pos[0] and player_pos[1] == goal_pos[1]:
        winning(LP, player_pos)
    if max(abs(player_pos[0] - MK.pos[0]), abs(player_pos[1] - MK.pos[1])) <= 1:
        losing(LP, MK.pos)

    traj = MK.ReactPlayerMotion(player_pos)
    draw_traj(LP, traj, goal_pos, speed)
    cnt += 1
