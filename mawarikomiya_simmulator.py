import time
import mawarikomiya
import launchpad

def draw_traj(LP, traj, speed):
    for i, item in enumerate(traj):
        if i != 0:
            LP.LedCtrlXY(x, y, 0, 0, 0)
        x = item // 8
        y = item % 8
        LP.LedCtrlXY(x, y, 63, 0, 0)
        print(x, y)
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
    print(msg)
    return msg

player_pos = [3,3]
MK = mawarikomiya.Mawarikomiya(player_pos)
LP = launchpad.Launchpad()
LP.LedCtrlXY(player_pos[0], player_pos[1], 0, 0, 30)

for i in range(3):
    msg = read_player_motion(LP)
    LP.LedCtrlXY(player_pos[0], player_pos[1], 0, 0, 0)
    LP.LedCtrlXY(msg[0], msg[1], 0, 0, 30)
    player_pos[0] = msg[0]
    player_pos[1] = msg[1]

    traj = MK.ReactPlayerMotion(player_pos)
    print(traj)
    draw_traj(LP, traj, 0.1)