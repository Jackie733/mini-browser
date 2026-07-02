import tkinter

import webtools
from lab1 import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c
        webtools.record("lex", text)
    return text


def layout(text, width=WIDTH):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_x = HSTEP
            cursor_y += VSTEP
            continue

        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if cursor_x >= width - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
        webtools.record("layout", display_list)
    return display_list


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.width = WIDTH
        self.height = HEIGHT
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        self.scroll = 0
        self.text = None

        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Down>", self.scrolldown)

        self.window.bind("<MouseWheel>", self.mousewheel)
        self.window.bind("<Button-4>", self.mousewheel)
        self.window.bind("<Button-5>", self.mousewheel)

        self.window.bind("<Configure>", self.resize)

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.height:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

        if self.display_list:
            max_y = self.display_list[-1][1]
            doc_height = max_y + VSTEP
            if doc_height > self.height:
                SCROLLBAR_WIDTH = 12
                scrollbar_top = (self.scroll / doc_height) * self.height
                scrollbar_bottom = (
                    (self.scroll + self.height) / doc_height
                ) * self.height
                self.canvas.create_rectangle(
                    self.width - SCROLLBAR_WIDTH,
                    scrollbar_top,
                    self.width,
                    scrollbar_bottom,
                    fill="blue",
                    outline="",
                )

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.clamp_scroll()
        self.draw()

    def scrollup(self, e):
        self.scroll = max(0, self.scroll - SCROLL_STEP)
        self.clamp_scroll()
        self.draw()

    def mousewheel(self, e):
        if e.num == 4 or e.delta > 0:
            self.scroll = max(0, self.scroll - SCROLL_STEP)
        elif e.num == 5 or e.delta < 0:
            self.scroll += SCROLL_STEP
        self.clamp_scroll()
        self.draw()

    def load(self, url):
        body = url.request()
        self.text = lex(body)
        self.display_list = layout(self.text, self.width)
        self.scroll = 0
        self.clamp_scroll()
        self.draw()

    def clamp_scroll(self):
        max_y = self.display_list[-1][1] if self.display_list else 0
        doc_height = max_y + VSTEP
        max_scroll = max(0, doc_height - self.height)
        self.scroll = max(0, min(self.scroll, max_scroll))

    def resize(self, e):
        if e.width != self.width or e.height != self.height:
            self.width = e.width
            self.height = e.height
            if self.text is not None:
                self.display_list = layout(self.text, self.width)
                self.clamp_scroll()
                self.draw()


if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
