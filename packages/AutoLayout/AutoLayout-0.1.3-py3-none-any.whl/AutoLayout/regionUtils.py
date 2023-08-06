import gdspy
from .layout import region

def make_rectRegion(width, height, layer, datatype):
  """This is a function that makes a rectangle region, which can be used to be the 
  function argument of the region class

  Args:
    width: width of the region
    height: height of the region
    layer:
    datatype:

  Return:
    a gdspy rectangle with the topleft concer is at the origion (0,0)
  """
  rect = gdspy.Rectangle((0,0),(width,height), layer = layer, datatype = datatype)
  
  return rect

def regionDivider(masterRegion, cut, typeLabel, buffer_infor, 
                  layer = 0, datatype = 0,
                  buffer_size = 40, max_points = 199,
                  numcode_size = 5, numcode_etchSpacing = 2, numcode_offset = 10, 
                  numcode_infor = {}):
  """Cuts the masterRegion into smaller sub region with n cuts on each side, 
  if cut = 2, there will be 4 subRegions
  if cut = 3, there will be 9 subRegions
  
  Args:
    masterRegion: the region being cut into subRegions
    cut: number of cut
    typeLabel: typeLabel of the subRegions
    buffer_infor: buffer infor of the subRegions
    layer: layer of the subRegions
    datatype: datatype of the subRegions
    max_points:
    numcode_size:
    numcode_etchSpacing:
    numcode_offset:
    numcode_infor:

  Returns:
    a list of subRegions that will fit onto the buffer of the masterRegion
  """
  bounds = masterRegion.get_buffer_bounding_box()
  w = bounds[1][0] - bounds[0][1]
  h = bounds[1][1] - bounds[0][1]
  width = int(w / cut)
  height = int(h / cut)
  multiple = (cut)**2 
  regions = []
  for i in range(multiple):
    aRegion = region(typeLabel = typeLabel, function = make_rectRegion, 
                        parameters = {'width':width,'height':height, 'layer':layer,'datatype':datatype}, 
                        buffer_infor = buffer_infor,
                        numcode_size = numcode_size, numcode_etchSpacing = numcode_etchSpacing, numcode_offset = numcode_offset,
                        numcode_infor = numcode_infor)
    regions.append(aRegion)
  return regions

def makeTicks(tickSize, tick_infor):
  h = min(tickSize)
  l = max(tickSize)
  tick = gdspy.Rectangle((0,-h/2),(l,h/2), **tick_infor)
  cell = gdspy.Cell('Tick', exclude_from_current=True)
  cell.add(tick)
  return cell

def regionTickMaker(region, dx, dy, tickSize = [1,10], rightSide = False, upSide = False):
  """Makes the tick mark for region

  Args:
    region: the region being marked
    dx: distance between the ticks on the x axis
    dy: distance between the ticks on the y axis
    tickSize: [length, height] of the tick mark
    rightSide: boolen, if True the tick mark will be generated on the right side
    upSide: boolen, if True the tick mark will be generated on the up side

  Returns:
    The region itself with ticks mark on it
  """
  region_dim = region.get_region_bounding_box()
  w = region_dim[1][0] - region_dim[0][1]
  h = region_dim[1][1] - region_dim[0][1]
  numX = int(w/dx)-1
  numY = int(h/dy)-1
  tick = makeTicks(tickSize, region.buffer_infor)

  #Makes ticks on the left side
  ticks=gdspy.CellArray(tick, 1, numY, (1,dy), origin=(0, dy))
  region.cell.add(ticks.get_polygonsets())
  #Makes ticks on the right side
  if rightSide:
    ticks=gdspy.CellArray(tick, 1, numY, (1,dy), origin=(w,h-dy), rotation=180)
    region.cell.add(ticks.get_polygonsets())

  #Makes ticks on the down side
  ticks=gdspy.CellArray(tick, 1, numX, (1,dx), origin=(w-dx,0), rotation=90)
  region.cell.add(ticks.get_polygonsets())
  #Makes ticks on the up side
  if upSide:
    ticks=gdspy.CellArray(tick, 1, numX, (1,dx), origin=(0+dx,h), rotation=270)
    region.cell.add(ticks.get_polygonsets())

