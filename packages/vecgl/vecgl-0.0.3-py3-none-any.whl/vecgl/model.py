from math import cos, pi, sin, sqrt
from typing import List, Union

from vecgl.linalg import Mat4, Vec3, Vec4, mul_mat4_vec4, str_vec4, to_vec4


kDefaultSurfaceColor = "gray"
kDefaultLineColor = "black"


class Point:
    def __init__(self, p: Union[Vec3, Vec4], color: str):
        self.p = to_vec4(p)
        self.color = color

    def transform(self, U: Mat4):
        transformed_p = mul_mat4_vec4(U, self.p)
        return Point(transformed_p, self.color)

    def __str__(self):
        return str_vec4(self.p)


class Line:
    def __init__(self, p: Union[Vec3, Vec4], q: Union[Vec3, Vec4], color: str):
        self.p = to_vec4(p)
        self.q = to_vec4(q)
        self.color = color

    def transform(self, U: Mat4):
        transformed_p = mul_mat4_vec4(U, self.p)
        transformed_q = mul_mat4_vec4(U, self.q)
        return Line(transformed_p, transformed_q, self.color)

    def __str__(self):
        return f"{str_vec4(self.p)} to {str_vec4(self.q)}"


class Triangle:
    def __init__(
        self,
        p: Union[Vec3, Vec4],
        q: Union[Vec3, Vec4],
        r: Union[Vec3, Vec4],
        color: str,
    ):
        self.p = to_vec4(p)
        self.q = to_vec4(q)
        self.r = to_vec4(r)
        self.color = color

    def transform(self, U: Mat4):
        transformed_p = mul_mat4_vec4(U, self.p)
        transformed_q = mul_mat4_vec4(U, self.q)
        transformed_r = mul_mat4_vec4(U, self.r)
        return Triangle(transformed_p, transformed_q, transformed_r, self.color)

    def __str__(self):
        return f"{str_vec4(self.p)}, {str_vec4(self.q)}, {str_vec4(self.r)}"


class Model:
    def __init__(self):
        self.points: List[Point] = []
        self.lines: List[Line] = []
        self.triangles: List[Triangle] = []
        self.rendered = False

    def add_point(self, p: Union[Vec3, Vec4], color: str = kDefaultLineColor):
        self.points.append(Point(p, color))

    def add_line(
        self, p: Union[Vec3, Vec4], q: Union[Vec3, Vec4], color: str = kDefaultLineColor
    ):
        self.lines.append(Line(p, q, color))

    def add_triangle(
        self,
        p: Union[Vec3, Vec4],
        q: Union[Vec3, Vec4],
        r: Union[Vec3, Vec4],
        color: str = kDefaultSurfaceColor,
    ):
        self.triangles.append(Triangle(p, q, r, color))

    def add_model(self, model: "Model"):
        self.points += model.points
        self.lines += model.lines
        self.triangles += model.triangles

    def transform(self, U: Mat4):
        transformed = Model()
        transformed.points = [pt.transform(U) for pt in self.points]
        transformed.lines = [ln.transform(U) for ln in self.lines]
        transformed.triangles = [tr.transform(U) for tr in self.triangles]
        return transformed


def get_cube_model(
    surface_color: str = kDefaultSurfaceColor,
    line_color: str = kDefaultLineColor,
    surfaces: bool = True,
    lines: bool = True,
) -> Model:
    cube = Model()

    # Create the 8 points.
    ps: List[Vec3] = []
    for i in range(8):
        px = 1.0 if i & 0x01 else -1.0
        py = 1.0 if i & 0x02 else -1.0
        pz = 1.0 if i & 0x04 else -1.0
        p = px, py, pz
        ps.append(p)

    # Add the 12 lines if needed.
    if lines:
        for i in range(8):
            for shift in range(3):
                mask = 0x01 << shift
                if not i & mask:
                    j = i | mask
                    cube.add_line(ps[i], ps[j], line_color)

    # Add the 12 triangles if needed.
    if surfaces:
        cube.add_triangle(ps[0], ps[1], ps[2], surface_color)
        cube.add_triangle(ps[0], ps[1], ps[4], surface_color)
        cube.add_triangle(ps[0], ps[2], ps[4], surface_color)
        cube.add_triangle(ps[1], ps[2], ps[3], surface_color)
        cube.add_triangle(ps[1], ps[3], ps[5], surface_color)
        cube.add_triangle(ps[1], ps[4], ps[5], surface_color)
        cube.add_triangle(ps[2], ps[3], ps[6], surface_color)
        cube.add_triangle(ps[2], ps[4], ps[6], surface_color)
        cube.add_triangle(ps[3], ps[5], ps[7], surface_color)
        cube.add_triangle(ps[3], ps[6], ps[7], surface_color)
        cube.add_triangle(ps[4], ps[5], ps[6], surface_color)
        cube.add_triangle(ps[5], ps[6], ps[7], surface_color)

    return cube


def get_sphere_model(
    n: int = 8,
    m: int = 16,
    surface_color: str = kDefaultSurfaceColor,
    line_color: str = kDefaultLineColor,
    surfaces: bool = True,
    latitude_lines: bool = True,
    longitude_lines: bool = True,
) -> Model:
    sphere = Model()

    # Create the n*m points and a unique north and south pole.
    p_north = 0.0, 1.0, 0.0
    p_south = 0.0, -1.0, 0.0
    ps: List[List[Vec3]] = []
    for i in range(n):
        angle_latitude = (i + 1) / (n + 1) * pi
        py = cos(angle_latitude)
        radius_xz = sqrt(1.0 - py**2)
        ps_latitude: List[Vec3] = []
        for j in range(m):
            angle_longitude = j / m * 2.0 * pi
            px = radius_xz * sin(angle_longitude)
            pz = radius_xz * cos(angle_longitude)
            p = px, py, pz
            ps_latitude.append(p)
        ps.append(ps_latitude)

    # Add lines and triangles defined by the grid.
    for i in range(n - 1):
        i_next = i + 1
        for j in range(m):
            j_next = (j + 1) % m
            p = ps[i][j]
            q = ps[i][j_next]
            r = ps[i_next][j]
            s = ps[i_next][j_next]
            if surfaces:
                sphere.add_triangle(p, q, r, surface_color)
                sphere.add_triangle(q, r, s, surface_color)
            if latitude_lines:
                sphere.add_line(p, q, line_color)
            if longitude_lines:
                sphere.add_line(p, r, line_color)

    # Add lines and triangles to connect the north and south poles.
    for j in range(m):
        j_next = (j + 1) % m
        p = ps[0][j]
        q = ps[0][j_next]
        r = ps[-1][j]
        s = ps[-1][j_next]
        if surfaces:
            sphere.add_triangle(p_north, p, q, surface_color)
            sphere.add_triangle(p_south, r, s, surface_color)
        if latitude_lines:
            sphere.add_line(r, s, line_color)
        if longitude_lines:
            sphere.add_line(p_north, p, line_color)
            sphere.add_line(p_south, r, line_color)

    return sphere
