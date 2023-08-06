import geopandas as gpd
# from osgeo import gdal
import rasterio

def nFields(shapeFile):
    """Returns number of fields in a shapefile
    """

    gdf = gpd.read_file(shapeFile)
    return len(gdf.columns)

def rasterInfo(raster):
    
    ds = rasterio.open(raster)
    xRes = ds.transform[0]
    yRes = ds.transform[4] * (-1)
    ncols = ds.width
    nrows = ds.height
    
    return {'ncols' : ncols, 'nrows' : nrows, 
            'xRes' : xRes, 'yRes' : yRes}