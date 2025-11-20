from lib import format
import os

def mapper(keys, data_fields):
    for key in keys.keys():  ## handles all key-matching that does not require additional formatting
        if key in data_fields:
            keys[key] = data_fields[key] ##TODO: time into UTC (i.e. 11:50 -> 11:50:00-09:00)

    keys["l_area"] = " " + data_fields["l_area"]
    keys["date_desc"] = format.date_descr(data_fields["date"])

    if data_fields["ms_v"]: ## only if a multispectral camera was used
        keys["ms_desc"] =  ", and multispectral orthomosaic"
        keys["ms_v"] =  " and " + data_fields["ms_v"] + " multispectral sensor"
        keys["ms_meth"] = " and an" + data_fields["ms_v"] + " was flown nadir with calibration photos taken at the start of each flight, and/or when lighting conditions changed"
    if data_fields["klau"]: ## only if Klau was used
        keys["klau_desc"] = "GPS post-processed using KlauPPK."
        keys["klau_meth"] = "GPS data were collected with an external PPK antenna (KlauPPK) for each image captured and post-processed using KlauPPK Version 7.22.1 (Klau Geomatics)."
    ## TODO make project-level dictionary and functions that pull from PI name
    keys["kword_desc"] = "..." ## eg "plant phenology, warming, shrubs"
    keys["kword_1"] = "" ## TODO how serious do I want to be about keyword dictionaries
    keys["kword_2"] = ""
    keys["kword_3"] = ""

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
        elif data_fields["tifs"][tif]["bands"] >= 3: ## anything over 3 bands should be multispectal
            keys["ms_name"] = os.path.basename(tif)  ## TODO: if not MX camera, metadata different 
            keys["ms_res_desc"] = ", multispectral orthomosaic: " + str(data_fields["tifs"][tif]["res"]) + " cm"
            keys["ms_res"]= str(data_fields["tifs"][tif]["res"])
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
    for person in proc:
        if person not in team:
            team.append(person)
    for i in range(len(team)):
        keys["fteam_" + str(i + 1) + "g"] = format.team_name(team[i]).split(" ")[0] ## I Rachel de Sobrino, acknowledge that this way of handling names
        keys["fteam_" + str(i + 1) + "s"] = format.team_name(team[i]).split(" ")[1] ## is the same reason my last name is always handled incorrectly in databases
    keys["pi_proj"] = "... (Rachel to add)"
    keys["pi_gname"] = data_fields["pi_name"].split(" ")[0]                              ## however, I am lazy
    keys["pi_sname"] = data_fields["pi_name"].split(" ")[1]                              ## apologies fellow Spanish-last-name-havers

    if data_fields["flag"] != "":
        print("Dataset has the following flag ***", data_fields["flag"], "***")
        ## TODO, maybe instead create a text file with the name, directory, and the flag?


    return keys





































