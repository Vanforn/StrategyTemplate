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
        self.count = 0
        self.id = 1
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
<<<<<<< HEAD
=======
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
        rb4 = field.allies[idb4]
        alf4 = 3.14 / 4 * idb4 + time() / 3

        alf = self.count / 180 * 3.14

        idb3 = 3
        b3 = field.allies[idb3].get_pos()

        idb0 = 0
        b0 = field.allies[idb0].get_pos()

        idy0 = 0
        y0 = field.enemies[idy0].get_pos()

        idb5 = 5
        b5 = field.allies[idb5].get_pos()


        ball = field.ball.get_pos()
        center = field.ally_goal.center
        a_up = field.ally_goal.frw_up
        a_down = field.ally_goal.frw_down
        e_up = field.enemy_goal.frw_up
        e_down = field.enemy_goal.frw_down

        #vec = (y0 - b0) / 8
        vec = aux.Point(500, 0)
        vec = aux.rotate(vec, alf4)

        actions[5] = Actions.GoToPointIgnore(ball, alf)
        actions[0] = Actions.GoToPointIgnore(ball, alf)
        #actions[4] = Actions.GoToPointIgnore(ball + vec, alf)

        self.count += 10
        if self.count >= 360:
            self.count = 0

        if self.id == 1:
            actions[4] = Actions.GoToPointIgnore(a_up, alf)
            if a_up.x - 10 < b4.x < a_up.x + 10 and a_up.y - 10 < b4.y < a_up.y + 10:
                self.id = 2
        elif self.id == 2:
            actions[4] = Actions.GoToPointIgnore(a_down, alf)
            if a_down.x - 10 < b4.x < a_down.x + 10 and a_down.y - 10 < b4.y < a_down.y + 10:
                self.id = 3
        elif self.id == 3:
            actions[4] = Actions.GoToPointIgnore(e_up, alf)
            if e_up.x - 10 < b4.x < e_up.x + 10 and e_up.y - 10 < b4.y < e_up.y + 10:
                self.id = 4
        elif self.id == 4:
            actions[4] = Actions.GoToPointIgnore(e_down, alf)
            if e_down.x - 10 < b4.x < e_down.x + 10 and e_down.y - 10 < b4.y < e_down.y + 10:
                self.id = 1
        
        # point =  aux.closest_point_on_line(center, ball, b4, 'S')
        # print(point)


        #actions[4] = Actions.GoToPointIgnore(center, 0)

       
        # if  ball.x + 10 > b4.x > ball.x + 5 and  ball.y - 3 < b4.y < ball.y + 3:
        #     actions[4] = Actions.GoToPointIgnore(center, (center - b4).arg())
        # else:
        #    actions[4] = Actions.BallGrab(3.14)
