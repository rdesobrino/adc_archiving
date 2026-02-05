from lib import format
import os
import math

def mapper(keys, data_fields, projects):
    for key in keys.keys():  ## handles all key-matching that does not require additional formatting
        if key in data_fields:
            keys[key] = data_fields[key]
    #keys["s_site"] = data_fields["s_site"] +"," ## actually, then rogue comma. if statement or just delete
    keys["l_area"] = ", " + data_fields["l_area"]
    keys["date_desc"] = format.date_descr(data_fields["date"])
    keys["f_start"] = data_fields["f_start"] + ":00-09:00"
    keys["f_stop"] = data_fields["f_stop"] + ":00-09:00"

    for attr_id in ["red_id", "green_id", "blue_id", "dsm_id", "ms_id_1", "ms_id_2", "ms_id_3", "ms_id_4", "ms_id_5", "ms_id_6"]:
        keys[attr_id] = format.attr_id()

    ## raster specific metadata
    for tif in data_fields["tifs"]:
        bobo = data_fields["tifs"][tif]["bobo"] ## only need one bounding box, RGB and MS will be slightly different but ah well
        keys["h_crs"] = data_fields["tifs"][tif]["hcs"] ## assumes all rasters are in same crs for description, but each gets written separately at data-level
        if data_fields["tifs"][tif]["bands"] == 1:
            keys["dem_name"] = os.path.basename(tif)
            keys["dem_res"] = str(data_fields["tifs"][tif]["res"])
            keys["dem_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["dem_cols"] = str(data_fields["tifs"][tif]["cols"])
        elif data_fields["tifs"][tif]["bands"] == 3:
            keys["rgb_name"] = os.path.basename(tif)
            keys["rgb_res"] = str(data_fields["tifs"][tif]["res"])
            keys["rgb_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["rgb_cols"] = str(data_fields["tifs"][tif]["cols"])
        elif data_fields["tifs"][tif]["bands"] >= 3: ## anything over 3 bands should be multispectral
            keys["ms_name"] = os.path.basename(tif)  ## TODO: if not MX camera, metadata different
            keys["ms_px_desc"] = ", multispectral orthomosaic: " + str(data_fields["tifs"][tif]["res"]) + "m"
            keys["ms_res"]= str(data_fields["tifs"][tif]["res"])
            keys["ms_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["ms_cols"] = str(data_fields["tifs"][tif]["cols"])
            if data_fields["tifs"][tif]["bands"] != 6:
                print("Double-check the raster bands. This rasters has ", data_fields["tifs"][tif]["bands"], "bands." )

    if data_fields["ms_v"]: ## only if a multispectral camera was used
        keys["ms_desc"] =  ", and multispectral orthomosaic"
        keys["ms_v"] =  "and " + data_fields["ms_v"] + " multispectral sensor"
        keys["ms_meth"] = "and an " + data_fields["ms_v"] + " was flown nadir with calibration photos taken at the start of each flight, and/or when lighting conditions changed"
    if data_fields["klau"]: ## only if Klau was used
        keys["klau_desc"] = "Image coordinates were post-processed using KlauPPK hardware and software. "
        keys["klau_meth"] = "Camera coordinates were recorded at the time of image capture using an external PPK antenna (KlauPPK) post-processed using KlauPPK Version 7.22.1 (Klau Geomatics)."
        center = [float(x) for x in data_fields["tifs"][tif]["center"].split(",")]
        bases = {"TLK2": ["the TLK2 CORS station", [394474.177, 7615113.754]], "Galbraith Rock": ["a mobile base station established on a rock", [399245.867,7601064.231]],
                 "AB45": ["the AB45 CORS station", [424362.468, 7628807.999]], "AB33": ["the AB33 CORS station", [621978.3273, 7462139.122]],
                 "Ice Cut": ["a mobile base station established on a rock", [426768.062,7660653.426]],
                 "Sagwon": ["a mobile base station established on a rock", [433486.0535, 7702537.337]], "Happy Valley": ["a mobile base station established on a rock", [427019.806,7672785.259]]}
        if "UTM" in keys["h_crs"]:
            dist = round((math.dist(center, bases[data_fields["klau_base"]][1])) / 1000, 2)
            keys["klau_meth"] = ("Camera coordinates were recorded at the time of image capture using an external PPK antenna (KlauPPK) for each image captured and "
                                 "post-processed using " + bases[data_fields["klau_base"]][0] + " " + str(dist) + " kilometers away with KlauPPK Version 7.22.1 (Klau Geomatics).")
            if dist > 20:
                print("The reported distance between the flight and corresponding base is more than 20km")

    keys["webo"] = "-" + str(bobo[0][0])
    keys["ebo"] = "-" + str(bobo[1][0])
    keys["nobo"] = str(bobo[0][1])
    keys["sobo"] = str(bobo[1][1])
    keys["hyph_date"] = format.hyphenate_date(data_fields["date"])
    keys["rgb_meth"] = data_fields["rgb_v"] + " on a gimbal"
    if data_fields["wx"]:
        keys["f_wx"] = "Flight occurred in " + data_fields["wx"] + " conditions."

    team = data_fields["team"].split(" ")
    proc = data_fields["proc"].split(" ")
    keys["fteam"] = ""
    for person in proc:
        if person not in team:
            team.append(person)
    for person in team:
        keys["fteam"] += format.make_creators(person)
    pi = data_fields["pi_name"]
    keys["project_info"] = ""
    if pi in projects.keys():
        project = projects[pi]
        for key in project:
            if key in keys.keys():
                keys[key] = project[key]
            if project[key] == "NSF":
                keys["project_info"]=format.make_nsf_project(project)

    if data_fields["flag"] != "":
        print("***Dataset has the following flag ***", data_fields["flag"], "***")
        ## TODO, maybe instead create a text file with the name, directory, and the flag?

    return keys





































