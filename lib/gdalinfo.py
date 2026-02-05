from osgeo import gdal
import os

os.chdir(os.path.split(os.path.abspath(__file__))[0])
cwd = os.path.join(os.getcwd(), "info")
gdal.UseExceptions()

def dms_dd(coords): ## transforms coordinates to decimal degrees from dms, as output from gdal
    nw = coords.split(",")
    for i in range(len(nw)):
        d = nw[i].split("d")[0].strip()
        m = nw[i].split("d")[1].split("'")[0].strip()
        s = nw[i].split("d")[1].split("'")[1].split('"')[0].strip()
        nw[i]=round(float(d)+(float(m)/60)+(float(s)/3600), 6)
    return nw

def bobo(info):
    bb = []
    for corner in ["Upper Left  (  ", "Lower Right (  "]:
        search = info[info.find(corner) + len(corner):].split(")")[1]
        bb.append(dms_dd(search[2:]))
    return bb

def centroid(info):
    center = info[info.find("Origin = (") + len("Origin = ("):].split(")")[0]
    return center

def get_hcs(info):
    hcs = info[info.find("PROJCRS[") + len("PROJCRS["):].split('"')[1] ##TODO change user-read format?
    if hcs == "NAD83(2011) / UTM zone 6N":
        return "NAD_1983_UTM_Zone_6N"
    elif hcs == "NAD83(2011) / UTM zone 5N":
        return "NAD_1983_UTM_Zone_5N"
    print("Change HCS to comply with https://eml.ecoinformatics.org/schema/eml-spatialreference_xsd#SpatialReferenceType_horizCoordSysName")
    return hcs

def get_res(info):
    res = info[info.find("Pixel Size = (") + len("Pixel Size = ("):].split(',')[0]
    return round(float(res), 3) ##

def get_bands(info):
    bands = 0
    for i in range(1, info[info.find("Band"):].count("Band")+1):
        bands += 1
    return bands

def get_rows(info):
    rows = info[info.find("Size is ") + len("Size is "):].split(',')[0]
    return rows

def get_cols(info):
    cols = info[info.find("Size is ") + len("Size is "):].split(',')[0]
    return cols

def get_gdal(tif_path):  ##
    name = os.path.basename(tif_path).split(".")[0]
    with open(os.path.join(cwd, name + "_gdalinfo.txt"), "w") as text:
        info = gdal.Info(tif_path)  ## awrsom,e now save as txt and then pull bounding box etc
        text.write(info)
    data = {}
    data["hcs"] = get_hcs(info)
    data["res"] = get_res(info)
    data["bands"] = get_bands(info)  ## TODO: returning 3 for multispec
    data["rows"] = get_rows(info)
    data["cols"] = get_cols(info)
    data["bobo"] = bobo(info)
    data["center"] = centroid(info)
    return data

