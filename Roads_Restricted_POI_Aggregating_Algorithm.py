import shapefile
import shapely
from shapely.geometry import point
from osgeo import ogr
import sklearn

error=0
minium=7         #if the number of POI in the specifc roads formed area is little than the minium number, then the area will be skipped
pointfile=r'E:\11111desktop\images\qingdao\jiancai2000qd.shp'  #file that saves the POI
roadsfile=r'E:\11111desktop\images\qingdao\roadsqingdao.shp'   #file that saves the area features formed by roads
outputfilepath=r'E:\11111desktop\images\qingdao\jiancaiqd60.shp'  #filepath for output
EPS=60           #The EPS parameter of DBSCAN algorithm

def readshapefile(dirct):
    return shapefile.Reader(dirct)

def pointsshape2shapely(shape):
    list1 = []
    for i in shape:
        list1.append(shapely.geometry.Point(i.points[0]))
    return list1

def polygonsshape2shapely(shapes):
    list1 =[]
    for shape1 in shapes:
        list1.append(shapely.geometry.Polygon(shape1.points))
    return list1

def pointsinpolygon(points,polygon):
    list1=[]
    for point1 in points:
        if polygon.contains(point1):
            list1.append([point1.x,point1.y])
    return list1

def DBSCANpointsinAOI(pointslist,defn,layer,aoi,error):
    result=sklearn.cluster.DBSCAN(eps = EPS, min_samples = minium).fit_predict(pointslist)
    typesdictionary={}
    convexhulldict={}

    for i1 in set(result):
        typesdictionary[i1]=[]
    for i in range(pointslist.__len__()):
        typesdictionary[result[i]].append(pointslist[i])
    for i2 in set(result):
        if typesdictionary[i2].__len__()<=minium or i2==-1:
            continue
        convexhulldict[i2] = shapely.geometry.MultiPoint(typesdictionary[i2])
        convexhull = convexhulldict[i2].convex_hull
        try:
            convexhull=convexhull.intersection(aoi)
        except:
            error=error+1
        write2shapefile(convexhull,defn=defn,layer=layer,n=typesdictionary[i2].__len__())

def write2shapefile(poly,defn,layer,n):
    feat = ogr.Feature(defn)
    feat.SetField('number',n)
    geom = ogr.CreateGeometryFromWkb(poly.wkb)
    feat.SetGeometry(geom)
    layer.CreateFeature(feat)

def main():
    # fig, ax = plt.subplots()
    point1 = readshapefile(pointfile).shapes()      #read data in shapefile type
    aois = readshapefile(roadsfile).shapes()

    # mydbf=open(r'E:\11111desktop\images\POIresidence\3\shape.gdb','rb',opener='Administrators')      #read data in gdb
    # mydbf2=open(r'E:\11111desktop\pointcluster\data\test.gdb','rb',opener='Administrators')
    # point1=shapefile.Reader(shp='canyin2000',dbf=mydbf).shapes()
    # aois=shapefile.Reader(shp='polygon',dbf=mydbf2).shapes()

    # gdb_read_driver=ogr.GetDriverByName("OpenFileGDB")
    # gdb_ds=gdb_read_driver.Open(r'E:\11111desktop\images\POIresidence\3\shape.gdb',1)        #read data in gdb
    # gdb_ds2=gdb_read_driver.Open(r'E:\11111desktop\pointcluster\data\test.gdb',1)
    # aois=shapefile.Reader(shp='polygon',dbf=gdb_ds2).shapes()
    # point1=shapefile.Reader(shp='canyin2000',dbf=gdb_ds).shapes()

    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource(outputfilepath)
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    layer.CreateField(ogr.FieldDefn('number', ogr.OFTInteger))
    defn = layer.GetLayerDefn()

    points = pointsshape2shapely(point1)
    aoishapely = polygonsshape2shapely(aois)

    # print(aoishapely[0].contains(points[0]))
    # print(aois[0].points)
    # print(points[0].distance(points[1]))

    for aoi in aoishapely:
        print(aoishapely.index(aoi))
        listjudge = pointsinpolygon(points, aoi)
        if listjudge.__len__() < minium:
            continue
        DBSCANpointsinAOI(listjudge, defn, layer, aoi, error)
    print(error)

    # plt.show()

    ds = layer = None

if __name__=="__main__":
    main()