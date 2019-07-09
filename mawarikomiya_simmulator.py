import time
import mawarikomiya
import launchpad

MK = mawarikomiya.Mawarikomiya()
LP = launchpad.Launchpad()

LP.LedCtrlXY(1,1,10,10,10)
time.sleep(1)
traj = MK.ReactPlayerMotion([4,4])
print(traj)
