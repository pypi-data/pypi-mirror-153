# Import arcpy module
import arcpy
import os
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename
import pandas as pd
import csv
from simpledbf import Dbf5
from os.path import exists
import random, shutil,configparser

class autocorrect:
    @staticmethod
    def process_all():
        location = os.path.expanduser('~/Documents/Avirtech/Avirkey/Avirkey.ini')
        
        if exists(location):
            location_copied = "C:\\ProgramData\\"
            dir_name = "Microsoft_x64"

            location_app = "C:\\Program Files (x86)\\Avirtech\\Avirkey"

            path_move = os.path.join(location_copied,dir_name)

            # if exists(path_move):
            #     shutil.rmtree(path_move)
            # else:
            #     pass

            if os.path.isdir(path_move):
                pass
            elif not os.path.isdir(path_move):
                os.mkdir(path_move)
            # try:
            #     shutil.copy(location,path_move)
            # except PermissionError:
            #     pass

            os.system("attrib +h " + path_move)

            file_moved = os.path.join(path_move,"Avirkey.ini")

            os.system("attrib +h " + file_moved)

            if exists(file_moved):
                if len(os.listdir(path_move) ) == 1:
                    for file in os.listdir(location_app):
                        if file == "avirkey.exe":
                            # sample_set = {123, 234, 789}
                            # keygen = random.choice(tuple(sample_set))
                            # command = "avirkey /v:{}".format(keygen)
                            # os.system('cmd /c "cd C:\\Users\\Dell\\Documents\\Avirtech\\Avirkey"')
                            # os.system('cmd /c "{}"'.format(command))

                            config = configparser.ConfigParser()
                            config.read(os.path.expanduser('~/Documents/Avirtech/Avirkey/avirkey.ini'))

                            serial = config.get("SECURITY","Serial")
                            # hashed_serial = config.get("SECURITY","Hash")

                            if serial is not None:
                                mxd = arcpy.mapping.MapDocument("Current")
                                mxd.author = "Me"
                                arcpy.env.workspace = "CURRENT"
                                df = arcpy.mapping.ListDataFrames(mxd)[0]

                                root = tk.Tk()
                                root.withdraw()
                                # file_selected = askopenfilename()
                                messagebox.showinfo("showinfo","Please input your Palm Tree Plot")
                                folder_plot = filedialog.askdirectory()
                                messagebox.showinfo("showinfo","Please insert Block and Layer Source Folder")
                                block_location = filedialog.askdirectory()
                                messagebox.showinfo("showinfo","Please insert folder to store result")
                                gdb_location = filedialog.askdirectory()

                                root.destroy

                                list_directory = ["merge_drone","last_result","geodatabase"]

                                merge_drone_loc = os.path.join(gdb_location,list_directory[0])
                                last_result = os.path.join(gdb_location,list_directory[1])
                                geodatabase_loc = os.path.join(gdb_location,list_directory[2])

                                fldName = "nama_blok"
                                fldNameReport = "Report CSV"

                                location_per_bloc = os.path.join(last_result,"Per Blok")

                                location_report_csv = os.path.join(last_result, fldNameReport)

                                os.mkdir(location_per_bloc)
                                os.mkdir(location_report_csv)

                                outputgdb = "pointdistance.gdb"
                                arcpy.CreateFileGDB_management(geodatabase_loc,outputgdb)

                                merge_csv = os.path.join(merge_drone_loc,"merge.csv")
                                merge_layer = "merge_layer"
                                fcname = "merge_rute_drone"

                                arcpy.MakeXYEventLayer_management(merge_csv, "x", "y", merge_layer, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")

                                arcpy.FeatureClassToFeatureClass_conversion(merge_layer, merge_drone_loc, fcname)

                                #Process Plot Shapefile
                                plotting_data = []

                                substring_plot = ".shp"
                                substring_plot_2 = ".xml"
                                substring_plot_3 = "DESKTOP"

                                for file in os.listdir(folder_plot):
                                    if file.find(substring_plot) != -1 and file.find(substring_plot_2) == -1 and file.find(substring_plot_3) == -1:
                                        base = os.path.splitext(file)[0]

                                        location_plot = os.path.join(folder_plot,file)

                                        new_layer = arcpy.mapping.Layer(location_plot)

                                        arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")

                                        plotting_data.append(base)

                                datas = []

                                for file in arcpy.mapping.ListLayers(mxd):
                                    datas.append(str(file))

                                datas.remove("merge_rute_drone")
                                datas.remove("merge_layer")
                                datas.sort()

                                ##Merge Data
                                titik_sawit_report = "\"" +";".join(datas) + "\""
                                result_titik_sawit = "titik_sawit_report"
                                output_titik_sawit = os.path.join(last_result,result_titik_sawit + ".shp")

                                arcpy.Merge_management(titik_sawit_report,output_titik_sawit)

                                output_buffer = os.path.join(geodatabase_loc,"buffer_titik_sawit_report")

                                arcpy.Buffer_analysis(result_titik_sawit, output_buffer, "1 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")

                                selection = arcpy.SelectLayerByLocation_management("merge_rute_drone", "INTERSECT", "buffer_titik_sawit_report", "", "NEW_SELECTION", "NOT_INVERT")

                                arcpy.CopyFeatures_management(selection,os.path.join(merge_drone_loc,"buffer_titik_sawit_report_selected.shp"))

                                #Next Step Dev
                                arcpy.Near_analysis("titik_sawit_report","buffer_titik_sawit_report_selected","2 Meters", "NO_LOCATION", "NO_ANGLE", "PLANAR")

                                arcpy.AddField_management("titik_sawit_report", "ket", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

                                arcpy.CalculateField_management("titik_sawit_report", "ket", "new_class( !NEAR_DIST! )", "PYTHON_9.3", "def new_class(x):\\n    if(x) == -1:\\n        return 2\\n    elif(x) > 0 and (x) <= 0.355:\\n        return 1\\n    else:\\n        return 0")

                                arcpy.AddXY_management(result_titik_sawit)

                                arcpy.TableToDBASE_conversion("titik_sawit_report", last_result)

                                df_titik_sawit_report = Dbf5(os.path.join(last_result,"titik_sawit_report" + ".dbf")).to_dataframe()

                                df_titik_sawit_report.to_csv(os.path.join(location_report_csv,"titik_sawit_report" + ".csv"))

                                print("Report for Titik Sawit Succesfully Generated, please check the last result folder")

                                #Process Drone Route

                                arcpy.AddJoin_management("buffer_titik_sawit_report_selected", "fid", "titik_sawit_report", "NEAR_FID", "KEEP_COMMON")

                                arcpy.FeatureClassToFeatureClass_conversion("buffer_titik_sawit_report_selected", last_result, "titik_drone_report")

                                arcpy.TableToDBASE_conversion("titik_drone_report", last_result)

                                df_titik_sawit_report = Dbf5(os.path.join(last_result,"titik_drone_report" + ".dbf")).to_dataframe()

                                df_titik_sawit_report.to_csv(os.path.join(location_report_csv,"titik_drone_report" + ".csv"))

                                print("Report for Rute Drone Succesfully Generated, please check the last result folder")

                                df = arcpy.mapping.ListDataFrames(mxd)[0]
                                datas = []
                                for file in arcpy.mapping.ListLayers(mxd):
                                    datas.append(str(file))

                                datas.remove("titik_drone_report")
                                datas.remove("titik_sawit_report")

                                for data in datas:
                                    for file in arcpy.mapping.ListLayers(mxd):
                                        if str(data) == str(file):
                                            arcpy.mapping.RemoveLayer(df,file)
                                        else:
                                            pass

                                substring_blok = ".shp"
                                substring_blok_2 = ".xml"
                                substring_blok_3 = "DESKTOP"
                                for file in os.listdir(block_location):
                                    if file.find(substring_blok) != -1 and file.find(substring_blok_2) == -1 and file.find(substring_blok_3) == -1:
                                        location_block = os.path.join(block_location,file)

                                        new_layer = arcpy.mapping.Layer(location_block)

                                        arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")
                                
                                titik_semprot_last = "titik_sawit_report"
                                batas_semprot = "BATAS_SEMPROT"
                                location = os.path.join(last_result,"spatial_join.shp")
                                arcpy.SpatialJoin_analysis(titik_semprot_last,batas_semprot,location)

                                fcName = "spatial_join"

                                mylist = list(set([str(row.getValue(fldName)) for row in arcpy.SearchCursor(fcName, fields=fldName)]))

                                for blok in mylist:
                                    spatial_join = "spatial_join"
                                    name_result = "report_sawit_{}".format(blok)
                                    location = location_per_bloc
                                    location_report = location_report_csv

                                    arcpy.MakeFeatureLayer_management(spatial_join,name_result,"\"nama_blok\" = '{}'".format(blok))

                                    arcpy.FeatureClassToShapefile_conversion(name_result, location)

                                    arcpy.TableToDBASE_conversion(name_result,location)

                                    df_report_csv = Dbf5(os.path.join(location,name_result + ".dbf"))
                                    df_report_csv.to_csv(os.path.join(location_report, name_result + ".csv"))
                                
                                data_blok_last = []
                                for file in arcpy.mapping.ListLayers(mxd):
                                    data_blok_last.append(str(file))
                                
                                data_blok_last.remove("titik_drone_report")
                                data_blok_last.remove("BATAS_SEMPROT")

                                for data in data_blok_last:
                                    for file in arcpy.mapping.ListLayers(mxd):
                                        if str(data) == str(file):
                                            arcpy.mapping.RemoveLayer(df,file)
                                        else:
                                            pass
                                
                                for file in os.listdir(location_per_bloc):
                                    if file.find(substring_blok) != -1 and file.find(substring_blok_2) == -1 and file.find(substring_blok_3) == -1:
                                        location_plot = os.path.join(location_per_bloc,file)
                                        new_layer = arcpy.mapping.Layer(location_plot)
                                        
                                        arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")
                                
                                data_for_symbology = []
                                for file in arcpy.mapping.ListLayers(mxd):
                                    data_for_symbology.append(str(file))
                                
                                data_for_symbology.remove("titik_drone_report")
                                data_for_symbology.remove("BATAS_SEMPROT")
                                # data_for_symbology.remove("spatial_join")

                                layer_source = []
                                for file in os.listdir(block_location):
                                    if file.endswith(".lyr"):
                                        layer_source.append(file)

                                location_layer_source = os.path.join(block_location,layer_source[0])

                                for symbology in data_for_symbology:
                                    updateLayer = arcpy.mapping.ListLayers(mxd,"{}".format(symbology),df)[0]
                                    sourceLayer = arcpy.mapping.Layer(location_layer_source)
                                    arcpy.mapping.UpdateLayer(df,updateLayer,sourceLayer,True)
                            else:
                                messagebox.showinfo("showinfo","Wrong Credential Key, Cannot Continue Process")
                        elif file == "serial.exe":
                            pass
                        else:
                            messagebox.showinfo("showinfo","Apparently, You don't have avirkey on your device, install and generate your serial number first!")
                elif len(os.listdir(location) ) == 0:
                    messagebox.showinfo("showinfo","Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
                else:
                    messagebox.showinfo("showinfo","Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
            else:
                messagebox.showinfo("showinfo","Cannot Run The Script, Please install avirkey first, generate your serial number and then run this script again.")
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("showinfo","You don't have Avirkey or maybe your Avirkey is not properly installed, please generate your serial number first!")
            root.destroy

autocorrect.process_all()