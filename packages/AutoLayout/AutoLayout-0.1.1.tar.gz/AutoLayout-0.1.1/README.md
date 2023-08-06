# AutoLayout


## About


AutoLayout is an automated layout generator software for the popular gdspy library​.
It does the packing process in a hierarchal way
![Hierarchy packing](./pics/hierarchy.png)

## Features:

* Automated fully optimized layout and device packing
* Full-Factorial Automatic Device Set Generation
* Device tracking on GDS Layout
* Device tracking via excel sheet

## Installation


Use pypi:
```bash
pip install AutoLayout
```

## Basic Usage

* First we need to create a **device generator**. 

The device generator generates a set of gdspy polygons that correspond to a particular device being laid out.  
As an example, lets consider three different example devices: RectCircle, Hole, and Flag.

![RectDev](./pics/rectDev.PNG)
![HoleDev](./pics/holeDev.PNG)
![FlagDev](./pics/flagDev.PNG)

Here are the device generation functions for the three devices shown above:
```python
def make_RectCircle(width, height):
    """Make a Rectangle with a circle inside"""
    if width > height: 
        radius = height / 2
    else:
        radius = width / 2
    rect = gdspy.Rectangle((0,0),(width,height))
    cir = gdspy.Round((width/2,height/2), radius, tolerance = 0.01)
    textSize = int(min(width,height) / 10)
    text = gdspy.Text(f'W:{width} H:{height}', textSize, (0,height))
    return [cir,rect,text]

def make_hole(outside, inside):
    """Make a square with a hole inside"""
    if outside % 2 != 1:
        raise ValueError('outside has to be an odd number.')
    if outside < inside:
        raise ValueError('outside has to be larger than inside')
    in_origin = int(outside / 2)
    cutout = gdspy.Polygon([(0, 0), (outside, 0), (outside, outside), (0, outside), 
                            (0, 0), (in_origin, in_origin), (in_origin, in_origin + inside), 
                            (in_origin + inside, in_origin + inside), 
                            (in_origin + inside, inside), (in_origin, in_origin)])
    return cutout 

def make_flag():
    """Make a device that looks like a flag"""
    p1 = gdspy.Rectangle((-300, -300), (300, 300))
    p2 = gdspy.Rectangle((-500, -300), (-300, 300))
    p3 = gdspy.Rectangle((500, -300), (300, 300))
    p4 = gdspy.Round((0, 0), 250, number_of_points=6)
    return [p1,p2,p3,p4]

```
Once the **device generator** functions have been written, we are ready to create our **device** objects:

```python
from AutoLayout.layout import device


rect_circle = device(typeLabel = 'Rect_Circle', 
                     function = make_RectCircle,
                     parameters = {'width':500, 'height':200},
                     numcode_infor = {'layer':5, 'datatype':5}, numcode_size=30,
                     buffer_infor = {'layer':0, 'datatype':0})
                     
flag = device(typeLabel = 'Flag', 
              function = make_flag,
              parameters = {},
              numcode_infor = {'layer':5, 'datatype':5}, numcode_size=30,
              buffer_infor = {'layer':0, 'datatype':0})

hole = device(typeLabel = 'Hole', 
             function = make_hole,
             parameters = {'outside': 411, 'inside': 111}, numcode_size=30,
             numcode_infor = {'layer':5, 'datatype':5},
             buffer_infor = {'layer':0, 'datatype':0})               
```

