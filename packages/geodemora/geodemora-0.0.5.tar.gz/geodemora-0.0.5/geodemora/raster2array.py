from osgeo import gdal, osr

class RasterFile:
    def __init__(self, raster):
        self.raster_name = raster
        
    def rasterInfo(self):
    
        ds = gdal.Open(self.raster_name)
        xRes = ds.GetGeoTransform()[1]
        yRes = ds.GetGeoTransform()[-1] * (-1)
        ncols = ds.RasterXSize
        nrows = ds.RasterYSize
        
        return {'ncols' : ncols, 'nrows' : nrows, 
                'xRes' : xRes, 'yRes' : yRes}
    
    def isProjected(self):
        
        ds = gdal.Open(self.raster_name)
        proj = osr.SpatialReference(wkt = ds.GetProjection())
        if proj.GetUTMZone() > 0:
            return True
        else:
            return False
    
    def getEPSG(self):
        
        ds = gdal.Open(self.raster_name)
        proj = osr.SpatialReference(wkt = ds.GetProjection())
        epsg = proj.GetAttrValue('AUTHORITY',1)
        return int(epsg)
    
    def convert2array(self):
        
        ds = gdal.Open(self.raster_name)
        ar = ds.ReadAsArray()
        return ar    
    
    @staticmethod
    def array_max(array):
        import numpy as np
        return np.nanmax(array)