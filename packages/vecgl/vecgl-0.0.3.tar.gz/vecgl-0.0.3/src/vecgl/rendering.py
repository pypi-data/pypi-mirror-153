from typing import Iterable, List, Optional, Tuple

from vecgl.bb3tree import BB3Tree, BoundingBox3, create_bb3tree
from vecgl.linalg import (
    Vec3,
    add_vec3,
    cross_vec3,
    dot_vec3,
    max_vec3,
    min_vec3,
    scale_vec3,
    sub_vec3,
    to_vec3,
    x_vec3,
    y_vec3,
    z_vec3,
)
from vecgl.model import Line, Model, Point, Triangle

Plane3 = Tuple[Vec3, Vec3]
Volume3 = Tuple[Plane3]


kDefaultEps = 0.000000001


def _get_clipping_space_volume() -> Volume3:

    # Collect the 6 boundary planes.
    # Ensure that normals point away from the clipping space volume.
    boundary_planes: List[Plane3] = []
    for i in range(3):
        for a in [-1.0, 1.0]:
            u = [0.0, 0.0, 0.0]
            u[i] = a
            p = tuple(u)
            n = tuple(u)
            pl = p, n
            boundary_planes.append(pl)
    return tuple(boundary_planes)


def _get_covered_triangle_volume(tr: Triangle) -> Volume3:
    p, q, r = tr.p, tr.q, tr.r

    # Do this in non-homogenious coordinates.
    p = to_vec3(p)
    q = to_vec3(q)
    r = to_vec3(r)

    # Get the triangle plane.
    pq = sub_vec3(q, p)
    pr = sub_vec3(r, p)
    n = cross_vec3(pq, pr)

    # Derive boundary plane.
    # Ensure that normals point away from the covered volume.
    ccwise = -1.0 if z_vec3(n) > 0.0 else 1.0
    n = scale_vec3(ccwise, n)
    boundary_planes = [(p, n)]

    # Collect the three remaining boundary planes per side of the triangle.
    n_pq = -ccwise * y_vec3(pq), ccwise * x_vec3(pq), 0.0
    boundary_planes.append((p, n_pq))
    qr = sub_vec3(r, q)
    n_qr = -ccwise * y_vec3(qr), ccwise * x_vec3(qr), 0.0
    boundary_planes.append((q, n_qr))
    rp = sub_vec3(p, r)
    n_rp = -ccwise * y_vec3(rp), ccwise * x_vec3(rp), 0.0
    boundary_planes.append((r, n_rp))

    return tuple(boundary_planes)


def _get_plane_side(pl: Plane3, q: Vec3) -> float:
    p, n = pl
    pq = sub_vec3(q, p)
    return dot_vec3(pq, n)


def _get_plane_line_intersection(
    pl: Plane3, q: Vec3, r: Vec3, eps: float = kDefaultEps
) -> Optional[float]:
    p, n = pl
    qr = sub_vec3(r, q)
    qp = sub_vec3(p, q)
    denom = dot_vec3(qr, n)
    if abs(denom) < eps:
        return None
    return dot_vec3(qp, n) / denom


def _get_point_on_line(a: float, p: Vec3, q: Vec3) -> Vec3:
    return add_vec3(scale_vec3(1.0 - a, p), scale_vec3(a, q))


def _get_triangle_query(bb: BoundingBox3) -> BoundingBox3:
    lb_x, lb_y, _ = bb.lb
    query_lb = lb_x, lb_y, -1.0
    query_ub = bb.ub
    return BoundingBox3(query_lb, query_ub)


def _is_point_visible_wrt_clipping_space(pt: Point, eps: float = kDefaultEps) -> bool:

    # Do this in non-homogenious coordinates.
    p = to_vec3(pt.p)

    px, py, pz = p
    lb = -1.0 - eps
    if px < lb or py < lb or pz < lb:
        return False
    ub = 1.0 + eps
    if px > ub or py > ub or pz > ub:
        return False
    return True


def _is_point_visible_wrt_triangle(
    pt: Point, tr: Triangle, eps: float = kDefaultEps
) -> bool:

    # Do this in non-homogenious coordinates.
    p = to_vec3(pt.p)

    # If point is on or outside of any boundary plane then it is visible.
    boundary_planes = _get_covered_triangle_volume(tr)
    for pl in boundary_planes:
        if _get_plane_side(pl, p) >= -eps:
            return True
    return False


def _get_point_bbox(pt: Point) -> BoundingBox3:

    # Do this in non-homogenious coordinates.
    p = to_vec3(pt.p)

    return BoundingBox3(p, p)


def _get_visible_points(
    points: Iterable[Point], triangle_tree: BB3Tree
) -> Iterable[Point]:
    for pt in points:
        if not _is_point_visible_wrt_clipping_space(pt):
            continue

        triangle_query = _get_triangle_query(_get_point_bbox(pt))
        rel_triangles = triangle_tree.find(triangle_query)
        if all(_is_point_visible_wrt_triangle(pt, tr) for tr in rel_triangles):
            yield pt


