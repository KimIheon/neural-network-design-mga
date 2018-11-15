# author: Lee Yechan

import random
import scipy.special

# [num_net, num_node, num_route, num_in, num_out] = map(int, input().split())
num_net, num_node, num_sys, num_in, num_out = 70, 14, 50, 4, 4  #개체 수, 노드의 수, 연결의 수, 입력노드의 수, 출력노드의 수
node_list = [i for i in range(num_node)]

gene_list = []
network = []

class Node:   #노드 객체를 만든다
    def __init__(self):             #노드 생성자
        self.value_inf = 0          #노드의 처음 값
        self.value_fin = 0          #노드의 나중 값
        pass

    def change_value(self, delta):  #노드의 값을 더해주는 함수
        self.value_fin += delta     #원래 있던 노드의 나중값에 델타(이전 노드의 처음 값 * 가중치 가 될 예정)를 더해간다
        return

    def func(self) :                #전이 함수
        self.value_inf = scipy.special.expit(self.value_fin)  #노드의 처음 값을 노드의 나중 값에 시그모이드함수를 취한 값으로 한다
        self.value_fin = 0                                    #노드의 나중 값을 0으로 설정한다
        pass
    pass


class Network() :       #신경망 개체
    def __init__ (self, gene_list) :         #생성자
        self.network = [Node() for i in range(num_node)]    #노드 수 만큼 노드 객체를 만들어 신경망의 network에 대입한다
        self.learning = 100  #신경망의 학습률이다.
        self.path_check = False
        self.count = 0
        self.gene_list = gene_list.keys()
        self.weight = gene_list

    def calculate(self, input_list) :  #계산함수
        self.restart()   #계산을 시작하기 전에 모든 노드의 나중 값을 0으로 설정한다
        for i in range(num_in) :     #모든 입력노드의 인덱스 값에 대하여
            if int(input_list[i]) :      #만약 입력리스트 값이 1(True)이면
                self.network[i].value_inf = 1  #입력노드의 초기 값을 1로 설정한다
            else :
                self.network[i].value_inf = -1 # 0(False)면 -1로 설정한다
        for i in range(num_node - num_out, num_node) :  #모든 출력노드에 대해서
            self.network[i].path_number = 0   #출력노드의 경로 길이 값(후술)을 0으로 설정한다


        self.result = [[self.network[i].value_inf] for i in range(num_node)]  #모든 계산 단계에서 모든 노드의 초기값을 저장할 것이다.
        tmp = 0  #값이 들어온 출력노드의 수
        for i in range(num_node) :
            if i < num_in :
                self.result[i].append(self.network[i].value_inf) 
            else :
                self.result[i].append(0)

        while True :
            for i in self.gene_list :  #염색체의 모든 유전자에 대해서
                self.network[i[1]].change_value(self.network[i[0]].value_inf * self.weight[(i[0], i[1])] )

                                            # 나중 노드의 나중 값에 (초기 노드의 초기 값 * 가중치)를 더한다


            for i in range(num_node - num_out) :  #입력, 출력노드를 제외한 모든 노드에서
                if self.network[i].value_fin != 0 :
                    self.network[i].func()  #전이함수처리를 한다.
                else :
                    self.network[i].value_inf = 0
            for i in range(num_in) :
                self.network[i].value_inf = 0
            if all([self.network[i].value_inf == 0 for i in range(num_in, num_node - num_out)]) :
                for i in range(num_node - num_out, num_node) :
                    self.network[i].func()
                for i in range(num_node) :
                    self.result[i].append(self.network[i].value_inf)
                break #while문을 종료한다
            else :
                for i in range(num_node) :
                    self.result[i].append(self.network[i].value_inf)
        return [self.network[i].value_inf for i in range(num_node - num_out, num_node)] #이 함수의 함숫값으로 
    
    def path(self) : #입력노드에서 출력노드로 가는 경로를 찾아주는 함수이다.
        start = [i for i in range(num_node - num_out, num_node)]  #경로 탐색알고리즘을 할 것인데, 출력노드에서부터 입력노드로 탐색한다
        path = [[i] for i in start if self.result[i]]   #경로목록

        self.visit = {} #노드마다 경로 수 새려고
        connect = {} #노드마다 갈 수 있는 이전 노드 목록
        result = []   #경로 목록
        for i in range(num_node) :
            connect[i] = []  #노드마다 갈 수 있는 이전 노드를 더해가기 위해 리스트를 만든다
        for i in self.gene_list :  #모든 유전자에 대해서
            connect[i[1]].append(i[0])   #나중 노드 리스트에 이전 노드를 더한다.
        cnt = 1 #처음 경로의 길이는 1로 시작한다.

        while True :
            path2 = []  #새로 생기는 경로를 여기에 저장한다
            for i in path :  #기존에 있던 모든 경로에 대해서
                for j in connect[i[cnt-1]] : #마지막 노드에 연결된 모든 노드에 대해서
                    path2.append( i+[j] )  #경로 목록에 새로운 경로를 추가한다
            path = [i for i in path2]
            if len(path2) == 0  :
                break   #만약 경로가 새로 생기지 않았거나, 출력 노드에 도달하는 경로의 수보다 현재 경로들의 수가 더 크면 break문을 쓴다
            else : #아니면
                for i in path2 :    #모든 새로운 경로에 대해
                    if i[cnt] in range(num_in) : #마지막 노드가 입력 노드이면
                        result.append(i)   #경로 목록에 경로를 추가하고
                        path.remove(i)    #새로운 경로 목록에는 제외한다
                cnt += 1   #지금 현재 경로 길이를 하나 더한다

        self.result2 = []   #모든 경로에 대해서 경로를 쪼갤 것이다.
        for i in result :
            road = []
            for j in range(len(i)-1) :
                road.append((i[j], i[j+1]))
            self.result2.append(road)   #모든 경로에 대해서 앞뒤로 (i, j)형식으로 경로를 나눈다.
        self.path_check = True  #학습시킬 때마다 경로를 찾으면 시간 낭비이므로 경로가 찾았는지 아닌지 저장한다

    def train(self, input_list) :  #학습함수이다.
        self.target_list = [abs(int(input_list[i]) -0.01) for i in range(num_in)]
        output_list = self.calculate(input_list)  #결과 목록에 계산된 값을 넣는다

        if not self.path_check :  #만약 경로를 안 찾아놨으면
            self.path()    #경로 찾기 함수를 실행시킨다.

        error = {}   #노드의 에러를 여기에 저장한다
        weight_sum = {}  #분기점에서 어떤 노드의 가중치의 합을 나타낸다.
        for i in range(num_node) :
            for j in range(num_node) :  #모든 노드간 (i, j) 연결에 대해서
                if (i, j) in self.weight.keys() :
                    weight_sum[(i,j)] = self.weight[(i,j)]   #가중치의 합에 자기 자신의 가중치로 초기 설정한다.

        for i in range(num_node - num_out, num_node) :  #모든 출력노드에 대해서
            error[i] = self.target_list[i+num_out - num_node] - output_list[i +num_out - num_node]
                            #오차값을 (목표값 - 결과값)으로 설정한다

        for i in self.result2 :   #계산과정에서 저장한 모든 단계에 다른 모든 노드의 결과값(전이함수 처리 후)이 저장되어있다.
            point = []  #경로가 갈라지는 분기점을 저장한다
            tmp = 0
            for j in i :
                tmp += 1
            for j in self.result2:
                if i[0][0] == j[0][0] :
                    for k in range( len(i) ) :
                        if i[k] == j[k] :
                            continue
                        else :
                            weight_sum[i[k][::-1]] += self.weight[j[k][::-1]]
                            if i[k] not in point :
                                point.append(i[k])

                            break
            errors = [error[i[0][0]]]
            length = len(i)
            for j in range(length) :
                oi = self.result[i[k][1]][length-k-4]
                oj = self.result[i[k][0]][length-k-3]
                if i[j] not in point :
                    errors.append(errors[j])
                    self.weight[i[j][::-1]] += self.learning*errors[j]*oj*(1-oj)*oi
                    k = j
                else :
                    x = errors[j]*self.weight[i[j][::-1]]/weight_sum[i[j][::-1]]
                    for l in range(k+1, length) :
                        self.weight[i[j][::-1]] += self.learning*x*oj*(1-oj)*oi
                    break
            for i in range(num_node) :
                for j in range(num_node) :  #모든 노드간 (i, j) 연결에 대해서
                    if (i, j) in self.weight.keys() :
                        weight_sum[(i,j)] = self.weight[(i,j)]   #가중치의 합에 자기 자신의 가중치로 초기 설정한다.


        
    def query(self, inputs_list) :  #입력 데이터를 바탕으로 결과를 출력한다
        result = self.calculate(inputs_list)
        return ((result[0]-0.01)*8 + (result[1]-0.01)*4 + (result[2]-0.01)*2 + (result[3]-0.01))*100/98

    
    def restart(self) :  #모든 노드의 값을 초기화하는 함수이다. 계산을 하기 전에 쓰인다.
        for i in self.network :
            i.value_inf, i.value_fin = 0, 0
            
    def quality(self, n) :   #신경망을 평가하는 함수이다. 값이 클수록 나쁜 신경망이라는 것을 나타낸다.
        data = ['0000', '0001','0010','0011','0100','0101','0110','0111','1000', '1001','1010','1011','1100','1101','1110','1111']
        cnt = 0
        print(1,end = ' ')
        for j in range(n) :
            for i in data :
                self.train(i)
        for i in data :
            cnt += (int(i,2) - self.query(i))**2 #오차의 제곱을 더한다

        return cnt

