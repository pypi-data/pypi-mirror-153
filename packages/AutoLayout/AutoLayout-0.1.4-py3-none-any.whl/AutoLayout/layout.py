import gdspy
from copy import deepcopy
from .numCodeGenerator import morseNumCodeGenerator
import warnings

def fracturizer(devices, max_points):
  """
  Fracturies the object

  Args:
    devices (list): the polygon(s)
    max_point (int): the max points to be fracturized
  
  Returns:
    polygon(s) already being fracturized
  """
  if type(devices) != list:
    devices.fracture(max_points)
  else:
    for dev in devices:
      dev.fracture(max_points)
  return devices

class device:
  """
  A device object class
  Takes in the device's information, make the devices and
  stores the information for furthur do

  Args:
    typeLabel: the type label of the device
    function: the function that makes the device in gdspy
    parameters: a dictionary that keys are the parameter of the function
                and value is its value to make the device
    numcode_infor: a dictionary with layer and datatype infor {'layer': ,'datatype': }
    buffer_infor: a dictionary with layer and datatype infor {'layer': ,'datatype': }
    max_points(optional): Used by gdspy to set the maximum points used in a polygon. Notice, 199 used by default, 0 represents the maximum allowed.
    morse(optional): Default = False, set True for morse style numcode
    numcode_size(optional): the height in microns of the numeric codes to be placed by each device, it is by default 5 gdspy units (usually 5um)
    numcode_echSpacing(optional): the distance between symbols of the numcode.
    numcode_offset(optional): the distance from the device pattern to the numcode
    devBufferSize (optional): the distance between the bounding box of the device and the bufferBox edge. By default this is 40 units (usually 40um)
  Returns:
    An instance of a device with all the properties
  """

  def __init__(self, typeLabel, function, parameters,  
               numcode_infor, buffer_infor, max_points=199, morse = False,
               numcode_size = 5, numcode_etchSpacing = 2, numcode_offset = 40,
               devBufferSize = 40):

    self.devBufferSize = devBufferSize
    self.typeLabel = typeLabel
    self.device = function(**parameters)
    cell = gdspy.Cell(f'{typeLabel}', exclude_from_current=True)
    cell.add(self.device)
    offset=cell.get_bounding_box()
    if type(self.device)==list:
      for dev in self.device:
        dev.translate(-offset[0][0], -offset[0][1])
        dev.translate(self.devBufferSize, self.devBufferSize)
    else:
        self.device.translate(-offset[0][0], -offset[0][1])
        self.device.translate(self.devBufferSize, self.devBufferSize)
    self.device = fracturizer(self.device, max_points)
    self.parameters = parameters
    
    cell = gdspy.Cell(f'{typeLabel}', exclude_from_current=True)
    cell.add(self.device)
    self.bounds=cell.get_bounding_box()
    self.cell = gdspy.copy(cell) 
    self.id = ''
    self.x = 0
    self.y = 0
    self.numcode_size = numcode_size
    self.morse = morse
    self.numcode_etchSpacing = numcode_etchSpacing
    self.numcode_infor = numcode_infor
    self.numcode_offset = numcode_offset
    self.buffer_infor = buffer_infor
    self.dev_type = True

  def copy(self):
    return deepcopy(self)

  def set_origin(self, x, y):
    """Set the origin of the device (left-low corner), this function is used in the autopacking process

    Args:
      x: X coord of the device
      y: Y coord of the device
    """
    self.x = x
    self.y = y

  def autolayoutPostProcessor(self, numCode):
    """Creates room for numCode and the buffer for the packing process"""
    bounds = self.bounds
    if self.morse:
      numCode = morseNumCodeGenerator(numCode, self.numcode_size, self.numcode_etchSpacing)
      numCode = gdspy.boolean(numCode[0], numCode[1:], "or", layer=99)
      numCode = numCode.translate(bounds[0][0], bounds[1][1]+self.numcode_offset)
    else:
      numCode = str(numCode)
      numCode = gdspy.Text(numCode, self.numcode_size, 
      (bounds[0][0],bounds[1][1]+self.numcode_offset), layer=99)
    self.cell.add(numCode)
    bounds = self.cell.get_bounding_box()
    self.buffer = gdspy.Rectangle((bounds[0][0]-self.devBufferSize, bounds[0][1]-self.devBufferSize),
                                  (bounds[1][0]+self.devBufferSize, bounds[1][1]+self.devBufferSize), 
                                  **self.buffer_infor)
    self.cell.add(self.buffer)
    

  def set_numCode(self, numCode):
    self.cell.remove_polygons(lambda pts, layer, datatype:
                              layer == 99)
    bounds = self.bounds
    if self.morse:
      numCode = morseNumCodeGenerator(numCode, self.numcode_size, self.numcode_etchSpacing)
      numCode = gdspy.boolean(numCode[0], numCode[1:], "or", **self.numcode_infor)
      numCode = numCode.translate(bounds[0][0], bounds[1][1]+self.numcode_offset)
    else:
      numCode = str(numCode)
      numCode = gdspy.Text(numCode, self.numcode_size, 
      (bounds[0][0],bounds[1][1]+self.numcode_offset), **self.numcode_infor)
    self.cell.add(numCode)                              

  def get_buffer_bounding_box(self):
    """Get the buffer of the bounding box (the device include the buffer box)"""
    return self.buffer.get_bounding_box()

  def get_device_bounding_box(self):
    """Get the bounding box of just the device itself (no buffer included)"""
    return self.bounds


  
