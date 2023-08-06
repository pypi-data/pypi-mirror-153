import arcpy
import os
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename
from os.path import exists
import shutil,configparser

class autoexport_jp2:
    @staticmethod
    def autoexport_jp2():
        location = os.path.expanduser('~/Documents/Avirtech/Avirkey/Avirkey.ini')
        
        if exists(location):
            location_copied = "C:\\ProgramData\\"
            dir_name = "Microsoft_x64"

            location_app = "C:\\Program Files (x86)\\Avirtech\\Avirkey"

            path_move = os.path.join(location_copied,dir_name)

            if exists(path_move):
                shutil.rmtree(path_move)
            else:
                pass

            if os.path.isdir(path_move):
                pass
            elif not os.path.isdir(path_move):
                os.mkdir(path_move)

            shutil.copy(location,path_move)

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

                                root = tk.Tk()
                                root.withdraw()
                                messagebox.showinfo("showinfo","Please input your TIF File to Process")
                                tif_loc = filedialog.askdirectory()
                                root.destroy
                                # print(tif_loc)

                                for file in os.listdir(tif_loc):
                                    if file.endswith(".tif"):
                                        data_process = os.path.join(tif_loc,file)
                                        print("Add {} to layer".format(file))
                                        data_show = file
                                        arcpy.MakeRasterLayer_management(data_process,data_show,"",data_process)

                                directory = "jp2"
                                os.mkdir(os.path.join(tif_loc,directory))
                                for layer in arcpy.mapping.ListLayers(mxd):
                                    if (0.0099 <= arcpy.Describe(layer).children[0].meanCellHeight <= 0.011) and (0.0099 <= arcpy.Describe(layer).children[0].meanCellWidth <= 0.011):
                                        print("Processing {} to JP2000 format".format(layer))
                                        result = os.path.join(tif_loc,directory)
                                        source = os.path.join(tif_loc,str(layer))
                                        arcpy.env.nodata = "NONE"
                                        arcpy.env.compression = "JPEG2000 100"
                                        arcpy.RasterToOtherFormat_conversion(source,result,"JP2000")
                                    else:
                                        print("No File with GSD One on your folder")

                                if os.path.isdir(os.path.join(tif_loc, directory)):
                                    for file in os.listdir(os.path.join(tif_loc,directory)):
                                        if not file.endswith(".jp2"):
                                            os.remove(os.path.join(os.path.join(tif_loc,directory),file))

                                for dirpath, dirnames, filenames in os.walk(os.path.join(tif_loc,directory),topdown=False):
                                    if not dirnames and not filenames:
                                        os.rmdir(dirpath)
                            else:
                                messagebox.showinfo("showinfo","Wrong Credential Key, Cannot Continue Process")
# autoexport_jp2.autoexport_jp2()