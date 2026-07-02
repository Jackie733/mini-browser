import os
import tkinter
import unicodedata

import webtools
from lab1 import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


def is_rtl_char(c):
    try:
        return unicodedata.bidirectional(c) in ("R", "AL")
    except Exception:
        return False


def place_line(line_items, y, width, rtl_flag, display_list):
    if not line_items:
        return
    # 1.判定改行是否包含RTL字符
    line_is_rtl = any(is_rtl_char(c) for c, _, _ in line_items)
    # 2. 计算对齐方式
    # 默认模式下：RTL 文本靠右对齐；--rtl 模式下: LTR 文本靠右对齐
    align_right = (line_is_rtl and not rtl_flag) or (not line_is_rtl and rtl_flag)

    line_width = sum(w for _, _, w in line_items)

    if align_right:
        start_x = width - HSTEP - line_width
    else:
        start_x = HSTEP

    # 3. 摆放字符
    current_x = start_x
    if line_is_rtl:
        # 如果是 RTL 文本，字符从右向左依次排列
        current_x = start_x + line_width
        for c, img, w in line_items:
            current_x -= w
            if img:
                display_list.append(("image", current_x, y, img))
            else:
                display_list.append(("text", current_x, y, c))
    else:
        for c, img, w in line_items:
            if img:
                display_list.append(("image", current_x, y, img))
            else:
                display_list.append(("text", current_x, y, c))
            current_x += w


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


def layout(text, width=WIDTH, get_emoji_fn=None, rtl=False):
    display_list = []
    current_line = []
    line_width = 0
    cursor_y = VSTEP

    def flush_line():
        nonlocal current_line, line_width, cursor_y
        if not current_line:
            return
        place_line(current_line, cursor_y, width, rtl, display_list)
        current_line = []
        line_width = 0
        cursor_y += VSTEP

    for c in text:
        if c == "\n":
            flush_line()
            cursor_y += VSTEP
            continue

        is_emoji = ord(c) > 0xFFFF
        img = get_emoji_fn(c) if (is_emoji and get_emoji_fn) else None
        char_w = 16 if img else HSTEP

        if line_width + char_w > width - 2 * HSTEP:
            flush_line()

        current_line.append((c, img, char_w))
        line_width += char_w

    flush_line()
    webtools.record("layout", display_list)
    return display_list


class Browser:
    def __init__(self, rtl=False):
        self.window = tkinter.Tk()
        self.width = WIDTH
        self.height = HEIGHT
        self.rtl = rtl

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

        self.display_list = layout(
            self.text, self.width, self.get_emoji_image, self.rtl
        )
        self.scroll = 0
        self.clamp_scroll()
        self.draw()

    def resize(self, e):
        if e.width != self.width or e.height != self.height:
            self.width = e.width
            self.height = e.height
            if self.text is not None:
                self.display_list = layout(
                    self.text, self.width, self.get_emoji_image, self.rtl
                )
                self.clamp_scroll()
                self.draw()


if __name__ == "__main__":
    import sys

    rtl_mode = False
    if "--rtl" in sys.argv:
        rtl_mode = True
        sys.argv.remove("--rtl")

    url = sys.argv[1] if len(sys.argv) > 1 else "about:blank"

    Browser(rtl=rtl_mode).load(url)
    tkinter.mainloop()
