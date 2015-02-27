#!/bin/python

import subprocess
import sys

from index import PLAYS, simple_name, noncap_name

def generate_html(githash):
    def generate_play_line(play, githash):
        template = """
<div class="play">
    <div class="title">{name}</div>
    <a href="{githash}/{shortname}.epub">ePub</a>
    <a href="{githash}/{shortname}.mobi">Kindle</a>
    <a href="{githash}/{shortname}.pdf">pdf</a>
</div>
"""
        return template.format(name=noncap_name(play), shortname=simple_name(play), githash=githash)

    css = """
body {
    font-family: 'Merriweather', serif;
    background: #fffde9;
}
a {
    text-decoration: none;
    color: #8c0000;
}
a:hover {
    color: #3c3c3c;
}
h1.title {
    margin: 0 auto;
    line-height: 2.4em;
    width: 80%;
    max-width: 1000px;
    font-weight:300;
    text-align: center;
    border-bottom: solid 1px black;
    margin-bottom: 1em;
}
div.plays {
    margin: 0 auto;
    width: 50em;
    max-width: 100%;
}
div.title {
    display: block;
    font-size: 1.17em;
    margin: 1.2em 0 .2em 0;
}
div.play {
    width: 21em;
    padding: 0 2em;
    float:left;
}
div.play a {
    padding-right: 1.3em;
    font-size: .8em;
}
div.footer {
    margin: 0 auto;
    width: 80%;
    clear: both;
    max-width: 1000px;
}
div.footer div {
    font-weight:300;
    text-align: center;
    line-height: 2.4em;
    padding: 2em 0 1em 0;
    }

"""

    ga_tag = """
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-45348725-4', 'auto');
  ga('send', 'pageview');

</script>
"""

    template = """
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <meta name=viewport content="width=device-width, initial-scale=1">
    <title>The Complete Works for Shakespeare</title>
    <link href='//fonts.googleapis.com/css?family=Merriweather:300,400' rel='stylesheet' type='text/css'>
    <style>
      {css}
    </style>
    {ga_tag}
  </head>
  <body>
    <h1 class="title">The Complete Works of Shakespeare</h1>
    <div class="plays">
    {content}
    </div>
    <div class="footer">
      <div>
        Liyan Chang - <a href="https://www.ldchang.com">ldchang.com</a>
      </div>
    </div>
  </body>
</html>
"""

    plays = PLAYS[:]
    plays = sorted(plays, key=noncap_name)

    return template.format(
            content="\n".join(generate_play_line(play, githash) for play in plays),
            githash=githash,
            css=css,
            ga_tag=ga_tag
            )


def get_githash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()


def main():
    o = open('output/index.html', 'w')
    o.write(generate_html(get_githash()))


if '__main__' == __name__:
    sys.exit(main())
