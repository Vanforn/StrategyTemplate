from bridge.strategy.attacker_Ivan import Attacker_Ivan
import math  # type: ignore
from time import time  # type: ignore
from typing import Optional

from bridge import const
from bridge.auxiliary import aux, fld, rbt  # type: ignore
from bridge.const import State as GameStates
from bridge.router.base_actions import Action, Actions, KickActions  # type: ignore

def TIMEOUT(field: fld.Field, actions: list[Optional[Action]],  we_active: bool) -> None:
    if len(field.active_allies(True)) > 0:
        one = field.gk_id
        two, three = GetIds(field, actions)
        if field.ally_goal.center_up.y > field.ally_goal.center_down.y:
            actions[one] = Actions.GoToPoint(field.ally_goal.center_up + aux.Point(0, 100), 0)
            if two is not None:
                actions[two] = Actions.GoToPoint(field.ally_goal.center_up + aux.Point(0, 250), 0)
            if three is not None:
                actions[three] = Actions.GoToPoint(field.ally_goal.center_up + aux.Point(0, 400), 0)
        else:
            actions[one] = Actions.GoToPoint(field.ally_goal.center_down + aux.Point(0, 100), 0)
            if two is not None:
                actions[two] = Actions.GoToPoint(field.ally_goal.center_down + aux.Point(0, 400), 0)
            if three is not None:
                actions[three] = Actions.GoToPoint(field.ally_goal.center_down + aux.Point(0, 700), 0)


def PREPARE_PENALTY(field: fld.Field, actions: list[Optional[Action]],  we_active: bool) -> None:
    if len(field.active_allies(True)) > 0:
        gkId = field.gk_id
        saId, faId = GetIds(field, actions)

        if saId is None and faId is not None:
            saId = faId
        elif faId is None and saId is None:
            saId = gkId

        if faId is None and saId is not None:
            faId = saId
        elif faId is None and saId is None:
            faId = gkId

        if gkId is not None:
            gk_pos = field.allies[gkId].get_pos()
            gk = field.enemies[gkId]
        if faId is not None:
            atacker_first_pos = field.allies[faId].get_pos()
            atacker_first = field.allies[faId]

        if saId is not None:
            atacker_second_pos = field.allies[saId].get_pos()
            atacker_second = field.allies[saId]

        point_first = aux.Point(const.FIELD_DX / 2 * -field.polarity, const.FIELD_DY / 2)
        point_second = aux.Point(const.FIELD_DX / 2 * -field.polarity, -const.FIELD_DY / 2)
        if we_active:
            if gkId is not None:
                actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
                # pass
            if faId is not None:
                actions[faId] = Actions.GoToPoint(aux.Point(const.FIELD_DX / 2 * field.polarity, const.FIELD_DY / 2), 0)
                # pass
            if saId is not None:
                actions[saId] = Actions.GoToPoint(aux.Point(200 * -const.POLARITY), (field.ball.get_pos() - atacker_second_pos).arg())
                # pass
        else:
            #code for GK, its for time:
            if gkId is not None:
                actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
            #////
            if faId is not None:
                actions[faId] = Actions.GoToPoint(point_first, 0)
            if saId is not None:
                actions[saId] = Actions.GoToPoint(point_second, 0)
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw   , 0)

def PENALTY(field: fld.Field, actions: list[Optional[Action]],  we_active: bool) -> None:
    if len(field.active_allies(True)) > 0:
        gkId = field.gk_id
        saId, faId = GetIds(field, actions)

        if saId is None and faId is not None:
            saId = faId
        elif faId is None and saId is None:
            saId = gkId

        if faId is None and saId is not None:
            faId = saId
        elif faId is None and saId is None:
            faId = gkId

        if gkId is not None:
            gk_pos = field.allies[gkId].get_pos()
            gk = field.enemies[gkId]
        if faId is not None:
            atacker_first_pos = field.allies[faId].get_pos()
            atacker_first = field.allies[faId]

        if saId is not None:
            atacker_second_pos = field.allies[saId].get_pos()
            atacker_second = field.allies[saId]
        ball = field.ball.get_pos()

        point_first = aux.Point(const.FIELD_DX / 2 * -field.polarity, const.FIELD_DY / 2)
        point_second = aux.Point(const.FIELD_DX / 2 * -field.polarity, -const.FIELD_DY / 2)
        if we_active:
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
            if faId is not None:
                actions[faId] = Actions.GoToPoint  (-point_first, 0)
            point_for_score: Optional[aux.Point] = find_point_to_goal(field, ball)
            if point_for_score is not None and saId is not None:
                actions[saId] = Actions.Kick(point_for_score)

        else:
            #code for GK, its for time:
            actions[gkId] = Actions.GoToPoint(field.ally_goal.center, 0)
            #////
            if faId is not None:
                actions[faId] = Actions.GoToPoint(point_first, 0)
            if saId is not None:
                actions[saId] = Actions.GoToPoint(point_second, 0)
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)

