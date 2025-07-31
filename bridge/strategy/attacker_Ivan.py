import math  # type: ignore
from time import time  # type: ignore
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

class Attacker_Ivan():
    def __init__(self, id: int) -> None:
        self.id = id

    def run(self, field: fld.Field, actions: list[Optional[Action]]) -> None:
        enemies = field.active_enemies(False)
        ally = field.active_allies(False)
        all_robots = enemies + ally
        if len(ally) != 0:
            rbM: rbt.Robot
            rbK: rbt.Robot
            rbM, rbK = GetMyRobot(self.id, field)
            bM = rbM.get_pos()
            bK = rbK.get_pos()

        ball = field.ball.get_pos()
        ball_obj = field.ball

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
                if bK == aux.find_nearest_point(ball, [bM, bK]):
                    if field.is_ball_in(rbK):
                        bot_ , min_ = Find_closest_bot_line(enemies, bK, bM, "S")
                        if min_ < 200:
                            if aux.get_angle_between_points(bot_.get_pos(), bM, bK) > 0:
                                bM = bM + aux.rotate(aux.Point(500,0), rbM.get_angle() + 3.14 / 5)
                            else:
                                bM = bM + aux.rotate(aux.Point(500,0), rbM.get_angle() - 3.14 / 5)
                        # field.strategy_image.draw_circle(aux.nearest_point_on_circle(b2, b1, 1000), (0, 0, 0), 50)
                        actions[self.id] = Actions.GoToPoint(aux.nearest_point_on_circle(bM, bK, 1000), (ball - bM).arg())
                    else:
                        actions[self.id] = Actions.GoToPoint(my_point_to_goal, (my_point_to_goal - bM).arg())
                else:
                    actions[self.id] =Actions.BallGrab((ball - bM).arg())
                    if field.is_ball_in(rbM):
                        point_to_kick = find_point_to_goal(field, field.allies[self.id].get_pos())
                        if point_to_kick is not None:
                            actions[self.id] = Actions.Kick(point_to_kick)
                        else: 
                            actions[self.id] = Actions.Kick(field.allies[rbK.r_id].get_pos(), is_pass= True)

            else:
                if field.is_ball_in(nearest_robot):
                    Close_pass(nearest_robot, rbM, ball, field, actions)
                else:
                    if bM == aux.find_nearest_point(ball, [bM, bK]):
                        point_to_grab = aux.find_nearest_point(bM, [ball + aux.rotate(aux.Point(110, 0), (ball - nearest_robot.get_pos()).arg() - 45 / 180 * 3.14), ball + aux.rotate(aux.Point(110, 0), (ball - nearest_robot.get_pos()).arg() + 45 / 180 * 3.14)])
                        actions[self.id] = Actions.GoToPoint(point_to_grab, (ball - bM).arg(), ignore_ball= True)
                        if (ball - bM).mag() <= 120:
                            actions[self.id] = Actions.BallGrab((ball - bM).arg())
                            if field.is_ball_in(rbM):
                                point_to_goal_now = find_point_to_goal(field, bM)
                                actions[self.id] = Actions.Kick(point_to_goal)
                            if field.is_ball_in(rbM):
                                actions[self.id] = Actions.Kick(bK, is_pass= True)
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
    #print(bot1.r_self.id)
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

    my_self.id = self.id моего робота
    """
    bots = field.active_allies(True)
    bots_id = [bots[0].r_id, bots[1].r_id, bots[2].r_id]
    bots_id.remove(my_id)
    not_my_id = bots_id[0]
    return field.allies[my_id], field.allies[not_my_id]



def find_point_to_goal(field: fld.Field, pointFrom: aux.Point) -> Optional[aux.Point]:
    """
    Find the nearest point to a given point (center) from a list, optionally excluding some points.

    Args:
        center (Point): The reference point.
        points (list[Point]): The list of candself.idate points.
        exclude (Optional[list[Point]]): Points to ignore during the search (default is None).

    Returns:
        Point: The closest point to center that is not in exclude.
    """
    pointFrom = field.ball.get_pos()
    qPoint = 8
    qPoint +=2
    d = field.enemy_goal.up.y - field.enemy_goal.down.y
    points = [aux.Point(field.enemy_goal.up.x, field.enemy_goal.up.y-(d/qPoint*i)) for i in range(1, qPoint)]
    enemys = field.active_enemies(True)
    closest = None
    min_dist = 10e10
    for _, point in enumerate(points):
        if aux.dist(pointFrom, point) < min_dist:
            if all(len(aux.line_circle_intersect(pointFrom, point, enemyR.get_pos(), const.ROBOT_R*1.5, "S")) == 0 for enemyR in enemys):
                """if noone enemy r prevent this kick"""
                min_dist = aux.dist(pointFrom, point)
                closest = point
    if closest != None:
        field.strategy_image.draw_line(pointFrom, closest, color=(0, 255, 0))
    # else:
    #     field.strategy_image.draw_circle(pointFrom, color=(0, 0, 0), size_in_mms=100)
    return closest

def Get_ids(bots: list[rbt.Robot], field: fld.Field, actions: list[Optional[Action]]) -> tuple[int, int, int]:
    '''
    Возвращает self.id роботов

    self.id:
        1: вратарь
        2: первый атак.
        3: второй атак.
    '''
    gk = const.GK
    for bot in bots:
        if bot.r_id == gk:
            bots.remove(bot)
            break
    return gk, bots[0].r_id, bots[1].r_id