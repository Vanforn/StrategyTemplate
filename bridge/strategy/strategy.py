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


        # point1 = aux.nearest_point_in_poly(b4, hull1)
        # point2 = aux.nearest_point_in_poly(b4, hull2)

        # if (point1 - b4).mag() <= (point2 - b4).mag():
        #     point = point1
        # else:
        #     point = point2
        

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
        #     p = aux.closest_point_on_line(b1, b2 + aux.Point(300, 0), bot.get_pos(), "S")
        #     if (p - bot.get_pos()).mag() < min_:
        #         min_ = (p - bot.get_pos()).mag()
        #         bot_ = bot

        # if bot_ is not None:
        #     b = bot_.get_pos()
        #     if min_ <= 200:
        #         yes = 1
        #     else:
        #         yes = 0
            
        #     if yes == 1:
        #actions[1] = Actions.Kick(b2, const.VOLTAGE_SHOOT, True)
        if field.ally_color == const.Color.BLUE:
            
            enemies = field.active_enemies(True)
            ally = field.active_allies(True)
            all_robots = enemies + ally
            if len(ally) != 0:
                rbM: rbt.Robot
                rbK: rbt.Robot
                rbM, rbK = GetMyRobot(2, field)
                bM = rbM.get_pos()
                bK = rbK.get_pos()

            idb0 = 0
            b0 = field.allies[idb0].get_pos()
            rb0 = field.enemies[idb0]

            idb1 = 1
            b1 = field.allies[idb1].get_pos()
            rb1 = field.allies[idb1]

            idb2 = 2
            b2 = field.allies[idb2].get_pos()
            rb2 = field.allies[idb2]

            spin = self.count / 180 * 3.14


            idy0 = 0
            y0 = field.enemies[idy0].get_pos()
            ry0 = field.enemies[idy0]


            ball = field.ball.get_pos()
            ball_obj = field.ball
            #field.strategy_image.draw_circle(ball, (0, 255, 255), 50)
            

            centerEnemy = field.enemy_goal.center
            centerAlly = field.ally_goal.center
            frw = field.enemy_goal.frw

            frw_upA = field.ally_goal.frw_up
            frw_downA = field.ally_goal.frw_down
            center_upA = field.ally_goal.center_up
            center_downA = field.ally_goal.center_down

            center_upE = field.enemy_goal.frw_up
            center_downE = field.enemy_goal.frw_down
            center_upE = field.enemy_goal.center_up
            center_downE = field.enemy_goal.center_down

            hullA = field.ally_goal.hull
            hullE = field.enemy_goal.hull

            upE = field.enemy_goal.up
            downE = field.enemy_goal.down

            upA = field.ally_goal.up
            downA = field.ally_goal.down

            fupE = field.enemy_goal.frw_up
            fdownE = field.enemy_goal.frw_down

            fupA = field.ally_goal.frw_up
            fdownA = field.ally_goal.frw_down

            # bot 1 closer
            bot_ , min_ = Find_closest_bot_line(enemies, b1, b2, "S")
            enemyClose = 0
            if const.ENEMY_GK == 0:
                enemyClose = 2
            
            bEnemy = field.enemies[enemyClose].get_pos()
            rbEnemy = field.enemies[enemyClose]


            rad: float
            if (bEnemy - ball).mag() > 400:
                rad = 400
            else:
                rad = (bEnemy - ball).mag() - 50
            
            # point = aux.nearest_point_on_circle(ball, bEnemy, rad)
            # if rad < 400 and min_ > 200:
            #     actions[1] = Actions.Kick(b2, const.VOLTAGE_SHOOT, True)
            # elif rad < 400 and min_ < 200:
            #     if aux.get_angle_between_points(bot_.get_pos(), b2, b1) > 0:
            #         b2 = b2 + aux.rotate(aux.Point(200,0), rb2.get_angle() + 3.14 / 5)
            #     else:
            #         b2 = b2 + aux.rotate(aux.Point(200,0), rb2.get_angle() - 3.14 / 5)
            #     actions[2] = Actions.GoToPoint(aux.nearest_point_on_circle(b2, bEnemy, rad), (ball - b2).arg())
            # else:
            #     actions[1] = Actions.GoToPoint(point, (ball - b1).arg())
            #/////////////////////////////////////////////


            #bot 2 attacker
            if len(enemies) != 0:
                #поиск 2 тотчек для удара
                nearest_robot = fld.find_nearest_robot(ball, all_robots)
                point_to_goal_up = aux.Point(const.FIELD_DX / 2 * -field.polarity, const.FIELD_DY / 2)
                point_to_goal_down = aux.Point(const.FIELD_DX / 2 * -field.polarity, -const.FIELD_DY / 2)
                point_to_goal = aux.find_nearest_point(bM, [point_to_goal_down, point_to_goal_up])

                #если ближайший робот союзник, то едет к точке удара, к которой не едет другой атакующий
                if nearest_robot.color == const.COLOR:
                    not_my_point_to_goal = aux.find_nearest_point(bK, [point_to_goal_down, point_to_goal_up])
                    points = [point_to_goal_down, point_to_goal_up]
                    points.remove(not_my_point_to_goal)
                    my_point_to_goal = points[0]
                    field.strategy_image.draw_line(bM, my_point_to_goal, (0, 255, 255), 20)
                    actions[rbM.r_id] = Actions.GoToPoint(my_point_to_goal, (my_point_to_goal - bM).arg())
                else:
                    if field.is_ball_in(nearest_robot):
                        Close_pass(nearest_robot, rbM, ball, field, actions)
                    else:



                # nearest_robotE = fld.find_nearest_robot(ball, enemies)
                # Close_pass(nearest_robotE, rbM, ball, field, actions)

            # pointDown = field.enemy_goal.eye_up
            # old_b2 = b2
            # pointUp = -field.enemy_goal.eye_up
            # yesUp = 0
            # yesDown= 0
            # for bot in enemies:
            #     p1 = aux.closest_point_on_line(b2, upE, bot.get_pos(), "S")
            #     p2 = aux.closest_point_on_line(b2, downE, bot.get_pos(), "S")
            #     if (p1 - bot.get_pos()).mag() < 250:
            #         yesUp = 1
            #     elif (p2 - bot.get_pos()).mag() < 200:
            #         yesDown = 1

            # if (ball - b2).mag() >= 500 and rad >= 400:
            #     actions[2] = Actions.BallGrab((ball - b2).arg())
            # elif (ball - b2).mag() < 500:
            #     if not yesUp:
            #         # if (ball - b2).mag() < 250:
            #         #     self.time += 1
            #         # actions[2] = Actions.GoToPoint(ball + aux.rotate(aux.Point(150, 0), (ball - upE).arg()), (ball - b2).arg())
            #         # field.strategy_image.draw_circle(b2, [0, 0, 0], 50)
            #         # if(self.time >= 150):
            #         actions[2] =Actions.Kick(upE + pointUp)
            #             # self.time = 0
            #     elif not yesDown:
            #         if  (ball - b2).mag() < 500:
            #             self.time += 1
            #         actions[2] = Actions.GoToPoint(ball + aux.rotate(aux.Point(150, 0), (ball - upE).arg()), (ball - b2).arg())
            #         field.strategy_image.draw_circle(b2, [0, 0, 0], 50)
            #         if self.time >= 100 and (ball - b2).mag() < 150:
            #             actions[2] =Actions.Kick(downE + pointDown)
            #         if (ball - b2).mag() > 500:
            #             self.time = 0
            #     else:
            #         actions[2] =Actions.Kick(b1, const.VOLTAGE_SHOOT ,True)
            # elif rad < 400:
            #     # if const.ENEMY_GK == 0:
            #     bot_ , min_ = Find_closest_bot_line(enemies, b1, b2, "S")
            #     if min_ < 200:
            #         if aux.get_angle_between_points(bot_.get_pos(), b2, b1) > 0:
            #             b2 = b2 + aux.rotate(aux.Point(200,0), rb2.get_angle() + 3.14 / 5)
            #         else:
            #             b2 = b2 + aux.rotate(aux.Point(200,0), rb2.get_angle() - 3.14 / 5)
            #     field.strategy_image.draw_circle(aux.nearest_point_on_circle(b2, b1, 1000), (0, 0, 0), 50)
            #     field.strategy_image.draw_line(old_b2, b1)
            #     actions[2] = Actions.GoToPoint(aux.nearest_point_on_circle(b2, b1, 1000), (ball - b2).arg())
            #/////////////////////////////////////////////





            #bot 0 gk
            
            point_gk1 = aux.line_circle_intersect(ball, ball_obj.get_vel(), centerAlly, (upA - centerAlly + (center_upA - upA) / 2).mag(), "R")
            if len(point_gk1) == 2:
                point_gk2 = aux.closest_point_on_line(center_downA, center_upA, ball, "S")
                actions[0] = Actions.GoToPointIgnore(point_gk2, (ball - b0).arg())
            elif aux.is_point_inside_poly(ball, hullA):
                if b2.x > 0:
                    actions[0] = Actions.Kick(b2)
                    if b0.x < center_upA.x:
                        b0.x = center_upA.x
                else:
                    actions[0] = Actions.Kick(b2, const.VOLTAGE_SHOOT, True)
                    if b0.x < center_upA.x:
                        b0.x = center_upA.x
            else:
                actions[0] = Actions.GoToPointIgnore(aux.closest_point_on_line(center_downA, center_upA, ball, "S"), (ball - b0).arg())
            #/////////////////////////////////

            # yesUp = 0
            # yesDown= 0
            # for bot in enemies:
            #     p1 = aux.closest_point_on_line(b1, up, bot.get_pos(), "S")
            #     p2 = aux.closest_point_on_line(b1, down, bot.get_pos(), "S")
            #     if (p1 - bot.get_pos()).mag() < 200:
            #         yesUp = 1
            #     elif (p2 - bot.get_pos()).mag() < 200:
            #         yesDown = 1

            # if (ball - b1).mag() >= 150 and (ball - b1).mag() < (ball - b2).mag():
            #     actions[1] = Actions.BallGrab((ball - b1).arg())
            # elif (ball - b1).mag() < 150:
            #     if not yesUp:
            #         actions[1] =Actions.Kick(up + pointUp)
            #     elif not yesDown:
            #         actions[1] =Actions.Kick(down + pointDown)
            #     else:
            #         actions[1] =Actions.Kick(b2, const.VOLTAGE_SHOOT, True)
            # else: 
            #     # if const.ENEMY_GK == 0:
            #     actions[1] = Actions.GoToPoint(fup + aux.Point(-300, 300), (ball - b1).arg())
            #     print("b1")

        else:
            enemies = field.active_enemies(True)

            idb0 = 0
            b0 = field.enemies[idb0].get_pos()
            rb0 = field.enemies[idb0]

            idb1 = 1
            b1 = field.allies[idb1].get_pos()
            rb1 = field.allies[idb1]

            idb2 = 2
            b2 = field.allies[idb2].get_pos()
            rb2 = field.allies[idb2]

            spin = self.count / 180 * 3.14


            idy0 = 0
            y0 = field.enemies[idy0].get_pos()
            ry0 = field.enemies[idy0]


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

            up = field.enemy_goal.up
            down = field.enemy_goal.down

            fup = field.enemy_goal.frw_up
            fdown = field.enemy_goal.frw_down

            

