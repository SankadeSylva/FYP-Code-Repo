import csv
import random
from faker import Faker

fake = Faker()

# NE_monsoon_season = []
# NE_dry_season = []

SW_monsoon_season = ["05", "06", "07", "08", "09"]
SW_dry_season = ["12", "01", "02", "03"]

months = ["01", "02", "03", "04", "05",
          "06", "07", "08", "09", "10", "11", "12"]
thirty_day_months = ["04", "06", "09", "11"]

days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
for day in range(11, 32):
    days.append(str(day))

Table_Headers = ["Date + Time", "Temperature",
                 "Humidity", "Hours of Sunshine", "Soil Moisture"]

f_path = "/Users/sankadesylva/Documents/Python_Projects/FYP_Python_Code/Data_Generator/FYP_Sensor_testData.csv"
with open(f_path, "w")as DataFile:
    csv_writer = csv.writer(DataFile)
    csv_writer.writerow(Table_Headers)

    data_list = [0, 0, 0, 0, 0]
    for month in months:
        for day in days:
            # create time stamp:
            #   using format 2012-04-23T18:25:43.511Z
            #   check "FYP Correct Time Format.rtf" for why.
            d_stamp = "2020-" + month + "-" + day
            t_stamp = "T" + fake.time() + "." + str(random.randint(100, 999)) + "Z"
            date_time = d_stamp + t_stamp

            # generate data depending on season:
            if month in SW_monsoon_season:
                temp = round((random.uniform(22, 33)), 2)
                Humidity = round((random.uniform(70, 100)), 1)
                Sun_Hrs = round((random.uniform(6, 8)), 1)
                Soil_M = round((random.uniform(40, 70)), 2)

            elif month in SW_dry_season:
                temp = round((random.uniform(28, 38)), 2)
                Humidity = round((random.uniform(40, 60)), 1)
                Sun_Hrs = round((random.uniform(8, 12)), 1)
                Soil_M = round((random.uniform(20, 50)), 2)
            else:
                temp = round((random.uniform(23, 32)), 2)
                Humidity = round((random.uniform(60, 90)), 1)
                Sun_Hrs = round((random.uniform(7, 9)), 1)
                Soil_M = round((random.uniform(38, 70)), 2)

            data_list = [date_time, temp, Humidity, Sun_Hrs, Soil_M]
            csv_writer.writerow(data_list)

            # if month is february and the 28th day:
            if month == "02" and day == "28":
                break
            # if month only has 30 days:
            if month in thirty_day_months and day == "30":
                break
    # notify that data created for whole year
    print("FYP_Sensor_testData.csv created")