def _get_line_fragments_outside_convex_volume(
    ln: Line, boundary_planes: Volume3, inverted: bool = False, eps: float = kDefaultEps
) -> Tuple[bool, List[Line]]:

    # Do this in non-homogenious coordinates.
    p, q = to_vec3(ln.p), to_vec3(ln.q)

    # For convex volumes, the line fragments outside of the volume will be at
    # most two:
    #   - a head fragment starting in p, and
    #   - a tail fragment ending in q.
    # For a line fragment to be outside of the volume, it must be on the outer
    # side of one of the boundary planes. Start with empty head and tail
    # fragments as an under approximation.
    head_fragment_ub = 0.0
    tail_fragment_lb = 1.0

    # Find the complete line fragments by updating them per boundary plane.
    pq = sub_vec3(q, p)
    for pl in boundary_planes:
        intersection = _get_plane_line_intersection(pl, p, q)
        if intersection is not None:

            # Line and boundary plane intersect. Update head and tail fragment.
            _, n = pl
            is_same_direction = dot_vec3(n, pq) > 0
            if is_same_direction:
                tail_fragment_lb = min(intersection, tail_fragment_lb)
            else:
                head_fragment_ub = max(intersection, head_fragment_ub)
        else:

            # Line and boundary plane are parallel to each other. Return the
            # line unchanged if it is entirely outside of the volume.
            is_outside_volume = _get_plane_side(pl, p) >= -eps
            if is_outside_volume:
                intersects = False
                return intersects, [ln] if not inverted else []

    # If head and tail fragment are overlapping, the line does not intersect the
    # volume and we can return it as is.
    if head_fragment_ub + eps >= tail_fragment_lb:
        intersects = False
        return intersects, [ln] if not inverted else []

    # Otherwise, the line and triangle intersect, resulting in up to two line
    # fragments.
    intersects = True
    lines: List[Line] = []
    if not inverted:
        if head_fragment_ub >= eps:
            head_fragment_q = _get_point_on_line(head_fragment_ub, p, q)
            head_fragment = Line(p, head_fragment_q, ln.color)
            lines.append(head_fragment)
        if tail_fragment_lb <= 1.0 - eps:
            tail_fragment_p = _get_point_on_line(tail_fragment_lb, p, q)
            tail_fragment = Line(tail_fragment_p, q, ln.color)
            lines.append(tail_fragment)
    else:
        center_fragment_p = _get_point_on_line(head_fragment_ub, p, q)
        center_fragment_q = _get_point_on_line(tail_fragment_lb, p, q)
        center_fragment = Line(center_fragment_p, center_fragment_q, ln.color)
        lines.append(center_fragment)
    return intersects, lines


def _get_visible_line_fragment_wrt_clipping_space(ln: Line) -> Optional[Line]:
    boundary_planes = _get_clipping_space_volume()
    _, line_fragments = _get_line_fragments_outside_convex_volume(
        ln, boundary_planes, inverted=True
    )
    assert len(line_fragments) <= 1
    if len(line_fragments) == 1:
        return line_fragments[0]
    return None


def _get_visible_line_fragments_wrt_triangle(
    ln: Line, tr: Triangle, eps: float = kDefaultEps
) -> Tuple[bool, List[Line]]:
    boundary_planes = _get_covered_triangle_volume(tr)
    return _get_line_fragments_outside_convex_volume(ln, boundary_planes, False, eps)


def _get_line_bbox(ln: Line) -> BoundingBox3:

    # Do this in non-homogenious coordinates.
    p, q = to_vec3(ln.p), to_vec3(ln.q)

    lb = min_vec3(p, q)
    ub = max_vec3(p, q)
    return BoundingBox3(lb, ub)


def _get_visible_line_fragments(
    lines: List[Line], triangle_tree: BB3Tree
) -> List[Line]:

    # Find visible line fragments wrt. clipping space.
    line_fragments_in_clipping_space: List[Line] = []
    for ln in lines:
        ln_fragment = _get_visible_line_fragment_wrt_clipping_space(ln)
        if ln_fragment is not None:
            line_fragments_in_clipping_space.append(ln_fragment)

    # Find visible line fragments within clipping space.
    visible_line_fragments: List[Line] = []
    worklist = line_fragments_in_clipping_space
    while len(worklist) > 0:
        ln = worklist.pop()
        triangle_query = _get_triangle_query(_get_line_bbox(ln))
        is_fully_visible = True
        for tr in triangle_tree.find(triangle_query):
            intersects, ln_fragments = _get_visible_line_fragments_wrt_triangle(ln, tr)
            if intersects:
                worklist.extend(ln_fragments)
                is_fully_visible = False
                break
        if is_fully_visible:
            visible_line_fragments.append(ln)
    return visible_line_fragments


def _get_triangle_bbox(tr: Triangle) -> BoundingBox3:

    # Do this in non-homogenious coordinates.
    p, q, r = to_vec3(tr.p), to_vec3(tr.q), to_vec3(tr.r)

    lb = min_vec3(p, min_vec3(q, r))
    ub = max_vec3(p, max_vec3(q, r))
    return BoundingBox3(lb, ub)


def render(model: Model) -> Model:
    rendered = Model()
    triangle_tree = create_bb3tree(model.triangles, _get_triangle_bbox)
    rendered.points = list(_get_visible_points(model.points, triangle_tree))
    rendered.lines = _get_visible_line_fragments(model.lines, triangle_tree)
    rendered.triangles = model.triangles  # Not yet implemented.
    rendered.rendered = True
    return rendered
