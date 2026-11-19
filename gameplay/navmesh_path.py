"""导航网格寻路：漏斗、代价与路径裁剪：待实现的核心模块。"""

from __future__ import annotations


def portal_side(prev, curr, next):
    """返回路径在 curr 处的转向：left/right/straight。"""
    raise NotImplementedError

def path_cost(points, offmesh_penalty):
    """返回路径总代价。"""
    raise NotImplementedError

def clip_path(points, max_cost):
    """按预算裁剪路径，返回保留的点。"""
    raise NotImplementedError
