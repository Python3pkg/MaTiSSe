#!/usr/bin/env python
"""
titlepage.py, module definition of Titlepage class.
This defines the title page the presentation being designed as an helper
object for writing a slide with a style very different from others.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# MaTiSSe.py modules
from ..theme.theme import Theme
from .regexs import __regex_titlepage__, __regex_endtitlepage__
from .slide import Slide
# class definition
class Titlepage(Slide):
  """
  Object for handling the title page, its attributes and methods.
  """
  def __init__(self,plain=False,source=None):
    """
    Parameters
    ----------
    plain : bool, optional
      flag for resetting the slide style to plain
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    found : bool
      flag for checking is title page was found
    plain : bool
      flag for resetting the slide style to plain
    """
    super(Titlepage,self).__init__(title='titlepage')
    self.found = False
    self.plain = plain
    if source:
      self.get(source=source)
    return

  def __str__(self):
    string = ''
    if self.found:
      string = self.raw_body
    return string

  def get(self,source):
    """Method for getting the title page contained into the source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without titlepage
    """
    match = re.search(__regex_titlepage__,source)
    if match:
      self.found = True
      if match.group('plain') and str(match.group('plain')).lower() == 'plain':
        self.plain = True
        self.overtheme = Theme(set_all_custom=True)
      end = -1
      endmatch = re.search(__regex_endtitlepage__,source[match.end():])
      if endmatch:
        end = endmatch.start()+match.end()
      self.raw_body = source[match.end():end]
      source = source[0:match.start()]+source[end:]
    return source
