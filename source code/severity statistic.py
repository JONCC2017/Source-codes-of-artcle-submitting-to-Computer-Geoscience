import json
import xlrd
import math

types=["Entertainment_venue","Restaurant","Government_building","Shopping_mall","Hospital","Tourist_attraction","School","Flyover",
       "Factory","Building_Materials_market","Sports_field","Agricultural_facility ","Train_station","Toll_station","Service_area"]

def Assessingmodel(DN, x, band=500):
    molecule = x * x
    demominator = 2 * band * band
    left = 1 / (math.sqrt(2 * math.pi) * band)
    return DN*left * math.exp(-molecule / demominator)

def length(type):
    residence_table = xlrd.open_workbook("E:/11111desktop/DATA/QD/" + type + ".xls")
    residence_sheet = residence_table.sheet_by_index(0)
    columnid = residence_sheet.col(colx=0, start_rowx=1, end_rowx=None)
    return columnid.__len__()

def statistic(data):
    typecounter={}
    for t in types:
        typecounter[t]={}
    for residence in data:
        print(data.index(residence)," has been done")
        if residence['list'].__len__()==0:
            continue
        for POI in range(residence['list'].__len__()):
            if Assessingmodel(DN=residence['list'][POI]['DN'], x=residence['list'][POI]['distance'])>60:
                typecounter[residence['list'][POI]['type']][residence['list'][POI]['NO']]='serious'
                continue
            if Assessingmodel(DN=residence['list'][POI]['DN'], x=residence['list'][POI]['distance'])>30:
                typecounter[residence['list'][POI]['type']][residence['list'][POI]['NO']]='medium'
                continue
            else:
                typecounter[residence['list'][POI]['type']][residence['list'][POI]['NO']] = 'none'
    return typecounter

def analyze(data):
    seriouscounter={}
    mediumcounter = {}
    nonecounter = {}
    for i in types:
        seriouscounter[i]=0
        mediumcounter[i]=0
        nonecounter[i]=0
    for t in data.keys():
        for tt in data[t].keys():
            if data[t][tt]=='serious':
                seriouscounter[t]=seriouscounter[t]+1
            if data[t][tt]=='medium':
                mediumcounter[t]=mediumcounter[t]+1
            if data[t][tt]=='none':
                nonecounter[t]=nonecounter[t]+1

        len=length(t)
        if t == "jiancaiagg":
            len=191
        if t == "canyinagg":
            len=302
        print(t+' s ',seriouscounter[t]/len)
        print(t+' m ',mediumcounter[t] / len)
        print(t+' n ',nonecounter[t] / len)

def main():
    length(types[0])
    with open('E:/11111desktop/DATA/QD/2.json', 'r') as file:
        data1 = json.load(file)
    data2 = statistic(data1)
    analyze(data2)

if __name__=="__main__":
    main()
