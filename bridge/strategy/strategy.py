"""High-level strategy code"""

# !v DEBUG ONLY
import math  # type: ignore
from time import time  # type: ignore
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore


class Strategy:
    """Main class of strategy"""

    def __init__(
        self,
    ) -> None:
        self.we_active = False

    def process(self, field: fld.Field) -> list[Optional[Action]]:
        """Game State Management"""
        if field.game_state not in [GameStates.KICKOFF, GameStates.PENALTY]:
            if field.active_team in [const.Color.ALL, field.ally_color]:
                self.we_active = True
            else:
                self.we_active = False

        actions: list[Optional[Action]] = []
        for _ in range(const.TEAM_ROBOTS_MAX_COUNT):
            actions.append(None)

        if field.ally_color == const.COLOR:
            text = str(field.game_state) + "  we_active:" + str(self.we_active)
            field.strategy_image.print(aux.Point(600, 780), text, need_to_scale=False)
        match field.game_state:
            case GameStates.RUN:
                self.run(field, actions)
            case GameStates.TIMEOUT:
                pass
            case GameStates.HALT:
                return [None] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY:
                pass
            case GameStates.PENALTY:
                pass
            case GameStates.PREPARE_KICKOFF:
                pass
            case GameStates.KICKOFF:
                pass
            case GameStates.FREE_KICK:
                pass
            case GameStates.STOP:
                # The router will automatically prevent robots from getting too close to the ball
                self.run(field, actions)

        return actions

    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        """
        ONE ITERATION of strategy
        NOTE: robots will not start acting until this function returns an array of actions,
              if an action is overwritten during the process, only the last one will be executed)

        Examples of getting coordinates:
        - field.allies[8].get_pos(): aux.Point -   coordinates  of the 8th  robot from the allies
        - field.enemies[14].get_angle(): float - rotation angle of the 14th robot from the opponents

        - field.ally_goal.center: Point - center of the ally goal
        - field.enemy_goal.hull: list[Point] - polygon around the enemy goal area


        Examples of robot control:
        - actions[2] = Actions.GoToPoint(aux.Point(1000, 500), math.pi / 2)
                The robot number 2 will go to the point (1000, 500), looking in the direction π/2 (up, along the OY axis)

        - actions[3] = Actions.Kick(field.enemy_goal.center)
                The robot number 3 will hit the ball to 'field.enemy_goal.center' (to the center of the enemy goal)

        - actions[9] = Actions.BallGrab(0.0)
                The robot number 9 grabs the ball at an angle of 0.0 (it looks to the right, along the OX axis)
        """
        # idx = 0
        # ally_pos = field.allies(idx)
        #get_line_intersection
        # ball_pos = field.ball.get_pos()
        # print((ally_pos - ball_pos) / 2)

        # idxB0 = 0
        # idxB1 = 1
        # idxY0 = 0
        # b0 = field.allies[idxB0].get_pos()
        # b1 = field.allies[idxB1].get_pos()
        # y0 = field.enemies[idxY0].get_pos()
        # ball = field.ball.get_pos()
        # point = aux.get_line_intersection(b0, b1, y0, ball, 'LL')
        # print(point)

        idb4 = 4
        b4 = field.allies[idb4].get_pos()

        idy4 = 4
        y4 = field.enemies[idy4].get_pos()

        ball = field.ball.get_pos()
        center = field.ally_goal.center
        # point =  aux.closest_point_on_line(center, ball, b4, 'S')
        # print(point)

        rb4 = field.allies[idb4]

        actions[4] = Actions.GoToPointIgnore(y4, (y4 - b4).arg())

       
        if field.is_ball_in(rb4):
            actions[4] = Actions.GoToPointIgnore(center, (center - b4).arg())
        elif b4.x > ball.x:
             actions[4] = Actions
             actions[4] = Actions.GoToPointIgnore(ball, (ball - b4).arg())
        else:
            actions[4] = Actions.BallGrab(180)