import math
import random


class Skills:#技能类
    cost=0#花费
    who=0#对象
    priority=0#优先级
    def __init__(self,a,b,c=3):
        self.cost= a
        self.who=b
        self.priority = c
skills=[Skills(-1,0),#ジ
Skills(1,1,2),#枪
Skills(2,1),#激光剑
Skills(2,1),#坦克
Skills(2,1,1),#狙击
Skills(0,0),#防御
Skills(0,0),#反弹
Skills(1,0)]#超反

class Player:#玩家类
    Ep=0
    power=0#蓄能
    HP=3
    skill=0#使用技能

def Doing(n,who):#技能模块
    0

def Settlement():#结算
    0


print('欢迎来到拍手游戏')
player,computer = Player(),Player();

while player.HP>0 and computer.HP>0:
    print('Player HP:{} Ep{}   Computer HP:{} Ep{}'.format(player.HP,player.Ep,computer.HP,computer.Ep))
    check=0
    player.skill = int(input('输入你的技能符'))
    if(player.Ep>=skills[player.skill].cost):
        player.Ep-=skills[player.skill].cost
        Doing(player.skill,0)
    else:#贷款判定
        player.HP-=(skills[player.skill].cost-player.Ep)/2
        player.Ep=0
    while not check:#电脑不会贷款
        computer.skill=random.choice(range(0,10))
        if(computer.skill>7):computer.skill=0
        check=computer.Ep>=skills[computer.skill].cost
    computer.Ep-=skills[computer.skill].cost
    Doing(computer.skill,1)
