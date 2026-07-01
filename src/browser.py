import socket
import ssl

SOCKET_CACHE = {}
HTTP_CACHE = {}

def read_chunked_body(response):
    body = b""
    while True:
        line = response.readline()
        if not line:
            break
        chunk_size_str = line.split(b";", 1)[0].strip()
        chunk_size = int(chunk_size_str, 16)
        if chunk_size == 0:
            response.readline()
            break
        chunk_data = response.read(chunk_size)
        body += chunk_data
        response.readline()
    return body

class URL:

    def __init__(self, url):
        self.url = url
        if ":" not in url:
            raise ValueError("URL must have a scheme")
        self.scheme, url = url.split(":", 1)
        if url.startswith("//"):
            url = url[2:]

        assert self.scheme in ["http", "https", "file", "data", "view-source"]

        if self.scheme == "view-source":
            self.inner_url = URL(url)
            self.host = ""
            self.port = None
            return

        if self.scheme == "file":
            self.path = url
            self.host = ""
            self.port = None
            return

        if self.scheme == "data":
            self.media_type, self.data = url.split(",", 1)
            self.host = ""
            self.port = None
            return

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def request(self, headers=None, redirect_limit=10):
        import time
        if self.url in HTTP_CACHE:
            expiry, cached_content = HTTP_CACHE[self.url]
            if time.time() < expiry:
                return cached_content
            else:
                del HTTP_CACHE[self.url]

        if self.scheme == "view-source":
            html = self.inner_url.request(headers, redirect_limit)
            return html.replace("<", "&lt;").replace(">", "&gt;")

        if self.scheme == "file":
            with open(self.path, "r", encoding="utf8") as f:
                return f.read()

        if self.scheme == "data":
            import urllib.parse
            return urllib.parse.unquote(self.data)



        s = None
        use_cached = (self.host, self.port) in SOCKET_CACHE
        if use_cached:
            s = SOCKET_CACHE[(self.host, self.port)]

        request_headers = {
            "Host": self.host,
            "Connection": "keep-alive",
            "User-Agent": "AntigravityBrowser/1.0",
            "Accept-Encoding": "gzip",
        }
        if headers:
            for k, v in headers.items():
                request_headers[k] = v

        request_string = "GET {} HTTP/1.1\r\n".format(self.path)
        for header, value in request_headers.items():
            request_string += "{}: {}\r\n".format(header, value)
        request_string += "\r\n"

        try:
            if s is None:
                raise OSError("No cached socket")
            s.send(request_string.encode("utf8"))
        except OSError:
            s = socket.socket(
                family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
            )
            s.connect((self.host, self.port))
            if self.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=self.host)
            SOCKET_CACHE[(self.host, self.port)] = s
            s.send(request_string.encode("utf8"))

        response = s.makefile("rb")
        statusline = response.readline().decode("utf8")
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline().decode("utf8")
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        if response_headers.get("transfer-encoding") == "chunked":
            content_bytes = read_chunked_body(response)
        elif "content-length" in response_headers:
            content_length = int(response_headers["content-length"])
            content_bytes = response.read(content_length)
        else:
            content_bytes = response.read()
            if (self.host, self.port) in SOCKET_CACHE:
                del SOCKET_CACHE[(self.host, self.port)]
            s.close()

        if response_headers.get("content-encoding") == "gzip":
            import gzip
            content_bytes = gzip.decompress(content_bytes)

        content = content_bytes.decode("utf8")

        if response_headers.get("connection") == "close":
            if (self.host, self.port) in SOCKET_CACHE:
                del SOCKET_CACHE[(self.host, self.port)]
            s.close()


        if status in ["200", "301", "404"]:
            can_cache = False
            max_age = 0
            if "cache-control" in response_headers:
                directives = [d.strip().lower() for d in response_headers["cache-control"].split(",")]
                allowed = True
                for d in directives:
                    if d == "no-store":
                        allowed = False
                        break
                    elif d.startswith("max-age="):
                        try:
                            max_age = int(d.split("=")[1])
                            can_cache = True
                        except ValueError:
                            allowed = False
                            break
                    else:
                        allowed = False
                        break
                if allowed and can_cache:
                    HTTP_CACHE[self.url] = (time.time() + max_age, content)

        if status.startswith("3"):
            if redirect_limit <= 0:
                raise RuntimeError("Too many redirects")
            location = response_headers.get("location")
            if not location:
                raise ValueError("Redirect response missing Location header")

            # Resolve redirect URL
            if location.startswith("/"):
                if location.startswith("//"):
                    new_url = self.scheme + ":" + location
                else:
                    host_port = self.host
                    if self.port and ((self.scheme == "http" and self.port != 80) or (self.scheme == "https" and self.port != 443)):
                        host_port += ":" + str(self.port)
                    new_url = self.scheme + "://" + host_port + location
            elif ":" not in location:
                parent_path = self.path.rsplit("/", 1)[0]
                host_port = self.host
                if self.port and ((self.scheme == "http" and self.port != 80) or (self.scheme == "https" and self.port != 443)):
                    host_port += ":" + str(self.port)
                new_url = self.scheme + "://" + host_port + parent_path + "/" + location
            else:
                new_url = location

            return URL(new_url).request(headers, redirect_limit - 1)

        return content




def show(body):
    in_tag = False
    accumulated_text = ""
    for c in body:
        if c == "<":
            in_tag = True
            if accumulated_text:
                print(accumulated_text.replace("&lt;", "<").replace("&gt;", ">"), end="")
                accumulated_text = ""
        elif c == ">":
            in_tag = False
        elif not in_tag:
            accumulated_text += c
    if accumulated_text:
        print(accumulated_text.replace("&lt;", "<").replace("&gt;", ">"), end="")



def load(url):
    body = url.request()
    show(body)


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        default_file_path = os.path.abspath("default.html")
        if not os.path.exists(default_file_path):
            with open(default_file_path, "w", encoding="utf8") as f:
                f.write("<html><body><h1>Hello World</h1><p>Welcome to your custom browser!</p></body></html>")
        url = "file://" + default_file_path

    load(URL(url))

