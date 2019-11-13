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

motorSpeed = dict(speedLeft=2, speedRight=2)    # Straight forward.
World.setMotorSpeeds(motorSpeed)
for x in range(0, 75000000):                    # Wait.
    pass

motorSpeed = dict(speedLeft=0, speedRight=0)    # Stop.
World.setMotorSpeeds(motorSpeed)
World.collectNearestBlock()                     # Collect first energy block.

motorSpeed = dict(speedLeft=0, speedRight=2)    # Turn right.
World.setMotorSpeeds(motorSpeed)
for x in range(0, 30000000):                    # Wait.
    pass

motorSpeed = dict(speedLeft=2, speedRight=2)    # Straight forward.
World.setMotorSpeeds(motorSpeed)
for x in range(0, 95000000):                    # Wait.
    pass

World.collectNearestBlock()
'''elif World.getSimulationTime() < 10000:
    motorSpeed = dict(speedLeft=-1.5, speedRight=-1.0)
    World.setMotorSpeeds(motorSpeed)
elif World.getSimulationTime() < 15000:
    print("Turning for a bit...",)
    World.execute(dict(speedLeft=2, speedRight=-2), 15000, -1)
    print("... got dizzy, stopping!")
    print("BTW, nearest energy block is at:",
          World.getSensorReading("energySensor"))
    World.setMotorSpeeds(motorSpeed)'''

########################################
# Action Phase: Assign speed to wheels #
########################################
# assign speed to the wheels
World.setMotorSpeeds(motorSpeed)
# try to collect energy block (will fail if not within range)

print("Trying to collect a block...", World.collectNearestBlock())
