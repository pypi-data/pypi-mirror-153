from functools import reduce
from math import cos, sin
from typing import List, Tuple, Union

Vec3 = Tuple[float, float, float]
Vec4 = Tuple[float, float, float, float]
Mat3 = Tuple[Vec3, Vec3, Vec3]
Mat4 = Tuple[Vec4, Vec4, Vec4, Vec4]


def to_vec3(u: Union[Vec3, Vec4]) -> Vec3:
    if len(u) == 3:
        return u
    ux, uy, uz, uw = u
    return ux / uw, uy / uw, uz / uw


def x_vec3(u: Vec3) -> float:
    ux, _, _ = u
    return ux


def y_vec3(u: Vec3) -> float:
    _, uy, _ = u
    return uy


def z_vec3(u: Vec3) -> float:
    _, _, uz = u
    return uz


def str_vec3(u: Vec3) -> str:
    ux, uy, uz = u
    return f"({ux:.2f}, {uy:.2f}, {uz:.2f})"


def scale_vec3(a: float, u: Vec3) -> Vec3:
    ux, uy, uz = u
    return a * ux, a * uy, a * uz


def add_vec3(u: Vec3, v: Vec3) -> Vec3:
    ux, uy, uz = u
    vx, vy, vz = v
    return ux + vx, uy + vy, uz + vz


def sub_vec3(u: Vec3, v: Vec3) -> Vec3:
    ux, uy, uz = u
    vx, vy, vz = v
    return ux - vx, uy - vy, uz - vz


def dot_vec3(u: Vec3, v: Vec3) -> float:
    ux, uy, uz = u
    vx, vy, vz = v
    return ux * vx + uy * vy + uz * vz


def cross_vec3(u: Vec3, v: Vec3) -> Vec3:
    ux, uy, uz = u
    vx, vy, vz = v
    return uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx


def min_vec3(u: Vec3, v: Vec3) -> Vec3:
    ux, uy, uz = u
    vx, vy, vz = v
    return min(ux, vx), min(uy, vy), min(uz, vz)


def max_vec3(u: Vec3, v: Vec3) -> Vec3:
    ux, uy, uz = u
    vx, vy, vz = v
    return max(ux, vx), max(uy, vy), max(uz, vz)


def to_vec4(u: Union[Vec3, Vec4]) -> Vec4:
    if len(u) == 4:
        return u
    ux, uy, uz = u
    return ux, uy, uz, 1.0


def x_vec4(u: Vec4) -> float:
    ux, _, _, _ = u
    return ux


def y_vec4(u: Vec4) -> float:
    _, uy, _, _ = u
    return uy


def z_vec4(u: Vec4) -> float:
    _, _, uz, _ = u
    return uz


def w_vec4(u: Vec4) -> float:
    _, _, _, uw = u
    return uw


def str_vec4(u: Vec4) -> str:
    ux, uy, uz, uw = u
    return f"({ux:.2f}, {uy:.2f}, {uz:.2f}, {uw:.2f})"


def dot_vec4(u: Vec4, v: Vec4) -> float:
    ux, uy, uz, uw = u
    vx, vy, vz, vw = v
    return ux * vx + uy * vy + uz * vz + uw * vw


def mul_mat4_vec4(U: Mat4, v: Vec4) -> Vec4:
    return tuple([dot_vec4(u, v) for u in U])


def mul_mat4(*Us: Mat4) -> Mat4:
    def mul_mat4_mat4(U: Mat4, V: Mat4) -> Mat4:
        l = len(U)
        m = len(V)
        n = len(V[0])
        W: List[Tuple[float, float, float, float]] = []
        for i in range(l):
            Wi: List[float] = []
            for j in range(n):
                Wij = sum([U[i][k] * V[k][j] for k in range(m)])
                Wi.append(Wij)
            W.append(tuple(Wi))
        return tuple(W)

    return reduce(mul_mat4_mat4, Us)


def get_unit_mat4() -> Mat4:
    return (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_scale_mat4(ax: float, ay: float, az: float) -> Mat4:
    return (
        (ax, 0.0, 0.0, 0.0),
        (0.0, ay, 0.0, 0.0),
        (0.0, 0.0, az, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_translate_mat4(dx: float, dy: float, dz: float) -> Mat4:
    return (
        (1.0, 0.0, 0.0, dx),
        (0.0, 1.0, 0.0, dy),
        (0.0, 0.0, 1.0, dz),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_rotate_x_mat4(da: float) -> Mat4:
    return (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, cos(da), sin(da), 0.0),
        (0.0, -sin(da), cos(da), 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_rotate_y_mat4(da: float) -> Mat4:
    return (
        (cos(da), 0.0, -sin(da), 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (sin(da), 0.0, cos(da), 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_rotate_z_mat4(da: float) -> Mat4:
    return (
        (cos(da), -sin(da), 0.0, 0.0),
        (sin(da), cos(da), 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_ortho_mat4(l: float, r: float, b: float, t: float, n: float, f: float) -> Mat4:
    return (
        (2.0 / (r - l), 0.0, 0.0, -(r + l) / (r - l)),
        (0.0, 2.0 / (t - b), 0.0, -(t + b) / (t - b)),
        (0.0, 0.0, -2.0 / (f - n), -(f + n) / (f - n)),
        (0.0, 0.0, 0.0, 1.0),
    )


def get_frustum_mat4(
    l: float, r: float, b: float, t: float, n: float, f: float
) -> Mat4:
    return (
        (2.0 * n / (r - l), 0.0, (r + l) / (r - l), 0.0),
        (0.0, 2.0 * n / (t - b), (t + b) / (t - b), 0.0),
        (0.0, 0.0, -(f + n) / (f - n), -2.0 * f * n / (f - n)),
        (0.0, 0.0, -1.0, 0.0),
    )


def get_viewport_mat4(x: float, y: float, w: float, h: float) -> Mat4:
    return (
        (w / 2.0, 0.0, 0.0, x + w / 2.0),
        (0.0, h / 2.0, 0.0, y + h / 2.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )
