from copy import deepcopy
from .layout import device

class expVar:
  """
  ExpVar simply holds a list, this is done to elegantly denote the variable being used as an autolayout experimental variable. This is because some layouts might use lists as input variables

  Args:
    parmlist: A numpy or python list
  """
  def __init__(self, parmList):
    self.varList=parmList
  
  def getVarList(self):
    """getVarList, is a getter that returns the expSet list

    Returns:
      The experimental variable list
    """
    return self.varList
  
  def setVarList(self, newVarList):
    """Takes a list and overwrites the old experimental variable list

    Args:
      newVarList: The new experimental variable list to replace the current expVar varList.

    """
    self.varList=newVarList

class experimentalSetGenerator:
  """
  Instantiates an experimental set. The goal of this class is to create a set of lists with different permutations, according to design of experiments rules.

  Args:
    parameters: A dictionary containing the total list of variables required for an associated deviceGenerator. The experimental variables are stored to be used by the different types of generator functions available in this class.
  
  """
  def __init__(self, parameters):

    self.numLayer=None
    self.parameters = parameters
    for v in self.parameters.values():
      if type(v)==expVar:
        self.numLayer=len(v.getVarList())
        break    
    if self.numLayer==None:
      raise ValueError(f'No experimental Variable found in the parameter list, please add expVar variable to the parameter list to continue')
    self.usePara = {}
    self.unUsePara = {}
    for k, v in self.parameters.items():
      if type(v) == expVar: 
        #count = len(v.getVarList())
        #if count != self.numLayer:
        #  raise ValueError(f'This {k} is not having the same numLayer with others!')
        self.usePara[k] = v.getVarList()
      else:
        self.unUsePara[k] = v

  def specifiedCombinations(self):
    """
    This takes the parameters stored by the experimentalSet, and generates an experimental set of input lists with only the specified combinations used. 
    FOR THIS ALL THE EXPERIMENTAL VARIABLES MUST HAVE THE SAME LENGTH!. If we have two exp var (1,2) and (3,4), then only the lists [1,3] and [2,4] will be produced. Hence the specified combinations.

    Returns:
      l (list): A list of dictionaries, the dictionaries returned can be inputted directly into the device generator and will produce a device. Essentially, the expVars are converted to individual dictionarys.

    Raises:
      ValueError: If the number of variables in all expVars is not the same, this code will raise a value error, and message.
    """
    l = []
    for i in range(self.numLayer):
      d = {}
      for key in self.parameters:
        if key in self.usePara:
            if len(self.usePara[key])!=self.numLayer:
              raise ValueError(f'The variable: \"{key}\" is not the same length as the others!')
            d[key] = self.usePara[key][i]
        else:
          d[key] = self.unUsePara[key]
      l.append(d)
    
    return l
  
  def factorizer(self, aList, changePosition):
    """A recursive function, that will generate a full factorial set of lists for each experimental variable. This is used internally by the factorial function.

    Args:
      alist: This takes in the list to be factorized
      changePosition: This is used as the indicator during factorial operations
    """
    self.usedValueList
    self.paraValueList

    for item in aList:
      self.paraValueList.append(item)
    if changePosition < 0:
      pass
    else:
      li = []
      for item in aList:
        for num in self.usedValueList[changePosition]:
          l = deepcopy(item)
          l[changePosition] = num
          li.append(l)
      changePosition -= 1
      for item in aList:
        self.factorizer(li, changePosition)    

  def factorial(self):
    """Generates a full factorial set for each of the experimental variables.

    Returns:
      l_return (list): A list of dictionaries, each dictionary does not have any expVars in it but just one of the values from the expVar. The full set holds the combinatorically generated set of expVar values.

    """
    self.usedValueList = [l for l in self.usePara.values()]
    self.paraValueList = []
    tempList = []
    l = [aList[0] for aList in self.usedValueList[:-1]]
    for num in self.usedValueList[-1]:
      li = deepcopy(l)
      li.append(num)
      tempList.append(li)
    changePosition = len(tempList[0]) - 1
    self.factorizer(tempList, changePosition)
    l = []
    for so in self.paraValueList:
      so = tuple(so)
      l.append(so)
    self.paraValueList = set(l)
    keys = [key for key in self.usePara.keys()]
    l_return = []
    for value in self.paraValueList:
      d = {}
      for key in self.parameters:
        if key in self.usePara:
          d[key] = value[keys.index(key)]
        else:
          d[key] = self.unUsePara[key]
      l_return.append(d)
    
    return l_return


