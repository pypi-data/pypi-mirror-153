import geopandas as gpd
# from osgeo import gdal

def nFields(shapeFile):
    """Returns number of fields in a shapefile
    """

    gdf = gpd.read_file(shapeFile)
    return len(gdf.columns)

# def rasterInfo(raster):
    
#         ds = gdal.Open(raster)
#         xRes = ds.GetGeoTransform()[1]
#         yRes = ds.GetGeoTransform()[-1] * (-1)
#         ncols = ds.RasterXSize
#         nrows = ds.RasterYSize
        
#         return {'ncols' : ncols, 'nrows' : nrows, 
#                 'xRes' : xRes, 'yRes' : yRes}