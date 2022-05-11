import VL53L1X, sys
full_speed = 1.0
tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29, tca9548a_num=2, tca9548a_addr=0x70)
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29, tca9548a_num=7, tca9548a_addr=0x70)
tof1.open()
tof2.open()


tof1.start_ranging(3)
tof2.start_ranging(3)
def get_walls():
    while True:
        distance1_in_mm = float(tof1.get_distance())
        distance2_in_mm = float(tof2.get_distance())
        if distance1_in_mm < 0 or distance2_in_mm < 0:
            print("sensor error")
            continue
        else:
            break
    error = distance1_in_mm - distance2_in_mm
    try:
        error_factor = error/(distance1_in_mm + distance2_in_mm)
    except:
        print("sensor error")
        error_factor = 2.000
    print("The distance is {}mm".format(distance1_in_mm))
    print("The distance is {}mm".format(distance2_in_mm))
    print("The errorfactor is {:.3f}".format(error_factor))
    return error_factor

def speed_calc(err,fullv):
    if err == 0:
        return[fullv,fullv]
    elif err>0:
        return [fullv,(1-abs(err))*fullv]
    elif err<0:
        return [(1-abs(err))*fullv,fullv]
    else:
        return [0,0]

if __name__ == "__main__":
    while True:
        try:
            a = get_walls()
            motorspeeds = speed_calc(a,full_speed)
            print(motorspeeds)
        except KeyboardInterrupt:
            print("quitting")
            tof1.stop_ranging()
            tof2.stop_ranging()
            sys.exit()
