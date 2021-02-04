# 本程序用于输出训练过程数据
# 规则：输出为赢方上回合HP，本回合使用技能及使用后Ep，之后是输方相应内容
# 以6个-1作为结尾

import math
import random
import copy
fo = open('data', 'w')


class Players:  # 玩家类
    Ep = 0
    HP = 3
    skill = 0  # 使用技能
    last_skill = 0  # 上回合技能
    no = [0]  # 禁用技能
    last_Ep = 0


player = [Players(), Players()]
data = [player[0], player[1]]
ff = open('time', 'r')
xx = int(ff.read())
m, n = 18, 18
ai = [[[[[[[0 for a in range(n-1)]for b in range(m)]for c in range(n)]for d in range(3)]
        for e in range(m)]for f in range(n)]for g in range(3)]
f1 = open('table.data', 'r')
for a in range(3):
    for b in range(n):
        for c in range(m):
            for d in range(3):
                for e in range(n):
                    for f in range(m):
                        ai[a][b][c][d][e][f] = list(map(int, f1.readline().split()))
fo = open('data', 'w')

ti = 0


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
          Skills('雷击之枪', 2, 1, 5),
          Skills('摄魂指法', 3, 1),
          Skills('电磁炮', 2, 1),
          Skills('激光眼', 2, 1),
          Skills('蓄能', 1, 0, 0),
          Skills('聚能环', '第一次使用3个ジ并获得个1个ジ，第二次连续使用获得2个ジ，第三次及之后获得3个ジ', 0, 0)]

player[0].no = player[1].no = [0] * len(skills)
# 基础结算表
#          无       防御     反弹      超反     地雷     转伤
table = [[[-1, 0], [0, 0], [0, -1], [0, 0], [-1, -1], [0, -1]],  # 枪
         [[-1, 0], [0, 0], [-1, 0],  [0, 0], [-1, -1], [0, -1]],  # 激光剑
         [[-1, 0], [-1, 0], [0, -1], [0, 0], [-1, -1], [-1, 0]],  # 坦克
         [[-1, 0], [-1, 0], [-1, 0], [0, 0], [-1, 0], [0, -1]],  # 狙击
         [[-2, 0], [0, 0], [0, 0], [0, 0], [-2, 0], [-2, -2]]]  # 大雷

attact_num, lightning, snipe, bagua, gou, power = 0, 0, 0, 0, 0, len(skills) - 2
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
            player[(i + 1) & 1].skill = 0
            return 0
        else:
            return 1
    else:
        return 0


def Pass():
    player[0].Ep -= skills[player[0].skill].cost
    skills[player[0].skill].doing(0)


def Fail():
    player[0].Ep -= skills[player[0].skill].cost
    player[0].skill = 0


def Choose_Skill(i):
    a = (i + 1) & 1
    check = 0
    if (player[i].Ep == 0 and player[0].Ep == 0):
        player[i].skill = 0
    else:
        while not check:
            player[i].skill = random.randint(0, len(skills) * 2 - 1)
            if player[i].skill >= len(skills):  # 电脑算法区
                player[i].skill -= len(skills)
                if(player[i].Ep < 18 and player[a].last_Ep < 18):
                    #                    print(player[i].HP,player[i].last_skill,player[i].Ep,player[a].HP,player[a].last_skill,player[a].last_Ep)
                    ta = ai[player[i].HP-1][player[i].last_skill][player[i].Ep][player[a].HP-1][player[a].last_skill][player[a].last_Ep]
                    s = sum(ta)
                    ss = 0
                    for x in range(17):
                        ss += ta[x]
                        if ss >= s * player[i].skill / 17:
                            player[i].skill = x
                            break

                '''if player[i].skill > len(skills) + 5:
                    player[i].skill = 0
                elif player[i].HP == 1:
                    player[i].skill = gou
                elif player[i].last_skill == power:
                    player[i].skill = random.choice([gou + 1, gou + 2])
                elif player[t].last_skill == power:
                    player[i].skill = random.choice([3, 5, 6])
                elif player[t].last_skill == power - 1:
                    player[i].skill = random.randint(attact_num, gou)
                else:
                    player[i].skill = lightning'''
            if player[i].skill == power + 1:
                player[i].skill = 0
#            print(ti,player[i].skill,player[i].no[player[i].skill])
            check = (player[i].Ep >= skills[player[i].skill].cost
                     and player[i].no[player[i].skill] == 0)
            if(player[i].skill == gou and player[i].HP > 1):
                check = 0
            if(player[i].skill == gou + 1 and player[i].last_skill != power):
                check = 0
            if player[i].skill == gou + 2:
                if player[i].last_skill == power:
                    player[i].Ep += 1
                elif player[i].last_skill != gou + 2:
                    check = 0
            if(player[i].skill == power and player[i].Ep < 3):
                check = 0
    player[i].Ep -= skills[player[i].skill].cost