def PREPARE_KICKOFF(field: fld.Field, actions: list[Optional[Action]],  we_active: bool) -> None:
    if len(field.active_allies(True)) > 0:
        gkId = field.gk_id
        saId, faId = GetIds(field, actions)
        actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
        if saId is None and faId is not None:
            saId = faId
        elif faId is None and saId is None:
            saId = gkId

        if faId is None and saId is not None:
            faId = saId
        elif faId is None and saId is None:
            faId = gkId
        print(faId, saId, gkId)
        if we_active:
            if faId is not None:
                actions[faId] = Actions.GoToPoint(aux.Point(600 * -const.POLARITY), 0)
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
            if saId is not None:
                actions[saId] = Actions.GoToPoint(aux.Point(200 * -const.POLARITY), (field.ball.get_pos() - field.allies[saId].get_pos()).arg())
        else:
            y = 130
            x = math.sqrt(600 * 600 - y * y) * -const.POLARITY
            if faId is not None:
                actions[faId] = Actions.GoToPoint(aux.Point(x, y), (field.ball.get_pos() - field.allies[faId].get_pos()).arg())
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
            if saId is not None:
                actions[saId] = Actions.GoToPoint(aux.Point(x, -y), (field.ball.get_pos() - field.allies[saId].get_pos()).arg()) 
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)

            # points_first = aux.get_tangent_points(field.allies[faId].get_pos(), field.allies[gkId].get_pos() + aux.Point(0, 100), 100.0)
            # if points_first[0].y < points_first[1].y:
            #     point_first = points_first[0]
            # else:
            #     point_first = points_first[1]

            # points_first = aux.get_tangent_points(field.allies[saId].get_pos(), field.allies[gkId].get_pos() + aux.Point(0, -100), 100.0)
            # if points_first[0].y < points_first[1].y:
            #     point_second = points_first[1]
            # else:
            #     point_second = points_first[0]
            
            # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[gkId].get_pos() + aux.Point(0, -100) - (field.ball.get_pos() - field.allies[gkId].get_pos() + aux.Point(0, -100)) * 100)
            # field.strategy_image.draw_line(field.ball.get_pos(), field.allies[gkId].get_pos() + aux.Point(0, 100) - (field.ball.get_pos() - field.allies[gkId].get_pos() + aux.Point(0, 100)) * 100)
            # field.strategy_image.draw_line(field.ball.get_pos(), point_first + (field.allies[faId].get_pos() - field.ball.get_pos() + aux.Point(0, -100)) * 100, (0, 0, 0))
            # field.strategy_image.draw_line(field.ball.get_pos(), point_second + (field.allies[saId].get_pos() - field.ball.get_pos() + aux.Point(0, 100)) * 100, (0, 0, 0))
def KICKOFF(field: fld.Field, actions: list[Optional[Action]],  we_active: bool) -> None:
    if len(field.active_allies(True)) > 0:
        gkId = field.gk_id
        saId, faId = GetIds(field, actions)
        
        if saId is None and faId is not None:
            saId = faId
        elif faId is None and saId is None:
            saId = gkId

        if faId is None and saId is not None:
            faId = saId
        elif faId is None and saId is None:
            faId = gkId
        if we_active:
            if saId is not None:
                point_to_kick = find_point_to_goal(field, field.allies[saId].get_pos())
            if point_to_kick is not None:
                if saId is not None:
                    actions[saId] = Actions.Kick(point_to_kick)
            else: 
                if saId is not None and faId is not None and saId != faId:
                    actions[saId] = Actions.Kick(field.allies[faId].get_pos(), is_pass= True)
                elif saId is not None and faId is not None and saId == faId:
                    actions[saId] = Actions.Kick(field.allies[gkId].get_pos(), is_pass= True)
                elif faId is not None:
                    actions[faId] = Actions.Kick(field.allies[gkId].get_pos(), is_pass= True)
                else:
                    actions[gkId] = Actions.Kick(field.enemy_goal.frw)
        else:
            y = 130
            x = math.sqrt(600 * 600 - y * y) * -const.POLARITY
            if faId != saId and faId is not None:
                actions[faId] = Actions.GoToPoint(aux.Point(x, y), (field.ball.get_pos() - field.allies[faId].get_pos()).arg())
            if saId is not None:
                actions[saId] = Actions.GoToPoint(aux.Point(x, -y), (field.ball.get_pos() - field.allies[saId].get_pos()).arg()) 
            actions[gkId] = Actions.GoToPoint(field.ally_goal.frw, 0)
    
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
    #print(bot1.r_id)
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



def find_point_to_goal(field: fld.Field, pointFrom: aux.Point) -> Optional[aux.Point]:
    """
    Find the nearest point to a given point (center) from a list, optionally excluding some points.

    Args:
        center (Point): The reference point.
        points (list[Point]): The list of candidate points.
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

def GetIds(field: fld.Field, actions: list[Optional[Action]]) -> tuple[Optional[int], Optional[int]]:
    '''
    Возвращает id роботов

    id:
        1: вратарь
        2: первый атак.
        3: второй атак.
    '''
    mass_idx: Optional[list]
    mass_idx = [robot.r_id for robot in field.active_allies()]
    gk = field.gk_id
    for bot in mass_idx:
        if mass_idx == gk:
            mass_idx.remove(bot)
            break
    need_none = 2 - len(mass_idx)
    for i in range(0, need_none):
        mass_idx.append(None)
    return mass_idx