
import os
import random
import math
from lib import creator_ids
cwd = os.getcwd()

def date_descr(date):
    YY = date[0:2]
    MM = date[2:4]
    DD = date[4:6]
    months = {"01": "January", "02":"February", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"August", "09":"September", "10":"October", "11":"November","12":"December"}
    return DD + " " + months[MM] + ", 20" + YY

def hyphenate_date(date):
    YY = date[0:2]
    MM = date[2:4]
    DD = date[4:6]
    return "20" + YY + "-" + MM + "-" + DD

def attr_id(): ## random ID
    id = ""
    for i in range(30):
        id += str(random.randint(0, 9))
    return id

def make_tfs_creators(initials): ## Rd and RF included as dataset creators by default (but RF not in 2026 template)
    team = {"RF": ["Randy Fulweber", "2350913618209244", "https://orcid.org/0000-0003-0537-4194", "GIS and Remote Sensing Manager"],
            "JN": ["Jorge Noguera", "7438520647130753", "", "GIS and Remote Sensing Technician"],
            "AC": ["Adam Chavez", "1818551077413436", "https://orcid.org/0009-0001-0308-8461", "GIS and Remote Sensing Technician"],
            "MK": ["Matteo Kuizenga", "4947775109728476", "", ""],
            "OCG": ["Olivia Cronin-Golomb", "7272403399156581", "https://orcid.org/0000-0003-2842-158X", "GIS and Remote Sensing Technician"],
            "MS": ["Mary Stack", "1380340284973222", "", "GIS and Remote Sensing Technician"],
            "LW": ["Lyndee Weaver", "8872743468265462", "", "GIS and Remote Sensing Technician"],
            "RM": ["Rowan McPherson", "3323562272538209", "", "GIS and Remote Sensing Analyst"],
            "SS": ["Soumitra Sakhalkar", "3128214525321854", "https://orcid.org/0000-0002-1375-3883", ""],
            "HD": ["Haley Dunleavy", "9799509437574473", "https://orcid.org/0000-0002-7383-8598", ""],
            "QW": ["Quentin Walker", "0714959883143746", "", "GIS and Remote Sensing Manager"],
            "SP": ["Sophia Parker", "4052078996786969", "https://orcid.org/0009-0004-7219-6628", "GIS and Remote Sensing Technician"],
            "AH": ["Abigail Haas", "9092033674650736", "", "GIS and Remote Sensing Technician"],
            }

    if initials in team:
        with open(os.path.join(cwd, "team.txt"), "r") as creator:
            text = creator.read()
            text = text.replace("cr_id", team[initials][1] )
            text = text.replace("first", team[initials][0].split(" ")[0])
            text = text.replace("last", team[initials][0].split(" ")[1])
            text = text.replace("orc_id", team[initials][2])
            text = text.replace("role", team[initials][3])
        return text   ## return completed creator text

    elif initials not in ["RF", "Rd"]:
        print("Who is " + initials + "?")
    return " "

def make_pi_creators(pi_dic):
    with open(os.path.join(cwd, "pi_creator.txt"), "r") as creator:
        text = creator.read()
        text = text.replace("cr_id", creator_ids.make_random_id())
        text = text.replace("first", pi_dic["First"].strip())
        text = text.replace("last", pi_dic["Last"].strip())
        text = text.replace("org_name", pi_dic["Institution"].strip())
        text = text.replace("role", pi_dic["Role"].strip())
        text = text.replace("email", pi_dic["Email"].strip())
        text = text.replace("orc_id", pi_dic["OrcID"].strip())
    return text  ## return completed creator text

def make_nsf_project(pis, project_info):   ## TODO - not actually just NSF project, change
    main_proj = project_info[pis[0]] ## uses the project of the first pi listed
    with open(os.path.join(cwd, "create_project.txt"), "r") as proj:
        text = proj.read()
        main_proj["people"] = ""
        main_proj["fund_id"] = ""
        if main_proj["funder_"] == 'NSF':
            main_proj["funder_"] = "National Science Foundation"
            main_proj["fund_id"] = "https://doi.org/10.13039/100000001"
        main_proj["people"] = ""
        for pi in pis:
            main_proj["people"] += "<individualName>\n<givenName>" +project_info[pi]["First"]+"</givenName>\n<surName>"+project_info[pi]["Last"]+"</surName>\n</individualName>\n<role>" + project_info[pi]["Role"] + "</role>"
        for key in main_proj:
            text = text.replace(key, main_proj[key])
    return text

