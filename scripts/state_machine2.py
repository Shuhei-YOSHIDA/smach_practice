#!/usr/bin/env python3

import rospy
from smach import State, StateMachine
import time
import smach_ros
import random


class StateA(State):
    def __init__(self):
        State.__init__(self, outcomes=['success', 'failed'])

    def execute(self, userdata):
        print('StateA works for 2 sec')
        time.sleep(2)
        return 'failed'


class StateB(State):
    def __init__(self):
        State.__init__(self, outcomes=['success', 'failed'])

    def execute(self, userdata):
        print('StateB works for 1 sec')
        time.sleep(1)
        num = random.randrange(0, 3)
        if num % 2 == 0:
            return 'success'
        else:
            return 'failed'


class StateC(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])

    def execute(self, userdata):
        print('StateC works for 1 sec')
        time.sleep(1)
        return 'success'


if __name__ == "__main__":
    rospy.init_node('state_machine2')

    sm_top = StateMachine(outcomes=['END'])

    with sm_top:
        StateMachine.add('state_3', StateC(),
                         transitions={'success': 'SubStateMachine'})

        sm = StateMachine(outcomes=['success'])

        with sm:
            StateMachine.add('state_1', StateA(),
                             transitions={'failed': 'state_2'})
            StateMachine.add('state_2', StateB(),
                             transitions={'failed': 'state_1'})
        StateMachine.add('SubStateMachine', sm,
                         transitions={'success': 'END'})

    # For smach_viewer
    sis = smach_ros.IntrospectionServer('state_machine_server', sm_top, '/SM_ROOT')
    sis.start()

    outcome = sm_top.execute()
    rospy.spin()
    print(outcome)
    sis.stop()
