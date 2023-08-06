from math import pi
from typing import Any

from vecgl.linalg import (
    get_frustum_mat4,
    get_rotate_x_mat4,
    get_rotate_y_mat4,
    get_translate_mat4,
    mul_mat4,
)
from vecgl.model import Model, get_cube_model, get_sphere_model
from vecgl.rendering import render


def test_benchmark_sphere_renderig(benchmark: Any):
    model = get_sphere_model()
    view_mat4 = mul_mat4(
        get_translate_mat4(0.0, 0.0, -3.0),
        get_rotate_x_mat4(-0.2 * pi),
        get_rotate_y_mat4(0.15 * pi),
    )
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model_in_ndc = model.transform(mul_mat4(projection_mat4, view_mat4))
    rendered: Model = benchmark(render, model_in_ndc)
    assert len(rendered.lines) == 107
    assert len(rendered.triangles) == 256


def test_benchmark_cube_renderig(benchmark: Any):
    model = get_cube_model()
    view_mat4 = mul_mat4(
        get_translate_mat4(0.0, 0.0, -3.0),
        get_rotate_x_mat4(-0.2 * pi),
        get_rotate_y_mat4(0.15 * pi),
    )
    projection_mat4 = get_frustum_mat4(-1.0, 1.0, -1.0, 1.0, 1.0, 100.0)
    model_in_ndc = model.transform(mul_mat4(projection_mat4, view_mat4))
    rendered: Model = benchmark(render, model_in_ndc)
    assert len(rendered.lines) == 9
    assert len(rendered.triangles) == 12
