import collections
import sys
import time

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import rcParams
import requests


class GetArticle:
    URL = 'https://qiita.com/items/?page='
    langs = ["actionscript", "activebasic", "ada", "algol", "applescript",
             "arc/anaarki", "assembly", "awk", "bash", "shellscript", "basic",
             "batch", "boruneshell", "brainfuck", "c", "cshell", "c#", "c++",
             "clojure", "cmd.exe", "cobol", "coffeescript", "commonlisp",
             "crystal", "cython", "d", "dart", "deno", "eiffel", "elixir",
             "elm", "emacslisp", "erlang", "f#", "f-basic", "fortran",
             "freepascal", "friendlyinteractiveshell", "go",
             "googleappsscript", "groovy", "hack/hhvm", "haskell", "haxehsp",
             "java", "javascript", "jruby", "julia", "kornshell", "kotlin",
             "lazyk", "lua", "luajit", "matlab", "micropython", "mint", "ml",
             "moosscript", "mruby", "msx-basic", "nn88-basic", "nadesiko",
             "nim", "node.js", "objectpascal/delphi", "objective-c", "ocaml",
             "octave", "opal", "pascal", "perl", "php", "piet", "pli",
             "powershell", "processing", "prolog", "pypy", "python", "r",
             "racket", "raku", "reason", "ruby", "rust", "scala", "scala.js",
             "scheme", "scratch", "sed", "simula", "smalltalk", "standardml",
             "streem", "swift", "typescript", "unlambda", "vba", "vimscript",
             "viscuit", "visualbasic", "webassembly", "whitespace", "wsh",
             "xtend", "zshell"]

    def __init__(self, num_pages=30):
        self.tags = []
        for page in range(1, num_pages):
            self.get_tags(page)
        self.c_tags = collections.Counter(self.tags)
        self.plot_graph()

    def get_tags(self, page):
        result = requests.get(self.URL + str(page))
        content = result.content
        soup = BeautifulSoup(content, 'lxml')
        tags = soup.find_all('a', 'u-link-unstyled TagList__label')
        tags_lang = [t.get_text().lower() for t in tags
                     if t.get_text().lower() in self.langs]
        self.tags.extend(tags_lang)
        time.sleep(0.1)

    def plot_graph(self):
        rcParams["font.family"] = "sans-serif"
        rcParams["font.sans-serif"] = "Hiragino Maru Gothic Pro"
        rcParams['font.size'] = 12.0
        rcParams['figure.figsize'] = (15, 10)
        items = sorted(self.c_tags.items(), key=lambda x: x[1], reverse=True)
        keys = [x[0] for x in items]
        values = [x[1] for x in items]
        data_dic = {"Figure": values,
                    "Label": keys}
        plt.pie(
                data_dic["Figure"],
                labels=data_dic["Label"],
                autopct=lambda p: '{:1.1f}%'.format(p) if p >= 2 else '',
                counterclock=False,
                pctdistance=0.8,
                rotatelabels=True,
                startangle=90,
                wedgeprops={"edgecolor": "black"}
                )
        # plt.title("Programming language popularity order")
        plt.tight_layout()
        plt.savefig("popular_lang.png")
        plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        g = GetArticle()
    else:
        g = GetArticle(int(sys.argv[1]))
