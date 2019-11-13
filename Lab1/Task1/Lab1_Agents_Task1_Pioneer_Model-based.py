# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
import random

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

counter = 0
stuckCounter = 0

while robot:  # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime % 1000 == 0:
        # print some useful info, but not too often
        print('Time:', simulationTime,
              'ultraSonicSensorLeft:', World.getSensorReading(
                  "ultraSonicSensorLeft"),
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    if counter < 200:
        print("Counter: ", counter)
     # If nearest block is to the left.
        if World.getSensorReading('energySensor').get('direction') < 0:
            motorSpeed = dict(speedLeft=0, speedRight=2)
    # If nearest block is to the right.
        elif World.getSensorReading('energySensor').get('direction') >= 0:
            motorSpeed = dict(speedLeft=2, speedRight=0)

    elif counter > 200:          # When robot has been stuck for a while.
        stuckCounter += 1
        print('StuckCounter: ', stuckCounter)
        World.execute(dict(speedLeft=-1,
                           speedRight=-0.8), 40000, -1)

        '''if stuckCounter < 500:
            motorSpeed = dict(speedLeft=random.randrange(-2, 2, 1),
                              speedRight=random.randrange(-2, 2, 1))
        else:'''
        stuckCounter = 0
        counter = 0

    # If energy block is close enough, pick it up.
    if World.getSensorReading('energySensor').get('distance') < 0.3:
        World.collectNearestBlock()
        counter = 0

    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)
    counter += 1

    # try to collect energy block (will fail if not within range)
