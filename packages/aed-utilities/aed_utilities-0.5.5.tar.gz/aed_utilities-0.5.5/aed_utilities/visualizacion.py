from graphviz import Source
from IPython.display import display_svg, SVG,display
import numpy as np

class SegmentationFault(Exception):
    pass

class LinkedListDrawer:
  def __init__(self, **kwargs):
    self.strHeader = kwargs.get('strHeader', '')
    self.fieldLink = kwargs.get('fieldLink', '')
    self.fieldHeader = kwargs.get('fieldHeader', '')
    self.fieldData = kwargs.get('fieldData', '')
    self.fieldReverseLink = kwargs.get('fieldReverseLink', None)
    self.pointers = kwargs.get('pointers', {}) # dict of [int] -> [str]
  
  def draw_linked_list(self, nList):
    listStr = ''

    if self.strHeader!="":
      listStr = f'HEAD [shape=plaintext label="{self.strHeader}"];\n'
    listStr += 'NULL [shape=square label=""];\n'

    for position, label in self.pointers.items():
      listStr += f'_label_pos{position} [shape=plaintext label="{label}"];\n'

    listStr += 'node[shape=circle];\n'
    if self.strHeader != "":
      listStr += 'HEAD -> '

    p = getattr(nList, self.fieldHeader)
    position = 0
    pointedNodes = []
    while p is not None:
      nodeData = str(getattr(p, self.fieldData))
      p = getattr(p, self.fieldLink)
    
      if position in self.pointers:
        listStr += f'_nodo_pos{position} -> '
        pointedNodes.append(f'_nodo_pos{position} [shape=circle label="{nodeData}"];\n'
                                    f'_label_pos{position} -> _nodo_pos{position};\n'
                                    f'{{ rank="same"; _label_pos{position}; _nodo_pos{position} }};')
      else:
        listStr += f'{nodeData} -> '
      position+=1
  
    listStr += 'NULL;\n'

    listStr += '\n'.join(pointedNodes)
    if position in self.pointers: # Last position is NULL
      listStr += f'''
        _label_pos{position} -> NULL;
        {{ rank="same"; _label_pos{position}; NULL }} '''

    if len(self.pointers) > 1 and max(self.pointers) > position:
      raise SegmentationFault(f'Tried to draw a pointer to node {max(self.pointers)}, but list length is {position}.')

    src = Source('digraph "Lista" { rankdir=LR; ' + listStr +' }')
    src.render('lista.gv', view=True)
    display(SVG(src.pipe(format='svg')))
  
  def ascending_list(self, nList):
    p = getattr(getattr(nList, self.fieldHeader), self.fieldLink)
    while p is not getattr(nList, self.fieldHeader):
      yield getattr(p, self.fieldData)
      p = getattr(p, self.fieldLink)

  def descending_list(self, nList):
    p = getattr(getattr(nList, self.fieldHeader), self.fieldReverseLink)
    while p is not getattr(nList, self.fieldHeader):
      yield getattr(p, self.fieldData)
      p = getattr(p, self.fieldReverseLink)

  def draw_double_linked_list(self, nList):
    listStrAsc = "node[shape=circle]; "
    listaAsc = [x for x in self.ascending_list(nList)]
    for i, x in enumerate(listaAsc):
      listStrAsc = listStrAsc + str(x)
      if i < len(listaAsc) - 1:
        listStrAsc = listStrAsc + ' -> '
  
    listStrDesc = ""

    listaDesc = [x for x in self.descending_list(nList)]
    for i, x in enumerate(listaDesc):
      listStrDesc = listStrDesc + str(x)
      if i < len(listaDesc) - 1:
        listStrDesc = listStrDesc + ' -> '
  
    src = Source('digraph "Lista" { rankdir=LR; ' + listStrAsc + ' ' + listStrDesc +' }')
    src.render('lista.gv', view=True)
    display(SVG(src.pipe(format='svg')))


class PositionNode:
  def __init__(self, left, info, right, nodetype, code):
        self.left=left
        self.info=info
        self.right=right
        self.x = 0.0
        self.y = 0.0
        self.nodetype = nodetype
        self.code = code

