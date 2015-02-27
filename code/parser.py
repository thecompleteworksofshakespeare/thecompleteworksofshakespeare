#!/bin/python
import shutil
import sys
import re
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont
from index import WORKS, PLAYS, simple_name

def split(contents):
    out = {}
    pointer = []
    for line in contents:
        if line.strip() in WORKS:
            play = line.strip()
            if play not in out:
                out[play] = []
            pointer = out[play]
        pointer.append(line)
    return out

def parse_play(contents, title):
    class State:
        TEXT, PERSONAE = range(2)

    out = []
    out.append('% ' + title)
    out.append('% William Shakespeare')
    state = State.TEXT
    for line in contents:

        if state == State.TEXT:
            line = line.rstrip()

            if not line.strip():
                continue

            if line.strip() == title:
                continue

            if line.strip() == "DRAMATIS PERSONAE":
                state = State.PERSONAE
                continue

            if line.startswith('ACT'):
                out.append('')
                out.append('<div class="break"></div>\pagebreak')
                out.append('')
                out.append('# ' + line)
                continue

            if line.startswith('SCENE'):
                if not line.strip().startswith('SCENE I\t'):
                    out.pop()
                out.append('## ' + line.replace('\t', ' - '))
                continue

            line = line.replace('[', '*').replace(']', '*')

            if line.startswith('\t'):
                out.append('| ' + line.strip())
                continue

            if '\t' in line:
                speaker, _, line = line.partition('\t')
                out.append('')
                out.append(speaker)
                out.append('')
                out.append('| ' + line.strip())
                continue

            continue

        if state == State.PERSONAE:
            if line.startswith('ACT'):
                state = State.TEXT
                out.append('# ' + line.strip())
                continue
            continue
    return '\n'.join(out)


def generate_style():
    return """
body { margin: 5%; text-align: justify; font-size: medium; }
code { font-family: monospace; }
h1 { text-align: left; }
h2 { text-align: left; }
h3 { text-align: left; }
h4 { text-align: left; }
h5 { text-align: left; }
h6 { text-align: left; }
h1.title { }
h2.author { }
h3.date { }
ol.toc { padding: 0; margin-left: 1em; }
ol.toc li { list-style-type: none; margin: 0; padding: 0; }
div.break { page-break-after: always;}
"""


def generate_cover(title, f):
    h1font = ImageFont.truetype("arial.ttf", 30)
    h2font = ImageFont.truetype("arial.ttf", 15)
    W, H = 625, 1000

    h1 = title
    h2 = "William Shakespeare"

    image = Image.new('RGB', (W, H), color='White')
    draw = ImageDraw.Draw(image)

    w, h = draw.textsize(h1, font=h1font)
    draw.text(((W-w)/2,150), h1, fill="black", font=h1font)

    w, h = draw.textsize(h2, font=h2font)
    draw.text(((W-w)/2,200), h2, fill="black", font=h2font)
    del draw

    image.save(f)


def create_path(path):
    try:
        os.stat(path)
    except:
        os.makedirs(path)


def write_file(path, contents):
    with open(path, 'w') as f:
        f.write(contents)


def get_githash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()


def main():
    output = 'output/{githash}/'.format(githash=get_githash())
    create_path(output)

    with open('raw/shakespe.are') as f:
        raw = f.readlines()
        contents = raw[0].split('\r')
        works = split(contents)

        for i, work in enumerate(works):
            #PLAYS = ["ALL'S WELL THAT ENDS WELL"]
            if work in PLAYS:
                parsed = parse_play(works[work], work)
                simple_play_path = simple_name(work)
                path = 'build/' + simple_play_path + '/'
                create_path(path)

                o = open(path + 'cover.jpg', 'w')
                generate_cover(work, o)
                write_file(path + 'style.css', generate_style())
                write_file(path + 'text.md', parsed)

                subprocess.call("pandoc \
                        -o book.epub \
                        text.md --toc \
                        --epub-cover-image=cover.jpg \
                        --epub-stylesheet=style.css",
                        shell=True, cwd=path)
                subprocess.call("pandoc \
                        -o book.pdf\
                        text.md",
                        shell=True, cwd=path)
                subprocess.call("kindlegen book.epub -o book.mobi",
                        shell=True, cwd=path)

                # Finalize
                # Copy epub, mobi, pdf, html versions to output folder
                shutil.copyfile(path + 'book.epub', output + simple_play_path
                        + '.epub')
                shutil.copyfile(path + 'book.mobi', output + simple_play_path
                        + '.mobi')
                shutil.copyfile(path + 'book.pdf', output + simple_play_path
                        + '.pdf')

                print "done " + work
                print "{i} of {all}".format(all=len(works), i=i)


if '__main__' == __name__:
    sys.exit(main())
