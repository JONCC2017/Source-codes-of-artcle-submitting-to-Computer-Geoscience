import xlrd
import numpy
import json

parameter=1500                                            #thereshold for max distance
filespath="C:/Users/Administrator/Desktop/qd/"            #Path of excel files
types=["Entertainment_venue","Restaurant","Government_building","Shopping_mall","Hospital","Tourist_attraction","School","Flyover",
       "Factory","Building_Materials_market","Sports_field","Agricultural_facility ","Train_station","Toll_station","Service_area"]        #POI types

datalist=[]
residence_table=xlrd.open_workbook("C:/Users/Administrator/Desktop/qd/residence2.xls")
residence_sheet=residence_table.sheet_by_index(0)
columnid=residence_sheet.col(colx=0,start_rowx=1,end_rowx=None)
columnx=residence_sheet.col(colx=9,start_rowx=1,end_rowx=None)
columny=residence_sheet.col(colx=10,start_rowx=1,end_rowx=None)
columnDN=residence_sheet.col(colx=11,start_rowx=1,end_rowx=None)

def cal_distance(x1,y1,x2,y2):
    return numpy.power(numpy.square(x1-x2)+numpy.square(y1-y2),0.5)

def calculate(x1,y1,x2,y2,thereshold):
    distance=cal_distance(x1,y1,x2,y2)
    if distance<thereshold:
        return distance
    else:
        return 0

for residence in range(columnid.__len__()):
    dictionary1 = {'DN':columnDN[residence].value}
    dictionary = {}
    dictionarylist=[]
    for i in range(types.__len__()):
        if types[i]=="Building_Materials_market":
            table = xlrd.open_workbook(filespath + types[i] + ".xls")
            sheet = table.sheet_by_index(0)
            id = sheet.col(colx=0, start_rowx=1, end_rowx=None)            
            x = sheet.col(colx=9, start_rowx=1, end_rowx=None)
            y = sheet.col(colx=10, start_rowx=1, end_rowx=None)
            DN = sheet.col(colx=11, start_rowx=1, end_rowx=None)
            count=sheet.col(colx=1,start_rowx=1,end_rowx=None)
            area=sheet.col(colx=2,start_rowx=1,end_rowx=None)
            for POI in range(id.__len__()):
                dis = calculate(columnx[residence].value, columny[residence].value, x[POI].value, y[POI].value,
                                parameter)
                if dis != 0:
                    dic={'type':types[i],'count':count[POI].value,'area':int(area[POI].value),'NO':id[POI].value,'distance':int(dis),'DN':int(DN[POI].value)}
                    dictionarylist.append(dic)
            continue

        if types[i]=="Restaurant":
            table = xlrd.open_workbook(filespath + types[i] + ".xls")
            sheet = table.sheet_by_index(0)
            id = sheet.col(colx=0, start_rowx=1, end_rowx=None)            
            x = sheet.col(colx=9, start_rowx=1, end_rowx=None)
            y = sheet.col(colx=10, start_rowx=1, end_rowx=None)
            DN = sheet.col(colx=11, start_rowx=1, end_rowx=None)
            count=sheet.col(colx=1,start_rowx=1,end_rowx=None)
            area=sheet.col(colx=2,start_rowx=1,end_rowx=None)
            for POI in range(id.__len__()):# id.__len__()
                dis = calculate(columnx[residence].value, columny[residence].value, x[POI].value, y[POI].value,
                                parameter)
                if dis != 0:
                    dic={'type':types[i],'count':count[POI].value,'area':int(area[POI].value),'NO':id[POI].value,'distance':int(dis),'DN':int(DN[POI].value)}
                    dictionarylist.append(dic)
            continue
        
        else:
            table = xlrd.open_workbook(filespath + types[i] + ".xls")
            sheet = table.sheet_by_index(0)
            id = sheet.col(colx=0, start_rowx=1, end_rowx=None)            
            x = sheet.col(colx=9, start_rowx=1, end_rowx=None)
            y = sheet.col(colx=10, start_rowx=1, end_rowx=None)
            DN = sheet.col(colx=11, start_rowx=1, end_rowx=None)
            for POI in range(id.__len__()):# id.__len__()
                dis = calculate(columnx[residence].value, columny[residence].value, x[POI].value, y[POI].value,
                                parameter)
                if dis != 0:
                    dic={'type':types[i],'count':0,'area':0,'NO':id[POI].value,'distance':int(dis),'DN':DN[POI].value}
                    dictionarylist.append(dic)
            

    dictionary[residence+1]=dictionary1
    dictionary['list']=dictionarylist
    datalist.append(dictionary)
    
    print('residence',residence+1," has been done")


with open('C:/Users/Administrator/Desktop/qd/2.json','w') as file:
    json.dump(datalist,file)









