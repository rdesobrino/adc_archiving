from lib import format
import os

def mapper(keys, data_fields, people_info):
    for key in keys.keys():  ## handles all key-matching that does not require additional formatting
        if key in data_fields:
            keys[key] = data_fields[key]
    keys["l_area"] = ", " + data_fields["l_area"]
    keys["date_desc"] = format.date_descr(data_fields["date"])
    keys["f_start"] = data_fields["f_start"] + ":00-09:00"
    keys["f_stop"] = data_fields["f_stop"] + ":00-09:00"

    for attr_id in ["red_id", "green_id", "blue_id", "dsm_id", "ms_id_1", "ms_id_2", "ms_id_3", "ms_id_4", "ms_id_5", "ms_id_6", "ms_id_7"]:
        keys[attr_id] = format.attr_id()

    ## raster specific metadata
    for tif in data_fields["tifs"]:
        bobo = data_fields["tifs"][tif]["bobo"] ## only need one bounding box, RGB and MS will be slightly different but ah well
        keys["h_crs"] = data_fields["tifs"][tif]["hcs"] ## assumes all rasters are in same crs for description, but each gets written separately at data-level
        if data_fields["tifs"][tif]["bands"] == 1: ## TODO call separate function, identifies tif type, returns {tif_name:[res, spatialRaster text}
            keys["dem_name"] = os.path.basename(tif)
            keys["dem_res"] = str(data_fields["tifs"][tif]["res"])
            keys["dem_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["dem_cols"] = str(data_fields["tifs"][tif]["cols"])
        elif data_fields["tifs"][tif]["bands"] == 3:
            keys["rgb_name"] = os.path.basename(tif)
            keys["rgb_res"] = "RGB orthomosaic: " + str(data_fields["tifs"][tif]["res"]) + ", "
            keys["rgb_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["rgb_cols"] = str(data_fields["tifs"][tif]["cols"])
        elif data_fields["tifs"][tif]["bands"] >= 3: ## anything over 3 bands should be multispectral
            keys["ms_name"] = os.path.basename(tif)
            keys["ms_px_desc"] = ", multispectral orthomosaic: " + str(data_fields["tifs"][tif]["res"]) + "m"
            keys["ms_res"]= str(data_fields["tifs"][tif]["res"])
            keys["ms_rows"]  = str(data_fields["tifs"][tif]["rows"])
            keys["ms_cols"] = str(data_fields["tifs"][tif]["cols"])
            if data_fields["tifs"][tif]["bands"] != 6 and data_fields["date"][:2] != "26":
                print("Double-check the raster bands. This rasters has ", data_fields["tifs"][tif]["bands"], "bands." )

    sensor_ct = 0
    if data_fields["rgb_v"]: ## if RGB camera used
        keys["rgb_desc"] = "true-color orthomosaic, "
        keys["rgb_meth"] = "RGB imagery was captured with a " + data_fields["rgb_v"] + " on a gimbal at " + data_fields[
            "f_alt"] + " meters altitude at " + data_fields["f_spd"] + " m/s with along-track overlap of " + \
                           data_fields["f_flap"] + "% and across-track overlap of " + data_fields["f_slap"] + "%."
        sensor_ct += 1

    if data_fields["ms_v"]: ## only if a multispectral camera was used
        keys["ms_desc"] =  ", and multispectral orthomosaic"
        keys["ms_v"] =  data_fields["ms_v"] + " multispectral sensor"
        keys["ms_meth"] = "A " + data_fields["ms_v"] + " was flown nadir at " + data_fields[
            "m_alt"] + " meters altitude at " + data_fields["m_spd"] + " m/s with along-track overlap of " + data_fields[
                              "m_flap"] + "% and across-track overlap of " + data_fields[
                              "m_slap"] + "%. Calibration photos were taken at the start of each flight, and/or when lighting conditions changed."
        sensor_ct += 1

    count_orthos = ["", "", "s"]       ## honestly embarrassing way to handle some specific grammar
    rgb_and_ortho = ["", "", " and"]
    keys["ortho_s"] = count_orthos[sensor_ct]
    keys["rgb_and_ortho"] = rgb_and_ortho[sensor_ct]

    keys["gps_desc"], keys["gps_meth"] = format.gps_methodology(data_fields["tifs"][tif], data_fields["gps_meth"], data_fields["gps_ref"])

    keys["webo"] = "-" + str(bobo[0][0])
    keys["ebo"] = "-" + str(bobo[1][0])
    keys["nobo"] = str(bobo[0][1])
    keys["sobo"] = str(bobo[1][1])
    keys["hyph_date"] = format.hyphenate_date(data_fields["date"])
    if data_fields["wx"]:
        keys["f_wx"] = "Flight occurred in " + data_fields["wx"] + " conditions."

    pis = data_fields["pis_last"].split(" ")
    keys["fteam"] = ""
    keys["project_info"] = ""
    for person in pis:
        if person in people_info.keys(): ## TODO:  filter by year for project ?
            person_info = people_info[person]
            keys["fteam"] += format.make_pi_creators(person_info)
            for key in person_info:
                if key in keys.keys():
                   keys[key] = person_info[key]
                if person_info[key] == "NSF":                                 ## TODO add non-NSF projects
                    keys["project_info"]=format.make_nsf_project(person_info) ## TODO: this currently only lists one PI on the project
        else:
            print("Who is ", person, "?????")
        keys["pi_name"] += person_info["pi"] + ", "
    keys["pi_name"] += "and the '" + person_info["project_name"] + "' project"

    team = data_fields["team"].split(" ")
    proc = data_fields["proc"].split(" ")
    for person in proc:
        if person not in team:
            team.append(person)
    for person in team:
        keys["fteam"] += format.make_tfs_creators(person)

    if data_fields["flag"] != "":
        print("**********Dataset has the following flag ***", data_fields["flag"], "***")
    if ":" not in data_fields["f_start"] or ":" not in data_fields["f_stop"]:
        print("***********Time is formatted incorrectly. Thanks csv")

    return keys





































