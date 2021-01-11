#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi

class MoveGroup():
	
	about = "This class is to command the motions of KUKA KR10 arm to perform certain tasks"


	def __init__ (self, group, hand_group, robot):
		self.group = group
		self.hand_group = hand_group
		self.robot = robot


	def pose_goal(self,ox, oy, oz, ow, x, y, z):

		group = self.group

		pose_goal = geometry_msgs.msg.Pose()
		pose_goal.orientation.x = ox
		pose_goal.orientation.y = oy
		pose_goal.orientation.z = oz
		pose_goal.orientation.w = ow
		pose_goal.position.x = x
		pose_goal.position.y = y
		pose_goal.position.z = z
		group.set_pose_target(pose_goal)
		plan = group.go(wait=True)
		group.stop()

	def pick(self):
		hand_group = self.hand_group

		##open gripper
		hand_group.set_named_target("open")
		plan1 = hand_group.go()


		##Go_Close_pose
		self.pose_goal(-0.580485429137, 0.45844355482, 0.538497854139, 0.403591668262, -0.306729882408, -1.95442187176, 1.54037061059)

		##hold object
		hand_group.set_named_target("close")
		plan1 = hand_group.go()


		##lift object
		self.pose_goal(-0.591900830057, 0.460260319172, 0.525701725788, 0.401810330227, -0.26290724605, -1.99983537529, 1.74536497488)

	def place(self):
		hand_group = self.hand_group

		##down pose
		self.pose_goal(0.493590210497, 0.477585645861, -0.464176200638, 0.559304129906, 0.477911326918, -2.96654655776, 1.55904875023)

		##open gripper to place
		hand_group.set_named_target("open")
		plan1 = hand_group.go()
		hand_group.stop()

	def change_station(self):
		##change station
		self.pose_goal(0.512815495686, 0.54697938831, -0.448549280087, 0.486453861617, 0.390815965456, -2.83459126106, 1.74535246983)

	def transfer_object(self):
		## calling defined functions sequentially to complete task
		self.pick()
		self.change_station()
		self.place()

def main():
	try:
	  moveit_commander.roscpp_initialize(sys.argv)
	  rospy.init_node('move_group_python', anonymous=True)
	  robot = moveit_commander.RobotCommander()

	  group = moveit_commander.MoveGroupCommander("kuka_arm")

	  hand_group = moveit_commander.MoveGroupCommander("hand")

	  ## Creating an instance of the class
	  move = MoveGroup(group, hand_group, robot)
		
	  group.set_named_target("initial_pose")
	  plan = group.go()

	  move.transfer_object()
	except rospy.ROSInterruptException:
	    return
	except KeyboardInterrupt:
	    return
if __name__ == '__main__':
  main()