class BinaryTreeDrawer:
  def __init__(self, fieldData, fieldLeft, fieldRight, classNone=None, drawNull = False, shapeInternal='circle'):
    self.nameInfo = fieldData
    self.nameLeft = fieldLeft
    self.nameRight = fieldRight
    self.offset = 0.35
    self.classNone = classNone
    self.drawNull = drawNull
    self.counterNull = 0
    self.counterNodes = 0
    self.shapeInternal = shapeInternal
    
  def gen_code(self):
    code = "node" + str(self.counterNodes)
    self.counterNodes = self.counterNodes + 1
    return code

  def copy_tree(self, node):
    if self.classNone is not None:
      if isinstance(node, self.classNone):
        if not hasattr(node, "info"):
          if not self.drawNull:
            return None
          else:
            newNode = PositionNode(None, "", None, "square", "null" + str(self.counterNull))
            self.counterNull = self.counterNull + 1
            return newNode
        else:
          if not self.drawNull:
            return PositionNode(None, getattr(node, self.nameInfo), None, "square", self.gen_code())
          else:
            newNode1 = PositionNode(None, "", None, "square", "null" + str(self.counterNull))
            self.counterNull = self.counterNull + 1
            newNode2 = PositionNode(None, "", None, "square", "null" + str(self.counterNull))
            self.counterNull = self.counterNull + 1
            return PositionNode(newNode1, getattr(node, self.nameInfo), newNode2, self.shapeInternal, self.gen_code())
    else:
      if node is None:
        if not self.drawNull:
          return None
        else:
          newNode = PositionNode(None, "", None, "square", "null" + str(self.counterNull))
          self.counterNull = self.counterNull + 1
          return newNode
  
    newLeft = self.copy_tree(getattr(node, self.nameLeft))
    newRight = self.copy_tree(getattr(node, self.nameRight))

    return PositionNode(newLeft, getattr(node, self.nameInfo), newRight, self.shapeInternal, self.gen_code())

  def update_position(self, node, shiftX, shiftY):
    if node is not None:
      self.update_position(node.left, shiftX, shiftY)
      self.update_position(node.right, shiftX, shiftY)
      node.x = node.x + shiftX
      node.y = node.y + shiftY

  def compute_position(self, node):
    if node.left is None and node.right is None:
      return 0.0,-self.offset/3,self.offset/3
  
    if node.left is not None:
      center1, min1, max1 = self.compute_position(node.left)
    else:
      min1 = 0.0
      max1 = 0.0

    if node.right is not None:  
      center2, min2, max2 = self.compute_position(node.right)
    else:
      min2 = 0.0
      max2 = 0.0

    self.update_position(node.left, -(max1 + self.offset), -0.6)
    self.update_position(node.right,-(min2 - self.offset), -0.6)

    return 0.0, min1 - (max1 + self.offset), max2 - (min2 - self.offset)

  def inorden(self, node, L):
    if node is not None:
      self.inorden(node.left, L)
      L.append((node.info, node.x, node.y, node.code, node.nodetype))
      self.inorden(node.right, L)

  def encode_nodes(self,node):
    L = []
    self.inorden(node, L)
    
    listStr = ""

    for item in L:
      data = item[0]
      if data == np.inf:
        data='+&infin;'

      if "null" in str(item[3]):
        listStr = listStr + ' ' + str(item[3])+ '[pos="' + str(item[1]) + ',' + str(item[2]) + '!" shape=square label="'+str(data)+'" width="0.2"] '  
      else:
        listStr = listStr + '"' + str(item[3])+ '"' + '[pos="' + str(item[1]) + ',' + str(item[2]) + '!" label="'+str(data)+'" shape='+str(item[4])+' margin=0] '
  
    return listStr

  def encode_edges(self, node):
    listStr = ""

    if node.left is not None:
      listStr = listStr + " " + str(node.code) + "--" + str(node.left.code)
      listStr = listStr + self.encode_edges(node.left) + " "
 
    if node.right is not None:
      listStr = listStr + " " + str(node.code) + "--" + str(node.right.code)
      listStr = listStr + self.encode_edges(node.right) + " "
 
    return listStr

  def draw_tree(self, tree, root):
    self.counterNull = 0
    self.counterNodes = 0
    
    B = self.copy_tree(getattr(tree, root))
    x,y,z=self.compute_position(B)

    listNodes = self.encode_nodes(B)
    listStr = self.encode_edges(B)
  
    src = Source('graph "Arbol" { rankdir=TB; ' + listNodes + ' node[shape='+ self.shapeInternal +'] ' + listStr +' }')
    src.engine="neato"
    src.render('lista.gv', view=True)
    display(SVG(src.pipe(format='svg')))

