from typing import Any, Callable, Iterator, List, Optional, Tuple

from vecgl.linalg import Vec3, max_vec3, min_vec3


class BoundingBox3:
    def __init__(self, lb: Vec3, ub: Vec3):
        self.lb = lb
        self.ub = ub

    def union(self, other: "BoundingBox3") -> "BoundingBox3":
        lb = min_vec3(self.lb, other.lb)
        ub = max_vec3(self.ub, other.ub)
        return BoundingBox3(lb, ub)

    def intersect(self, other: "BoundingBox3") -> "BoundingBox3":
        lb = max_vec3(self.lb, other.lb)
        ub = min_vec3(self.ub, other.ub)
        return BoundingBox3(lb, ub)

    def empty(self) -> bool:
        for a, b in zip(self.lb, self.ub):
            if a > b:
                return True
        return False


class BB3Tree:
    def __init__(
        self,
        bbox: Optional[BoundingBox3],
        lhs: Optional["BB3Tree"],
        rhs: Optional["BB3Tree"],
        elem: Optional[Any],
    ):
        self.bbox = bbox
        self.lhs = lhs
        self.rhs = rhs
        self.elem = elem

    def find(self, query: BoundingBox3) -> Iterator[Any]:
        if self.bbox == None or self.bbox.intersect(query).empty():
            return
        if self.elem is not None:
            yield self.elem
        if self.lhs is not None:
            yield from self.lhs.find(query)
        if self.rhs is not None:
            yield from self.rhs.find(query)


def _create_bb3tree_recusrively(
    pairs: List[Tuple[BoundingBox3, Any]], split_dim: int
) -> BB3Tree:

    # Empty case.
    if len(pairs) == 0:
        return BB3Tree(None, None, None, None)

    # Single element case.
    if len(pairs) == 1:
        bbox, elem = pairs[0]
        return BB3Tree(bbox, None, None, elem)

    # Sort elements by their bounding box center in the split dimension.
    pairs.sort(key=lambda pair: pair[0].lb[split_dim] + pair[0].ub[split_dim])

    # Split in half and recur.
    split_at = len(pairs) // 2
    pairs_lhs = pairs[:split_at]
    pairs_rhs = pairs[split_at:]
    split_dim_next = (split_dim + 1) % 3
    assert len(pairs_lhs) >= 1 and len(pairs_rhs) >= 1
    lhs = _create_bb3tree_recusrively(pairs_lhs, split_dim_next)
    rhs = _create_bb3tree_recusrively(pairs_rhs, split_dim_next)

    # Find enclosing bounding box and create tree.
    assert lhs.bbox is not None and rhs.bbox is not None
    surrounding_bbox = lhs.bbox.union(rhs.bbox)
    return BB3Tree(surrounding_bbox, lhs, rhs, None)


def create_bb3tree(elems: List[Any], fn_bbox3: Callable[[Any], BoundingBox3]):
    pairs = [(fn_bbox3(e), e) for e in elems]
    initial_split_dim = 0
    return _create_bb3tree_recusrively(pairs, initial_split_dim)
