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

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

while robot:    # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()

    # print some useful info, but not too often
    print('Time:', simulationTime,
          'ultraSonicSensorLeft:', World.getSensorReading(
              "ultraSonicSensorLeft"),
          "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################

    # Go forward for 6000 simulation ticks.
    World.execute(dict(speedLeft=2, speedRight=2), 6000, -1)
    World.collectNearestBlock()
    # Turn left for 2900 simulation ticks.
    World.execute(dict(speedLeft=0, speedRight=2), 2900, -1)
    World.collectNearestBlock()
    # Go forward for 8500 simulation ticks.
    World.execute(dict(speedLeft=2, speedRight=2), 8500, -1)
    World.collectNearestBlock()
