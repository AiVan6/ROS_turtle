#! /usr/bin/python3

import rospy
import time
import math
from turtlesim.msg import Pose
from turtlesim.msg import Pose as TurtlePose
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn


class myNode:
	def __init__(self):
		rospy.init_node('turtle_follower_node')

		rospy.wait_for_service('/spawn')
		spawn_func = rospy.ServiceProxy('/spawn',Spawn)
		spawn_func(5.0,5.0, 0.0, 'turtle2')

		rospy.Subscriber('/turtle1/pose',TurtlePose,self.leader_pose_callback)
		rospy.Subscriber('/turtle2/pose',TurtlePose,self.follower_pose_callback)		

		self.pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size = 10)
		
		self.rate = rospy.Rate(10)
		self.leader_pose = None
		self.follower_pose = None
		
		
	def leader_pose_callback(self,data):
		self.leader_pose = data
		
	
	def follower_pose_callback(self,data):
		self.follower_pose = data
		#self.func()
		
	def func(self):
		while not rospy.is_shutdown():
			if self.leader_pose and self.follower_pose:
				self.speed = rospy.get_param('~speed', 1)
				dx = self.leader_pose.x - self.follower_pose.x
				dy = self.leader_pose.y - self.follower_pose.y
				angle_diff = math.atan2(dy, dx)
				distance = math.sqrt(dx**2 + dy**2)
				msg = Twist()
				msg.linear.x = self.speed * distance
				msg.angular.z = 8.0 * (angle_diff - self.follower_pose.theta)

				# Устанавливаем угловую скорость
				self.pub.publish(msg) 
			self.rate.sleep()
	
	def run(self):
		self.func()
		rospy.spin()	
		

	#rospy.spin()
if __name__ =='__main__':
	try:
		node = myNode()
		#node.func()
		node.run()
	except rospy.ROSInterruptException:
		pass