class region:  
  """
  A region object class
  Takes in the region's information, make the devices and
  stores the information for furthur do

  Args:
    typeLabel(str): the type label of the device
    function: the function that makes the device in gdspy
    parameters(dict): a dictionary that keys are the parameter of the function
                and value is its value to make the device
    buffer_infor(dict): a dictionary with layer and datatype infor {'layer': ,'datatype': }
    numcode_infor(optional): default = empty dictionary (no numcode); A dictionary with layer and datatype infor {'layer': ,'datatype': }
    max_points(optional): Used by gdspy to set the maximum points used in a polygon. Notice, 199 used by default, 0 represents the maximum allowed.
    morse(optional): Default = False, set True for morse style numcode
    numcode_size(optional): Default = 0 (no numcode), the height in microns of the numeric codes to be placed by each device
    numcode_echSpacing(optional): the distance between symbols of the numcode.
    numcode_offset(optional): the distance from the device pattern to the numcode
    buffer_size (optional): the distance between the bounding box of the region and the bufferBox edge. By default this is 40 units (usually 40um)
 
  Returns:
    An instance of a region with all the properties
  """
  def __init__(self, typeLabel, function, parameters, buffer_infor,
               buffer_size = 40, max_points = 199, morse = False,
               numcode_size = 0, numcode_etchSpacing = 0, numcode_offset = 0, numcode_infor = {}):


    self.typeLabel = typeLabel       
    if (numcode_size + numcode_offset) > buffer_size:
      raise ValueError('numcode_size + numcode_offset has to be smaller than buffer_size.')
    self.region = function(**parameters)
    self.region = fracturizer(self.region, max_points)
    self.parameters = parameters
    cell = gdspy.Cell(f'{typeLabel}', exclude_from_current=True)
    cell.add(self.region)
    self.cell = cell
    # for polygon in self.cell.get_polygonsets():
    #   polygon.fracture(max_points)    
    self.id = ''
    self.x = 0
    self.y = 0
    self.morse = morse
    self.buffer_size = buffer_size
    self.buffer_infor = buffer_infor
    self.numcode_size = numcode_size
    self.numcode_etchSpacing = numcode_etchSpacing
    self.numcode_infor = numcode_infor
    self.numcode_offset = numcode_offset
    self.references = []
    self.dev_type = False
    
    #Makes buffer
    bounds = self.cell.get_bounding_box()
    self.buffer = gdspy.Rectangle((bounds[0][0]+self.buffer_size, bounds[0][1]+self.buffer_size),
                                  (bounds[1][0]-self.buffer_size, bounds[1][1]-self.buffer_size), 
                                  **self.buffer_infor)
    self.cell.add(self.buffer)

    #Makes buffer
    bounds = self.cell.get_bounding_box()
    self.buffer = gdspy.Rectangle((bounds[0][0]+self.buffer_size, bounds[0][1]+self.buffer_size),
                                  (bounds[1][0]-self.buffer_size, bounds[1][1]-self.buffer_size), 
                                  **self.buffer_infor)
    self.cell.add(self.buffer)


  def copy(self):
    return deepcopy(self)

  def set_origin(self, x, y):
    """Set the origin of the region (left-low corner), this function is used in the autopacking process
    
    Args:
      x: X coord of the device
      y: Y coord of the device
    """
    self.x = x
    self.y = y
  
  def autolayoutPostProcessor(self, numCode = 0):
    """Creates room for numCode (if numcode_infor is filled)"""
    #Makes numcode
    if self.numcode_infor:
      bounds = self.buffer.get_bounding_box()
      if self.morse:
        numCode = morseNumCodeGenerator(numCode, self.numcode_size, self.numcode_etchSpacing)
        numCode = gdspy.boolean(numCode[0], numCode[1:], "or", layer=99)
        numCode = numCode.translate(bounds[0][0], bounds[1][1]+self.numcode_offset)
      else:
        numCode = str(numCode)
        numCode = gdspy.Text(numCode, self.numcode_size, 
        (bounds[0][0],bounds[1][1]+self.numcode_offset), layer=99)
      self.cell.add(numCode)
    
  def set_numCode(self, numCode):
    if self.numcode_infor:
      self.cell.remove_polygons(lambda pts, layer, datatype:
                                layer == 99)      
      bounds = self.buffer.get_bounding_box()
      if self.morse:
        numCode = morseNumCodeGenerator(numCode, self.numcode_size, self.numcode_etchSpacing)
        numCode = gdspy.boolean(numCode[0], numCode[1:], "or", **self.numcode_infor)
        numCode = numCode.translate(bounds[0][0], bounds[1][1]+self.numcode_offset)
      else:
        numCode = str(numCode)
        numCode = gdspy.Text(numCode, self.numcode_size, 
        (bounds[0][0],bounds[1][1]+self.numcode_offset), **self.numcode_infor)
        self.cell.add(numCode)
  def get_buffer_bounding_box(self):
    """Get the buffer bounding box of the region (will be less than region's actually size)"""
    return self.buffer.get_bounding_box()

  def get_region_bounding_box(self):
    """Get the bounding box of the region (actual size, see the make region tutorial for more information)"""
    return self.cell.get_bounding_box()
  
  def add(self, subObject):
    self.references.append(subObject)
  