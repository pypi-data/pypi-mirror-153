import arcpy
import os
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename

class autoexport_jp2:
    @staticmethod
    def autoexport_jp2():
        mxd = arcpy.mapping.MapDocument("Current")
        mxd.author = "Me"
        arcpy.env.workspace = "CURRENT"

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("showinfo","Please input your Palm Tree Plot")
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
# autoexport_jp2.autoexport_jp2()