import csv
import random
from time import sleep
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

OFDs = []
n_OFDS = 25
for OFD in range(1, (n_OFDS+1)):
    OFDs.append(OFD)

Data_forDay = []

Table_Headers = ["Date + Time", "OFD #", "Temperature",
                 "Humidity", "Hours of Sunshine", "Soil Moisture"]

# f_path = "/Users/sankadesylva/Desktop/FYP/FYP Progress/Software/FYP-Code-Repo/FYP_NodeRED/Data_Generator/FYP_Sensor_testData.csv"
f_path = "/Users/sankadesylva/Desktop/FYP/FYP Progress/Software/FYP-Code-Repo/FYP_NodeRED/Data_Generator/"
# f_path = "/home/pi/FYP-Code-Repo/FYP_NodeRED/Data_Generator/FYP_Sensor_testData.csv

print("starting csv write")
for month in months:
    for day in days:
        sleep(5)  # delay to simulate "days":
        for OFD in OFDs:
            data_list = [0, 0, 0, 0, 0, 0]
            # create time stamp:
            #   using format 2012-04-23T18:25:43.511Z
            #   check "FYP Correct Time Format.rtf" for why.
            d_stamp = "2020-" + month + "-" + day
            t_stamp = "T" + fake.time() + "." + str(random.randint(100, 999)) + "Z"
            # date_time = d_stamp + t_stamp

            date_time = d_stamp  # only include date
            # date_time = "/"  # if date not needed

            # generate data depending on season:
            if month in SW_monsoon_season:
                Temp = round((random.uniform(22, 33)), 2)
                Humidity = round((random.uniform(70, 100)), 1)
                Sun_Hrs = round((random.uniform(6, 8)), 1)
                Soil_M = round((random.uniform(40, 70)), 2)

            elif month in SW_dry_season:
                Temp = round((random.uniform(28, 38)), 2)
                Humidity = round((random.uniform(40, 60)), 1)
                Sun_Hrs = round((random.uniform(8, 12)), 1)
                Soil_M = round((random.uniform(20, 50)), 2)
            else:
                Temp = round((random.uniform(23, 32)), 2)
                Humidity = round((random.uniform(60, 90)), 1)
                Sun_Hrs = round((random.uniform(7, 9)), 1)
                Soil_M = round((random.uniform(38, 70)), 2)

            data_list = [date_time, OFD, Temp, Humidity, Sun_Hrs, Soil_M]
            # create daily reading for each OFD:
            # with open(f_path+str(OFD)+"OFD.csv", "w")as DataFile:
            #     csv_writer = csv.writer(DataFile)
            #     csv_writer.writerow(data_list)
            Data_forDay.append(data_list)

            # if month is february and the 28th day:
            if month == "02" and day == "28":
                break
            # if month only has 30 days:
            if month in thirty_day_months and day == "30":
                break
        print("\t" + day + " day(s) completed")
        # create daily readings for all OFDs:
        with open(f_path + "_Daily_OFD_data.csv", "w")as DataFile:
            csv_writer = csv.writer(DataFile)
            csv_writer.writerows(Data_forDay)
        Data_forDay = []

    print(month + " of 12 months completed")

# notify that data created for whole year
print("COMPLETE: FYP_Sensor_testData.csv created")


# ONLY have to save daily to the csv for the OFDs
# Read these daily from NodeRED and push to influxdb
# influx can use the OFD # field to plot accordingly.
# Remember: influxdb is a time-series database - so make use of this (!)
