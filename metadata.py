import os

import argparse
from lib import gdalinfo, mapping

if  __name__ == "__main__":

    os.chdir(os.path.split(os.path.abspath(__file__))[0])
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description="""Produce metadata xml for ToolikGIS drone products""")
    parser.add_argument("-i", help=" : input csv file(s) to process")
    parser.add_argument("-o", help=" : Output metadata folder", default = os.path.join(cwd, "emls"))
    args = parser.parse_args()

    csv = args.i
    fields_dic = {} ## populate a dictionary with input fields for each dataset from csv
    with open(csv, "r") as f:
        fields_list = f.readline().strip().split(',')
        for dataset in f.readlines():
            fields = dataset.strip().split(",")
            if fields[0] != "":
                fields_dic[fields[0]] = {}
                for i in range(len(fields)):
                    fields_dic[fields[0]][fields_list[i]] = fields[i].strip()

    people_txt = r"C:\Users\rcdesobrino\Desktop\repos\ADC_archiving\adc_archiving\lib\people_projects.txt"  ## todo txt file does not savwe utf-8 encoding, messes up umlaut
    people_info = {}  # populate a dictionary with people and project information
    with open(people_txt, "r") as f:
        fields_list = f.readline().strip().split('\t')
        for dataset in f.readlines():
            fields = dataset.strip().split("\t")
            if fields[0] != "":
                fields[0] = fields[0].strip()
                people_info[fields[0]] = {}
                for i in range(len(fields)):
                    people_info[fields[0]][fields_list[i]] = fields[i].replace('"', "").strip()

    for dataset in fields_dic: ## populate a dictionary with metadata for each raster dataset
        fields_dic[dataset]["tifs"] = {}
        fprod = fields_dic[dataset]["fprod"].replace('"','')
        for file in os.listdir(fprod):
            file = os.path.join(fprod, file)
            if file.upper().endswith('.TIF'):
                fields_dic[dataset]["tifs"][file] = gdalinfo.get_gdal(file)  ## creates raster metadata file from gdal

        with open(os.path.join(cwd, r"lib\adc_template_2026.xml"), "r") as template: ## TODO change to pcik tmeplate based on year?
            # print("You are using the 2026 template")
            template = template.read()

        with open(os.path.join(cwd, r"lib\adc_eml_keys.csv"), "r") as f:
            keys = {}
            f.readline()
            for line in f.readlines():
                keys[line.split(",")[0]] = ""

        with open(os.path.join(cwd, "emls", fields_dic[dataset]["fname"] + ".xml"), "w") as eml:
            print("Processing ", dataset)
            mapped = mapping.mapper(keys, fields_dic[dataset], people_info) ## map keys to appropriate values
            for key in mapped.keys():  ## replace keywords with values
                template = template.replace(key, mapped[key])
            start = template.find("</title>")+len("</title>")
            eml.write(template[:start])
            eml.write(mapped["fteam"])

            nsf = template.find("</project")
            eml.write(template[start:nsf])
            if mapped["project_info"] != "":
                eml.write(mapped["project_info"])
            ## add spatialRaster objects for each tif
            data = template.find("</dataset>")
            eml.write(template[nsf:data])

            for raster in fields_dic[dataset]['tifs'].keys():
                with open(fields_dic[dataset]['tifs'][raster]['txt'], "r") as data_template:
                    data_template = data_template.read()
                for key in fields_dic[dataset]['tifs'][raster].keys():  ## replace keywords with values
                    if key != 'bobo':  ## embarrassing
                        data_template = data_template.replace(key, fields_dic[dataset]['tifs'][raster][key])
                eml.write(data_template)

            eml.write(template[data:])







