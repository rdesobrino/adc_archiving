import os

import argparse
from lib import gdalinfo, mapping, format
import shutil
import pprint

if  __name__ == "__main__":

    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description="""Produce metadata xml for ToolikGIS drone products""")
    parser.add_argument("-i", help=" : input csv file(s) to process")
    parser.add_argument("-o", help=" : Output metadata folder", default = os.path.join(cwd, "emls"))
    args = parser.parse_args()

    csv = args.i
    fields_dic = {}
    with open(csv, "r") as f:
        fields_list = f.readline().strip().split(',')
        for dataset in f.readlines():
            fields = dataset.strip().split(",")
            if fields[0] != "":
                fields_dic[fields[0]] = {}
                for i in range(len(fields)):
                    fields_dic[fields[0]][fields_list[i]] = fields[i]

    for dataset in fields_dic:
        fields_dic[dataset]["tifs"] = {}
        fprod = fields_dic[dataset]["fprod"].replace('"','')
        for file in os.listdir(fprod):
            file = os.path.join(fprod, file)
            if file.upper().endswith('.TIF'):
                fields_dic[dataset]["tifs"][file] = gdalinfo.get_gdal(file)

        with open(os.path.join(cwd, r"lib\ADC_template.xml"), "r") as template:
            template = template.read()
        with open(os.path.join(cwd, r"lib\ms_spatialRaster.txt"), "r") as ms_template:
            ms_template = ms_template.read()

        with open(os.path.join(cwd, r"lib\adc_eml_keys.csv"), "r") as f:
            keys = {}
            f.readline()
            for line in f.readlines():
                keys[line.split(",")[0]] = ""

        # with open(os.path.join(fprod, fields_dic[dataset]["fname"] + ".xml"), "w") as eml: ##TODO swap abck when out of testing
        with open(os.path.join(cwd, "emls", fields_dic[dataset]["fname"] + ".xml"), "w") as eml:
            print("Processing ", dataset)
            mapped = mapping.mapper(keys, fields_dic[dataset])
            for key in mapped.keys():
                template = template.replace(key, mapped[key])
                ms_template = ms_template.replace(key, mapped[key])
            start = template.find("</dataset>")
            eml.write(template[:start])
            if mapped["ms_desc"] != "":  ## TODO , implemet same logic for dem and rgb
                eml.write(ms_template)
            eml.write(template[start:])







