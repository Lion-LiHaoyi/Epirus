import math
import random
import copy
import time
from tkinter import*
import tkinter.font as tkFont
from tkinter import messagebox
import threading


root = Tk()
root.title('拍手游戏Epirus')
sb = Scrollbar(root)
lb = Listbox(root, yscrollcommand=sb.set)
lb.pack(side=RIGHT, fill=Y, ipadx=200, ipady=100)
sb.pack(side=RIGHT, fill=Y)
te = Text(root, width=30, font=tkFont.Font(family='微软雅黑', size=12))
te.pack(side=LEFT, fill=Y)


class Players:  # 玩家类
    name = ''
    Ep = 0
    last_Ep = 0
    HP = 3
    skill = 0  # 使用技能
    last_skill = 0  # 上回合技能
    no = [0]  # 禁用技能

    def __init__(self, n):
        self.name = n


player = [Players('玩家'), Players('电脑')]
global data, flag1, flag2
data, flag1, flag2 = [player[0], player[1]], 1, 0


# AI初始化
def Reading():
    lb.insert(END, '欢迎来到拍手游戏')
    lb.insert(END, '正在加载AI，请稍候')
    global m, n, flag1
    m, n = 15, 18
    start = time.time()
    global ai
    ai = [[[[[[[0 for a in range(n - 1)]for b in range(m)]for c in range(n)]for d in range(3)]
            for e in range(m)]for f in range(n)]for g in range(3)]
    end1 = time.time()
    lb.insert(END, '已加载30%，用时{0:.3f}s'.format(end1 - start))
    with open('table.data', 'rb') as f1:
        for a in range(3):
            for b in range(n):
                for c in range(m):
                    for d in range(3):
                        for e in range(n):
                            for f in range(m):
                                ai[a][b][c][d][e][f] = list(map(int, f1.readline().split()))
    f1.close()
    end = time.time()
    lb.insert(END, '加载完成，用时{0:.3f}s'.format(end - start))
    lb.insert(END, '开始')
    flag1 = 0


Read = threading.Thread(target=Reading)
Read.daemon = True
Read.start()


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
        lb.insert(END, '{}对{}使用了{}'.format(
            player[n].name, player[(self.who + n) & 1].name, self.name))


skills = [Skills('ジ', -1, 0, 0),
          Skills('防御', 0, 0),
          Skills('反弹', 0, 0),
          Skills('原型制御', 1, 0),
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
          Skills('聚能环', '第一次使用3个ジ并获得个1个ジ,第二次连续使用获得2个ジ,第三次及之后获得3个ジ', 0, 0)]

player[0].no = [0] * len(skills)
player[1].no = [0] * len(skills)
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
            lb.insert(END, '判定失败')
            player[(i + 1) & 1].skill = 0
            return 0
        else:
            lb.insert(END, '判定成功')
            return 1
    else:
        return 0


def Pass():
    player[0].Ep -= skills[player[0].skill].cost
    skills[player[0].skill].doing(0)


def Fail():
    player[0].Ep -= skills[player[0].skill].cost
    player[0].skill = 0


global t, w
t, w = 0, 0

for i in range(0, len(skills)):
    te.insert(END, '{} \t花费为{}\n'.format(skills[i].name, skills[i].cost))


def Choose_Skill(i):  # 电脑选择技能
    while flag1:
        messagebox.showinfo(message='请稍候')
    a = (i + 1) & 1
    check = 0
    if (player[i].Ep == 0 and player[0].Ep == 0):
        player[i].skill = 0
    else:
        while not check:
            player[i].skill = random.randint(0, len(skills) * 2 - 1)
            if player[i].skill >= len(skills):  # 电脑算法区
                player[i].skill -= len(skills)
                if(player[a].HP < 4 and player[i].HP < 4 and player[i].Ep < m and player[a].last_Ep < m):
                    # lb.insert(END,player[i].HP,player[i].last_skill,player[i].Ep,player[a].HP,player[a].last_skill,player[a].last_Ep)
                    ta = ai[int(player[i].HP - 1)][player[i].last_skill][player[i].Ep][
                        int(player[a].HP - 1)][player[a].last_skill][player[a].last_Ep]
                    s = sum(ta)
                    ss = 0
                    for x in range(16):
                        ss += ta[x]
                        if ss >= s * player[i].skill / 16:
                            player[i].skill = x
                            #lb.insert(END,'Using AI')
                            break
            if player[i].skill == power + 1:
                player[i].skill = 0
            try:
                check = (player[i].Ep >= skills[player[i].skill].cost and player[i].no[player[i].skill] == 0)
            except:
                lb.insert(END, player[i].skill)
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