def Find_closest_bot_line(bots: list[rbt.Robot], p1: aux.Point, p2: aux.Point, type_: str) -> tuple[rbt.Robot, float]:
    min_: float = 9999999999
    bot_: Optional[rbt.Robot] = None
    p = aux.Point(0, 0)
    for bot in bots:
        p = aux.closest_point_on_line(p1, p2, bot.get_pos(), type_)
        if (p - bot.get_pos()).mag() < min_:
            min_ = (p - bot.get_pos()).mag()
            bot_ = bot
    return bot_, min_ # type:ignore

def Close_pass(bot1: rbt.Robot, bot2: rbt.Robot, target: aux.Point,field: fld.Field, actions: list[Optional[Action]]) -> None:
    """
    Блокирует пас ближайшеиу роботу от робота цели.

    аргументы:
        bot1 = робот которого надо блокировать.
        bot2 = робот для блокировки.
        minR = 
        target = на какую точку смотреть.
        field =  field.
        acnions = actions.
    """
    botPos1 = bot1.get_pos()
    botPos2 = bot2.get_pos()
    enemies = field.enemies.copy()
    print(bot1.r_id)
    enemies.remove(bot1)
    botClose = aux.find_nearest_point(field.ball.get_pos(),[enemies[0].get_pos(), enemies[1].get_pos()])#[enemies[0].get_pos(), enemies[1].get_pos()]
    field.strategy_image.draw_circle(botClose, (255, 0, 255), 50)
    vec = aux.Point(150, 0)
    vec_first = aux.rotate(vec, (botPos1 - botPos2).arg())
    field.strategy_image.draw_circle(vec_first, (0, 255 ,255), 50)
    vec_second = aux.rotate(vec, (botClose - botPos2).arg())
    field.strategy_image.draw_circle(vec_second, (255, 255 ,0), 50)
    point_to_go = aux.closest_point_on_line(botPos1 + vec_first, botClose + vec_second, botPos2, "S")
    field.strategy_image.draw_circle(point_to_go, (0, 0 ,0), 50)
    actions[bot2.r_id] = Actions.GoToPoint(point_to_go, (target - botPos2).arg(), ignore_ball=True)
    field.strategy_image.draw_line(botClose, botPos2)


def GetMyRobot(my_id: int, field: fld.Field) -> tuple[rbt.Robot, rbt.Robot]:
    """
    Возвращает моего и Костиного робота

    my_id = id моего робота
    """
    bots = field.active_allies(True)
    bots_id = [bots[0].r_id, bots[1].r_id, bots[2].r_id]
    bots_id.remove(my_id)
    not_my_id = bots_id[0]
    return field.allies[my_id], field.allies[not_my_id]