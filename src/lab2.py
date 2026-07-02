import os
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


def layout(text, width=WIDTH, get_emoji_fn=None):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        # Exercise 2-1: Newline paragraph breaks
        if c == "\n":
            cursor_x = HSTEP
            cursor_y += VSTEP * 2
            continue

        # Exercise 2-5: Emoji layout
        if ord(c) > 0xFFFF and get_emoji_fn:
            img = get_emoji_fn(c)
            if img:
                display_list.append(("image", cursor_x, cursor_y, img))
                cursor_x += 16
                if cursor_x >= width - HSTEP:
                    cursor_y += VSTEP
                    cursor_x = HSTEP
                webtools.record("layout", display_list)
                continue

        display_list.append(("text", cursor_x, cursor_y, c))
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
        # Exercise 2-3: Resizable Canvas packing
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)

        self.scroll = 0
        self.text = None
        self.emoji_cache = {}

        # Exercise 2-2: Mouse Wheel and Keyboard Scroll
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<MouseWheel>", self.mousewheel)
        self.window.bind("<Button-4>", self.mousewheel)
        self.window.bind("<Button-5>", self.mousewheel)

        # Exercise 2-3: Configure callback for resizing
        self.window.bind("<Configure>", self.resize)

    def get_emoji_image(self, char):
        code_point = f"{ord(char):X}"
        img_path = f"emojis/{code_point}.png"

        # Check cache first
        if img_path in self.emoji_cache:
            return self.emoji_cache[img_path]

        # Load from disk if exists
        if os.path.exists(img_path):
            try:
                img = tkinter.PhotoImage(file=img_path)
                self.emoji_cache[img_path] = img
                return img
            except Exception:
                return None
        return None

    def clamp_scroll(self):
        # Exercise 2-4: Scroll limits
        max_y = 0
        if self.display_list:
            max_y = self.display_list[-1][2]
        doc_height = max_y + VSTEP
        max_scroll = max(0, doc_height - self.height)
        self.scroll = max(0, min(self.scroll, max_scroll))

    def draw(self):
        self.canvas.delete("all")
        # Exercise 2-5: Draw text and images
        for item_type, x, y, val in self.display_list:
            if y > self.scroll + self.height:
                continue
            if y + VSTEP < self.scroll:
                continue

            if item_type == "text":
                self.canvas.create_text(x, y - self.scroll, text=val)
            elif item_type == "image":
                self.canvas.create_image(x, y - self.scroll, image=val)

        # Exercise 2-4: Blue scrollbar
        if self.display_list:
            max_y = self.display_list[-1][2]
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
        self.scroll -= SCROLL_STEP
        self.clamp_scroll()
        self.draw()

    def mousewheel(self, e):
        if e.num == 4 or e.delta > 0:
            self.scroll -= SCROLL_STEP
        elif e.num == 5 or e.delta < 0:
            self.scroll += SCROLL_STEP
        self.clamp_scroll()
        self.draw()

    def load(self, url_str):
        if url_str == "about:blank":
            self.text = ""
            self.display_list = []
            self.scroll = 0
            self.draw()
            return

        try:
            url = URL(url_str)
            body = url.request()
            self.text = lex(body)
        except Exception as e:
            print(f"Error loading {url_str}: {e}")
            self.text = ""

        self.display_list = layout(self.text, self.width, self.get_emoji_image)
        self.scroll = 0
        self.clamp_scroll()
        self.draw()

    def resize(self, e):
        if e.width != self.width or e.height != self.height:
            self.width = e.width
            self.height = e.height
            if self.text is not None:
                self.display_list = layout(self.text, self.width, self.get_emoji_image)
                self.clamp_scroll()
                self.draw()


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "about:blank"

    Browser().load(url)
    tkinter.mainloop()
