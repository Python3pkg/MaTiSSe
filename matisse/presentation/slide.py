#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
This defines a slide of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from ..config import __config__
from ..theme import box
from ..theme import columns
from ..theme import figure
from ..theme import note
from ..theme import table
from ..theme.slide.position import Position
from ..theme.theme import Theme
from ..utils.source_editor import __source_editor__ as seditor
# global variables
# class definition
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.

  Attributes
  ----------
  slides_number : int
    global number of slides (equals to the number of Slide instances)
  """
  slides_number = 0

  def __init__(self,raw_body='',title='',data=None,theme=None,local_number=1):
    """
    Parameters
    ----------
    raw_body : str, optional
      string containing the body of the slide in raw format
    title : str, optional
      slide title
    data : OrderedDict object, optional
      slide metadata
    local_number : int, optional
      subsection number in local-to-section numeration

    Attributes
    ----------
    raw_body : str
      string containing the body of the slide in raw format
    number : int
      slide number in global numeration
    local_number : int
      subsection number in local-to-subsection numeration
    title : str
      slide title
    data : OrderedDict object
      slide metadata
    overtheme : Theme object
      overriding theme of the current slide
    pos : Position object
      slide position
    """
    Slide.slides_number += 1
    self.raw_body     = raw_body
    self.number       = Slide.slides_number
    self.local_number = local_number
    self.title        = title
    self.data         = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val
    self.data['slidetitle' ] = self.title
    self.data['slidenumber'] = str(self.number)
    self.overtheme = None
    self.pos = Position()
    self.__get_overtheme(theme=theme)
    return

  def __get_overtheme(self,theme=None):
    """Method for checking if the slide has a personal theme overriding the global one.

    Parameters
    ----------
    theme: Theme object, optional
      base theme used to set other overtheme data not being defined
    """
    source = seditor.get_overtheme(source=self.raw_body)
    if source:
      self.overtheme = Theme(source=source)
      if theme:
        self.overtheme.set_from(other=theme)
      self.overtheme.slide.adjust_dims()
      self.raw_body = seditor.strip_overtheme(self.raw_body)
      if __config__.verbose:
        print('Found overriding theme for slide n. '+str(self.number))
        print(self.get_css(only_custom=True))
    return

  def get_css(self,only_custom=False):
    """Method returning slide's css.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data

    Returns
    -------
    str
      a string containing the css code of the theme
    """
    css = []
    if self.overtheme:
      css = self.overtheme.slide.get_css(only_custom=only_custom,as_list=True)
    if len(css)>0:
      return ''.join(['\n#slide-'+str(self.number)+' '+c[1:] for c in css])
    else:
      return ''

  def put_attributes(self,doc):
    """Method for putting html attibutes of the slide.

    Parameters
    ----------
    """
    doc.attr(('id','slide-'+str(self.number)))
    doc.attr(('title',self.title))
    if 'sectiontitle' in self.data:
      doc.attr(('sectiontitle',self.data['sectiontitle']))
    if 'sectionnumber' in self.data:
      doc.attr(('sectionnumber',self.data['sectionnumber']))
    if 'subsectiontitle' in self.data:
      doc.attr(('subsectiontitle',self.data['subsectiontitle']))
    if 'subsectionnumber' in self.data:
      doc.attr(('subsectionnumber',self.data['subsectionnumber']))
    return

  @staticmethod
  def subtokenize(tokens,tokenize,subtokens_name):
    """Method for sub-tokenizing a previous (master) tokenization.

    Parameters
    ----------
    tokens : list
      list of master tokens
    tokenize : function
      for for tokenizing
    subtokens_name : str
      name of the subtokens tag to be inserted into the master tokens into the elements that
      have been subtokenized

    Returns
    -------
    list
      list of subtokens which each element is [index_in_master_tokens,subtokens]
    """
    subtokens = []
    for tkn,token in enumerate(tokens):
      if token[0]=='unknown':
        toks = tokenize(source=token[1])
        if len(toks)>1:
          subtokens.append([tkn,toks])
          tokens[tkn] = [subtokens_name]
    return subtokens

  @staticmethod
  def merge_subtokens(tokens,subtokens,tkn):
    """Method for merge subtokens into tokens.

    Parameters
    ----------
    tokens : list
      list of tokens
    subtokens : list
      list of subtokens
    tkn : int
      token index
    """
    for sub_token in subtokens:
      if sub_token[0] == tkn:
        for tok in sub_token[1]:
          tokens.append(tok)
        break
    return

  def raw_body_tokenize(self):
    """Method for tokenizing raw_body.

    The tokens hierarchy is the following:

    + columns environments can contain anything (also other environments);
    + box(figure/table/note) environments can contain box or markdown data, but no other environments;
    + markdown data without MaTiSSe.py environments;

    Returns
    -------
    list
      list of tokens whose elements are ['type',source_part]
    """
    c_tokens = columns.tokenize(source=self.raw_body)
    b_tokens = self.subtokenize(tokens=c_tokens,tokenize=box.tokenize,   subtokens_name='box tokens'   )
    f_tokens = self.subtokenize(tokens=c_tokens,tokenize=figure.tokenize,subtokens_name='figure tokens')
    t_tokens = self.subtokenize(tokens=c_tokens,tokenize=table.tokenize, subtokens_name='table tokens' )
    n_tokens = self.subtokenize(tokens=c_tokens,tokenize=note.tokenize,  subtokens_name='note tokens'  )
    tokens = []
    for tkn,token in enumerate(c_tokens):
      if token[0]=='columns' or token[0]=='unknown':
        tokens.append(token)
      elif token[0]=='box tokens':
        self.merge_subtokens(tokens=tokens,subtokens=b_tokens,tkn=tkn)
      elif token[0]=='figure tokens':
        self.merge_subtokens(tokens=tokens,subtokens=f_tokens,tkn=tkn)
      elif token[0]=='table tokens':
        self.merge_subtokens(tokens=tokens,subtokens=t_tokens,tkn=tkn)
      elif token[0]=='note tokens':
        self.merge_subtokens(tokens=tokens,subtokens=n_tokens,tkn=tkn)
    return tokens

  def raw_body_parse(self):
    """Method for parsing raw_body.

    Returns
    -------
    str
      string containing the parsed raw_body
    """
    tokens = self.raw_body_tokenize()
    parsed_body = ''
    for token in tokens:
      if token[0] == 'unknown':
        parsed_body += '\n'+seditor.md_convert(source=token[1])
      elif token[0]=='columns':
        parsed_body += '\n'+columns.parse(source=token[1])
      elif token[0]=='box':
        parsed_body += '\n'+box.parse(source=token[1])
      elif token[0]=='figure':
        parsed_body += '\n'+figure.parse(source=token[1])
      elif token[0]=='table':
        parsed_body += '\n'+table.parse(source=token[1])
      elif token[0]=='note':
        parsed_body += '\n'+note.parse(source=token[1])
    return parsed_body

  def to_html(self,position,theme):
    """Method for converting slide content into html format.

    Parameters
    ----------
    position : SlidePosition object
      current slide position
    doc : yattag.Doc object
      the main html doc
    theme : Theme object
      the base theme
    """
    doc = Doc()
    with doc.tag('div'):
      self.put_attributes(doc=doc)
      # get slide positioning data
      actual_theme = None
      if self.overtheme:
        actual_theme = self.overtheme.slide
      else:
        actual_theme = theme
      position.set_position(theme=theme,overtheme=actual_theme)
      if self.title != '$overview':
        doc.attr(('class','step slide'))
        doc.attr(('data-x',str(position.position[0])))
        doc.attr(('data-y',str(position.position[1])))
        doc.attr(('data-z',str(position.position[2])))
        doc.attr(('data-scale',str(position.scale)))
        doc.attr(('data-rotate-x',str(position.rotation[0])))
        doc.attr(('data-rotate-y',str(position.rotation[1])))
        doc.attr(('data-rotate-z',str(position.rotation[2])))
        # inserting elements
        for header in actual_theme.headers.values():
          header.to_html(doc=doc,metadata=self.data)
        for sidebar in actual_theme.sidebars.values():
          if sidebar.position == 'L':
            sidebar.to_html(doc=doc,metadata=self.data)
        if self.number == 2:
          self.raw_body_parse()
        #content = columns.parse(source=self.raw_body)
        #content = figure.parse(source=content)
        #content = note.parse(source=content)
        #content = table.parse(source=content)
        #content = box.parse(source=content)
        #actual_theme.content.to_html(doc=doc,content='\n'+seditor.md_convert(content))
        actual_theme.content.to_html(doc=doc,content='\n'+self.raw_body_parse())
        for sidebar in actual_theme.sidebars.values():
          if sidebar.position == 'R':
            sidebar.to_html(doc=doc,metadata=self.data)
        for footer in actual_theme.footers.values():
          footer.to_html(doc=doc,metadata=self.data)
      else:
        doc.attr(('class','step overview'))
        doc.attr(('style',''))
        doc.attr(('data-x','0'))
        doc.attr(('data-y','0'))
        doc.attr(('data-z','0'))
        doc.attr(('data-scale',str(position.scale)))
    return doc.getvalue()
