# Uzoenr - a web browser with CLI interface.
# Copyright (C) 2022 Uzoenr
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import urllib.request, urllib.parse, os.path, os, configparser
from html.parser import HTMLParser
from uzoenr.fb2 import FB2
from uzoenr.rss import rss
hello = """
Uzoenr Copyright (C) 2022 Uzoenr
This program comes with ABSOLUTELY NO WARRANTY; for details open `about:warranty' page.
This is free software, and you are welcome to redistribute it
under certain conditions; open `about:copyright' page for details.
"""

warranty = """
15. Disclaimer of Warranty.

THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

16. Limitation of Liability.

IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
"""

copy = """
uzoenr - a web browser with CLI interface.
Copyright (C) 2022 uzoenr

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

class Engine(HTMLParser):
    data = ""
    permit = False
    def handle_starttag(self, tag, attrs):
        self.permit = (lambda tag: tag not in ["style", 'script'] or tag in ["a", "form", "input"])(tag)
        if tag == 'a':
           try:
               url = dict(attrs)["href"]
               self.data = self.data + "<" + url + " "
           except:
               pass
        elif tag == "form":
            try:
                url = dict(attrs)["action"]
                self.data = self.data + "\n[[FORM "+url
            except:
                pass
        elif tag == "input":
            try:
                name = dict(attrs)["name"]
                self.data = self.data + "(INPUT "+name+")\n"
            except:
                pass
        elif tag == "img":
            try:
                name = dict(attrs)["alt"]
                self.data = self.data + "{IMG "+name+"}\n"
            except:
                self.data = self.data + "{?!IMG}\n"
    def handle_endtag(self, tag):
        if tag == "a":
            self.data = self.data + "///>\n"
        elif tag == "form":
            self.data = self.data + "]]\n"
    def handle_data(self, data):
        if self.permit:
            self.data = self.data + data

def readbook(fb2):
    engine = FB2()
    with open(fb2) as f:
        engine.feed(f.read())
    return engine.finish()

val = {}
head = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36',
       "DNT":"1"}
d = urllib.parse.urlencode(val).encode('utf-8')
def load(url):
    if url == "about:warranty":
        return warranty.split("\n")
    if url == "about:copyright":
        return copy.split("\n")
    if url == "about:rule":
        return """