Note: A buffer with be automatically added (you can adjust the buffer's size or set it 0 if you want). This buffer places space around the outer bounds of your device so devices are not touching each other. Naturally, the buffer could be added manually if so desired in the device generator function. For example, in the device below, the actual device is the yellow star with red background, the buffer is added around the whole device (star + background) so neighboring devices done touch.

![Device](./pics/device.png)

Once you have the devices you would like to pack, we now need to specify the regions they will be packed into. As an example if you have only one region it may be the size of the entire die, or we can subdivide the die into subregions to make it easier to find different devices. These regions are also heirarchical, so one can have regions with subregions, and subsubregions if desired. 

* Below we show how to create **region** objects

```python
from AutoLayout.layout import region
from AutoLayout import regionUtils

#Here we use the make_rectRegion fucntion in regionUtils library
masterRegion = region(typeLabel='Dice', 
                      function=regionUtils.make_rectRegion,
                      parameters={'width':8080, 'height':8080, 'layer':3, 'datatype':3},
                      buffer_infor={'layer':13, 'datatype':13})

#If wanted, we can create subRegion using regionDivider in regionUtils, 
# here we want to divide the Master Region into 4 subRegions, so the number of cut is 2
subRegions = regionUtils.regionDivider(masterRegion=masterRegion,
                                      cut =2, 
                                      typeLabel="Sub Region",
                                      numcode_infor = {'layer':5, 'datatype':5}, numcode_size=15,
                                      buffer_infor={'layer':0, 'datatype':0},
                                      layer=1,
                                      datatype=1)
```


*Note: for the **region**, the buffer will cut within the region, thus actually packing area will be smaller than the region area. To make it easier for you to divide the masterRegion into subRegions, we have included an automatic regionDivider function in the regionUtils library.

![Region](./pics/region.png)

Now that we have the devices and the packing regions we are ready to pack our layout.

* Here we all the autopacker function.

```python
from AutoLayout.autopacker import autopacker
packer = autopacker()

#device_list = [(device, mandatory times, optional times)]
device_list = [(rect_circle,10,100),(hole,20,100),(flag,10,100)]
packer.set_device(device_list, randomOptional=True)

#region_list = [[MasterRegion], [subRegions], [sub_sub_regions],...]
regions_list = [[masterRegion], subRegions]
packer.set_region(regions_list)

packer.pack()
```
The process of lay out is as follows:

In the first line, we create a packer object.  

In the second line, we create a device_list. This device_list will contains a list of tuples (device, mandatory times, optional times) where:  
_ device:          is the device object previously created (in our case the rect_circle, hole, and flag devices created earlier in the notebook)
_ mandatory times: are the number of times a device must appear on the layout otherwise the packer will declare the packing attempt a failure.  
_ optional times:  after all the mandatory devices are packed, if there is leftover room, the packer will add optional devices to the layout until there is no more room.  

In the third line, we set the device for the packer. **The optional list will be prioritize based on the order in the device_list, set randomOptional = True will shuffle the optional devices.**

In the fourth line, we create a regions_list. This regions_list contains a list of list regions. Notice that the subregions are packed into the regions, thus each set of subregions must be smaller than the set above it!
For example, the MasterRegion is an object, so we have to put it into a bracket; whereas for the subRegions, it already a list created by the 'regionUtils.regionDivider' function.

In the fifth line, we initialize the packer, by loading the regions into it.   
In the last line, we execute the pack. The function does not return anything, however, at this point the packer object now has a full layout stored in it. To save this layout to a gds file for viewing or use we run the to_layout command.

* Generating the layout:

```python
#packer.to_layout(filename)
packer.to_layout("autopackerDemo")
```

The result of the packing is:

![LayoutDemo](./pics/autopackerDemo.PNG)

**Note: every device and every region and subregion has a buffer!**  
In the example below, the Master Region is divided into 9 subRegions, and the devices are first packed into the subRegions, then the subRegions are packed into the regions, and finally, the regions are packed into the master region. This is a very simple example with mostly identical devices. We call this the manual mode since every device variation is manually specified. In the next example is a demonstration of fully automatic full-factorial and other combinatorial experimental set layout and generation.

![Manual Layout](./pics/manual.png)

Another great feature of this library is that documentation is automatically generated for the entire experimental set. This is done by writing the entire set of generation parameters, and the devices locations on the layout to an excel file. Additionally, unique codes are assigned to each device that may be traced via this excel file.

* Automated device documentation

AutoLayout package provides an excel file to track the device generation conditions and layout location. This is done as shown here:

```python
packer.to_excel('filename')
```

![excel](./pics/excel.png)

In the excel file above, each sheet is dedicated for one type of device. In one sheet, it has:  
_ Device label: the label of the device.  
_ Dev ID: the location in a hierarchical way for example (1,3,3) means the device will be in the first MasterRegion (always 1), the third subRegion and the third device of that subRegion.  
_ Local location: the location with respect to the bottom left concer of the region in which it is packed.  
Then the following collumns are the parameters of the device. (The parameters that are passed into the function that makes the device).  

* Automatic Device Tracking on the gds file (on the chip)

Using the information along with a GDS viewer like KLayout we can quickly find a specific device in a region by looking through the GDS Hierarchy as shown here:

![GDS Hierachy](./pics/gdsHierachy.png)

**On the chip, the numeric codes are autogenerated. The default setting is alphanumeric. These number are associated with their region to prevents very long codes. Another provided option is a morse style for single mask etching layouts (alphanumeric would be unreadable in that case).**

Below is an example of a device with the automatically generated unique numeric code.  
Note that if you provide the numcode_infor argument for the region object of the AutoLayout, the region will have a unique numcode as well.

![device with numcode](./pics/device_with_num.png)

Finally, region tick marks can be automatically generated via the regionsUtils library (you can set the layer and datatype of the region tick marker). These are provided as aids to help find device using the excel map. 

Region tickmarks.

![Region tick](./pics/regionTickmark.png)

* Region tickmarkers example

An example of region tickmarkers using gdspy library

```python
#Create a region
from AutoLayout.device import region
from AutoLayout.regionUtils import regionTickMaker, make_rectRegion
dieParms={
"width":1000,
"height":3000,
"layer":1,
"datatype":1
}
die= region(typeLabel="die", 
                  function=make_rectRegion, 
                  parameters=dieParms,
                  buffer_size=40,
                  buffer_infor={'layer':2,'datatype':2})

#regionTickMaker(region, distance between ticks in the bottom, distance between ticks in the leftside)
regionTickMaker(die, 10, 10, rightSide=True, upSide = True)

#Use gdsy to display the tickmarks
import gdspy
lib = gdspy.GdsLibrary('lib')
lib.add(die.cell)
lib.write_gds('RegionTickMakerDemo.gds')
```
Note that the tickmark will be in the same layer and datatype with the buffer information.

Here we can see the buffer are inside the region and the tickmarks are on the side of the reigon
![regionTick](./pics/regionTick.PNG)

* Experimental Variable

Here have an example of how an experimental set can be automatically generated. This will result in many devices with different variables of one type label.   
For example, if the device is a rectangle, we have two pamameter: width and height. We can try to make many rectangle with different widths and different heights. This is accomplished by using the expVar, and expSetGenerator modules as shown here. In this example we have a scdDevice, which is a device generator function for a simple cantilever device. 

```python
#import expVariable
from AutoLayout.expSet import expVar, expSetGenerator

#Create a parameter for the function that makes the device
scdParms={"beamLength":expVar([30, 50, 75, 100, 150]),
"beamWidth":expVar([10,20, 30, 50]),
"anchorLength":50,
"anchorWidth":50,
"etchWindowWidth":20,
"filletR": expVar([2,4,10]), 
"cantileverInfo":ld_waferLayer,
"etchInfo":ld_etchWindow}

#Now we create one type of devices with different parameters
scdDevExperiment=expSetGenerator(typeLabel = 'Simple Cantilever',
                     mandatory=1, optional=10 ,
                     function = scd.cantileverDeviceGenerator,
                     parameters = scdParms,
                     numcode_infor = ld_numCodeInfo,
                     buffer_infor = ld_regionOutline)

scdDevs=scdDevExperiment.factorial()
```
Note: in the scdDev above, we have set the beamLength, beamWidth, and filletR to be the experimental variables while the rest are standard variables. In the last line, we generate a full factorial set of those experimental variables. This list of automatically generated devices can then be loaded directly into the autopacker as shown here:
```python
from AutoLayout.autopacker import autopacker
from AutoLayout.layout import region
import AutoLayout.regionUltils as regionUtils

#Here we already set the mandatory and optional times above, so we do not have to do it manually again
device_list = scdDevs
packer.set_device(device_list)

#Make the regions
dieParms={
"width":10000,
"height":10000,
"layer":3,
"datatype":3
}
die=layout.region(typeLabel="die", function=regionUtils.make_rectRegion, parameters=dieParms, buffer_size=0 ,buffer_infor=ld_waferLayer)

regions=regionUtils.regionDivider(die, 3, "Region", buffer_infor=ld_regionOutline, numcode_infor=ld_numCodeInfo)

#We can make a manual region and add it to the region_list
lregionParms={
"width": 10000,
"height":int(10000/3),
"layer":ld_regionOutline["layer"],
"datatype":ld_regionOutline["datatype"]
}
longRegion=layout.region(typeLabel="Long Region", function=regionUtils.make_rectRegion, parameters=lregionParms, buffer_size=40 ,buffer_infor=ld_regionOutline)
regions=regions[0:6]+[longRegion]

#Now we set the region for the packer
regions_list=[[die], regions]
packer.set_regions(regions_list)

packer.pack()
packer.to_layout("AutoExperimentDemo")
```

To add multiple kinds of devices to the layout simply take the list of devices generated and perform concatenations so all devices generated are in one list, and then load into autopacker. An example of such a layout with around 400 devices and 50 variations is shown here. 

![Autoexperimental Layout](./pics/autoexperimental.png)

The exciting thing is that the code required to generate this optimally packed layout is simple, short, and much more densely packed than a typical layout. This allows for rapid adaptation of layouts for new studies along with high throughput fabrication of devices without wasting an enormous amount of time on repacking layouts. 

