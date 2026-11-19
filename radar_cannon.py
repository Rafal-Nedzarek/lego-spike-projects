from hub import port, light, light_matrix
import runloop, motor, distance_sensor, color

# Ports
RADAR_MOTOR = port.C
CANNON_MOTOR = port.F
DISTANCE_SENSOR = port.E

# Radar settings
RADAR_EDGE_LEFT = -175
RADAR_EDGE_RIGHT = 175
RADAR_SPEED = 200

# Cannon settings
CANNON_READY = 220
CANNON_SHOT_TURN = 360
CANNON_SPEED = 1000
TRIGGER_DISTANCE_MM = 500# fire at anything closer than 50 cm


async def setup():
    light.color(0, color.RED)
    light.color(1, color.RED)
    light_matrix.clear()
    

async def radar_sweep():
    await setup()
    while True:
        await motor.run_to_absolute_position(RADAR_MOTOR, RADAR_EDGE_LEFT, RADAR_SPEED, direction=motor.COUNTERCLOCKWISE)
        await motor.run_to_absolute_position(RADAR_MOTOR, RADAR_EDGE_RIGHT, RADAR_SPEED, direction=motor.CLOCKWISE)


async def fire_gun():
    # stretch the rubber band, and hold to keep it ready to go
    await motor.run_to_absolute_position(CANNON_MOTOR, CANNON_READY, CANNON_SPEED, stop=motor.HOLD)
    while True:
        await runloop.sleep_ms(1)
        distance = distance_sensor.distance(DISTANCE_SENSOR)
        if distance != -1 and distance < TRIGGER_DISTANCE_MM:# -1 means nothing detected
            # make a whole turn to release the rubber band, stretch it again, and hold
            await motor.run_for_degrees(CANNON_MOTOR, CANNON_SHOT_TURN, CANNON_SPEED, stop=motor.HOLD)


runloop.run(radar_sweep(), fire_gun())