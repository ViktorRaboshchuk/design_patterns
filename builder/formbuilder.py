"""
Паттерн построитель аналогичен паттерну Абстрактная фабрика в том смысле, что оба
предназначены дял создания сложных объектов составленных из других объектов.

Отличается он тем, что не только представляет методы для построения сложных объектов, но и
хранит внутри себя его полное представление


Этот паттерн допускает такую же композиционную структуру, как Абстрактная фабрика
(то есть сложные объекты, составленные из нескольких более простых),
но особенно удобен в ситуациях, когда представление составного объекта
должно быть отделено от алгоритмов композиции
"""
import abc
import os
import re
import tempfile
from html import escape


def main():
    html_filename = os.path.join(tempfile.gettempdir(), "login.html")
    html_form = create_login_form(HtmlFormBuilder())
    with open(html_filename, "w", encoding="utf-8") as file:
        file.write(html_form)

    tk_filename = os.path.join(tempfile.gettempdir(), "login.py")
    tk_form = create_login_form(TkFormBuilder())
    with open(tk_filename, "w", encoding="utf-8") as file:
        file.write(tk_form)


def create_login_form(builder):
    builder.add_title("Login")
    builder.add_label("Username", 0, 0, target="username")
    builder.add_entry("username", 0, 1)
    builder.add_label("Password", 1, 0, target="password")
    builder.add_entry("password", 1, 1, kind="password")
    builder.add_button("Login", 2, 0)
    builder.add_button("Cancel", 2, 1)
    return builder.form()


class AbstractFormBuilder(metaclass=abc.ABCMeta):
    # из-за наследования от abc.ABCMeta данный класс нельзя инстанцировать
    # то есть можно использовать только в качестве абстрактного базового класса
    @abc.abstractmethod
    def add_title(self, title):
        self.title = title

    @abc.abstractmethod
    def form(self):
        pass

    @abc.abstractmethod
    def add_label(self, text, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_entry(self, variable, row, column, **kwargs):
        pass

    @abc.abstractmethod
    def add_button(self, text, row, column, **kwargs):
        pass


# first, second, *rest = sequence
# first == sequence[0]
# second == sequence[1]
# rest == sequence[2:]

# args = (600,900)
# kwargs = dict(copies=2, collate=False)
# print_setup(*args, **kwargs)

class HtmlFormBuilder(AbstractFormBuilder):
    def __init__(self):
        self.title = "HtmlFormBuilder"
        self.items = {}

    def add_title(self, title):
        super().add_title(escape(title))

    def add_label(self, text, row, column, **kwargs):
        self.items[(row, column)] = '<td><label for="{}">{}:'\
                                '</label></td>'.format(kwargs["target"], escape(text))

    def add_entry(self, variable, row, column, **kwargs):
        print('add_entry', kwargs)
        print(kwargs.get("kind", "text"))
        html = """<td><input name="{}" type="{}" /></td>""".format(
                variable, kwargs.get("kind", "text"))
        self.items[(row, column)] = html

    def add_button(self, text, row, column, **kwargs):
        html = """<td><input type="submit" value="{}" /></td>""".format(
                escape(text))
        self.items[(row, column)] = html

    def form(self):
        html = ["<!doctype html>\n<html><head><title>{}</title></head>"
                "<body>".format(self.title), '<form><table border="0">']
        thisRow = None
        for key, value in sorted(self.items.items()):
            row, column = key
            if thisRow is None:
                html.append("  <tr>")
            elif thisRow != row:
                html.append("  </tr>\n  <tr>")
            thisRow = row
            html.append("    " + value)
        html.append("  </tr>\n</table></form></body></html>")
        return "\n".join(html)


class TkFormBuilder(AbstractFormBuilder):

    TEMPLATE = """#!/usr/bin/env python3
    import tkinter as tk
    import tkinter.ttk as ttk
    class {name}Form(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.withdraw()     # hide until ready to show
            self.title("{title}")
            {statements}
            self.bind("<Escape>", lambda *args: self.destroy())
            self.deiconify()    # show when widgets are created and laid out
            if self.winfo_viewable():
                self.transient(master)
            self.wait_visibility()
            self.grab_set()
            self.wait_window(self)
    if __name__ == "__main__":
        application = tk.Tk()
        window = {name}Form(application)
        application.protocol("WM_DELETE_WINDOW", application.quit)
        application.mainloop()
    """

    def __init__(self):
        self.title = "TkFormBuilder"
        self.statements = []

    def form(self):
        return TkFormBuilder.TEMPLATE.format(title=self.title,
                name=self._canonicalize(self.title, False),
                statements="\n        ".join(self.statements))

    def add_label(self, text, row, column, **kwargs):
        name = self._canonicalize(text)
        create = """self.{}Label = ttk.Label(self, text="{}:")""".format(name, text)
        layout = """self.{}Label.grid(row={}, column={}, sticky=tk.W, \
            padx="0.75m", pady="0.75m")""".format(name, row, column)
        self.statements.extend((create, layout))

    def add_entry(self, variable, row, column, **kwargs):
        name = self._canonicalize(variable)
        extra = "" if kwargs.get("kind") != "password" else ', show="*"'
        create = "self.{}Entry = ttk.Entry(self{})".format(name, extra)
        layout = """self.{}Entry.grid(row={}, column={}, sticky=(\
                tk.W, tk.E), padx="0.75m", pady="0.75m")""".format(name, row, column)
        self.statements.extend((create, layout))

    def add_button(self, text, row, column, **kwargs):
        name = self._canonicalize(text)
        create = ("""self.{}Button = ttk.Button(self, text="{}")""".format(name, text))
        layout = """self.{}Button.grid(row={}, column={}, padx="0.75m", \
                pady="0.75m")""".format(name, row, column)
        self.statements.extend((create, layout))

    def add_title(self, title):
        super().add_title(title)

    def _canonicalize(self, text, startLower=True):
        text = re.sub(r"\W+", "", text)
        if text[0].isdigit():
            return "_" + text
        return text if not startLower else text[0].lower() + text[1:]


if __name__ == "__main__":
    main()
