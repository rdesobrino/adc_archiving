
import os
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

def make_creators(initials): ## Rd and RF included as dataset creators by default
    team = {#"Rd": [" ", "1221893104692641", ""],
            #"RF": [" ", "4874726551979884", ""],
            "JN": ["Jorge Noguera", "7438520647130753", ""],
            "AC": ["Adam Chavez", "1818551077413436", "https://orcid.org/0009-0001-0308-8461"],
            "MK": ["Matteo Kuizenga", "4947775109728476", ""],
            "OCG": ["Olivia Cronin-Golomb", "7272403399156581", "https://orcid.org/0000-0003-2842-158X"],
            "MS": ["Mary Stack", "1380340284973222", ""],
            "LW": ["Lyndee Weaver", "8872743468265462", ""],
            "RM": ["Rowan McPherson", "3323562272538209", ""]}
    if initials in team:
        with open(os.path.join(cwd, "creator.txt"), "r") as creator:
            text = creator.read()
            text = text.replace("cr_id", team[initials][1] )
            text = text.replace("first", team[initials][0].split(" ")[0])
            text = text.replace("last", team[initials][0].split(" ")[1])
            text = text.replace("orc_id", team[initials][2])  ## TODO potentially delete orcID if empty
        return text   ## return completed creator text
    elif initials not in ["RF", "Rd"]:
        print("Who is " + initials + "?")
    return " "

def make_nsf_project(project):
    with open(os.path.join(cwd, "nsf_project.txt"), "r") as nsf_proj:
        text = nsf_proj.read()
        for key in project:
            text = text.replace(key, project[key])
        text = text.replace("gname", project["PI"].split(" ")[0]) ## I am lazy
        text = text.replace("sname", project["PI"].split(" ")[1]) ## apologies fellow Spanish-last-name-havers
    return text