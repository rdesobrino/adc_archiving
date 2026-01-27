from lib import format
import os

def mapper(keys, data_fields, projects):
    for key in keys.keys():  ## handles all key-matching that does not require additional formatting
        if key in data_fields:
            keys[key] = data_fields[key]
    #keys["s_site"] = data_fields["s_site"] +"," ## actually, then rogue comma. if statement or just delete
    keys["l_area"] = " " + data_fields["l_area"]
    keys["date_desc"] = format.date_descr(data_fields["date"])
    keys["f_start"] = data_fields["f_start"] + ":00-9:00"
    keys["f_stop"] = data_fields["f_stop"] + ":00-9:00"

    if data_fields["ms_v"]: ## only if a multispectral camera was used
        keys["ms_desc"] =  ", and multispectral orthomosaic"
        keys["ms_v"] =  "and " + data_fields["ms_v"] + " multispectral sensor"
        keys["ms_meth"] = "and an " + data_fields["ms_v"] + " was flown nadir with calibration photos taken at the start of each flight, and/or when lighting conditions changed"
    if data_fields["klau"]: ## only if Klau was used
        keys["klau_desc"] = "GPS post-processed using KlauPPK. "
        keys["klau_meth"] = "GPS data were collected with an external PPK antenna (KlauPPK) for each image captured and post-processed using KlauPPK Version 7.22.1 (Klau Geomatics)."

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
            ## TODO do I need to check if NDVI included on all?
            keys["ms_px_desc"] = ", multispectral orthomosaic: " + str(data_fields["tifs"][tif]["res"]) + "m"
            # keys["ms_res"]= str(data_fields["tifs"][tif]["res"]) + "m"
            keys["ms_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["ms_cols"] = str(data_fields["tifs"][tif]["cols"])
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





































