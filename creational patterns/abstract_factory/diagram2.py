import os
import tempfile


def main():

    text_filename = os.path.join(tempfile.gettempdir(), "diagram.txt")
    svg_filename = os.path.join(tempfile.gettempdir(), "diagram.svg")

    txt_diagram = create_diagram(DiagramFactory())
    txt_diagram.save(text_filename)
    print("wrote", text_filename)

    svg_diagram = create_diagram(SvgDiagramFactory())
    svg_diagram.save(svg_filename)
    print("wrote", svg_filename)


def create_diagram(factory):
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, "yellow")
    text = factory.make_text(7, 3, "Abstract Factory")
    diagram.add(rectangle)
    diagram.add(text)
    return diagram


class DiagramFactory:
    BLANK = " "
    CORNER = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"

    # @classmethod - это метод, который получает класс как первый аргумент.
    # Это означает, что вы можете использовать класс и его свойства внутри этого метода,
    # а не конкретного экземпляра

    # @classmethod - это обычный метод класса, имеющий доступ ко всем атрибутам класса
    # То есть он привязан к классу, а не к экземпляру класса.

    # Если вы хотите получить доступ к свойству класса,
    # а не к свойству конкретного экземпляра класса, нужно использовать @classmethod

    @classmethod
    def make_diagram(cls, width, height):
        return cls.Diagram(width, height)

    @classmethod
    def make_rectangle(cls, x, y, width, height, fill="white", stroke="black"):
        return cls.Rectangle(x, y, width, height, fill, stroke)

    @classmethod
    def make_text(cls, x, y, text, fontsize=12):
        return cls.Text(x, y, text, fontsize)

    class Diagram:

        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.diagram = DiagramFactory._create_rectangle(self.width, self.height, DiagramFactory.BLANK)

        def add(self, component):
            for y, row in enumerate(component.rows):
                for x, char in enumerate(row):
                    self.diagram[y + component.y][x + component.x] = char

        def save(self, filename):
            file = None if isinstance(filename, str) else filename
            try:
                if file is None:
                    file = open(filename, "w", encoding="utf-8")
                    for row in self.diagram:
                        print("".join(row), file=file)
            finally:
                if isinstance(filename, str) and file is not None:
                    file.close()

    class Text:

        def __init__(self, x, y, text, fontsize):
            self.x = x
            self.y = y
            self.rows = [list(text)]

    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            self.x = x
            self.y = y
            self.rows = DiagramFactory._create_rectangle(width, height,
                                          DiagramFactory.BLANK if fill == "white" else "%")

    def _create_rectangle(width, height, fill):
        rows = [[fill for _ in range(width)] for _ in range(height)]
        for x in range(1, width - 1):
            rows[0][x] = DiagramFactory.HORIZONTAL
            rows[height - 1][x] = DiagramFactory.HORIZONTAL
        for y in range(1, height - 1):
            rows[y][0] = DiagramFactory.VERTICAL
            rows[y][width - 1] = DiagramFactory.VERTICAL
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0),
                     (height - 1, width - 1)):
            rows[y][x] = DiagramFactory.CORNER
        return rows


class SvgDiagramFactory(DiagramFactory):
    SVG_START = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
        "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    <svg xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
        width="{pxwidth}px" height="{pxheight}px">"""

    SVG_END = "</svg>\n"

    SVG_RECTANGLE = """<rect x="{x}" y="{y}" width="{width}" \
    height="{height}" fill="{fill}" stroke="{stroke}"/>"""

    SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" \
    font-family="sans-serif" font-size="{fontsize}">{text}</text>"""

    SVG_SCALE = 20

    class Diagram:

        def __init__(self, width, height):
            pxwidth = width * SvgDiagramFactory.SVG_SCALE
            pxheight = height * SvgDiagramFactory.SVG_SCALE
            self.diagram = [SvgDiagramFactory.SVG_START.format(**locals())]
            outline = SvgDiagramFactory.Rectangle(0, 0, width, height, "lightgreen", "black")
            self.diagram.append(outline.svg)

        def add(self, component):
            self.diagram.append(component.svg)

        def save(self, filenameOrFile):
            file = None if isinstance(filenameOrFile, str) else filenameOrFile
            try:
                if file is None:
                    file = open(filenameOrFile, "w", encoding="utf-8")
                file.write("\n".join(self.diagram))
                file.write("\n" + SvgDiagramFactory.SVG_END)
            finally:
                if isinstance(filenameOrFile, str) and file is not None:
                    file.close()

    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            width *= SvgDiagramFactory.SVG_SCALE
            height *= SvgDiagramFactory.SVG_SCALE
            self.svg = SvgDiagramFactory.SVG_RECTANGLE.format(**locals())

    class Text:
        def __init__(self, x, y, text, fontsize):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            fontsize *= SvgDiagramFactory.SVG_SCALE // 10
            self.svg = SvgDiagramFactory.SVG_TEXT.format_map(locals())


if __name__ == "__main__":
    main()