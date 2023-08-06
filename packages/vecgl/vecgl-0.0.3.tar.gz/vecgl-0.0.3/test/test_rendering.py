from random import uniform

from vecgl.linalg import (
    Vec4,
    get_frustum_mat4,
    get_rotate_y_mat4,
    get_translate_mat4,
    mul_mat4,
    to_vec3,
)
from vecgl.model import Model, get_cube_model
from vecgl.rendering import kDefaultEps, render


def test_render_points_outside_of_clipping_space():
    model = Model()
    model.add_point((1.25, 0.0, 0.0), "green")
    model.add_point((0.0, 1.0, 0.0), "green")
    model.add_point((0.0, 1.0, 0.5), "green")
    rendered = render(model)
    assert len(rendered.points) == 2


def _get_random_vec3(a: float = -2.0, b: float = 2.0):
    return tuple(uniform(a, b) for _ in range(3))


def _is_in_cipping_space(p: Vec4, eps: float = kDefaultEps):
    p3 = to_vec3(p)
    return all(-1.0 - eps <= a and a <= 1.0 + eps for a in p3)


def test_render_random_points():
    model = Model()
    n = 256
    for _ in range(n):
        p = _get_random_vec3()
        model.add_point(p, "green")
    rendered = render(model)
    assert len(rendered.points) <= n
    for pt in rendered.points:
        assert _is_in_cipping_space(pt.p)


def test_render_point_behind_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_point((0.25, 0.25, 1.0), "green")
    rendered = render(model)
    assert len(rendered.points) == 0
    assert len(rendered.triangles) == 1


def test_render_point_in_front_of_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_point((0.25, 0.25, -1.0), "green")
    rendered = render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_next_to_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_point((-0.5, 0.5, 0.0), "green")
    rendered = render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_on_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_point((0.2, 0.2, 0.0), "green")
    rendered = render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_point_on_triangle_edge():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_point((0.5, 0.5, 0.0), "green")
    rendered = render(model)
    assert len(rendered.points) == 1
    assert len(rendered.triangles) == 1


def test_render_lines_outside_of_clipping_space():
    model = Model()
    model.add_line((-1.0, -1.0, 1.0), (1.0, 1.0, 0.5), "green")
    model.add_line((0.0, 0.0, 0.0), (0.3, 0.4, 0.5), "green")
    model.add_line((-2.3, 0.0, 0.0), (4.5, 0.0, 0.0), "green")
    model.add_line((-2.3, -0.1, 0.4), (4.5, 0.2, -0.3), "green")
    model.add_line((-2.0, -2.0, -2.0), (2.0, 2.0, 2.0), "green")
    model.add_line((2.0, 2.0, -2.0), (2.0, 2.0, 2.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 5


def test_render_random_lines():
    model = Model()
    n = 256
    for _ in range(n):
        p = _get_random_vec3()
        q = _get_random_vec3()
        model.add_line(p, q, "green")
    rendered = render(model)
    assert len(rendered.points) <= n
    for ln in rendered.lines:
        assert _is_in_cipping_space(ln.p)
        assert _is_in_cipping_space(ln.q)


def test_render_line_behind_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), "red")
    model.add_line((-1.0, -1.0, 1.0), (1.0, 1.0, 0.5), "green")
    rendered = render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_line_in_front_of_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_line((-1.0, -1.0, -0.5), (1.0, 1.0, -1.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_next_to_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_line((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_on_triangle():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_line((0.0, 0.0, 0.0), (0.5, 0.5, 0.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_on_triangle_edge():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_line((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 1
    assert len(rendered.triangles) == 1


def test_render_line_through_triangle_cw():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), "red")
    model.add_line((-0.5, -0.5, 1.0), (1.0, 1.0, -1.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_line_through_triangle_ccw():
    model = Model()
    model.add_triangle((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), "red")
    model.add_line((1.0, 1.0, -1.0), (-0.5, -0.5, 1.0), "green")
    rendered = render(model)
    assert len(rendered.lines) == 2
    assert len(rendered.triangles) == 1


def test_render_model():
    model = get_cube_model()
    view_mat4 = mul_mat4(get_translate_mat4(0.0, 0.0, -3.0), get_rotate_y_mat4(0.5))
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model_in_ndc = model.transform(mul_mat4(projection_mat4, view_mat4))
    rendered = render(model_in_ndc)
    assert len(rendered.lines) == 7
    assert len(rendered.triangles) == 12
