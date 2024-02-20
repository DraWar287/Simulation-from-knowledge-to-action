import random
import time


def creat_adjTable(n, probability=0.3):
    ''' 创建n的邻接表 '''
    random.seed(int(time.time()))
    adjTable = [[]for _ in range(n)]
    adjMatrix = [[0 for _ in range(n)]for _ in range(n)]
    for i in range(n):
        for j in range(i):
            adjMatrix[i][j] = adjMatrix[j][i] = random.choices(
                [0, 1], [1-probability, probability])[0]
    for i in range(n):
        for j in range(n):
            if adjMatrix[i][j] == 1:
                adjTable[i].append(j)
    return adjTable


def creat_threshold(n, referrence=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]):
    ''' 创建阈值 '''
    threshold = list(random.choices(referrence, k=n))
    return threshold


def print_adjTable(adjTable, threshold):
    ''' 打印邻接表 '''
    print("Adjacency Table:")
    for i in range(len(adjTable)):
        print(f"<Node{i}>", end='')
        print(f"threshold={threshold[i]}", " adjanceNode: ", sep=",", end="")
        print(* adjTable[i], sep=",")


def spread(adjTable, threshold, start):
    ''' 从知晓到扩散 '''
    n = len(adjTable)
    # 初始化 接受集，知晓时间点，延时
    accept = set()
    kown_time = [-1 for _ in range(len(adjTable))]
    delay = [-1 for _ in range(len(adjTable))]

    # 初始化初始节点为已接受，其邻接点为已知晓，时间点为0
    time = 0
    accept.add(start)
    kown_time[start] = 0
    delay[start] = 0
    for adj in adjTable[start]:
        kown_time[adj] = 0

    # 迭代，直到不再有扩散的可能
    while True:
        time += 1
        new_accept = set({})  # 记录本轮新扩散的节点
        for node in range(n):
            if node in accept:
                continue
            # 判断是否满足阈值要求
            if 1+len(list(filter(lambda adj: adj in accept, adjTable[node]))) >= threshold[node]*len(adjTable[node]):
                new_accept.add(node)
                delay[node] = time-kown_time[node]
                # 若该节点成功扩散，则更新其邻接点的知晓时间
                for adj in adjTable[node]:
                    if kown_time[adj] == -1:
                        kown_time[adj] = time

        # 判断是否已经没有节点可以扩散, 如果没有，则退出
        if len(new_accept) == 0:
            break
        accept.update(new_accept)  # 更新接受集

        # 打印本轮结果
        print(f"time {time}:")
        print("accept:", end='')
        for node in new_accept:
            print(f"({node}, delay:{delay[node]})", end=' ')
        print("\n")

    delayTime = list(filter(lambda x: x != -1, delay))
    aver_delay = sum(delayTime)/len(delayTime)
    print("Average delay time: {:.2f}".format(aver_delay))


probability = 0.3
n = 20
print(f"Number of node: {n}",
      " Adjacency probability : {:.2f}".format(probability))
adjanceTable = creat_adjTable(20)
threshold = creat_threshold(20)
print_adjTable(adjanceTable, threshold)
spread(adjanceTable, threshold, 0)
print("Done")
