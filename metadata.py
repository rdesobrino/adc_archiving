import os

import argparse
from lib import gdalinfo, mapping, format
import shutil
import pprint

if  __name__ == "__main__":

    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description="""Produce metadata xml for ToolikGIS drone products""")
    parser.add_argument("-i", help=" : input csv file(s) to process") ## TODO do I really want to require an input csv??
    parser.add_argument("-o", help=" : Output metadata folder", default = os.path.join(cwd, "emls"))
    args = parser.parse_args()

    csv = args.i
    fields_dic = {} ## populate dictionary with input fields from user
    with open(csv, "r") as f:
        fields_list = f.readline().strip().split(',')
        for dataset in f.readlines():
            fields = dataset.strip().split(",")
            if fields[0] != "":
                fields_dic[fields[0]] = {}
                for i in range(len(fields)):
                    fields_dic[fields[0]][fields_list[i]] = fields[i].strip()

    projects = r"C:\Users\rcdesobrino\Desktop\repos\ADC_archiving\adc_archiving\lib\projects.txt"
    projects_dic = {} # populate dictionary with standard list of projects
    with open(projects, "r") as f:
        fields_list = f.readline().strip().split('\t')
        for dataset in f.readlines():
            fields = dataset.strip().split("\t")
            if fields[0] != "":
                fields[0]=fields[0].strip()
                projects_dic[fields[0]] = {}
                for i in range(len(fields)):
                    projects_dic[fields[0]][fields_list[i]] = fields[i].replace('"', "").strip()

    for dataset in fields_dic: ## populate dictionary with dataset-specific (raster) metadata
        fields_dic[dataset]["tifs"] = {}
        fprod = fields_dic[dataset]["fprod"].replace('"','')
        for file in os.listdir(fprod):
            file = os.path.join(fprod, file)
            if file.upper().endswith('.TIF'):
                fields_dic[dataset]["tifs"][file] = gdalinfo.get_gdal(file)  ## creates raster metadata file from gdal

        with open(os.path.join(cwd, r"lib\ADC_template.xml"), "r") as template:
            template = template.read()
        with open(os.path.join(cwd, r"lib\ms_spatialRaster.txt"), "r") as ms_template:
            ms_template = ms_template.read()

        with open(os.path.join(cwd, r"lib\adc_eml_keys.csv"), "r") as f:
            keys = {}
            f.readline()
            for line in f.readlines():
                keys[line.split(",")[0]] = ""

        # with open(os.path.join(fprod, fields_dic[dataset]["fname"] + ".xml"), "w") as eml: ##TODO swap back and forth between implementation. avoid accidentally overwrite manually-edited files.
        with open(os.path.join(cwd, "emls", fields_dic[dataset]["fname"] + ".xml"), "w") as eml:
            print("Processing ", dataset)
            mapped = mapping.mapper(keys, fields_dic[dataset], projects_dic) ## map keys to appropriate values
            for key in mapped.keys():  ## replace keywords with values
                template = template.replace(key, mapped[key])
                ms_template = ms_template.replace(key, mapped[key])
            start = template.find("</creator>")+len("</creator>")
            eml.write(template[:start])
            if mapped["fteam"] != "":
                eml.write(mapped["fteam"])

            nsf = template.find("</project")
            eml.write(template[start:nsf])
            if mapped["project_info"] != "":
                eml.write(mapped["project_info"])

            multi = template.find("</dataset>")
            eml.write(template[nsf:multi])  ## write new file
            if mapped["ms_desc"] != "":  ## TODO , implement same logic for rgb and dem, how many cases?
                eml.write(ms_template)
            eml.write(template[multi:])