def gps_methodology(tif, method, ref):
    bases = {"TLK2": ["the TLK2 CORS station", [394474.177, 7615113.754]],
             "Galbraith Rock": ["a mobile base station established on a rock", [399245.867, 7601064.231]],
             "AB45": ["the AB45 CORS station", [424362.468, 7628807.999]],
             "AB33": ["the AB33 CORS station", [621978.3273, 7462139.122]],
             "Ice Cut": ["a mobile base station established on a rock", [426768.062, 7660653.426]],
             "TRTK Rock": ["a mobile base station established on a rock", [413710.988, 7621097.657]],
             "Sagwon": ["a mobile base station established on a rock", [433486.0535, 7702537.337]],
             "Happy Valley": ["a mobile base station established on a rod and PVC driven into the tundra",
                              [427019.806, 7672785.259]],
             "Imnavait": ["a mobile base station established in bedrock", [405540.121, 7613587.016]],
             "EDOC": ["the EDOC CORS station", [450425.545, 7801011.498]]}

    dist = 0

    if ref in bases:
        center = [float(x) for x in tif["center_xy"].split(",")]
        dist = round((math.dist(center, bases[ref][1])) / 1000, 2)
        if dist > 20:
            print("The reported distance between the flight and corresponding base is more than 20km")

    gps_desc = {"GCPs" : "Ground Control Points were deployed throughout the survey area to georeference the dataset. ",
                "Emlid Reach M2" : "Image coordinates were collected using an Emlid Reach M2. ",
                "KlauPPK" : "Image coordinates were collected using a KlauPPK kit and post-processed in KlauPPK Version 7.22.1 (Klau Geomatics). ",
                "align" : ""}

    if method == "GCPs" and dist > 0:
        gps_meth = "A real-time-kinematic (RTK) survey of Ground Control Points with baseline " + str(dist) + " kilometers from " + bases[ref][0] + " was conducted to georeference the point cloud. "
    elif method == "GCPs":
        gps_meth = "A Post-Processing Kinematic (PPK) survey of Ground Control Points distributed throughout the survey area was conducted to georeference the point cloud. "
    elif method == "align":
        gps_meth = "Point clouds were aligned to a flight of the same study site surveyed on " + ref + " due to a lack of available positioning data. "
    else:
        ppk = {
            "Emlid Reach M2": "Camera coordinates were recorded for each image at the time of capture using an Emlid Reach M2 external PPK antenna and "
                              "post-processed using " + bases[ref][0] + " " + str(
                dist) + " kilometers away with Emlid Studio 1.10. ",
            "KlauPPK": "Camera coordinates were recorded for each image at the time of capture using a KlauPPK external PPK antenna and "
                       "post-processed using " + bases[ref][0] + " " + str(
                dist) + " kilometers away with KlauPPK Version 7.22.1 (Klau Geomatics). "
        }
        gps_meth = ppk[method]

    return gps_desc[method], gps_meth

def describe_raster(fpath, tif, mica, dem_ct, ortho_ct):
    ## raster specific metadata
    keys = {}  ## todo why are we doing all of this when we already have done it
    keys["bobo"] = tif["bobo"]  ## only need one bounding box, RGB and MS will be slightly different but ah well
    keys["hcs"] = tif["hcs"]  ## assumes all rasters are in same crs for description, but each gets written separately at data-level
    keys["_name"] = os.path.basename(fpath)
    keys["_res"] = str(tif["res"])
    keys["_rows"] = str(tif["rows"])
    keys["_cols"] = str(tif["cols"])
    keys["center_xy"] = str(tif["center"])
    if tif["bands"] == 1:
        keys["txt"] = r"lib\dem_spatialRaster.txt"
        dem_ct += 1
    elif tif["bands"] == 3:
        keys["txt"] = r"lib\rgb_ortho_spatialRaster.txt"
        ortho_ct += 1
    elif mica == 'Micasense RedEdge-P':
        keys["txt"] = r"lib\rededge_p_spatialRaster.txt"
        ortho_ct += 1
    elif mica == 'Micasense RedEdge-MX':
        keys["txt"] = r"lib\rededge_mx_spatialRaster.txt"
        ortho_ct += 1
    if tif["bands"] not in [1, 3, 4, 6, 7] :  ##todo really what on earth am I catching with this wide net
        print("Double-check the raster bands. This rasters has ", tif["bands"], "bands.")

    return keys, dem_ct, ortho_ct