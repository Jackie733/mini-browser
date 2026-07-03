import tkinter
import tkinter.font

import webtools
from lab1 import URL
from lab2 import HEIGHT, HSTEP, VSTEP, WIDTH, Browser

FONTS = {}


class Text:
    def __init__(self, text):
        self.text = text


class Tag:
    def __init__(self, tag):
        self.tag = tag


def get_font(size, weight, style):
    key = (size, weight, style)
    if key not in FONTS:
        font = tkinter.font.Font(size=size, weight=weight, slant=style)
        label = tkinter.Label(font=font)
        FONTS[key] = (font, label)
    return FONTS[key][0]


def lex(body):
    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Tag(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out


class Layout:
    def __init__(self, tokens):
        self.tokens = tokens
        self.display_list = []
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        self.weight = "normal"
        self.style = "roman"
        self.size = 12
        self.is_centered = False
        self.is_superscript = False

        self.line = []
        for tok in tokens:
            self.token(tok)

        self.flush()

    def token(self, tok):
        if isinstance(tok, Text):
            for word in tok.text.split():
                self.word(word)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
        elif tok.tag == "small":
            self.size -= 2
        elif tok.tag == "/small":
            self.size += 2
        elif tok.tag == "big":
            self.size += 4
        elif tok.tag == "/big":
            self.size -= 4
        elif tok.tag in ['h1 class="title"', "h1 class='title'"]:
            self.flush()
            self.is_centered = True
        elif tok.tag == "/h1":
            self.flush()
            self.is_centered = False
        elif tok.tag == "sup":
            self.is_superscript = True
            self.size -= 6
        elif tok.tag == "/sup":
            self.is_superscript = False
            self.size += 6
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP

    def word(self, word):
        font = get_font(self.size, self.weight, self.style)
        SHY = "\u00ad"
        clean_word = word.replace(SHY, "")
        w = font.measure(clean_word)
        
        if self.cursor_x + w > WIDTH - HSTEP:
            if SHY in word:
                split_indices = [i for i, c in enumerate(word) if c == SHY]
                for index in reversed(split_indices):
                    part1_raw = word[:index]
                    part2_raw = word[index + 1 :]
                    part1 = part1_raw.replace(SHY, "") + "-"
                    w_part1 = font.measure(part1)
                    if self.cursor_x + w_part1 <= WIDTH - HSTEP:
                        self.line.append((self.cursor_x, part1, font, self.is_superscript))
                        self.flush()
                        self.word(part2_raw)
                        return
            
            if self.cursor_x > HSTEP:
                self.flush()
                self.word(word)
                return

        self.line.append((self.cursor_x, clean_word, font, self.is_superscript))
        self.cursor_x += w + font.measure(" ")

    def flush(self):
        if not self.line:
            return
        last_x, last_word, last_font, _ = self.line[-1]
        right_edge = last_x + last_font.measure(last_word)
        remaining_space = (WIDTH - HSTEP) - right_edge
        offset = remaining_space / 2
        metrics = [font.metrics() for x, word, font, is_sup in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font, is_sup in self.line:
            if is_sup:
                y = baseline - max_ascent
            else:
                y = baseline - font.metrics("ascent")
            if self.is_centered:
                self.display_list.append((x + offset, y, word, font))
            else:
                self.display_list.append((x, y, word, font))
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = HSTEP
        self.line = []


@webtools.patch(Browser)
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.display_list = []

    def load(self, url):
        body = url.request()
        tokens = lex(body)
        self.display_list = Layout(tokens).display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, word, font in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + font.metrics("linespace") < self.scroll:
                continue
            self.canvas.create_text(
                x, y - self.scroll, text=word, font=font, anchor="nw"
            )


if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