class expSetGenerator:
  """
  This init function for the experimental set generator. This class takes in a list with experimental variables and returns a list of devices with the appropriate set generation of devices done.

  Args:
    typeLabel: A string holding the user interpretable name of this type of device, eg. "Cantilever" or "Membrane", etc.
    function: This is the device generator function
    parameters: This is a dictionary holding the expVars to be used to generate the list of devices. Note this dictonary can be inputted into the device Generator function via **parameters**
    numcode_infor: This is a dictionary with the layer information used for the numeric codes placed by each device (this is used to write the unique name of the device beside it, and should be visible in the final fab!)
    buffer_infor: This is a dictionary with the layer information used for the buffer placed around each device, this is usually not included in the fabrication, so a non-fabrication layer should be used.
    max_points: Used by gdspy to set the maximum points used in a polygon. Notice, 199 used by default, 0 represents the maximum allowed.
    numcode_size: This is the height in microns of the numeric codes to be placed by each device, it is by default 5 gdspy units (usually 5um)
    numcode_etchSpacing: This is the distance between symbols of the numcode.
    numcode_offset: This is the distance from the device pattern to the numcode
    devBufferSize: This is the distance between the bounding box of the device and the bufferBox edge. By default this is 40 units (usually 40um)
    mandatory: This is the number of devices that must be placed into the layout otherwise the packer will return an error
    optional: This is the number of optional devices that will be packed if there is enough room left on the die after all the mandatory devices are packed.      
  """
  def __init__(self, typeLabel, mandatory, optional, function, parameters,  
               numcode_infor, buffer_infor, max_points=199,
               numcode_size = 5, numcode_etchSpacing = 2, numcode_offset = 40,
               devBufferSize = 40):

    self.typeLabel=typeLabel
    self.function=function
    self.parameters=parameters
    self.numcode_infor=numcode_infor
    self.buffer_infor=buffer_infor
    self.max_points=max_points
    self.numcode_size=numcode_size
    self.numcode_etchSpacing=numcode_etchSpacing
    self.numcode_offset=numcode_offset
    self.devBufferSize=devBufferSize
    self.mandatory=mandatory
    self.optional=optional
    self.experiment=experimentalSetGenerator(self.parameters)

  def specifiedCombinations(self):
    """This takes the expVars in the input params, and generates an experimental set of input lists with only the specified combinations used. 
    FOR THIS ALL THE EXPERIMENTAL VARIABLES MUST HAVE THE SAME LENGTH!. If we have two expVar a=(1,2), b=(3,4) given as parameters for the experimental set. 
    Then a list of devices d with inputs (a,b) will be returned as follows [d(1,3),d(2,4)]

    Returns:
      A list of dictionaries, the dictionaries returned can be inputted directly into the device generator and will produce a device. Essentially, the expVars are converted to individual dictionarys.

    Raises:
      ValueError: If the number of variables in all expVars is not the same, this code will raise a value error, and message.

    """
    expSetVars=self.experiment.specifiedCombinations()
    expDevSet=[]
    for parm in expSetVars:
      dev=device(self.typeLabel, self.function, parm, self. numcode_infor, self.buffer_infor, 
        self.max_points, self.numcode_size, self.numcode_etchSpacing, self.numcode_offset, self.devBufferSize)
      expDevSet.append((dev, self.mandatory, self.optional))
    return expDevSet

  def factorial(self):  
    """Generates a full factorial list of devices based on the expVars given as input parameters.

    Returns:
      A list of devices where every combination of expVars is used to created the devices. eg. If we have two expVar a=(1,2), b=(3,4) given as parameters for the experimental set. 
      Then a list of devices d with inputs (a,b) will be returned as follows [d(1,3), d(1,4), d(2,3),d(2,4)]

    """

    expSetVars=self.experiment.factorial()
    expDevSet=[]
    for parm in expSetVars:
      dev=device(self.typeLabel, self.function, parm, self. numcode_infor, self.buffer_infor, 
        self.max_points, self.numcode_size, self.numcode_etchSpacing, self.numcode_offset, self.devBufferSize)
      expDevSet.append((dev, self.mandatory, self.optional))
    return expDevSet


      

