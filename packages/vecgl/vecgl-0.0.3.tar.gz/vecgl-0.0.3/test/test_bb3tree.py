from typing import List

from vecgl.bb3tree import BoundingBox3, create_bb3tree


def test_disjoint_bboxes():

    # Create 9 test bounding boxes from spanning form 0-1, 2-3, and 4-5 in each
    # dimension.
    bboxes: List[BoundingBox3] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lb = 2.0 * i, 2.0 * j, 2.0 * k
                ub = 2.0 * i + 1.0, 2.0 * j + 1.0, 2.0 * k + 1.0
                bboxes.append(BoundingBox3(lb, ub))

    # For testing, use the bounding boxes also as values.
    bbtree = create_bb3tree(bboxes, lambda bb: bb)

    # Assert all yielded bounding boxes to intersect with the query.
    count = 0
    query = BoundingBox3((0.5, 0.5, 0.5), (1.5, 2.5, 4.5))
    for bb in bbtree.find(query):
        assert not query.intersect(bb).empty()
        count += 1
    assert count == 6


def test_overlapping_bboxes():

    # Create 9 test bounding boxes from spanning form 0-2, 1-3, and 2-4 in each
    # dimension.
    bboxes: List[BoundingBox3] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                lb = 1.0 * i, 1.0 * j, 1.0 * k
                ub = 1.0 * i + 2.0, 1.0 * j + 2.0, 1.0 * k + 2.0
                bboxes.append(BoundingBox3(lb, ub))

    # For testing, use the bounding boxes also as values.
    bbtree = create_bb3tree(bboxes, lambda bb: bb)

    # Assert all yielded bounding boxes to intersect with the query.
    count = 0
    query = BoundingBox3((0.5, 2.5, 3.5), (1.5, 3.5, 4.0))
    for bb in bbtree.find(query):
        assert not query.intersect(bb).empty()
        count += 1
    assert count == 4


def test_yield_tangent_bboxes():
    bbox = BoundingBox3((0.0, 1.0, 2.0), (1.0, 2.0, 3.0))
    elems = ["the bbox"]
    bbtree = create_bb3tree(elems, lambda e: bbox)

    tangent_query_lbx = BoundingBox3((-1.0, 1.5, 2.5), (0.0, 2.5, 3.5))
    count = 0
    for value in bbtree.find(tangent_query_lbx):
        assert value == "the bbox"
        count += 1
    assert count == 1

    tangent_query_ubx = BoundingBox3((1.0, 1.5, 2.5), (2.0, 2.5, 3.5))
    count = 0
    for value in bbtree.find(tangent_query_ubx):
        assert value == "the bbox"
        count += 1
    assert count == 1
