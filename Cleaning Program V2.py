
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
df = pd.read_csv("shifts.csv")


#for joining the Staff by Commas
df = df.groupby(by=["Note","Duration"]).agg({'First Name':', '.join,
                           "Date": "first", 
                           "Start Time":'first',
                           "End Time": "first"}).reset_index()

#Reset index over here helps in joining the tables togather    
df = df.reset_index()
tmp = (df["Note"].str.split(",",expand=True,)).reset_index()


#Renaiming the comma separated columns
tmp = tmp.rename(columns={0:"Contact",1:"Client Name",2:"Address",
                   3:"Vendor",4:"Rate",5:"Materials?",6:"MOP",7:"Amount"})

#Join Operation
df = df.merge(tmp, how="inner",on="index")

#Sorting them on the basis of time
df["Start Time Sort"] = df["Start Time"].astype("datetime64[ns]")
df = df.sort_values(by=["First Name","Start Time Sort"]).reset_index()

#Duration ceil function
df["Total Time"] = df["Duration"].astype("float")


#Attended by staff
df["Attended by"] = df["First Name"].str.split(",").apply(len)

#Consolidated hours
df["Consolidated Hours"] = df["Total Time"] * df["Attended by"]

#Revenue
#df["Rate"] = df["Rate"].astype("float64")
#df["Revenue"] = df["Consolidated Hours"] * df["Rate"]
df["Vendor"] = df["Vendor"].str.strip()
df["Vendor"] = df["Vendor"].str.upper()

df["MOP"] = df["MOP"].str.strip()
df["MOP"] = df["MOP"].str.upper()

df["Materials?"] = df["Materials?"].str.strip()
df["Materials?"] = df["Materials?"].str.upper()
#df["Contact"] = df["Contact"].astype("int")

#overcoming the spelling mistakes done by them, because they'll never learn
rec = ["RECC","RECURRING"]
gp_cash = ["GP_CASH","GP-CASH",]
gp_rec = ["GP_REC","GP_RECC","GP-RECC","G-REC"]
ent = ["ENTERTAINER","ENTER"]
r_est = ["R-ESTATE","REAL-ESTATE","REAL ESTATE","R ESTATE","RESTATE","R-STATE"]
ust = ["MR-USTA","USTA"]
on_cash = ["ONLINE/CASH","CASH/ONLINE","VOUCHER/CASH","CASH/VOUCHER"]
material = ["M"]

df.loc[df["MOP"].isin(["BANK TRANSFER","BT","B.T","MR"]),"MOP"] = "MT"
df.loc[df["Vendor"].isin(rec),"Vendor"] = "REC"
df.loc[df["Vendor"].isin(gp_cash),"Vendor"] = "GP-CASH"
df.loc[df["Vendor"].isin(gp_rec),"Vendor"] = "GP-REC"
df.loc[df["Vendor"].isin(ent),"Vendor"] = "ENTER"
df.loc[df["Vendor"].isin(r_est),"Vendor"] = "R-EST"
df.loc[df["Vendor"].isin(ust),"Vendor"] = "USTA"
df.loc[df["MOP"].isin(on_cash),"MOP"] = "CASH/ONLINE"
df.loc[df["Materials?"].isin(material),"Materials?"] = "N"

df.loc[df["Vendor"].isin(["ONLINE,ONLIE"]),"Vendor"] = "ONLINE"

df["Contact"].map(lambda x : "".join(x.split(" "))).str.strip()
df["Date"] = df["Date"].astype("datetime64")

'''
#Code was writted because the file we downloaded had shift duration in 3h 30 min type format
duration = []
for x in df["Total Time"]:
    if int(x[3]) >= 3:
        duration.append(int(x[0])+.5)
    else:
        duration.append(x[0])
        
df["Total Time"] = duration
df["Total Time"] = df["Total Time"].astype("float")'''


#Consolidated hours
df["Consolidated Hours"] = df["Total Time"] * df["Attended by"]

#No GP-CASH, GP-RECC, REC should be online

#checklist = ["GP-REC","REC","GP-CASH"]
#if 




#timesheet report to be put into Access
df[["Date",'Contact',"Client Name","Address","Vendor","MOP","First Name","Attended by","Start Time",'End Time','Total Time',"Rate",'Materials?',"Consolidated Hours",'Amount']].to_excel(str(df.Date.astype("str").unique().tolist()[0])+" "+"Cleaning_Report.xlsx",index_label = "SNO")

#whatsapp messaging text
with open("Whatsapp Staff", "w+") as f:
    for j in range(df.shape[0]):
        for i in df.columns.tolist():
            if i not in ["Contact","level_0","index","Note","Start Time Sort","Date","Duration"]:
                if i in ["First Name"]:
                    f.write("\n")
                    f.write(df.loc[j,i])
                    f.write("\n")
                    continue
                f.write(str(i)+" :"+str(df.loc[j,i]))
                f.write("\n")

#whatsapp messaging text
with open("Whatsapp Team Leaders", "w+") as f:
    for j in range(df.shape[0]):
        for i in df.columns.tolist():
            if i not in ["level_0","index","Note","Start Time Sort","Date","Duration"]:
                if i in ["First Name"]:
                    f.write("\n")
                    f.write(df.loc[j,i])
                    f.write("\n")
                    continue
                f.write(str(i)+" :"+str(df.loc[j,i]))
                f.write("\n")
        

