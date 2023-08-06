from tkinter import ROUND, Canvas, Tk
from typing import Iterable

from vecgl.linalg import Vec4, get_viewport_mat4, to_vec3
from vecgl.model import Model
from vecgl.rendering import render

kDefaultWidth = 600
kDefaultHeight = 600
kDefaultStrokeWidth = 1


def show(
    model: Model,
    width: int = kDefaultWidth,
    height: int = kDefaultHeight,
    stroke_width: int = kDefaultStrokeWidth,
) -> None:

    # Render if needed.
    model = model if model.rendered else render(model)

    # Transform the model to window space.
    model = model.transform(get_viewport_mat4(0.0, height, width, -height))

    # Create a canvas.
    frame = Tk()
    canvas = Canvas(frame, bg="white", height=height, width=width)

    # Draw the triangles first so that later drawn lines and points are visible.
    for tr in model.triangles:
        px, py, _ = to_vec3(tr.p)
        qx, qy, _ = to_vec3(tr.q)
        rx, ry, _ = to_vec3(tr.r)
        canvas.create_polygon([px, py, qx, qy, rx, ry], fill=tr.color)

    # Draw the lines fragments, which are fully visible.
    for ln in model.lines:
        px, py, _ = to_vec3(ln.p)
        qx, qy, _ = to_vec3(ln.q)
        canvas.create_line(
            px,
            py,
            qx,
            qy,
            width=stroke_width,
            fill=ln.color,
            capstyle=ROUND,
            joinstyle=ROUND,
        )

    # Draw the points, which are fully visible.
    for pt in model.points:
        px, py, _ = to_vec3(pt.p)
        canvas.create_line(
            px,
            py,
            px,
            py,
            width=stroke_width,
            fill=pt.color,
            capstyle=ROUND,
            joinstyle=ROUND,
        )

    # Display the hard work.
    canvas.pack()
    frame.mainloop()


def to_svg(
    model: Model,
    width: int = kDefaultWidth,
    height: int = kDefaultHeight,
    stroke_width: int = kDefaultStrokeWidth,
) -> Iterable[str]:

    # Render if needed.
    model = model if model.rendered else render(model)

    # Transform to canvas space.
    model = model.transform(get_viewport_mat4(0.0, height, width, -height))

    yield f"<svg version='1.1' width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg'>\n"

    # Add the triangles.
    for tr in model.triangles:
        px, py, _ = to_vec3(tr.p)
        qx, qy, _ = to_vec3(tr.q)
        rx, ry, _ = to_vec3(tr.r)
        yield f"  <polygon points='{px},{py} {qx},{qy} {rx},{ry}' fill='{tr.color}'/>\n"

    # Add the lines.
    for ln in model.lines:
        px, py, _ = to_vec3(ln.p)
        qx, qy, _ = to_vec3(ln.q)
        yield f"  <line x1='{px}' y1='{py}' x2='{qx}' y2='{qy}' stroke='{ln.color}' stroke-linecap='round' stroke-width='{stroke_width}'/>\n"

    # Add the points.
    for pt in model.points:
        px, py, _ = to_vec3(pt.p)
        yield f"  <circle cx='{px}' cy='{py}' r='{stroke_width/2}' fill='green'/>\n"

    yield f"</svg>\n"


def write_svg(
    model: Model,
    path: str,
    width: int = kDefaultWidth,
    height: int = kDefaultHeight,
    stroke_width: int = kDefaultStrokeWidth,
) -> None:
    with open(path, "w") as fout:
        fout.writelines(to_svg(model, width, height, stroke_width))


def to_json(model: Model) -> Iterable[str]:
    def p_to_json(p: Vec4):
        return "[ " + ", ".join(str(a) for a in p) + " ]"

    yield "{\n"

    # Add the points.
    yield '  "points": [\n'
    for pt in model.points:
        is_last = pt == model.points[-1]
        yield f"    {{\n"
        yield f'      "p": {p_to_json(pt.p)},\n'
        yield f'      "color": "{pt.color}"\n'
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ],\n"

    # Add the lines.
    yield '  "lines": [\n'
    for ln in model.lines:
        is_last = ln == model.lines[-1]
        yield f"    {{\n"
        yield f'      "p": {p_to_json(ln.p)},\n'
        yield f'      "q": {p_to_json(ln.q)},\n'
        yield f'      "color": "{ln.color}"\n'
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ],\n"

    # Add the triangles.
    yield '  "triangles": [\n'
    for tr in model.triangles:
        is_last = tr == model.triangles[-1]
        yield f"    {{\n"
        yield f'      "p": {p_to_json(tr.p)},\n'
        yield f'      "q": {p_to_json(tr.q)},\n'
        yield f'      "r": {p_to_json(tr.r)},\n'
        yield f'      "color": "{tr.color}"\n'
        yield f"    }}{'' if is_last else ','}\n"
    yield "  ]\n"

    yield "}\n"


def write_json(model: Model, path: str) -> None:
    with open(path, "w") as fout:
        fout.writelines(to_json(model))
