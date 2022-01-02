#!/usr/bin/env python3
"""
File: state_action_server.py
Description: Test action server
"""

import rospy
import actionlib
from smach_practice.msg import SmachPracticeAction
import time


class StateActionServer:
    def __init__(self):
        self.server = actionlib.SimpleActionServer('state_action_server',
                                                   SmachPracticeAction,
                                                   self.execute, False)
        rospy.loginfo('start state_action_server')
        self.server.start()

    def execute(self, goal):
        rospy.loginfo(goal.message)
        rospy.loginfo('Wait 1sec')
        time.sleep(1)
        self.server.set_succeeded()  # outcome "succeeded"
        # self.server.set_aborted()  # outcome "aborted"
        # self.server.set_preempted()  # outcome "preempted"


if __name__ == "__main__":
    rospy.init_node('state_action_server')
    server = StateActionServer()
    rospy.spin()
