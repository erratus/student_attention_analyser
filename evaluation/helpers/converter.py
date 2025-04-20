# -*- coding: utf-8 -*-

from xml.dom import minidom
import os
import glob

# Look-Up Table 
lut = {
    "hand_up":0
}

# Define XML file location
xml_folder = 'D:/misc/langs/python/attendance sys/dataset/xml_labels'  
output_folder = 'D:/misc/langs/python/attendance sys/dataset/yolo_labels'  
os.makedirs(output_folder, exist_ok=True)  

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_xml2yolo(lut):
    for fname in glob.glob(os.path.join(xml_folder, "*.xml")):
        
        xmldoc = minidom.parse(fname)
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(fname))[0] + '.txt')

        with open(output_file, "w") as f:
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int(size.getElementsByTagName('width')[0].firstChild.data)
            height = int(size.getElementsByTagName('height')[0].firstChild.data)

            for item in itemlist:
                # Get class label
                classid = item.getElementsByTagName('name')[0].firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "-1"
                    print(f"Warning: label '{classid}' not in look-up table")

                # Get bounding box coordinates
                xmin = float(item.getElementsByTagName('bndbox')[0].getElementsByTagName('xmin')[0].firstChild.data)
                ymin = float(item.getElementsByTagName('bndbox')[0].getElementsByTagName('ymin')[0].firstChild.data)
                xmax = float(item.getElementsByTagName('bndbox')[0].getElementsByTagName('xmax')[0].firstChild.data)
                ymax = float(item.getElementsByTagName('bndbox')[0].getElementsByTagName('ymax')[0].firstChild.data)
                b = (xmin, xmax, ymin, ymax)
                bb = convert_coordinates((width, height), b)

                # Write to YOLO format file
                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print(f"Converted {fname} to {output_file}")

def main():
    convert_xml2yolo(lut)

if __name__ == '__main__':
    main()
