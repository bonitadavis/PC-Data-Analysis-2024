# Reusable script for cleaning and combining attendance data from SMU360 (SMU's student organization platform)

# import libraries
import pandas as pd
import glob
import os

# read, combine, and clean csv files
attendance_dir = "Attendance Data"
files = glob.glob(os.path.join(attendance_dir, "*.csv"))
df_list = []

# list of the columns we will need for analysis
columnsNeeded = ["First Name", "Last Name", "Email", "Account Type", "Year of Graduation", "Is Member", "Degree", "Registration Date", "Checked-In Date", "Attendee's Rating", "Attendee's Feedback", "Net ID"]

# read each file
for file in files:
    fileName = os.path.basename(file).replace(".csv", "")
    try:
        df = pd.read_csv(file, usecols=columnsNeeded) # remove unnecessary columns
    except ValueError as e: # if a column needed isn't found
        print(f"Warning: {fileName} does not contain all specified columns. Skipping missing ones.")
        df = pd.read_csv(file)
        df = df[df.columns.intersection(columnsNeeded)]

    # update individual event data after subsetting
    df.to_csv(os.path.join(attendance_dir, f"{fileName}.csv"), index=False)

    # add event name column before combining dataset
    df["Event Name"] = fileName
    df_list.append(df)

# combine all csv files
df = pd.concat(df_list, ignore_index=True)
df.head() # check if things look good

# handles missing degree values
df["Degree"] = df["Degree"].fillna("Unknown")

# handles missing check-in dates
df["Checked-In Date"] = df["Checked-In Date"].fillna("No show")

# calculates avg ratings
avgRatings = df.groupby("Event Name")["Attendee's Rating"].mean()

# handles missing rating values
df["Attendee's Rating"] = df["Attendee's Rating"].fillna(df["Event Name"].map(avgRatings))

# handles missing feedback
df["Attendee's Feedback"] = df["Attendee's Feedback"].fillna("N/A")

# rename undergrad schools
df["Degree"] = df["Degree"].replace({"SMU Pre-Majors":"Pre-Majors", "Dedman College":"Dedman", "UG Cox School of Business":"Cox", "UG School of Engr & Appl Sci":"Lyle", "UG Meadows School of the Arts":"Meadows","Simmons School - Undergraduate":"Simmons"})

df # check before exporting

df.to_csv("attendance2024.csv", index=False)