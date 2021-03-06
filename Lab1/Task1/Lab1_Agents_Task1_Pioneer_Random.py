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

while robot:  # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    # if-statement changed since simulationTime%1000==0 behaved unexpectedly at times.
    if (World.getSimulationTime() - simulationTime) < 2000:
        # print some useful info, but not too often
        print('Time:', simulationTime,
              'ultraSonicSensorLeft:', World.getSensorReading(
                  "ultraSonicSensorLeft"),
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    # Assigns random motoring speed to the wheels, from -2 to +2.
    motorSpeed = dict(speedLeft=random.randrange(-2, 2, 1),
                      speedRight=random.randrange(-2, 2, 1))

    # If energy block is close enough, pick it up.
    if World.getSensorReading('energySensor').get('distance') < 0.3:
        World.collectNearestBlock()
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    World.setMotorSpeeds(motorSpeed)