# 游戏过程
while ti <= xx:
    player[0] = Players()
    player[1] = Players()
    player[0].no = [0] * len(skills)
    player[1].no = [0] * len(skills)
    ti += 1
    t, w = 0, 0
    data = [player[0], player[1]]
    while player[0].HP > 0 and player[1].HP > 0:
        t += 1

    #    fo.write('1:{}\t2:{}'.format(skills[player[0].last_skill].name,skills[player[1].last_skill].name))
        Choose_Skill(0)
        Choose_Skill(1)
        P0 = copy.deepcopy(player[0])
        P1 = copy.deepcopy(player[1])
        data += [P0, P1]
    #    fo.write('%d %d %d\t%d %d %d\n'%(player[0].HP,player[0].skill,player[0].Ep,player[1].HP,player[1].skill,player[1].Ep))

        # 结算

        # 蓄能
        f = 0
        for i in range(0, 2):
            num = (i + 1) & 1
            player[i].last_skill = player[i].skill
            player[i].last_Ep = player[i].Ep
            if player[i].skill == power:
                player[i].skill = 0
            # 雷击之枪
            if player[i].skill == gou - 1:
                if player[num].skill == 0:
                    player[num].Ep -= 1
                player[num].skill = player[num].last_skill = 0
                f = 1
        if f:
            continue
        for i in range(0, 2):
            num = (i + 1) & 1
            for j in range(0, power - 3):
                if player[i].no[j] > 0:
                    player[i].no[j] -= 1
            # 勾
            if player[i].skill == gou:
                if Bagua(i):
                    break
                elif player[num].skill == bagua - 1:
                    break
                elif player[num].skill == 4:
                    break
                elif skills[player[num].skill].priority < 2:
                    player[i].HP += 1
                    player[num].HP -= 1
            # 电磁炮
            elif player[i].skill == gou + 1:
                if Bagua(i):
                    break
                elif player[num].skill == bagua - 1:
                    player[i].HP -= 2
                elif player[num].skill != 3:
                    player[num].HP -= 2
                    if player[num].skill == 4:
                        player[i].HP -= 1
                    if player[num].skill == snipe:
                        player[num].skill = 0
                if player[i].skill == lightning:
                    player[i].HP -= 2
                    player[i].no[player[i].skill] = 3
            # 激光眼
            elif player[i].skill == gou + 2:
                if player[num].skill == bagua - 2:
                    player[num].HP -= 1
                    player[i].HP -= 1
                elif player[num].skill == bagua - 1:
                    player[i].HP -= 1
                elif player[num].skill >= attact_num or player[num].skill == 0:
                    player[num].HP -= 1
                if player[num].skill == snipe:
                    player[num].skill = 0
                # 同时攻击类
            elif player[num].skill != gou + 1:
                if(player[i].skill >= attact_num and player[num].skill >= attact_num):
                    if skills[player[i].skill].priority > skills[player[num].skill].priority:
                        player[num].HP += table[player[i].skill - attact_num][0][0]
                    if player[i].skill == lightning:
                        player[i].HP -= 2
                        player[i].no[player[i].skill] = 3
            # 一方防御类
                elif(player[i].skill >= attact_num):
                    if Bagua(i):
                        break
                    player[num].HP += table[player[i].skill - attact_num][player[num].skill][0]
                    player[i].HP += table[player[i].skill - attact_num][player[num].skill][1]
            # 狙击
            if player[i].skill == snipe:
                if player[num].skill == 0:
                    if(random.randint(0, 8) == 0):
                        player[num].HP -= 1
                elif player[num].skill == bagua - 1:
                    if(random.randint(0, 8) == 0):
                        player[i].HP -= 1
            # 大雷
            if(player[i].skill == lightning):
                player[num].last_skill = 0
                if(player[num].skill > 2):
                    player[num].last_skill = 0
                    player[num].no[player[num].skill] = 3
                if player[num].last_skill >= power:
                    player[num].no[player[num].last_skill] = 3

    # 游戏结束
    if(not (player[0].HP <= 0 and player[1].HP <= 0)):
        if player[0].HP <= 0:
            for i in range(1, t + 1):
                fo.write('%d %d %d\t%d %d %d\n' % (data[i * 2 + 1].HP, data[i * 2 + 1].last_skill, data[i * 2 + 1].Ep,
                                                   data[i * 2 + 0].HP, data[i * 2 + 0].last_skill, data[i * 2 + 0].Ep))
        elif player[1].HP <= 0:
            for i in range(1, t + 1):
                fo.write('%d %d %d\t%d %d %d\n' % (data[i * 2 + 0].HP, data[i * 2 + 0].last_skill, data[i * 2 + 0].Ep,
                                                   data[i * 2 + 1].HP, data[i * 2 + 1].last_skill, data[i * 2 + 1].Ep))
    fo.write('-1 -1 -1\t-1 -1 -1\n')
