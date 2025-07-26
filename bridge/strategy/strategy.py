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
        self.time = 0
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

    # def Grab(self, field: fld.Field, id: int, a: int, time: int):
    #     rb = field.allies[id].get_pos()
    #     ball = field.ball.get_pos()
    #     vec = ball - rb
    #     if vec.mag() > 120:





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
git rebase upstream/master
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

        enemies = field.active_enemies(True)

        idb4 = 4
        b4 = field.allies[idb4].get_pos()
        rb4 = field.allies[idb4]

        spin = self.count / 180 * 3.14

        idy4 = 4
        y4 = field.enemies[idy4].get_pos()
        ry4 = field.enemies[idy4]

        idb0 = 0
        b0 = field.enemies[idb0].get_pos()
        rb0 = field.enemies[idb0]

        idy0 = 0
        y0 = field.enemies[idy0].get_pos()
        ry0 = field.enemies[idy0]

        idb5 = 5
        b5 = field.allies[idb5].get_pos()

        ball = field.ball.get_pos()
        #field.strategy_image.draw_circle(ball, (0, 255, 255), 50)
        

        center = field.enemy_goal.center
        frw = field.enemy_goal.frw

        a_up = field.ally_goal.frw_up
        a_down = field.ally_goal.frw_down
        ac_up = field.ally_goal.center_up
        ac_down = field.ally_goal.center_down
        e_up = field.enemy_goal.frw_up
        e_down = field.enemy_goal.frw_down
        ec_up = field.enemy_goal.center_up
        ec_down = field.enemy_goal.center_down
        hull1 = field.ally_goal.hull
        hull2 = field.enemy_goal.hull

        point1 = aux.nearest_point_in_poly(b4, hull1)
        point2 = aux.nearest_point_in_poly(b4, hull2)

        if (point1 - b4).mag() <= (point2 - b4).mag():
            point = point1
        else:
            point = point2
        

        #vec = (y0 - b0) / 8

        
        #actions[0] = Actions.GoToPointIgnore(ball, alf)
        #actions[4] = Actions.GoToPointIgnore(ball + vec, alf)

        self.count += 10
        if self.count >= 360:
            self.count = 0


        # match self.id:
        #     case 1:
        #         actions[4] = Actions.GoToPointIgnore(ball, spin)
        #     case 2:
        #         actions[4] = Actions.GoToPointIgnore(point, spin)

        # if self.id == 1 and (ball - b4).mag() <= 120:
        #     self.id = 2
        # if self.id == 2 and  (point - b4).mag() <= 100:
        #     self.id = 1
        # print(self.id)

        # rb = fld.find_nearest_robot(ball, enemies)
        # robot = rb.get_pos()
        # min_ = 9999999999
        # bot_: rbt.Robot = None
        # for bot in enemies:
        #     p = aux.closest_point_on_line(robot, ball, bot.get_pos(), "R")
        #     if (p - bot.get_pos()).mag() < min_ and bot != rb:
        #         min_ = (p - bot.get_pos()).mag()
        #         bot_ = bot
        # if bot_ is not None:
        #     point = aux.closest_point_on_line(robot, bot_.get_pos(), b4)
        #     field.strategy_image.draw_circle(point, (0, 255, 255), 50)
        #     field.strategy_image.draw_circle(robot, (0, 0, 0), 50)
        #     field.strategy_image.draw_circle(bot_.get_pos(), (255, 255, 255), 50)
        #     if (point - robot).mag() >= 500:
        #         actions[4] = Actions.GoToPointIgnore(point, (ball - b4).arg())
        #     else:
        #         actions[4] = Actions.GoToPointIgnore(point, (ball - b4).arg())
        #     #actions[5] = Actions.GoToPointIgnore(ball, spin)
        #     speed = b4

        # min_ = 9999999999
        # yes = 0
        # bot_: rbt.Robot = None
        # p = aux.Point(0, 0)
        # for bot in enemies:
        #     p = aux.closest_point_on_line(b4, ball, bot.get_pos(), "S")
        #     if (p - bot.get_pos()).mag() < min_:
        #         min_ = (p - bot.get_pos()).mag()
        #         bot_ = bot

        # if bot_ is not None:
        #     field.strategy_image.draw_circle(aux.closest_point_on_line(b4, ball, bot_.get_pos(), "S"), (0, 0, 0), 50)
        #     b = bot_.get_pos()
        #     if min_ <= 200:
        #         yes = 1
        #     else:
        #         yes = 0
            
        #     if aux.get_angle_between_points(b4, ball, b) < 0 and yes == 1:
        #         vec = aux.rotate(b4 - ball, 10 / 80 * 3.14)
        #         actions[4] = Actions.GoToPointIgnore(ball + vec, (ball - b4).arg())
        #     elif aux.get_angle_between_points(b4, ball, b) > 0 and yes == 1:
        #         vec = aux.rotate(b4 - ball, -(10 / 80 * 3.14))
        #         actions[4] = Actions.GoToPointIgnore(ball + vec, (ball - b4).arg())
        #     if b4.x < 0:
        #         print(b4.x)
        #         actions[4] = Actions.GoToPointIgnore(b4 + aux.Point(1000, 0), (ball - b4).arg())
        #     # actions[5] = Actions.GoToPointIgnore(ball, spin)

        vec = aux.Point(110, 0)
        vec = aux.rotate(vec, aux.get_angle_between_points(aux.Point(0,0), center, ball))
        if (vec + ball - b4).mag() >= 50:
            print((vec + ball - b4).mag())
            actions[4] = Actions.GoToPoint(ball + vec, (ball - b4).arg())
            field.strategy_image.draw_circle(ball + vec, (0, 0, 0), 50)
        else:
            actions[4] = Actions.GoToPoint(b4 + aux.rotate(aux.Point(100,0), aux.get_angle_between_points(vec + b4, b4, frw)), (ball - b4).arg(), True, True)
            field.strategy_image.draw_circle(frw, (255, 255, 0), 50)