import math
import random


class Players:  # 玩家类
    name = ''
    Ep = 0
    HP = 3
    skill = 0  # 使用技能
    last_skill = 0  # 上回合技能
    no = [0]  # 禁用技能

    def __init__(self, n):
        self.name = n


print('欢迎来到拍手游戏')
player = [Players('玩家'), Players('电脑')]


class Skills:  # 技能类
    cost = 0  # 花费
    who = 0  # 对象
    priority = 0  # 优先级
    name = ''

    def __init__(self, n, a, b, c=3):
        self.name = n
        self.cost = a
        self.who = b
        self.priority = c

    def doing(self, n):
        print('{}受到了{}使用的{}，技能的优先度为{}'.format(
            player[(self.who + n) & 1].name, player[n].name, self.name, self.priority))


skills = [Skills('ジ', -1, 0, 0),
          Skills('防御', 0, 0),
          Skills('反弹', 0, 0),
          Skills('超反', 1, 0),
          Skills('地雷', 3, 0, 0),
          Skills('转移伤害', 2, 1, 1),
          Skills('八卦阵', 0, 0),
          Skills('枪', 1, 1, 2),
          Skills('激光剑', 2, 1),
          Skills('坦克', 2, 1),
          Skills('狙击', 2, 1, 1),
          Skills('真正的落雷', 5, 1, 4),
          Skills('摄魂指法', 3, 1),
          Skills('电磁炮', 2, 1),
          Skills('激光眼', 2, 1),
          Skills('聚能环', '第一次使用3个ジ并获得个1个ジ，第二次连续使用获得2个ジ，第三次及之后获得3个ジ', 0, 0),
          Skills('蓄能', 1, 0, 0)]

player[0].no = player[1].no = [0] * len(skills)
# 基础结算表
#          无       防御     反弹      超反     地雷     转伤
table = [[[-1, 0], [0, 0], [0, -1], [0, 0], [-1, -1], [0, -1]],  # 枪
         [[-1, 0], [0, 0], [-1, 0],  [0, 0], [-1, -1], [0, -1]],  # 激光剑
         [[-1, 0], [-1, 0], [0, -1], [0, 0], [-1, -1], [-1, 0]],  # 坦克
         [[-1, 0], [-1, 0], [-1, 0], [0, 0], [-1, 0], [0, -1]],  # 狙击
         [[-2, 0], [0, 0], [0, 0], [0, 0], [-2, 0], [-2, -2]]]  # 大雷

attact_num, lightning, snipe, bagua, gou, power = 0, 0, 0, 0, 0, len(skills) - 1
for i in range(0, len(skills)):
    if skills[i].name == '枪':
        attact_num = i
    if skills[i].name == '狙击':
        snipe = i
    if skills[i].name == '八卦阵':
        bagua = i
    if skills[i].name == '摄魂指法':
        gou = i
    if skills[i].name == '真正的落雷':
        lightning = i


def Bagua(i):
    if player[(i + 1) & 1].skill == bagua:
        if(random.randint(0, 1) == 0):
            print('判定失败')
            player[(i + 1) & 1].skill = 0
            return 0
        else:
            print('判定成功')
            return 1
    else:
        return 0


def Pass():
    player[0].Ep -= skills[player[0].skill].cost
    skills[player[0].skill].doing(0)


def Fail():
    player[0].Ep -= skills[player[0].skill].cost
    player[0].skill = 0


t, w = 0, 0

# 游戏过程
while player[0].HP > 0 and player[1].HP > 0:
    t += 1
    print('Player HP:{} Ep{}   Computer HP:{} Ep{}\n'.format(player[0].HP, player[0].Ep, player[1].HP, player[1].Ep))
    for i in range(0, len(skills)):
        print('{}、{} \t花费为{}'.format(i, skills[i].name, skills[i].cost))

    player[0].skill = int(input('输入你的技能符：'))
