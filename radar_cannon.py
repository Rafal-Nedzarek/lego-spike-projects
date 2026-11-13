from hub import port, light, light_matrix
import runloop, motor, distance_sensor, color

async def main():
    light.color(1, color.RED)
    light.color(0, color.RED)
    light_matrix.clear
    motor.run_to_absolute_position(port.F, 270, 200)
    await motor.run_to_absolute_position(port.C, 180, 200)
    #await motor.run_to_absolute_position(port.C, 175, 200)
    while True:
        await runloop.sleep_ms(1)
        await motor.run_to_absolute_position(port.C, 185, 200, direction=motor.LONGEST_PATH)
        await motor.run_to_absolute_position(port.C, 175, 200, direction=motor.LONGEST_PATH)

async def fire_gun():
    while True:
        await runloop.sleep_ms(1)
        if distance_sensor.distance(port.E) != -1 and distance_sensor.distance(port.E) < 500:
            motor.run_to_absolute_position(port.F, 240, 1000)

runloop.run(main(), fire_gun())