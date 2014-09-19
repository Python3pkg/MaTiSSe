#!/usr/bin/env python
"""
content.py, module definition of Content class.
This defines the theme of the slide content element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from ..theme_element import ThemeElement
# class definition
class Content(ThemeElement):
  """
  Object for handling the presentation theme slide content, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    padding : str
      padding internal to the content container
    """
    super(Content,self).__init__(data_tag=r'theme_slide_content',special_keys=['padding'],class_name='slide-content')
    self.data.data['width'        ] = ['100%',   False]
    self.data.data['height'       ] = ['100%',   False]
    self.data.data['padding'      ] = ['0',      False]
    self.padding = None
    if source:
      self.get(source)
      self.check_specials()
    return

  def check_specials(self):
    """Method for checking specials data entries.

    This theme element has the following special entries:
    1. padding
    """
    super(Content,self).check_specials()
    for key,val in self.data.data.items():
      if val[1]:
        if key == 'padding':
          self.padding = val[0]
          self.data.data[key] = ['0',True]
    return

  def set_from(self,other):
    """Method for setting theme using data of other (theme element).

    Parameters
    ----------
    other : Content object
    """
    super(Content,self).set_from(other=other)
    if self.padding == '0' and other.padding and other.padding != '0':
      self.padding = other.padding
      self.data.data['padding'] = ['0',False]
    self.check_specials()
    return

  def adjust_dims(self,headers,footers,sidebars):
    """Method for adjusting content dimensions accordingly to the settings of other elements of the slide theme.

    Parameters
    ----------
    headers : dict
      dictionary with values of Header objects, being the list of headers defined into the slide
    footers : dict
      dictionary with values of Footer objects, being the list of footers defined into the slide
    sidebars : dict
      dictionary with values of Sidebar objects, being the list of sidebars defined into the slide
    """
    s_w = 100 # slide content width (in percent %); should be always 100% initially
    s_h = 100 # slide content height (in percent %); should be always 100% initially
    if len(headers)>0:
      for header in headers.values():
        if header.active:
          s_h -= int(header.data.data['height'][0].strip('%'))
    if len(footers)>0:
      for footer in footers.values():
        if footer.active:
          s_h -= int(footer.data.data['height'][0].strip('%'))
    if len(sidebars)>0:
      for sidebar in sidebars.values():
        if sidebar.active:
          s_w -= int(sidebar.data.data['width'][0].strip('%'))
    self.data.data['width']  = [str(s_w)+'%',True]
    self.data.data['height'] = [str(s_h)+'%',True]
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nSlide Content']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data
    as_list : bool, optional
      return a list instead of a string

    Returns
    -------
    str
      a string containing the css code of the theme if as_list = False
    list
      a list of one string containing the css code of the theme if as_list = True
    """
    css = "\n.slide-content {\n  float: left;"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
