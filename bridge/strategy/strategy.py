"""High-level strategy code"""

# !v DEBUG ONLY
from bridge.strategy.attacker_Ivan import Attacker_Ivan
from bridge.strategy.myFunc import *
from bridge.strategy import states
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
        self.baLL = None
        self.attacker_Ivan = Attacker_Ivan(6)

        self.state = 1
        self.idGettingPass = None
        self.idDoPass = None
        self.GKLastState = None
        self.YGKLastState = None

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
            print(text)
        match field.game_state:
            case GameStates.RUN: #OK
                self.run(field, actions)
            case GameStates.TIMEOUT: #READY
                states.TIMEOUT(field, actions, self.we_active)
            case GameStates.HALT: #READY
                return [Actions.Stop()] * const.TEAM_ROBOTS_MAX_COUNT
            case GameStates.PREPARE_PENALTY: #READY
                states.PREPARE_PENALTY(field, actions, self.we_active)
            case GameStates.PENALTY:#READY
                states.PENALTY(field, actions, self.we_active)
            case GameStates.PREPARE_KICKOFF:#READY
                states.PREPARE_KICKOFF(field, actions, self.we_active)
            case GameStates.KICKOFF:#READY
                states.KICKOFF(field, actions, self.we_active)
            case GameStates.FREE_KICK: #READY
                self.run(field, actions)
            case GameStates.STOP: #READY
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
            
            # if self.baLL is None:
            #     self.baLL = field.ball.get_pos()
            # print(-(self.baLL - field.ball.get_pos()).x)

            enemies = field.active_enemies(False)
            ally = field.active_allies(False)
            all_robots = enemies + ally
            # if len(ally) != 0:
            #     rbM: rbt.Robot
            #     rbK: rbt.Robot
            #     rbM, rbK = GetMyRobot(2, field)
            #     bM = rbM.get_pos()
            #     bK = rbK.get_pos()

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
            # if len(ally) > 0:
            #     self.attacker_Ivan.run(field, actions)
        idKostyaAttacker = 5
        idIvanAttacker = 6
        play = True
        if len(field.active_allies(True)) != 0:
            if field.ally_color == const.Color.BLUE:
                """code for blue"""
                # thisR = field.allies[0]
                # enemies = field.active_enemies(True)
                # nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemies)
                # otherAttackerR = field.allies[2]
                # ballPos = field.ball.get_pos()
                # actions[0] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())

                #if play:
                    # self.attacker(field, actions, 0, 2)
                 
                self.attacker_Ivan.run(field, actions)
                self.attacker(field, actions, idKostyaAttacker, idIvanAttacker)
                if field.allies[const.GK].is_used():
                    self.GKLastState = GK(field, actions, self.GKLastState)
            
                
                # goToNearestScorePoint(field, actions, 0, 2)
                # goToNearestScorePoint(field, actions, 2, 0)
                # print(len(field.active_enemies()), [r.r_id for r in field.active_enemies()])
                # if len(field.active_enemies()) == 2:
                #     idx = 0
                #     rPos = field.allies[idx].get_pos()
                #     ballPos = field.ball.get_pos()
                #     # enemyRPos = field.allies[3].get_pos() # HARD CODE
                #     enemyRsPos = field.active_enemies().copy()
                #     # print(len(enemyRsPos))
                #     enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                #     enemyRPos = enemyRsPos[0]
                #     # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                #     pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                #     actions[idx] = Actions.GoToPoint(pointGo, 0)
                # goToNearestScorePoint(field, actions, 0, 2)
                # self.attacker(field, actions, 0, 2)
                # if field.is_ball_in(field.allies[1]):
                #     actions[1] = Actions.GoToPoint(field.enemy_goal.center, (field.enemy_goal.center-field.allies[1].get_pos()).arg(), ignore_ball=True)
                #     field.allies[1].set_dribbler_speed(1)
                # else:
                #     actions[1] = Actions.BallGrab((field.enemy_goal.center-field.allies[1].get_pos()).arg())
                # self.attacker(field, actions, 2, 0)
                
                # p = findPointForScore(field) # for change koef
                # if p != None:
                #     actions[2] = Actions.Kick(p)
                # self.GKLastState = GK(field, actions, self.GKLastState) # for change koef
                # openForPass(field, 2, actions)
                # self.attacker(field, actions, 0, 2)
                # if not field.is_ball_in(field.allies[0]):
                #     actions[0] = Actions.BallGrab((field.ball.get_pos() - field.allies[0].get_pos()).arg())
                # else:
                #     field.strategy_image.draw_circle(field.allies[0].get_pos(), (255, 255, 255), 50)
                # self.attacker(field, actions, 1, 0)
                # """do pass"""
                # if self.idGettingPass != None:
                #     if not field.is_ball_in(field.allies[self.idGettingPass]):
                #         field.strategy_image.send_telemetry("status pass", "getting pass")
                #         actions[self.idGettingPass] = Actions.BallGrab((field.ball.get_pos()-field.allies[self.idGettingPass].get_pos()).arg())
                #     else:
                #         field.strategy_image.send_telemetry("status pass", "get pass")
                #         self.idDoPass = self.idGettingPass
                #         self.idGettingPass = None
                # # actions[0] = Actions.GoToPoint(aux.Point(0, 0), 0)
                # # findPointForScore(field, field.ball.get_pos())
                # # attacker(field, actions, 0, 1)
                
                # if field.is_ball_in(field.allies[self.idDoPass]):
                #     """do pass"""
                #     # field.strategy_image.send_telemetry("status", "pass")
                #     self.idGettingPass = doPassNearAllly(field, actions, self.idDoPass)
                # elif self.idGettingPass == None:
                #     """grab ball"""
                #     # field.strategy_image.send_telemetry("status", "grab")
                #     actions[self.idDoPass] = Actions.BallGrab((field.ball.get_pos() - field.allies[self.idDoPass].get_pos()).arg())  
                # else:
                #     """pass done"""
                #     # actions[self.idDoPass] = Actions.GoToPoint(aux.Point(0, 0), 0)  
                # # actions[0] = Actions.BallGrab((field.enemy_goal.center - field.ball.get_pos()).arg())  
                # # print(actions[0])
                # # actions[0] = Actions.Kick(field.enemy_goal.center)
            else:
                self.attacker_Ivan.run(field, actions)
                self.attacker(field, actions, idKostyaAttacker, idIvanAttacker)
                if field.allies[const.GK].is_used():
                    self.GKLastState = GK(field, actions, self.GKLastState)
                """code for yellow"""
                # findNearestScorePoint(field, actions, 0, 2)
                # enemies = field.active_enemies(True)
                # ballPos = field.ball.get_pos()
                # nearestEnemyR = fld.find_nearest_robot(ballPos, enemies)
                # actions[2] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())
                # actions[0] = Actions.BallGrab((-field.ball.get_pos() + field.enemy_goal.center).arg())#TEST
                #if play:
                # if field.allies[const.GK].is_used():
                #     self.YGKLastState = GK(field, actions, self.YGKLastState) 
                # #self.attacker(field, actions, 0, 2)
                # # try: 
                # #     self.attacker_Ivan.run(field, actions)
                # # except:
                # #     pass
                # self.attacker(field, actions, idKostyaAttacker, idIvanAttacker)
                # # now = time()%8//4 # for change koef
                # match now:
                #     case 0:
                #         # pointF = field.ally_goal.center_down
                #         pointF = aux.Point(0, 200)
                #         field.strategy_image.draw_circle(aux.Point(0, 200), (200, 0, 0), 50)
                #         # print("1")
                #     case 1:
                #         # pointF = field.ally_goal.frw_down
                #         pointF = aux.Point(0, 0)
                #         field.strategy_image.draw_circle(aux.Point(0, 0), (200, 0, 0), 50)
                #         # print(2)
                # actions[const.GK] = Actions.GoToPointIgnore(aux.Point(pointF.x+100, pointF.y), 0)

                # actions[const.GK] = Actions.GoToPoint(aux.Point(0, 0), 0)/
                
                # pointForGK = aux.nearest_point_on_poly(field.ball.get_pos(), field.ally_goal.hull)
                # field.strategy_image.draw_line(pointForGK, field.ball.get_pos(), color=(200, 0, 200), size_in_pixels=20)
                # actions[const.GK] = Actions.GoToPointIgnore(pointForGK, (field.ball.get_pos()-field.allies[const.GK].get_pos()).arg())
                # field.allies[const.GK].set_dribbler_speed(1)

                # rPos = field.allies[1].get_pos()
                # nearestScorePoint = None
                # firstScorePoint = aux.Point(const.FIELD_DX/2*-field.polarity, const.FIELD_DY/2)
                # secondScorePoint = aux.Point(const.FIELD_DX/2*-field.polarity, -const.FIELD_DY/2)
                # if aux.dist(rPos, firstScorePoint) < aux.dist(rPos, secondScorePoint):
                #     field.strategy_image.draw_line(rPos, firstScorePoint, color = (0, 0, 0), size_in_pixels = 20)
                # else:
                #     field.strategy_image.draw_line(rPos, secondScorePoint, color = (0, 0, 0), size_in_pixels = 20)

                # openForPass(field, 7, actions)
                # self.GKLastState = GK(field, actions, self.GKLastState)
                # actions[const.GK] =  Actions.Kick(aux.Point(0, 0), is_pass=True)
                # self.attacker(field, actions, 0, 2)
                # self.attacker(field, actions, 2, 0)
        else:
            print("WE HAVENT ROBOTS")

    def doPass(self, field, actions, idxThisR):
        if field.is_ball_in(field.allies[self.idDoPass]):
            """do pass"""
            self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
        elif self.idGettingPass == None:
            """grab ball"""
            actions[self.idDoPass] = Actions.BallGrab((field.ball.get_pos() - field.allies[self.idDoPass].get_pos()).arg())  
        else:
            self.idDoPass = None
            """pass done"""

    def gettingPass(self, field: fld.Field, actions, idxThisR):
        thisR = field.allies[self.idGettingPass]
        if self.idDoPass != None:
            actions[self.idGettingPass] = Actions.GoToPoint(thisR.get_pos(), (field.allies[self.idDoPass].get_pos()-thisR.get_pos()).arg())
        elif not field.is_ball_in(field.allies[self.idGettingPass]):
            # field.strategy_image.send_telemetry("status pass", "getting pass")
            """getting pass"""
            actions[self.idGettingPass] = Actions.BallGrab((field.ball.get_pos()-field.allies[self.idGettingPass].get_pos()).arg())
        else:
            """get pass"""
            # field.strategy_image.send_telemetry("status pass", "get pass")
            # actions[idxThisR] = Actions.Kick(findPointForScore(field))
            # self.idDoPass = self.idGettingPass
            self.idGettingPass = None

    def attacker(self, field: fld.Field, actions: list[Action], idxThisR, idxOtherAttacker):
        status = None
        enemies = field.active_enemies(True)
        enemysRsWithoutGK = field.active_enemies()
        allies = field.active_allies(True)
        # alliesWithoutGK = allies.copy()
        # alliesWithoutGK.remove(field.allies[const.GK])
        alliesRWithoutGK = field.active_allies()
        alliesWithoutGK = [r.get_pos() for r in alliesRWithoutGK]
        thisR: rbt.Robot = field.allies[idxThisR]
        thisRPos = thisR.get_pos()
        otherAttackerR = field.allies[idxOtherAttacker]
        ballPos = field.ball.get_pos()

        field.allies[idxThisR].set_dribbler_speed(0)

        if not field.allies[idxOtherAttacker].is_used():
            """if this attacker alone on field"""
            status = "No 1 r"
            nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemies)
            if ballPos.x*field.polarity > 0: # TODO need test
                """if ball on our part of field"""
                # TODO try replace ball from our part of field
                if not field.is_ball_in(thisR):
                    mostLikelyPointForScore = aux.closest_point_on_line(field.ally_goal.up, field.ally_goal.down, ballPos)
                    pointForR = aux.closest_point_on_line(ballPos, mostLikelyPointForScore, thisR.get_pos())
                    if not aux.is_point_on_line(thisR.get_pos(), ballPos, mostLikelyPointForScore, "S"):
                        """if this r not block maybe score, block"""
                        actions[idxThisR] = Actions.GoToPoint(pointForR, (ballPos-thisR.get_pos()).arg())
                        field.allies[idxThisR].set_dribbler_speed(15)
                    else:
                        """if this r block maybe score, try grab ball"""
                        # nearestEnemyR = fld.find_nearest_robot(field.ball.get_pos(), enemys)
                        actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())# GOOD
            else:
                """if ball on other part of field"""
                if field.is_ball_in(thisR):
                    pointForScore = findPointForScore(field, ballPos)
                    if pointForScore != None:
                        """if this r can do score, he do"""
                        actions[idxThisR] = Actions.Kick(pointForScore)
                    else:
                        newPointForScore = findPointForScore(field, ballPos, k = 1)
                        if newPointForScore != None:
                            """if this r can do score, he try do do another score"""
                            actions[idxThisR] = Actions.Kick(newPointForScore)
                        else:
                            """if this r cant do score, he kick to GK or do upper"""
                            if len(enemysRsWithoutGK) != 0:
                                actions[idxThisR] = Actions.Kick(fld.find_nearest_robot(thisRPos, enemysRsWithoutGK), is_upper=True)
                            else:
                                actions[idxThisR] = Actions.Kick(field.enemies[const.ENEMY_GK].get_pos())
                else:
                    actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())#GOOD
        elif self.idDoPass == idxThisR:
            """if thid R do pass"""
            status = "1"
            self.doPass(field, actions, idxThisR)
        elif idxThisR == self.idGettingPass:
            """if this R getting pass"""
            status = "2"
            self.gettingPass(field, actions, idxThisR)
        elif actions[idxThisR] == None:
            """if we dont send command on this robot"""
            allR = enemies.copy() + allies.copy()
            nearestRToBall = fld.find_nearest_robot(field.ball.get_pos(), allR)
            field.strategy_image.draw_circle(nearestRToBall.get_pos(), (200, 0, 255), 50)
            # print(nearestRToBall.r_id)
            if nearestRToBall == thisR: # TODO if nearest R to ball - enemy GK
                """if nearest to ball bot this"""
                if field.is_ball_in(thisR):
                    # field.strategy_image.draw_circle(thisR.get_pos(), (255, 255, 255), 50)
                    """if this robot have ball"""
                    pointForScore = findPointForScore(field)
                    if pointForScore != None:
                        """try do score if r can"""
                        # field.strategy_image.send_telemetry("status", "try do score if r can")
                        status = "try do score if r can"
                        actions[idxThisR] = Actions.Kick(pointForScore)
                    else:
                        """if this r cant do score"""
                        # nearestEnemyRToThisAttacker = fld.find_nearest_robot(thisR.get_pos(), enemys)
                        # nearestEnemyRToOtherAttacker = fld.find_nearest_robot(otherAttackerR.get_pos(), enemys)

                        # pointForScoreForOtherAttacker = findPointForScore(field, otherAttackerR.get_pos())
                        status = "if this r cant do score"
                        self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
                        # if pointForScoreForOtherAttacker != None:
                        #     """if other attacker can do score, pass other attacker"""
                        #     status = "if other attacker can do score, pass other attacker"
                        #     self.idGettingPass = doPassNearAllly(field, actions, idxThisR)
                        # else:
                        #     """if both attackers cant do score try do score: change position"""
                        #     status = "if both attackers cant do score try do score: change position"
                        #     goToNearestScorePoint(field, actions, 0, None)
                else:
                    if self.idGettingPass == None:
                        """if this r is nearest to ball, but dont grab him, grab ball"""
                        # field.strategy_image.send_telemetry("status", "if this r is nearest to ball, but dont grab him, grab ball")
                        status = "if this r is nearest to ball, but dont grab him, grab ball"
                        actions[idxThisR] = Actions.BallGrab((field.ball.get_pos() - thisR.get_pos()).arg())
                            
                    else:
                        """do do pass and wait for result"""
                        status = "do do pass and wait for result"
                        # actions[idxThisR] = Actions.GoToPoint(aux.Point(0, 0), (field.allies[idxOtherAttacker].get_pos()-thisR.get_pos()).arg())
                        # goToNearestScorePoint(field, actions, idxThisR, idxOtherAttacker)
                        actions[idxThisR] = Actions.BallGrab((ballPos-field.enemy_goal.center).arg())
                        # actions[idxThisR] = Actions.BallGrab((field.ball.get_pos() - thisR.get_pos()).arg())
            elif nearestRToBall == field.allies[idxOtherAttacker]:
                    """if other attacker have ball"""
                    status = "if other attacker have ball"
                    goToNearestScorePoint(field, actions, idxThisR, idxOtherAttacker)
            elif nearestRToBall == field.allies[const.GK]:
                """if GK have ball"""
                status = "if GK have ball"
                # print(alliesWithoutGK, field.allies)
                if len(alliesWithoutGK) != 0:
                    nearestRToGK = aux.find_nearest_point(field.ball.get_pos(), alliesWithoutGK)
                    if nearestRToGK == field.allies[idxThisR]:
                        """if this R nearest to GK"""
                        openForPass(field, idxThisR, actions)
                    else:
                        """if not this r nearest to GK"""
                        actions[idxThisR] = Actions.GoToPoint(aux.Point(0, 0), 0)
            elif nearestRToBall == field.enemies[const.GK]:
                """if nearest r to ball is enemy GK"""
                status = "if nearest r to ball is enemy GK"
                enemyRsPos = field.active_enemies().copy()
                if len(enemyRsPos) != 0:
                    enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                    enemyRPos = enemyRsPos[0]
                    pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                    actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-enemyRPos.get_pos()).arg())
                    field.allies[idxThisR].set_dribbler_speed(15)
                else:
                    actions[idxThisR] = Actions.BallGrab((ballPos-field.enemy_goal.center).arg())
            elif ballPos.x*field.polarity > 0: # TODO need test
                """if ball on our part of field"""
                status = "if ball on our part of field"
                dist2BallFromThisR = aux.dist(ballPos, thisR.get_pos())
                dist2BallFromOtherR = aux.dist(ballPos, otherAttackerR.get_pos())
                if dist2BallFromThisR < dist2BallFromOtherR:
                    """if this attacker nearest to ball then other"""
                    mostLikelyPointForScore = aux.closest_point_on_line(field.ally_goal.up, field.ally_goal.down, ballPos)
                    pointForR = aux.closest_point_on_line(ballPos, mostLikelyPointForScore, thisR.get_pos())
                    if not aux.is_point_on_line(thisR.get_pos(), ballPos, mostLikelyPointForScore, "S"):
                        """if this r not block maybe score, block"""
                        actions[idxThisR] = Actions.GoToPoint(pointForR, (ballPos-thisR.get_pos()).arg())
                        field.allies[idxThisR].set_dribbler_speed(15)
                    else:
                        """if this r block maybe score, try grab ball"""
                        nearestEnemyR = fld.find_nearest_robot(ballPos, enemies)
                        actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())#GOOD
                else:
                    """if nearest attacker for ball other, block maybe pass"""
                    # enemyRPos = field.allies[3].get_pos() # HARD CODE
                    enemyRsPos = field.active_enemies().copy()
                    enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                    enemyRPos = enemyRsPos[0]
                    # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                    pointGo = aux.point_on_line(ballPos, enemyRPos.get_pos(), 300)
                    actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-enemyRPos.get_pos()).arg())
                    field.allies[idxThisR].set_dribbler_speed(15)
            else:
                """if ball not on our part of field"""
                status = "if ball not on our part of field"
                # enemyRsPos = field.active_enemies().copy()
                # enemyRsPos.remove(fld.find_nearest_robot(ballPos, enemyRsPos))
                # enemyRPos = enemyRsPos[0]
                # enemies = field.active_enemies(True)
                nearestEnemyR = fld.find_nearest_robot(ballPos, enemies)
                dist2BallFromThisR = aux.dist(ballPos, thisR.get_pos())
                dist2BallFromOtherR = aux.dist(ballPos, otherAttackerR.get_pos())
                if dist2BallFromThisR < dist2BallFromOtherR:
                    """if this attacker nearest to ball then other, take ball"""
                    actions[idxThisR] = Actions.BallGrab((nearestEnemyR.get_pos()-ballPos).arg())#GOOD
                else:
                    """if nearest attacker for ball other, block maybe pass"""
                    # enemyRPos = field.allies[3].get_pos() # HARD CODE
                    # pointGo = aux.closest_point_on_line(enemyRPos, ballPos, rPos, "R")
                    pointGo = aux.point_on_line(ballPos, nearestEnemyR.get_pos(), 300)
                    actions[idxThisR] = Actions.GoToPoint(pointGo, (thisRPos-nearestEnemyR.get_pos()).arg())
                    field.allies[idxThisR].set_dribbler_speed(15)
        print(status, idxThisR)
        field.strategy_image.send_telemetry("statusAttacker"+str(idxThisR), status)

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

def GetIds(field: fld.Field, actions: list[Optional[Action]]) -> list[Optional[int]]:
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
