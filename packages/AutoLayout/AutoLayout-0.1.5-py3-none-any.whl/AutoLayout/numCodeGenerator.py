#Num Code Generator is used to generate the GDS of the num Codes
import gdspy
import math


def morseNumCodeGenerator(num, size, etchSpacing):
    """
    This morse code generator is specifically created for single mask processes that have an etch release 
    making writing pure numbers down impossible.
    The vertical bars indicate 10, the horizontal bars indicate 100, and the holes indicate 1.
    So code -|... is 114
    
    Args:
        num (int):
        size (int): Width of Bars and diameter of holes:
        etchSpacing: Spacing between elements to allow for etching tolerance:
    
    Returns:
        A gdspy polygonset with the encoded number code being returned. Its origin is at 0,0

    """
    thousands=math.floor(num/1000)
    num = num - thousands * 1000
    hundreds = math.floor(num / 100)
    num = num - hundreds * 100
    tens = math.floor(num / 10)
    singles = num - tens * 10
    numCode=[]
    length=size*6
    width=size
    k=0
    voff=0
    o=0
    hoff=0
    for i in range(thousands):
        numCode=numCode+[gdspy.Round((o+length/2, length/2), length/2)]
        o = o + (length + 2 * etchSpacing)

    for i in range(hundreds):
        k=k+i

        if i%3 == 0 :

            voff=width/2
            numCode = numCode + [gdspy.Rectangle((o, voff - width / 2), (length + o, voff + width / 2))]
        elif i%3 == 1:

            voff=length/2
            numCode = numCode + [gdspy.Rectangle((o, voff - width / 2), (length + o, voff + width / 2))]
        else:

            voff=length-width/2
            numCode = numCode + [gdspy.Rectangle((o, voff - width / 2), (length + o, voff + width / 2))]
            o = o + (length + 2 * etchSpacing)
    if hundreds%3!=0:
        o = o + (length + 2 * etchSpacing)
    for i in range(tens):
        k=k+i

        numCode=numCode+[gdspy.Rectangle((o,0), (o+width,length))]
        o = o + (width + 2 * etchSpacing)
    oh=o
    voff=length*.85
    for i in range(singles):
        if i==5:
            o=oh
            voff=length*.15
        k=k+i

        numCode=numCode+[gdspy.Round((o+size/2, voff), size/2)]
        o = o + (width + 2 * etchSpacing)

    return numCode



