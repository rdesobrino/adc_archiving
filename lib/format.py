
import os

cwd = r"C:\Users\rcdesobrino\Desktop\repos\ADC_archiving\lib\info"

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

def team_name(initials): ## Rd and RF included as dataset creators by default
    team = {"Rd" : " ", "RF": " ", "JN": "Jorge Noguera", "AC":"Adam Chavez"}
    if initials in team:
        return team[initials]
    else:
        print("Who is " + initials + "?")
        return " "
