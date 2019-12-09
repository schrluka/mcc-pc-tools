from matplotlib import pyplot as plt
import numpy as np
from bisect import bisect_left

filename = 'log.txt'

file = open(filename, 'r')

t_meas = []
rssi = []
speed_meas = []
pos_meas = []
ref_speed_meas = []

last_speed = None

for line in file.readlines():
    cols = line.split(' ')
    if len(cols) != 18:
        continue

    v = int(''.join(cols[4:2:-1]), 16)

    # filter repeating entries
    # if v == last_speed:
    #    continue
    # last_speed = v

    # first column is a timestamp in ms
    t_meas.append(int(cols[0][:-1]))

    speed_meas.append(v)

    # 2nd col is mac addr

    # 3rd rssi
    rssi.append(int(cols[2]))

    pos_meas.append(int(''.join(cols[10:6:-1]), 16))
    # ref_speed_meas.append(int(''.join(cols[16:14:-1]), 16))

    delta_pos.append(int(''.join(cols[14:10:-1]), 16))
    track_id.append(int(cols[15], 16))
    dist.append(int(cols[16], 16))
    i_ref.append(int(cols[17], 16))

n = len(t_meas)
print('number of records: ', n)

t_meas = np.array(t_meas)
t_meas = t_meas - t_meas[0]


# run a simple prediction / interpolation
t_calc = np.linspace(0, t_meas[-1], 5000)
pos_calc = []
#speed_calc = []
for now in t_calc:
    # get last measurement point available at that time
    ind = bisect_left(t_meas, now)
    if ind == 0:
        pos_calc.append(0)
        continue
    ind = ind - 1
    t = t_meas[ind]
    v = speed_meas[ind]
    x = pos_meas[ind]
    # most simple prediction: constant speed
    x = x + (now - t) / 1000 * v / 10    # /1000 to scale from ms to s, /10 to scale from mm to cm
    pos_calc.append(x)

A = [1, 2, 3, 4 ]
print(bisect_left(A, 1.5))

plt.scatter(t_meas, speed_meas)
plt.scatter(t_meas, pos_meas)
print(ref_speed_meas)
plt.scatter(t_meas, ref_speed_meas)
plt.plot(t_calc, pos_calc)

plt.show()

