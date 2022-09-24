#!/usr/bin/env python3
import rospy
from smach import StateMachine
from smach_ros import SimpleActionState, IntrospectionServer
from smach_practice.msg import SmachPracticeAction, SmachPracticeGoal


if __name__ == "__main__":
    rospy.init_node('state_machine3')
    rospy.loginfo('state_machine3 start')

    sm = StateMachine(['succeeded', 'aborted', 'preempted'])
    with sm:
        goal_1 = SmachPracticeGoal()
        goal_1.message = 'goal_1 message'
        # preempted, aborted...
        StateMachine.add('state_1',
                         SimpleActionState('state_action_server',
                                           SmachPracticeAction, goal=goal_1),
                         transitions={'succeeded': 'state_2'})

        goal_2 = SmachPracticeGoal()
        goal_2.message = 'goal_2 message'
        StateMachine.add('state_2',
                         SimpleActionState('state_action_server',
                                           SmachPracticeAction, goal=goal_2),
                         transitions={'succeeded': 'state_3'})

        goal_3 = SmachPracticeGoal()
        goal_3.message = 'goal_3 message'
        StateMachine.add('state_3',
                         SimpleActionState('state_action_server',
                                           SmachPracticeAction, goal=goal_3),
                         transitions={'succeeded': 'succeeded'})

    # For smach_viewer
    sis = IntrospectionServer('state_machine_server', sm, '/SM_ROOT')
    sis.start()

    outcome = sm.execute()
    print(outcome)
