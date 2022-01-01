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
        return 'success'


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


if __name__ == "__main__":
    rospy.init_node('state_machine')
    sm = StateMachine(outcomes=['success', 'failed', 'end'])

    with sm:
        # Initial state is the first added state.
        StateMachine.add('state_1', StateA(),
                         transitions={'success': 'state_2'})
        # transition, [outcome] : [state]
        # or [state outcome] : [state machine outcome] -> terminated
        StateMachine.add('state_2', StateB(),
                         transitions={'success': 'end', 'failed': 'state_1'})

    # For smach_viewer (Currently, not for noetic)
    sis = smach_ros.IntrospectionServer('state_machine_server', sm, '/SM_ROOT')
    sis.start()

    outcome = sm.execute()
    rospy.spin()
    print(outcome)
    sis.stop()
