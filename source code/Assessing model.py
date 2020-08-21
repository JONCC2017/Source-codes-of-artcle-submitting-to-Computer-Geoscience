from matplotlib import pyplot as plt
import json
import xlwt
import numpy
import math

types=["Entertainment_venue","Restaurant","Government_building","Shopping_mall","Hospital","Tourist_attraction","School","Flyover",
       "Factory","Building_Materials_market","Sports_field","Agricultural_facility ","Train_station","Toll_station","Service_area"]

def Assessingmodel(DN, x, band=500):                     # Assessing model can be changed to any other as long as the following parameter is given
    molecule = x * x                                     # DN refers to the Digtal Number extract from night-time light images
    demominator = 2 * band * band                        # x is the distance between residence and pollution source
    left = 1 / (math.sqrt(2 * math.pi) * band)           # Bandwith of the assessing model determines the influence distance of a light pollution
    return DN*left * math.exp(-molecule / demominator)

def judge(POIlist):
    MAX=0
    MAXtype=''
    if POIlist.__len__()==0:
        return 0,"None"
    else:
        for POI in POIlist:
            if POI['distance']<5:                        # Eliminate those points that are too close to each other
                MAXtype='else'
                continue
            if Assessingmodel(POI['DN'], POI['distance'])>=MAX:
                MAX=Assessingmodel(POI['DN'], POI['distance'])
                MAXtype=POI['type']
        if MAXtype=='else':
            return 0,'else'
        if MAX <60:
            return MAX, 'Little'
        else:
            return MAX, MAXtype

def acculmulate():
    maxcostdict={}
    init={}
    means={}
    for aa in types:
        maxcostdict[aa]=0
    maxcostdict['Little'] = 0
    maxcostdict['else'] = 0
    maxcostdict['None'] = 0
    for i in range(types.__len__()):
        init[types[i]]=numpy.zeros(5464)
        means[types[i]]=numpy.zeros(5464)
    for residence in data:
        print(data.index(residence)," has been done")
        typecount=numpy.zeros(types.__len__())
        if residence['list'].__len__()==0:
            continue
        for POI in range(residence['list'].__len__()):
            init[residence['list'][POI]['type']][data.index(residence)]= \
                init[residence['list'][POI]['type']][data.index(residence)] + \
                Assessingmodel(DN=residence['list'][POI]['DN'], x=residence['list'][POI]['distance'])
            typecount[types.index(residence['list'][POI]['type'])]=typecount[types.index(residence['list'][POI]['type'])]+1
        for type in range(types.__len__()):
            if init[types[type]][data.index(residence)]/typecount[type]>1:
                means[types[type]][data.index(residence)]=init[types[type]][data.index(residence)]/typecount[type]
            else:
                means[types[type]][data.index(residence)]
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('residence')
    worksheet.write(0, 0, 'NO')
    worksheet.write(0, 1, 'MAXcost')
    worksheet.write(0, 2, 'MAXtype')
    for i in range(types.__len__()):
        worksheet.write(0,i+4,types[i]+'Accumulate')
    for i in range(types.__len__()):
        worksheet.write(0, i+types.__len__()+5, types[i] + 'Mean')
    for i in range(data.__len__()):
        list = data[i]['list']
        cost, POItype = judge(list)
        maxcostdict[POItype]=maxcostdict[POItype]+cost
        worksheet.write(i + 1, 0, i + 1)
        worksheet.write(i + 1, 1, cost)
        worksheet.write(i + 1, 2, POItype)
        for i2 in range(types.__len__()):
            worksheet.write(i + 1, i2+4, init[types[i2]][i])
        for i3 in range(types.__len__()):
            worksheet.write(i + 1, i3+types.__len__()+5, means[types[i3]][i])
    workbook.save(r'E:\11111desktop\DATA\QD\3qd.xls')

def main():
    acculmulate()

if __name__=="__main__":
    with open(r'E:\11111desktop\DATA\QD\2.json', 'r') as file:
        data = json.load(file)
    POIcount = {}
    for i in range(types.__len__()):
        POIcount[types[i]] = 0
    POIcount['else'] = 0
