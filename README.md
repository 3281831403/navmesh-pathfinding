# 导航网格寻路：漏斗、代价与路径裁剪

寻路在漏斗拐点、动态障碍代价、路径平滑和预算裁剪上出错。本仓库固定路径几何与代价契约。

- 领域：游戏、图形与多媒体
- 子方向：其他
- 语言/框架：Python 3, pytest
- 初始状态：15 个参数化用例全部失败

## 目录结构

```
README.md
conftest.py
.gitignore
gameplay/__init__.py
gameplay/navmesh_path.py
tests/test_navmesh_path.py
```

## 需要修复的 10 个问题

1. 漏斗算法按左右边界收窄，不切出可行走区域
2. off-mesh link 计入额外代价与角色半径
3. 路径总长度按欧氏距离累计
4. 路径平滑不穿越障碍
5. 预算不足时返回可走的部分路径
6. 动态障碍按当前帧重算代价
7. 多角色路径缓存按角色隔离
8. 异步寻路结果校验起点与终点
9. 导航网格版本变化后丢弃旧路径
10. 路径点去重，避免原地抖动

## 15 条验收契约

    01. portal left — `portal_side`
    02. portal right — `portal_side`
    03. portal straight — `portal_side`
    04. portal back — `portal_side`
    05. portal diag — `portal_side`
    06. cost two — `path_cost`
    07. cost three — `path_cost`
    08. cost offmesh — `path_cost`
    09. cost zero — `path_cost`
    10. cost diag — `path_cost`
    11. clip full — `clip_path`
    12. clip partial — `clip_path`
    13. clip zero — `clip_path`
    14. clip one — `clip_path`
    15. clip all — `clip_path`

## 当前状态

`gameplay/navmesh_path.py` 只保留函数签名与文档字符串，所有函数体统一
`raise NotImplementedError`。`tests/test_navmesh_path.py` 使用一个
`@pytest.mark.parametrize` 装载 15 条契约，初始全部失败且没有 collection error。

```bash
python -m pytest -q
```

预期输出包含 `15 failed`。实现 `gameplay/navmesh_path.py` 后，15 条契约应全部通过。
