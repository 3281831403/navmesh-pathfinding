"""导航网格寻路：漏斗、代价与路径裁剪。

本模块固定路径几何与代价契约：

* :func:`portal_side` 判断漏斗在中间路径点处的转向。叉积为正表示向左
  （逆时针）收窄，为负表示向右收窄，为零表示共线直行（包含折返）。
* :func:`path_cost` 按欧氏距离累计路径长度，并为每一段 off-mesh link
  追加额外代价（角色半径、跳跃/攀爬等开销由调用方折算进
  ``offmesh_penalty``）。
* :func:`clip_path` 在预算不足时返回仍然可走的前缀路径。路径点不会被
  插值或拉直，裁剪只会在既有路径点之间截断，因此不会切出可行走区域。

三个函数都是纯函数，不修改入参，也不依赖任何全局状态（缓存/异步结果
应由调用方按角色与导航网格版本隔离）。
"""

from __future__ import annotations

import math

# 几何比较使用的相对容差。叉积在浮点下很少恰好为 0，直接与 0 比较会让
# 共线的 portal 被误判成左/右转，导致漏斗边界抖动。
_EPS = 1e-12


def _cross(ax, ay, bx, by):
    return ax * by - ay * bx


def portal_side(prev, curr, next):
    """返回路径在 ``curr`` 处的转向：``'left'`` / ``'right'`` / ``'straight'``。

    ``prev -> curr -> next`` 组成的两个向量做二维叉积：

    * 叉积 > 0：向左转（逆时针），漏斗应保留右边界并收窄左边界；
    * 叉积 < 0：向右转（顺时针），漏斗应保留左边界并收窄右边界；
    * 叉积 ≈ 0：共线或折返，按直行处理，不改变漏斗边界。
    """
    ax = curr[0] - prev[0]
    ay = curr[1] - prev[1]
    bx = next[0] - curr[0]
    by = next[1] - curr[1]

    len_a = math.hypot(ax, ay)
    len_b = math.hypot(bx, by)
    # 退化向量（重复路径点）没有方向可言，按直行处理。
    if len_a <= _EPS or len_b <= _EPS:
        return "straight"

    cross = _cross(ax, ay, bx, by)
    # 相对容差：叉积的量级与两向量长度之积成正比。
    if abs(cross) <= _EPS * len_a * len_b:
        return "straight"
    return "left" if cross > 0.0 else "right"


def path_cost(points, offmesh_penalty):
    """返回路径总代价：欧氏长度累计 + 每段 off-mesh link 的额外代价。

    * 长度按相邻路径点的欧氏距离累计，而不是按节点数计数；
    * 每一段都视为一条 link，额外代价按段累加，因此
      ``[(0, 0), (1, 0)]`` 且 ``offmesh_penalty=2.5`` 的代价是 ``3.5``；
    * 少于两个点（或空路径）没有 link，代价为 ``0.0``。

    入参中的重复点距离为 0，不会虚增长度。
    """
    pts = list(points)
    if len(pts) < 2:
        return 0.0

    total = 0.0
    for start, end in zip(pts, pts[1:]):
        total += math.dist(start, end)
        total += offmesh_penalty
    return total


def clip_path(points, max_cost):
    """按预算裁剪路径，返回仍然可走的部分路径（前缀）。

    从起点开始逐段累计欧氏长度；只要累计代价不超过 ``max_cost``，就保留
    该段的终点。一旦下一段会超出预算就停止，不再插值、不再拉直，保证
    返回的路径点全部来自原始路径。

    * 起点始终保留（即使 ``max_cost`` 为 0 或负数），因为原地待命仍然
      是可走的状态；
    * 预算恰好等于累计代价时保留该点（闭区间）；
    * 空路径返回空列表。
    """
    pts = list(points)
    if not pts:
        return []

    kept = [pts[0]]
    cost = 0.0
    # 容忍累计误差，避免恰好等于预算的路径点被浮点误差裁掉。
    limit = max_cost + _EPS
    for start, end in zip(pts, pts[1:]):
        cost += math.dist(start, end)
        if cost > limit:
            break
        kept.append(end)
    return kept