#    print('1:{}\t2:{}'.format(skills[player[0].last_skill].name,skills[player[1].last_skill].name))
    # 电脑技能判定
    check = 0
    if (player[1].Ep == 0 and player[0].Ep == 0):
        player[1].skill = 0
    else:
        while not check:
            player[1].skill = random.randint(0, len(skills) + 10)
            if player[1].skill >= len(skills):  # 电脑算法区
                if player[1].skill > len(skills) + 5:
                    player[1].skill = 0
                elif player[1].HP == 1:
                    player[1].skill = gou
                elif player[1].last_skill == power:
                    player[1].skill = random.choice([gou + 1, gou + 2])
                elif player[0].last_skill == power:
                    player[1].skill = random.choice([3, 5, 6])
                elif player[0].last_skill == power - 1:
                    player[1].skill = random.randint(attact_num, gou)
                else:
                    player[1].skill = lightning
            if player[1].skill == power - 1:
                player[1].skill = 0
            check = (player[1].Ep >= skills[player[1].skill].cost and player[1].no[player[1].skill - 3] == 0)
            if(player[1].skill == gou and player[1].HP > 1):
                check = 0
            if(player[1].skill == gou + 1 and player[1].last_skill != power):
                check = 0
            if player[1].skill == gou + 2:
                if player[1].last_skill == power:
                    player[1].Ep += 1
                elif player[1].last_skill != gou + 2:
                    check = 0
            if(player[1].skill == power and player[1].Ep < 3):
                check = 0
    player[1].Ep -= skills[player[1].skill].cost
    # 技能判定
    if (player[0].skill > power or player[0].skill < 0):  # 安全保护
        player[0].skill = 0
        Pass()
    elif (player[0].skill > 2 and player[0].no[player[0].skill - 3] > 0):
        player[0].HP -= 1
        player[0].skill = 0
        print('该技能还需{}回合才能使用'.format(player[0].no[player[0].skill - 3]))
    elif player[0].skill == power - 1:  # 聚能环
        if w == 0:
            if player[0].Ep < 3:
                print('你贷款了')
                player[0].HP -= (3 - player[0].Ep) / 2
                player[0].Ep = 0
                player[0].skill = 0
            else:
                player[0].Ep -= 2
                skills[player[0].skill].doing(0)
        elif w == 1:
            player[0].Ep += 2
            skills[player[0].skill].doing(0)
        else:
            player[0].Ep += 3
            skills[player[0].skill].doing(0)
    elif player[0].Ep < skills[player[0].skill].cost:  # 勾
        player[0].HP -= (skills[player[0].skill].cost - player[0].Ep) / 2
        player[0].Ep = 0
        player[0].skill = 0
        print('你贷款了')
    elif(player[0].skill == gou and player[0].HP > 1):
        print('只有一滴血时可以使用摄魂指法')
        Fail()
    elif player[0].skill == gou + 1:  # 电磁炮
        if player[0].last_skill != power:
            print('你没有蓄能')
            Fail()
        else:
            Pass()
    elif player[0].skill == gou + 2:  # 激光眼
        if player[0].last_skill == power:
            player[0].Ep += 1
            Pass()
        elif player[0].last_skill != gou + 2:
            print('你没有蓄能')
            Fail()
        else:
            Pass()
    else:
        Pass()
    skills[player[1].skill].doing(1)
    '''#test
    player[1].skill=gou
    player[0].skill=bagua-1'''

    # 结算

    # 蓄能及聚能环
    for i in range(0, 2):
        player[i].last_skill = player[i].skill
        if player[i].skill == power:
            player[i].skill = 0
    if player[0].skill == power - 1:
        player[0].skill = 0
        w += 1
    else:
        w = 0
    for i in range(0, 2):
        for j in range(0, power - 3):
            if player[i].no[j] > 0:
                player[i].no[j] -= 1
        # 勾
        if player[i].skill == gou:
            if Bagua(i):
                break
            elif player[(i + 1) & 1].skill == bagua - 1:
                break
            elif player[(i + 1) & 1].skill == 5:
                break
            elif skills[player[(i + 1) & 1].skill].priority < 2:
                player[i].HP += 1
                player[(i + 1) & 1].HP -= 1
        # 电磁炮
        elif player[i].skill == gou + 1:
            if Bagua(i):
                break
            elif player[(i + 1) & 1].skill == bagua - 1:
                player[i].HP -= 2
            elif player[(i + 1) & 1].skill != 3:
                player[(i + 1) & 1].HP -= 2
                if player[(i + 1) & 1].skill == 4:
                    player[i].HP -= 1
                if player[(i + 1) & 1].skill == snipe:
                    player[(i + 1) & 1].skill = 0
            if player[i].skill == lightning:
                player[i].HP -= 2
                player[i].no[player[i].skill - 3] = 3
        # 激光眼
        elif player[i].skill == gou + 2:
            if player[(i + 1) & 1].skill == bagua - 2:
                player[(i + 1) & 1].HP -= 1
                player[i].HP -= 1
            elif player[(i + 1) & 1].skill == bagua - 1:
                player[i].HP -= 1
            elif player[(i + 1) & 1].skill >= attact_num or player[(i + 1) & 1].skill == 0:
                player[(i + 1) & 1].HP -= 1
            if player[(i + 1) & 1].skill == snipe:
                player[(i + 1) & 1].skill = 0
            # 同时攻击类
        elif player[(i + 1) & 1].skill != gou + 1:
            if(player[i].skill >= attact_num and player[(i + 1) & 1].skill >= attact_num):
                if skills[player[i].skill].priority > skills[player[(i + 1) & 1].skill].priority:
                    player[(i + 1) & 1].HP += table[player[i].skill - attact_num][0][0]
                if player[i].skill == lightning:
                    player[i].HP -= 2
                    player[i].no[player[i].skill - 3] = 3
        # 一方防御类
            elif(player[i].skill >= attact_num):
                if Bagua(i):
                    break
                player[(i + 1) & 1].HP += table[player[i].skill - attact_num][player[(i + 1) & 1].skill][0]
                player[i].HP += table[player[i].skill - attact_num][player[(i + 1) & 1].skill][1]
        # 狙击
        if player[i].skill == snipe:
            if player[(i + 1) & 1].skill == 0:
                if(random.randint(0, 8) == 0):
                    print('{}被爆头！'.format(player[(i + 1) & 1].name))
                    player[(i + 1) & 1].HP -= 1
            elif player[(i + 1) & 1].skill == bagua - 1:
                if(random.randint(0, 8) == 0):
                    print('{}被爆头！'.format(player[(i + 1) & 1].name))
                    player[i].HP -= 1
        # 大雷
        if(player[i].skill == lightning):
            player[(i + 1) & 1].last_skill = 0
            if(player[(i + 1) & 1].skill > 2):
                player[(i + 1) & 1].no[player[(i + 1) & 1].skill - 3] = 3

# 游戏结束
if(player[0].HP <= 0 and player[1].HP <= 0):
    print('平局')
elif(player[0].HP <= 0):
    print('你输了')
else:
    print('你赢了')
print('一共进行了{}回合'.format(t))
input('按回车退出')
