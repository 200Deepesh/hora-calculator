import tkinter as tk
from tkinter import messagebox
import zoneinfo
from astral import LocationInfo
from astral.sun import sun
from datetime import date, timedelta, datetime
import pandas as pd
import geopy

#list of planet in definate order
planetNames = [['Moon'],['Saturn'],['Jupiter'],['Mars'],['Sun'],['Venus'],['Mercury']]

horaChart = []

#converting weekdays number into planetNames index
planetNamesIndex = {
    0:0, 1:3, 2:6, 3:2, 4:5, 5:1, 6:4
}




#verifing input date
def validate_inputdata(date_text, city):
    try:
        date.fromisoformat(date_text)
        print(date_text)
        loc = geopy.Nominatim(user_agent='hora calculater').geocode(city)
        print(f'latitude {loc.latitude}\nlongitude {loc.longitude}')

        return True          
    except:
        messagebox.showerror("Invalid Date", "Please enter the valid city name or date in YYYY/MM/DD format.")
        return False

def submit_date():
    input_date = date_entry.get()
    city = city_name.get()
    
    if validate_inputdata(input_date, city):
        loc = geopy.Nominatim(user_agent='hora calculater').geocode(city)

        #specifing location
        city = LocationInfo(
            timezone="Asia/Kolkata",
            latitude=loc.latitude,
            longitude=loc.longitude,
        )
        #converting UTC timezone to local timezone
        timezone = zoneinfo.ZoneInfo("Asia/Kolkata")
        currentDate = date.fromisoformat(input_date)
        nextDate = currentDate + timedelta(1)
        
        # Get the sunrise and sunset times
        s = sun(city.observer, date=date(currentDate.year, currentDate.month, currentDate.day), tzinfo=timezone)
        ss = sun(city.observer, date=date(nextDate.year, nextDate.month, nextDate.day), tzinfo=timezone)

        # converting sunrise and sunset times into datetime object
        firstSR = datetime.fromisoformat(str(s['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))
        firstSS = datetime.fromisoformat(str(s['sunset'].strftime('%Y-%m-%d %H:%M:%S')))
        nextSR = datetime.fromisoformat(str(ss['sunrise'].strftime('%Y-%m-%d %H:%M:%S')))

        #defining duration of a hora 
        dayHoraPeriod = (firstSS - firstSR)/12
        nightHoreaPeriod = (nextSR - firstSS)/12
        td = [dayHoraPeriod, nightHoreaPeriod]

        #defining index of the planets
        index = planetNamesIndex[currentDate.weekday()]
        print(index)

        #tt = ti.fromisoformat(str(firstSR.time())) #error
        tt = firstSR
        for i in range(0,2):
            for j in range(0,12):
                horaChart.append([planetNames[index],tt.time().isoformat(timespec='seconds'),(tt+td[i]).time().isoformat(timespec='seconds')])
                tt = td[i] + tt
                index += 1
                if(index == 7):
                    index = 0
        print(pd.DataFrame(horaChart, columns=['planet name', 'from', 'to']))
                
   



#GUI of app
root = tk.Tk()
root.title("Date Input")

#taking date as input
tk.Label(root, text="Enter your city name:").pack(pady=10)
city_name = tk.Entry(root)
city_name.pack(pady=5)
tk.Label(root, text="Enter Date (YYYY/MM/DD):").pack(pady=10)
date_entry = tk.Entry(root)
date_entry.pack(pady=5)

tk.Button(root, text="Submit", command=submit_date).pack(pady=10)

root.mainloop()
