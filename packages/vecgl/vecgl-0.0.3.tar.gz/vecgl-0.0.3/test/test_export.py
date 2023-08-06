from vecgl.export import to_json, to_svg
from vecgl.model import Model


def test_to_svg():
    model = Model()
    model.add_point((0.5, 1.0, 0.0), "red")
    model.add_line((-1.0, 0.0, 0.0), (1.0, 1.0, 0.0), "green")
    model.add_triangle((-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), "blue")
    model.add_point((-0.5, -0.5, 0.5), "hidden")
    expected = [
        "<svg version='1.1' width='300' height='400' xmlns='http://www.w3.org/2000/svg'>\n",
        "  <polygon points='0.0,400.0 300.0,400.0 0.0,0.0' fill='blue'/>\n",
        "  <line x1='0.0' y1='200.0' x2='300.0' y2='0.0' stroke='green' stroke-linecap='round' stroke-width='1'/>\n",
        "  <circle cx='225.0' cy='0.0' r='0.5' fill='green'/>\n",
        "</svg>\n",
    ]
    actual = list(to_svg(model, 300, 400))
    assert actual == expected


def test_to_json():
    model = Model()
    model.add_point((0.5, 1.0, 0.0), "red")
    model.add_line((-1.0, 0.0, 0.0), (1.0, 1.0, 0.0), "green")
    model.add_triangle((-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), "blue")
    model.add_point((-0.5, -0.5, 0.5), "hidden")
    expected = [
        "{\n",
        '  "points": [\n',
        "    {\n",
        '      "p": [ 0.5, 1.0, 0.0, 1.0 ],\n',
        '      "color": "red"\n',
        "    },\n",
        "    {\n",
        '      "p": [ -0.5, -0.5, 0.5, 1.0 ],\n',
        '      "color": "hidden"\n',
        "    }\n",
        "  ],\n",
        '  "lines": [\n',
        "    {\n",
        '      "p": [ -1.0, 0.0, 0.0, 1.0 ],\n',
        '      "q": [ 1.0, 1.0, 0.0, 1.0 ],\n',
        '      "color": "green"\n',
        "    }\n",
        "  ],\n",
        '  "triangles": [\n',
        "    {\n",
        '      "p": [ -1.0, -1.0, 0.0, 1.0 ],\n',
        '      "q": [ 1.0, -1.0, 0.0, 1.0 ],\n',
        '      "r": [ -1.0, 1.0, 0.0, 1.0 ],\n',
        '      "color": "blue"\n',
        "    }\n",
        "  ]\n",
        "}\n",
    ]
    actual = list(to_json(model))
    print(actual)
    assert actual == expected