«Человек есть мера всех вещей существующих, что они существуют, и несуществующих, что они не существуют»
(Платон, Теэтет 152а)
""".split("\n")
    r = urllib.request.Request(url, d, head)
    b = Engine()
    with urllib.request.urlopen(r) as dat:
        page = dat.read()
    try:
       page = str(page, "utf-8")
    except:
        try:
            page = str(page, "cp1251")
        except:
            try:
                page = str(page, "cp866")
            except:
                try:
                    page = str(page, "koi8-r")
                except:
                    raise RuntimeError("Неизвестная кодировка")
    b.feed(page)
    page = b.data.split("\n")
    return page
def setupme():
    os.mkdir(os.path.expanduser("~")+"/.uzoenr")
    os.mkdir(os.path.expanduser("~"+"/.uzoenr/library"))
    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini", "w") as f:
        cfg = configparser.ConfigParser()
        cfg["Bookmark"] = {"warranty":"about:warranty",
                           "copy":"about:copyright"}
        cfg.write(f)
def start():
    global d
    global val
    print(hello)
    if not os.path.exists(os.path.expanduser("~")+"/.uzoenr/"):
        setupme()
    elif not os.path.exists(os.path.expanduser("~")+"/.uzoenr/bm.ini"):
        with open(os.path.expanduser("~")+"/.uzoenr/bm.ini", "w") as f:
            cfg = configparser.ConfigParser()
            cfg["Bookmark"] = {"warranty":"about:warranty",
                               "copy":"about:copyright"}
            cfg.write(f)
    cfg = configparser.ConfigParser()
    cfg.read(os.path.expanduser("~")+"/.uzoenr/bm.ini")
    try:
        page = load(input("Адрес: "))
    except:
        try:
            page = load(cfg["Setup"]["Homepage"])
        except:
            print("Неизвестный адрес и не загружена домашняя страница")
            page = load("about:copyright")
    while True:
        cmd = input('? ')
        if len(cmd) == 0:
            continue
        if cmd == "q":
            break
        try:
            cmd2 = cmd.split(" ")
            print("\n".join(page[int(cmd2[0]):int(cmd2[1])+1]))
        except:
            if cmd[0] == "l":
                try:
                    page = load(cmd[1:])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "d":
                try:
                    param = cmd[1:].split(" ")
                    download(param[0], param[1])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "B":
                param = cmd[1:]
                try:
                    page = load(cfg["Bookmark"][param])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == 'b':
                param = cmd[1:].split(" ")
                try:
                    cfg["Bookmark"][param[0]] = param[1]
                except Exception as e:
                    print("ошибка: ", e)
                    continue
                print("Закладка создана")
                with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                    cfg.write(f)
                print("Закладки сохранены")
            elif cmd[0] == "F":
                param = cmd[1:].split(" ")
                try:
                    val[param[0]] = param[1]
                except:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "f":
                try:
                    d = urllib.parse.urlencode(val).encode("ascii")
                    page = load(cmd[1:])
                    val = {}
                    d = urllib.parse.urlencode(val).encode("ascii")
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "H":
                try:
                    cfg["Setup"] = {"Homepage":cmd[1:]}
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini",'w') as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "R":
                try:
                    page = readbook(cmd[1:]).split("\n")
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "r":
                try:
                    page = readbook(os.path.expanduser("~")+"/.uzoenr/library/"+cmd[1:]).split("\n")
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "s":
                try:
                    res = [[str(i), page[i]] for i in range(len(page)) if cmd[1:] in page[i]]
                    print("\n".join(["\t".join(i) for i in res]))
                except Excepfion as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "p":
                param = cmd[1:].split(" ")
                try:
                    if "Point" not in cfg:
                        cfg["Point"] = {}
                    cfg["Point"][param[0]] = str(int(param[1]))
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "P":
                try:
                    point = int(cfg["Point"][cmd[1:]])
                    print(point, page[point])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "!":
                try:
                    point = int(cfg["Point"][cmd[1:]])
                    url = cfg["Bookmark"][cmd[1:]]
                    page = load(url)
                    print(point, "\n", "\n".join(page[point:]))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == 'L':
                try:
                    param = cmd[1:].split(' ')
                    download(param[0], os.path.expanduser("~")+"/.uzoenr/library/"+param[1])
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "a":
                try:
                    with open(os.path.expanduser("~")+"/.uzoenr/library/"+cmd[1:], "w") as f:
                        f.write("\n".join(page))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "+":
                try:
                    param = cmd[1:].split(" ")
                    if "Feed" not in cfg:
                        cfg["Feed"] = {}
                    cfg["Feed"][param[0]] = param[1]
                    with open(os.path.expanduser("~")+"/.uzoenr/bm.ini","w") as f:
                        cfg.write(f)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "?":
                try:
                    url = cfg["Feed"][cmd[1:]]
                    page = loadfeed(url)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "o":
                try:
                    for feedname in cfg["Feed"]:
                        download(cfg["Feed"][feedname], os.path.expanduser("~")+"/.uzoenr/"+feedname)
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            elif cmd[0] == "O":
                try:
                    parser = rss()
                    with open(os.path.expanduser("~")+"/.uzoenr/"+cmd[1:]) as f:
                        parser.feed(f.read())
                    page = parser.finish().split("\n")
                except Exception as e:
                    print("ошибка: ",e)
                    continue
            elif cmd.isdigit():
                try:
                    print("\n".join(page[int(cmd):]))
                except Exception as e:
                    print("ошибка: ", e)
                    continue
            else:
                print("Неизвестная команда")
def download(url, fname):
    r = urllib.request.Request(url, d, head)
    with urllib.request.urlopen(r) as dat:
        with open(fname, "wb") as fp:
            fp.write(dat.read())
    print("Файл загружен")
def loadfeed(url):
    r = urllib.request.Request(url, None, head)
    with urllib.request.urlopen(r) as dat:
        rssfeed = dat.read()
    rssfeed = rssfeed.decode("utf-8")
    parser = rss()
    parser.feed(rssfeed)
    return parser.finish().split("\n")


if __name__ == "__main__":
    start()