# 游戏结束
def Ending():
    global flag2, t
    f0 = open('count.txt', 'r')
    count = int(f0.read())
    f0.close()
    if(player[0].HP <= 0 and player[1].HP <= 0):
        messagebox.showinfo(message='平局')
    elif(player[0].HP <= 0):
        messagebox.showinfo(message='你输了')
        for i in range(1, t):
            if data[i * 2 + 1].Ep < 15 and data[i * 2 + 0].Ep < 15:
                ai[int(data[(i + 1) * 2 + 1].HP - 1)][data[i * 2 + 1].last_skill][data[i * 2 + 1].Ep][
                    int(data[(i + 1) * 2 + 0].HP - 1)][data[i * 2 + 0].last_skill][data[i * 2 + 0].Ep][data[(i + 1) * 2 + 1].last_skill] += 1
    else:
        messagebox.showinfo(message='你赢了')
        for i in range(1, t):
            if data[i * 2 + 1].Ep < 15 and data[i * 2 + 0].Ep < 15 and data[(i + 1) * 2 + 0].last_skill <= power:
                ai[int(data[(i + 1) * 2 + 0].HP - 1)][data[i * 2 + 0].last_skill][data[i * 2 + 0].Ep][
                    int(data[(i + 1) * 2 + 1].HP - 1)][data[i * 2 + 1].last_skill][data[i * 2 + 1].Ep][data[(i + 1) * 2 + 0].last_skill] += 1
    lb.insert(END, '一共进行了{}回合'.format(t))
    lb.insert(END, '正在存储AI')
    lb.see(END)
    f1 = open('table.data', 'w')
    for a in range(3):
        for b in range(n):
            for c in range(m):
                for d in range(3):
                    for e in range(n):
                        for f in range(m):
                            for g in range(n - 1):
                                f1.write('{} '.format(ai[a][b][c][d][e][f][g]))
                            f1.write('\n')
    f1.close()
    f0 = open('count.txt', 'w')
    f0.write('{}'.format(count + 1))
    f0.close()
    messagebox.showinfo(message='完成')
    te.delete('1.0', END)
    te.insert(END, "按任意技能退出")
    flag2 = 2
# 游戏过程


def Doing(k):
    global flag2
    if flag2 == 1:
        messagebox.showinfo(message='请稍候')
        return
    if flag2 == 2:
        root.destroy()
        return
    global t, w
    t += 1

    P0 = copy.deepcopy(player[0])
    P1 = copy.deepcopy(player[1])
    data.append(P0)
    data.append(P1)
#    lb.insert(END,'1:{}\t2:{}'.format(skills[player[0].last_skill].name,skills[player[1].last_skill].name))
    # 电脑技能判定
    Choose_Skill(1)
    # 技能判定
    player[0].skill = k
    if (player[0].skill > 2 and player[0].no[player[0].skill] > 0):
        player[0].HP -= 1
        lb.insert(END, '该技能还需{}回合才能使用'.format(player[0].no[player[0].skill]))
        player[0].skill = 0
    elif player[0].skill == power + 1:  # 聚能环
        if w == 0:
            if player[0].Ep < 3:
                lb.insert(END, '你贷款了')
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
        lb.insert(END, '你贷款了')
    elif(player[0].skill == gou and player[0].HP > 1):
        lb.insert(END, '只有一滴血时可以使用摄魂指法')
        Fail()
    elif player[0].skill == gou + 1:  # 电磁炮
        if player[0].last_skill != power:
            lb.insert(END, '你没有蓄能')
            Fail()
        else:
            Pass()
    elif player[0].skill == gou + 2:  # 激光眼
        if player[0].last_skill == power:
            player[0].Ep += 1
            Pass()
        elif player[0].last_skill != gou + 2:
            lb.insert(END, '你没有蓄能')
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
    f = 0
    # 蓄能及聚能环
    for i in range(0, 2):
        for j in range(0, power + 1):  # 禁用表
            if player[i].no[j] > 0:
                player[i].no[j] -= 1
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
            w = 0
            f = 1
    if player[0].skill == power + 1:
        player[0].skill = 0
        w += 1
    else:
        w = 0
    if f:
        lb.insert(END, '你的HP:{}  ジ数:{}     电脑的HP:{} ジ数:{}\n'.format(
            player[0].HP, player[0].Ep, player[1].HP, player[1].Ep))
        lb.see(END)
        return
    for i in range(0, 2):
        num = (i + 1) & 1
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
                player[i].no[player[i].skill - 3] = 3
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
                    #lb.insert(END,'{} of {} is not usable\nYour list is{}\nIts is{}'.format(player[i].skill,i,player[0].no,player[1].no))
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
                    lb.insert(END, '{}被爆头！'.format(player[num].name))
                    player[num].HP -= 1
            elif player[num].skill == bagua - 1:
                if(random.randint(0, 8) == 0):
                    lb.insert(END, '{}被爆头！'.format(player[num].name))
                    player[i].HP -= 1
        # 大雷
        if player[i].skill == lightning:
            if player[num].skill > 2:
                player[num].last_skill = 0
                player[num].no[player[num].skill] = 3
                #lb.insert(END,'{} of {} is not usable\nYour list is{}\nIts is{}'.format(player[num].skill,num,player[0].no,player[1].no))
            if player[num].last_skill >= power:
                w = 0
                player[num].no[player[num].last_skill] = 3
    if player[0].HP <= 0 or player[1].HP <= 0:
        flag2 = 1
        End = threading.Thread(target=Ending)
        End.daemon = True
        End.start()
    lb.insert(END, '你的HP:{}  ジ数:{}     电脑的HP:{} ジ数:{}\n'.format(
        player[0].HP, player[0].Ep, player[1].HP, player[1].Ep))
    lb.see(END)


for i in range(len(skills)):
    a = Button(root, width=10, text=skills[i].name, command=lambda i=i: Doing(i)).pack()

root.mainloop()