class NumpyArrayDrawer:
  def __init__(self, animation = False):
    self.animation = animation

  def drawNumpy1DArray(self, array, showIndex=False, layout="row", ):
    maxLen = 0
    for i in range(array.shape[0]):
      val = str(array[i])
      if len(val) > maxLen:
        maxLen = len(val)

    size = 20 + 7*maxLen
    if layout=="row":
      strArray = "<TR>"
      for i in range(array.shape[0]):
        strArray = strArray + '<TD border="1" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(array[i]) +'</TD>'
      strArray = strArray + '</TR>'
      if showIndex:
        strArray = strArray + "<TR>"
        for i in range(array.shape[0]):
          strArray = strArray + '<TD border="0" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(i) +'</TD>'
        strArray = strArray + '</TR>'
    elif layout=="column":
      strArray = ""
      for i in range(array.shape[0]):
        if not showIndex:
          strArray = strArray + '<TR><TD border="1" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(array[i]) +'</TD></TR>'
        else:
          strArray = strArray + '<TR><TD border="0" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(i) +'</TD><TD border="1" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(array[i]) +'</TD></TR>'
  
    if not self.animation:
      src = Source('graph "Array" { node [fontsize=15, shape=plaintext]; a0 [label=< <TABLE border="0" cellspacing="0" cellpadding="3">' + strArray + '</TABLE> >] }')
      src.render('lista.gv', view=True)
      display(SVG(src.pipe(format='svg')))
      return None
    else:
      src = Source('graph "Array" { node [fontsize=15, shape=plaintext]; a0 [label=< <TABLE border="0" cellspacing="0" cellpadding="3">' + strArray + '</TABLE> >] }', format='png')
      return src
  
  def drawNumpy2DArray(self, array, showIndex=False):
    maxLen = 0
    for i in range(array.shape[0]):
      for j in range(array.shape[1]):
        val = str(array[i][j])
        if len(val) > maxLen:
          maxLen = len(val)

    size = 20 + 7*maxLen
    strArray=""

    if showIndex:
      strArray = strArray + '<TR><TD border="0" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'"></TD>'
      for j in range(array.shape[1]):
        strArray = strArray + '<TD border="0" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(j) +'</TD>'
      strArray = strArray + '</TR>'

    for i in range(array.shape[0]):
      if showIndex:
        strArray = strArray + '<TR><TD border="0" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(i)+ '</TD>'
      else:
        strArray = strArray + '<TR>'
      for j in range(array.shape[1]):
        strArray = strArray + '<TD border="1" fixedsize="true" width="'+str(size)+'" height="'+str(size)+'">' + str(array[i][j]) +'</TD>'
      strArray = strArray + "</TR>"

    src = Source('graph "Array" { node [fontsize=15, shape=plaintext]; a0 [label=< <TABLE border="0" cellspacing="0" cellpadding="3">' + strArray + '</TABLE> >] }')
    src.render('lista.gv', view=True)
    if not self.animation:
      display(SVG(src.pipe(format='svg')))
    else:
      return src

#class NumyArrayAnimation:
#  def __init__(self):
#    self.drawer = NumpyArrayDrawer(animation=True)
#    self.counter = 0
  
#  def post_array(self, array, showIndex=False, layout='row'):
#    src = self.drawer.drawNumpy1DArray(array, showIndex=showIndex, layout=layout)
#    src.render('file'+str(self.counter)+'.png')
#    self.counter = self.counter + 1
  
#  def view_animation(self, size,delay):
#    for k in range(self.counter):
#		call([ 'mogrify', '-gravity', 'center', '-background', 'white', '-extent', str(size), 'file'+ str(k) + '.png'])
	  
#    cmd = [ 'convert' ]
#	  for k in self.counter:
#		  cmd.extend( ( '-delay', str( delay ), 'file'+ str(k) + '.png' ) )
#	  cmd.append( 'animation.gif' )
#	  call( cmd )
  
