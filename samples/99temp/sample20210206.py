# -*- coding: utf-8 -*-
# makeLink4georef2warp v0.43
import os
import arcpy
import glob     # フォルダ内のファイルの一覧を取得用モジュール


def makeLink4georef(path4csv):
    arcpy.env.overwriteOutput = True

    GCPsX_geojson_csv = path4csv

    # Process: CSV To Line
    geocodedLink2450_XY = "C:\\Users\\mapco\\Downloads\\work\\temp\\temp.gdb\\geocoded4link2450_XY"
    arcpy.management.XYToLine(in_table=GCPsX_geojson_csv, out_featureclass=geocodedLink2450_XY, startx_field="X_Source", starty_field="Y_Source", endx_field="GeomX", endy_field="GeomY", line_type="GEODESIC", id_field="OBJECTID", spatial_reference="PROJCS['JGD_2000_Japan_Zone_8',GEOGCS['GCS_JGD_2000',DATUM['D_JGD_2000',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',138.5],PARAMETER['Scale_Factor',0.9999],PARAMETER['Latitude_Of_Origin',36.0],UNIT['Meter',1.0]];-450359962737.049 -450359962737.049 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision", attributes="ATTRIBUTES")

    # Process: Select "-"
    geocodedLink2450_GCP = "C:\\Users\\mapco\\Downloads\\work\\temp\\temp.gdb\\geocoded4link2450_GCP"
    arcpy.analysis.Select(in_features=geocodedLink2450_XY, out_feature_class=geocodedLink2450_GCP, where_clause="geocoded LIKE '%−%'")
    
    return()


def geref_warping(path4temp, filenum):
    arcpy.env.overwriteOutput = True
    
    #PolygonGroup_json = "C:\\Users\\mapco\\Downloads\\work\\temp\\geojson\\PolygonGroup2.json"
    PolygonGroup_json = path4temp + "geojson\\PolygonGroup" + filenum + ".json"
    geocoded4link2450_GCP = "geocoded4link2450_GCP"

    # Process: JSON To Features(conversion)
    PolygonGroup_JSONToFeatures = "C:\\Users\\mapco\\Downloads\\work\\temp\\temp.gdb\\PolygonGroup_JSONToFeatures"
    arcpy.conversion.JSONToFeatures(in_json_file=PolygonGroup_json, out_features=PolygonGroup_JSONToFeatures, geometry_type="POLYGON")

    # Process: Transform Features by SIMILARITY method
    resulttable = "C:\\Users\\mapco\\Downloads\\work\\temp\\resulttable"
    RMSE, PolygonGroup_JSONToFeatures_2_ = arcpy.edit.TransformFeatures(in_features=PolygonGroup_JSONToFeatures, in_link_features=geocoded4link2450_GCP, method="SIMILARITY", out_link_table=resulttable)

    # Process: Features To GeoJSON(conversion)
    output_polygongoup_geojson = "C:\\Users\\mapco\\Downloads\\work\\temp\\outputgeojsons\\outputpolygongoup.geojson"
    arcpy.conversion.FeaturesToJSON(in_features=PolygonGroup_JSONToFeatures_2_, out_json_file=output_polygongoup_geojson, format_json="NOT_FORMATTED", include_z_values="NO_Z_VALUES", include_m_values="NO_M_VALUES", geoJSON="GEOJSON", outputToWGS84="WGS84", use_field_alias="USE_FIELD_NAME")
    
    return()


def getallfilesinfolder(path):
	files = glob.glob(path) # カレントディレクトリ内のGCPsフォルダに入っているファイルをすべて選択
	for file in files:
		print(file)
		#makeLink4georef(file)
		folderpath4csv = os.path.dirname(file)
		folderpath4temp = folderpath4csv.rstrip("csv")
		targetfile_num = os.path.basename(file)
		targetfile_num = targetfile_num.rstrip(".geojson.csv")
		targetfile_num = targetfile_num.lstrip("GCPs")
		print(folderpath4temp, targetfile_num )
		geref_warping(folderpath4temp, targetfile_num)
		#getGeoJSONaddress(file)
	return()




if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\\Users\\mapco\\Downloads\\work\\temp\\temp.gdb", workspace=r"C:\Users\mapco\Downloads\work\temp\temp.gdb"):
        #makeLink4georef("C:\\Users\\mapco\\Downloads\\work\\temp\\csv\\GCPs2.geojson.csv")
        getallfilesinfolder("C:\\Users\\mapco\\Downloads\\work\\temp\\csv\\*.csv")


