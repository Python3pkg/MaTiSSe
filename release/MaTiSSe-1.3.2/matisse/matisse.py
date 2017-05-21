#!/usr/bin/env python
"""
MaTiSSe.py, Markdown To Impressive Scientific Slides
"""

import argparse
import os
import sys
from .matisse_config import MatisseConfig
from .presentation import Presentation

__appname__ = "MaTiSSe.py"
__description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides"
__long_description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides. It is a very simple and stupid-to-use (KISS) presentation maker based on simple markdown syntax producing high quality first-class html/css presentation with great support for scientific contents."
__version__ = "1.3.2"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/MaTiSSe"
__sample__ = r"""
---
metadata:
  - title: "Autogenerated Sample"
  - conference: "Very nice Conference"
  - date: "12th December 2012"
  - authors:
    - Stefano Zaghi
    - John Doe
  - authors_short:
    - S. Zaghi
    - J. Doe
  - affiliations:
    - University 1
    - University 2
  - affiliations_short:
    - Univ. 1
    - Univ. 2
---

# First Chapter

## First Section

### First Subsection

#### First Slide

##### A H5 heading

Lorem ipsum dolor sit amet...

##### Math

$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$

$note
$content{Just a note enviroment}
$endnote

##### Unordered list

+ $authors
+ $title

##### Ordered list

1. $affiliations
1. $conference

# Second Chapter

## Second Section

### Second Subsection

#### Second Slide

$table
$caption{Just a table enviroment}
$content{
| Foo | Bar | Baz | Authors  | Title  |
|-----|-----|-----|----------|--------|
| 1   |  2  |  3  | $authors | $title |
| 2   |  3  |  4  |    /     |   /    |
| 3   |  4  |  5  |    /     |   /    |
| 4   |  5  |  6  |    /     |   /    |
}
$endtable
"""


def make_presentation(config, source, output):
  """Make the presentation.

  Parameters
  ----------
  config: MatisseConfig()
  source: str
    source markdown
  output: str
    output path

  Returns
  -------
  source: str
    the parsed source
  """
  config.make_output_tree(output=output)
  if config.theme is not None:
    source = config.put_theme(source=source, output=output)
  presentation = Presentation()
  presentation.parse(config=config, source=source)
  presentation.save(config=config, output=output)
  return source


def main():
  """Main function."""
  cliparser = argparse.ArgumentParser(prog=__appname__, description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
  cliparser.add_argument('-v', '--version', action='version', help='Show version', version='%(prog)s ' + __version__)
  cliparser.add_argument('-i', '--input', required=False, action='store', default=None, help='Input file name of markdown source to be parsed')
  cliparser.add_argument('-o', '--output', required=False, action='store', default=None, help='Output directory name containing the presentation files')
  cliparser.add_argument('-t', '--theme', required=False, action='store', default=None, help='Select a builtin theme for initializing a new sample presentation')
  cliparser.add_argument('-hs', '--highlight-style', required=False, action='store', default='github.css', help='Select the highlight.js style (default github.css); select "disable" to disable highligth.js', metavar='STYLE.CSS')
  cliparser.add_argument('-s', '--sample', required=False, action='store', default=None, help='Generate a new sample presentation as skeleton of your one')
  cliparser.add_argument('--toc-at-chap-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each chapter beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--toc-at-sec-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each section beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--toc-at-subsec-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each subsection beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--print-highlight-styles', required=False, action='store_true', default=None, help='Print the available highlight.js style (default github.css)')
  cliparser.add_argument('--print-themes', required=False, action='store_true', default=None, help='Print the list of the builtin themes')
  cliparser.add_argument('--verbose', required=False, action='store_true', default=False, help='More verbose printing messages (default no)')
  cliparser.add_argument('--online-MathJax', required=False, action='store_true', default=None, help='Use online rendering of LaTeX equations by means of online MathJax service; default use offline, local copy of MathJax engine')
  cliparser.add_argument('--pdf', required=False, action='store_true', default=False, help='Disable impress effects for printing slides to pdf')
  cliparser.add_argument('--print_parsed_source', required=False, action='store_true', default=False, help='Print the actually parsed source, namely source after including external files')
  cliargs = cliparser.parse_args()
  config = MatisseConfig(cliargs=cliargs)
  if cliargs.print_themes:
    print(config.str_themes())
  elif cliargs.print_highlight_styles:
    print(config.str_highlight_styles())
  elif cliargs.sample:
    output = os.path.splitext(os.path.basename(cliargs.sample))[0]
    output = os.path.normpath(output)
    source = make_presentation(config=config, source=__sample__, output=output)
    with open(cliargs.sample, 'w') as sample_file:
      sample_file.write(source)
  elif cliargs.input:
    if not os.path.exists(cliargs.input):
      sys.stderr.write('Error: input file "' + cliargs.input + '" not found!')
      sys.exit(1)
    else:
      with open(cliargs.input, 'r') as mdf:
        source = mdf.read()
      if cliargs.output:
        output = cliargs.output
      else:
        output = os.path.splitext(os.path.basename(cliargs.input))[0]
      output = os.path.normpath(output)
      make_presentation(config=config, source=source, output=output)


if __name__ == '__main__':
  main()