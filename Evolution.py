# author: Kim Iheon
# version: 9
# 논리적 오류 해결

import random
import Prototype_Network as net


# import Network as net


# 염색체를 생성하고 진화시키는 클래스
class Chrom:
    def __init__(self):
        pass

    # 첫번째 세대의 염색체를 생성하는 함수
    # param {Int} num_net 신경망 염색체의 개수
    # param {Int} num_node 신경망의 초기 노드 수
    # param {Int} len_chrom 염색체의 길이
    # param {Int} num_in 입력 노드의 개수
    # param {Int} num_out 출력 노드의 개수
    # return {List} chrom_list 첫번째 세대의 모든 염색체를 리턴
    def create_chrom(self, num_net, num_node, len_chrom, num_in, num_out):
        self.NUM_NET = num_net
        self.NUM_NODE = num_node
        self.LEN_CHROM = len_chrom
        self.NUM_IN = num_in
        self.NUM_OUT = num_out
        self.chrom_list = []
        self.net_net = []

        # 현재 세대 수
        self.generation = 1

        # 하나의 신경망 염색체
        _network = []

        # 한 세대의 모든 염색체
        chrom_list = []

        # 존재하는 모든 노드의 리스트
        _node_list = list(range(num_node))

        # 시냅스의 시작과 끝에 존재가능한 노드
        _start_list = _node_list[:-num_out]
        _end_list = _node_list

        for m in range(num_net):
            for n in range(len_chrom):
                _start_node = random.choice(_start_list)

                # 시작과 끝이 중복일 가능성을 제거
                # 시이클을 제거하기 위해 시작 노드보다 커야함
                del _end_list[:_start_node + 1]

                _end_node = random.choice(_end_list)
                _end_list = list(range(num_node))
                synapse = (_start_node, _end_node)

                # 시냅스의 연결 여부
                connect = random.randint(0, 1)
                _network.append([synapse, connect])
            chrom_list.append(_network)
            _network = []

        self.chrom_list = chrom_list

        return chrom_list

    # 현재 세대의 염색체를 출력하는 함수
    # return {List} self.chrom_list 현재 세대의 모든 염색체를 리턴
    def get_chrom(self):
        return self.chrom_list

    # 현재 세대를 출력하는 함수
    # return {Int} self.generation 현재 세대를 받아옴
    def get_generation(self):
        return self.generation

    # 현재 개체의 품질을 평가하는 함수
    # param {Function} qual_func 개체의 품질을 평가하는 함수
    # return {List} qual_list 각 개체의 품질
    def get_quality(self, qual_func):
        chrom_list = self.expression()

        qual_list = []

        # 각 개체들의 품질을 평가한다
        for i in range(self.NUM_NET):
            i_qual = qual_func(chrom_list[i])
            qual_list.append(i_qual)

        self.qual_list = qual_list

        return qual_list

    # 한 세대의 염색체들을 신경망으로 발현하는 함수
    # return {List} result_exp 한 세대를 신경망으로 모두 발현
    def expression(self):
        result_exp = []

        # 현재 새대의 모든 염색체를 받아옴
        chrom_list = self.chrom_list

        for chrom in chrom_list:
            network = {}
            node_list = list(range(self.NUM_NODE))
            catch = []

            # 존재하는 유전자들을 발현
            for loc, prop in chrom:

                # 과잉 표현을 무시한다
                if loc not in catch:
                    if prop == 0:
                        catch.append(loc)
                    else:
                        network[loc] = random.random()
                        catch.append(loc)

            # 결손 표현들을 발현
            for i in range(self.NUM_NODE):
                for j in range(self.NUM_NODE):

                    # 사이클 제거
                    if i < j:
                        if (i, j) not in catch:

                            # 결손 표현이 발현될 확흏
                            p_exp = 0.2
                            if random.random() < p_exp:
                                network[(i, j)] = random.random()

            result_exp.append(network)

        self.net_list = result_exp

        return result_exp

    # 현재 세대 모든 염색체의 적합도 리스트를 리턴
    # return {List} fit_list 현재 세대의 모든 염색체의 적합도
    def fitness(self):

        # 현재 새대의 모든 개체를 받아옴
        chrom_list = self.net_list

        # 각 개체의 품질, 먼저 get_quality를 실행했어야 함
        qual_list = self.qual_list

        # 적합도 리스트
        fit_list = []

        # 가장 좋은 품질과 가장 안 좋은 품질
        best_qual = min(qual_list)
        werst_qual = max(qual_list)

        # 각 염색체에 대해 적합도를 계산
        for i_qual in qual_list:
            i_fit = (werst_qual - i_qual) \
                    + ((werst_qual - best_qual) / 3)
            fit_list.append(i_fit)

        self.fit_list = fit_list

        return fit_list

    # 적합도 리스트와 룰렛 휠 선택을 이용해 염색체를 선택
    # param {Tuple} num 선택하는 염색체의 개수. 없으면 1개 선택
    # return {List} sel_list 선택된 염색체 리스트
    def selection(self, *num):
        sel_list = []

        # 현재 새대의 모든 염색체를 받아옴
        chrom_list = self.chrom_list

        # 이전에 fitness를 실행했어야함
        fit_list = self.fit_list

        # 선택하는 염색체수. 입력하지 않으면 2개 선택
        cycle = 2 if num == () else num[0]
        point = random.uniform(0, sum(fit_list))
        sum_fit = 0

        for k in range(cycle):
            for i in range(self.NUM_NET):
                sum_fit += fit_list[i]
                if point < sum_fit:
                    sel_list.append(self.chrom_list[i])
                    break

        return sel_list

    # 두 부모 염색체를 교차시켜 자식염색체 두개를 얻음
    # param {List} sel_list 부모로 선택된 두 염색체
    # return {List} child 교차 후 두 자식 염색체
    def crossover(self, sel_list):
        parent1 = sel_list[0]
        parent2 = sel_list[1]
        cut_chrom1 = random.randint(0, len(parent1))
        cut_chrom2 = random.randint(0, len(parent2))

        # 일점 교차 방식을 이용
        child = [parent1[:cut_chrom1] + parent2[cut_chrom2:],
                 parent2[:cut_chrom2] + parent1[cut_chrom1:]]

        return child

    # 일정 확률로 염색체의 유전자를 변이시킴
    # param {List} chrom 변이시킬 염색체
    # return {List} result_mut 변이 후 염색체
    def mutation(self, chrom):
        num_node = self.NUM_NODE
        result_mut = chrom

        # 변이 확률
        p_mut = 0.001

        for k in range(len(chrom)):

            # 시이클을 제거
            if k // num_node > k % num_node:
                point = random.random()
                if point < p_mut:
                    result_mut[k] = (chrom[k][0], 1 - chrom[k][1])

        return result_mut

    # 해집단중 가장 품질이 낮은 해를 대치
    # 정규화를 만든 후에 군집대치 적용
    # param {List} child 교차, 변이된 자식 염색체 집단
    # return {List} result_rep 대치 이후 염색체 집단
    def replacement(self, child_list):
        result_rep = self.chrom_list

        # 대치 횟수
        rep_time = len(child_list)

        # 적합도 리스트
        fit_list = self.fit_list
        fit_list = sorted(fit_list)

        # 가장 낮은 품질을 횟수만큼 뽑음
        worst_fit = fit_list[:rep_time]

        # 정렬했던 것을 초기화
        fit_list = self.fit_list

        # 모든 자식 염색체들을 대치
        for k in range(len(worst_fit)):
            fit = worst_fit[k]

            # 대치할 염색체의 위치
            rep_loc = fit_list.index(fit)
            result_rep[rep_loc] = child_list[k]

        return result_rep

    # 각 연산을 수행해 기존 염색체 집단을 진화시킴
    # param {int} num_evol 진화시킬 횟수
    # param {Int} num_child 생성할 자식 염색체의 수
    # param {Function} qual_func 염색체의 품질을 정하는 함수
    # return {Tuple} all_qual, all_net 각 세대별 모든 개체와 그 품질
    def evolution(self, num_evol, num_child, qual_func):
        all_qual = []
        all_net = []

        for k in range(num_evol):

            # 각 개체의 품질을 계산
            k_qual = self.get_quality(qual_func)
            all_qual.append(k_qual)
            all_net.append(self.net_list)

            print(self.generation)
            print(sorted(k_qual))

            # 적합도를 계산
            self.fitness()

            # 자식 염색체 리스트
            child_list = []
            for i in range(num_child):

                # 교차 연산의 결과인 두 자식 중 하나를 선택
                selec = random.randint(0, 1)

                # 부모 염색체 선택
                sel_list = self.selection()

                # 교차후 자식 염색체
                child = self.crossover(sel_list)[selec]

                # 자식 염색체를 변이
                child = self.mutation(child)
                child_list.append(child)

            # 기존 염색체를 생성된 자식 염색체로 대치
            self.chrom_list = self.replacement(child_list)

            # 세대를 1 증가
            self.generation += 1

        # 마지막으로 생성된 세대를 평가함
        last_qual = self.get_quality(qual_func)
        all_qual.append(last_qual)
        all_net.append(self.net_list)

        print(self.generation)
        print(sorted(last_qual))

        return all_qual, all_net