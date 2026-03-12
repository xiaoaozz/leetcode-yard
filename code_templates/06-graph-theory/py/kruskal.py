from math import inf
from typing import List


class UnionFind:
    """
    并查集
    """

    def __init__(self, n: int):
        # 一开始有n个集合 {0}, {1}, ..., {n - 1}，集合i的代表元是自己
        self._fa = list(range(n))   # 代表元
        self.cc = n # 联通块个数

    # 返回 x 所在集合的代表元
    # 同时做路径压缩，也就是把 x 所在集合中的所有元素的 fa 都改成代表元
    def find(self, x: int) -> int:
        # 如果 fa[x] == x，则表示 x 是代表元
        if self._fa[x] != x:
            self._fa[x] = self.find(self._fa[x])    # fa 改成代表元
        return self._fa[x]

    # 把 from 所在的集合合并到 to 所在的集合中
    # 返回是否合并成功
    def merge(self, from_: int, to: int) -> bool:
        x, y = self.find(from_), self.find(to)
        if x == y:  # from 和 to 在同一个集合中，不做合并
            return False
        self._fa[x] = y # 合并集合，修改后就可以认为 from 和 to 在同一个集合中了
        self.cc -= 1    # 合并成功，连通块个数减一
        return True


def mstKruskal(n: int, edges: List[List[int]]) -> int:
    """
    计算图的最小生成树的边权之和

    时间复杂度 O(n + mlogm)，其中 m 是 edges 的长度
    :param n: 节点个数
    :param edges: 图
    :return: 最小生成树边权之和
    """
    edges.sort(key=lambda e: e[2])  # 按照权重从小到大排序

    uf = UnionFind(n)
    sum_wt = 0
    for x, y, wt in edges:
        if uf.merge(x, y): # x和y不连通，不会成环
            sum_wt += wt
    if uf.cc > 1:
        return inf # 图不联通
    return sum_wt