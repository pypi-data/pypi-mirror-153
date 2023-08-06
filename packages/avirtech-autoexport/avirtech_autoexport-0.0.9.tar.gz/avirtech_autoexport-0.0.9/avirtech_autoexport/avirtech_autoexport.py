import Metashape
import csv,math, os
from os import walk
from sys import path
from posixpath import split
import datetime, shutil
from datetime import datetime
from generate_report_1.generate_report_1 import create_csv
from generate_report_2.generate_report_2 import generate_report_2
from copy_camera_accuracy.copy_camera_accuracy import copy_camera_accuracy
# from copy_camera_accuracy.camera_acc_copy import copy_camera_accuracy
from generate_merge_report_camera.generate_merge_report_camera import generate_merge_report_camera
from making_directory.making_directory import making_directory
from copy_camera_selected.copy_camera_selected import copy_selected_foto
from process_foto.process_foto import process_foto
from generate_log_raw_petak.generate_log_raw_petak import generate_log_raw_petak
import configparser
import random
from genericpath import isdir
from pathlib import Path
import win32con, win32api
import copy
from os.path import exists


class autoexport:
    """
    This is a testing script for generate autoexport using Metashape, please make sure your chunk has a generated name so it can be processed automatically"""

    def __init__(self) -> None:
        pass
    
    def declare_doc_metashape():
        global doc
        doc = Metashape.app.document
        global chunk
        chunk = doc.chunk

    def get_project_name():
        # document_name = doc
        pars_document_name = str(doc).split(" ")
        get_project_name = pars_document_name[int(len(pars_document_name))-1].split("/")
        global project_name
        project_name = get_project_name[len(get_project_name)-1].replace(".psx'>","")
        print(project_name)
        
    def get_export_data():
        global path_ekspor
        path_ekspor = Metashape.app.getExistingDirectory("Hasil Ekspor")

    def generating_auto_orthomosaic():
        if path_ekspor == "":
            Metashape.app.messageBox("Pilih Direktori Terlebih Dahulu")
        else:
            chunks_list = []

            for chunk in doc.chunks:
                chunks_list.append(chunk)
            
            for chunk in chunks_list:
                index = chunks_list.index(chunk)
                doc.chunk = doc.chunks[index]
                keyids = []
                chunk_name = str(chunk).split(" ")
                chunk_name_real = chunk_name[1].replace(">","")
                chunk_name_real_2 = chunk_name_real.replace("'","")
                chunk_split = chunk_name_real_2.split("_")

                keyids.append(chunk_split[2:len(chunk_split)])

                keyids_2 = []
                for key in keyids[0]:
                    keyids_2.append(key)
                            
                keyids_2_distinct = list(set(keyids_2))

                shape_raw = []
                for shape in chunk.shapes:
                    shape.label = shape.attributes["Keyid"]
                    shape_raw.append(str(shape).replace("<Shape ","").replace(">","").replace("'",""))

                shape_double_raw = []
                for raw in shape_raw:
                    if shape_raw.count(raw) > 1:
                        shape_double_raw.append(raw)

                distinct_shape_raw = list(set(shape_raw))

                distinct_shape_double_raw = list(set(shape_double_raw))

                for i in distinct_shape_double_raw:
                    distinct_shape_raw.remove(i)

                shape_single_process = []
                shape_double_process = []
                for r in keyids_2_distinct:
                    for p in distinct_shape_raw:
                        if r == p:
                            shape_single_process.append(p)

                    for d in distinct_shape_double_raw:
                        if r == d:
                            shape_double_process.append(d)

                for shape in chunk.shapes:
                    for single in shape_single_process:
                        # #Get Plot Number (Nama Petak)
                        plot_no = shape.attributes["Keyid"]
                        
                        #Get atribut species
                        plant_spec = shape.attributes["Species"]

                        #Get district code
                        district_code = plot_no[0:3]

                        #Get datetimes
                        datetimes = []
                        for camera in chunk.cameras:
                            time = camera.photo.meta['Exif/DateTimeOriginal']
                            if time is None:
                                datetime_name = 'tidak_ada_datetime'
                            else:
                                time_split = time.split(" ")
                                date_only = time_split[0]
                                file_date = datetime.strptime(date_only, "%Y:%m:%d")
                                get_date = date_only.replace(":","")
                                get_hour = time_split[1].replace(":","")
                                hour_time = get_hour[0:4]
                                get_datetime = get_date + hour_time
                                datetimes.append(get_datetime)
                                datetime_name = datetimes[0]
                        
                        #Get chunk name
                        chunk_name = str(chunk).split(" ")
                        chunk_name_real = chunk_name[1].replace(">","")
                        chunk_name_real_2 = chunk_name_real.replace("'","")
                        chunk_split =  chunk_name_real_2.split("_")

                        #Get Flight Code and region code
                        flight_code = chunk_split[0]
                        region_code = chunk_split[1]

                        #Get start date and end date
                        start_date = datetime.strptime(shape.attributes["UAV_Start"],"%m/%d/%Y")
                        end_date = datetime.strptime(shape.attributes["UAV_End"], "%m/%d/%Y")
                        plant_date = datetime.strptime(shape.attributes["Plant_Date"], "%m/%d/%Y")

                        #Get file_name with some conditions
                        if datetime_name == 'tidak_ada_datetime':
                            file_name = "\\" + "data_tidak_memiliki_datetime_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB"
                        elif file_date >= start_date and file_date <= end_date:
                            file_name = "\\" + flight_code + '_' + datetime_name + "_" + region_code + "_" + district_code + "_" + plot_no + "_RGB"
                        else:
                            file_name = "\\" + "date_and_time_raw_foto_tidak_sesuai_dengan_window_akuisisi_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB"
                        format_file = ".tif"

                        #Logic GSD
                        gsd=10

                        plant_date = datetime.date(plant_date)

                        file_date = datetime.date(file_date)

                        delta = file_date - plant_date

                        umur = delta.days

                        print("Umur Tanaman",umur)

                        print("File Date :",file_date)

                        print("Plant Date :",plant_date)


                        if plant_spec == "ACRA":
                            if umur < 40 :
                                gsd = 0.01
                            elif umur < 91 :
                                gsd = 0.02
                            else:
                                gsd = 0.04
                        elif umur <= 90 :
                            gsd = 0.02
                        else:
                            gsd = 0.04
                        
                        if gsd == 10:
                            Metashape.app.messageBox("GSD Calculation Error")
                        else:
                            if plot_no == single:
                                compression = Metashape.ImageCompression()

                                compression.tiff_big = True

                                shape.boundary_type = Metashape.Shape.BoundaryType.OuterBoundary

                                chunk.exportRaster(path_ekspor + "\\" + file_name+format_file,image_compression=compression,image_format=Metashape.ImageFormat.ImageFormatTIFF,resolution_x=gsd, resolution_y=gsd, save_alpha=False, white_background=True, nodata_value=0)

                                shape.boundary_type = Metashape.Shape.BoundaryType.NoBoundary

                for shape in chunk.shapes:
                    for double in shape_double_process:
                        #Get Plot Number (Nama Petak)
                        plot_no = shape.attributes["Keyid"]

                        #Get atribut species
                        plant_spec = shape.attributes["Species"]

                        #Get district code
                        district_code = plot_no[0:3]

                        #Get datetimes
                        datetimes = []
                        for camera in chunk.cameras:
                            time = camera.photo.meta['Exif/DateTimeOriginal']
                            if time is None:
                                datetime_name = 'tidak_ada_datetime'
                            else:
                                time_split = time.split(" ")
                                date_only = time_split[0]
                                file_date = datetime.strptime(date_only, "%Y:%m:%d")
                                get_date = date_only.replace(":","")
                                get_hour = time_split[1].replace(":","")
                                hour_time = get_hour[0:4]
                                get_datetime = get_date + hour_time
                                datetimes.append(get_datetime)
                                datetime_name = datetimes[0]
                                    
                        #Get chunk name
                        chunk_name = str(chunk).split(" ")
                        chunk_name_real = chunk_name[1].replace(">","")
                        chunk_name_real_2 = chunk_name_real.replace("'","")
                        chunk_split =  chunk_name_real_2.split("_")

                        #Get Flight Code and region code
                        flight_code = chunk_split[0]
                        region_code = chunk_split[1]

                        #Get start date and end date
                        start_date = datetime.strptime(shape.attributes["UAV_Start"],"%m/%d/%Y")
                        end_date = datetime.strptime(shape.attributes["UAV_End"], "%m/%d/%Y")
                        plant_date = datetime.strptime(shape.attributes["Plant_Date"], "%m/%d/%Y")

                        #Get file_name with some conditions
                        if datetime_name == 'tidak_ada_datetime':
                            file_name = "\\" + "data_tidak_memiliki_datetime_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB"
                        elif file_date >= start_date and file_date <= end_date:
                            file_name = "\\" + flight_code + '_' + datetime_name + "_" + region_code + "_" + district_code + "_" + plot_no + "_RGB"
                        else:
                            file_name = "\\" + "date_and_time_raw_foto_tidak_sesuai_dengan_window_akuisisi_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB"
                        format_file = ".tif"

                        #Logic GSD
                        gsd=10

                        plant_date = datetime.date(plant_date)

                        file_date = datetime.date(file_date)

                        delta = file_date - plant_date

                        umur = delta.days

                        print("Umur Tanaman",umur)

                        print("File Date :",file_date)

                        print("Plant Date :",plant_date)


                        if plant_spec == "ACRA":
                            if umur < 40 :
                                gsd = 0.01
                            elif umur < 91 :
                                gsd = 0.02
                            else:
                                gsd = 0.04
                        elif umur <= 90 :
                            gsd = 0.02
                        else:
                            gsd = 0.04
                        
                        if gsd == 10:
                            Metashape.app.messageBox("GSD Calculation Error")
                        else:
                            if plot_no == double:
                                compression = Metashape.ImageCompression()

                                compression.tiff_big = True
                                
                                shape.boundary_type = Metashape.Shape.BoundaryType.OuterBoundary

                                chunk.exportRaster(path_ekspor + "\\" + file_name+format_file,image_compression=compression,image_format=Metashape.ImageFormat.ImageFormatTIFF,resolution_x=gsd,resolution_y=gsd,save_alpha=False,white_background=True,nodata_value=0)

    def processing_external_lib():
        def point_inside(point, poly):
            x, y = point.x, point.y
            inside = False
            p1x, p1y = poly[0]
            for i in range(len(poly) + 1):
                p2x, p2y = poly[i % len(poly)]
                if y >= min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y
            return inside
        
        chunks_list_raw = []
        global chunks_list_first
        chunks_list_first = []

        doc = Metashape.app.document
        chunk = doc.chunk
        
        for chunk in doc.chunks:
            chunks_list_raw.append(chunk)
            chunk_split = str(chunk).split(" ")
            get_chunk_name = chunk_split[len(chunk_split)-1].replace("'","").replace(">","")
            chunks_list_first.append(get_chunk_name)

        # print(chunks_list_first)
        rows = []
        global src_raw_foto
        src_raw_foto = []

        for chunk in chunks_list_first:
            index = chunks_list_first.index(chunk)

            doc.chunk = doc.chunks[index]

            csv_message_show = "Silahkan pilih log csv dari chunk " + str(chunk)

            foto_message_show = "Silahkan pilih direktori penyimpanan foto dari chunk " + str(chunk)

            Metashape.app.messageBox(csv_message_show)

            csv_hint = "Specify CSV Log from " + str(chunk)
            path = Metashape.app.getOpenFileName(hint = csv_hint)

            Metashape.app.messageBox(foto_message_show)

            raw_foto_hint = "Pilih Direktori Penyimpanan Foto Raw from " + str(chunk)

            src_path = Metashape.app.getExistingDirectory(hint=raw_foto_hint)

            #Adjust src path
            chunk_src = str(chunk) + "-" + str(src_path)
            src_raw_foto.append(chunk_src)

            #Adjust CSV Rows
            file = open(path)
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            rows_percsv = []
            for row in csv_reader:
                row.append(chunk)
                rows_percsv.append(row)
            rows.extend(rows_percsv)

        #Making Directory
        global shapes_name
        shapes_name = []
        for shape_name in chunks_list_first:
            split = str(shape_name).split("_")
            shapes_name.append(list(set(split[2:len(split)])))

        chunk_shape_dictionary = dict(zip(chunks_list_first,shapes_name))

        making_directory.making_directory(path_ekspor,chunks_list_first,chunk_shape_dictionary)
        
        if path_ekspor == "":
            Metashape.app.messageBox("Pilih Direktori Penyimpanan")
        else:
            global chunks_list
            chunks_list = []
            reports = []

            for chunk in doc.chunks:
                chunks_list.append(chunk)
            
            for chunk in chunks_list:
                index = chunks_list.index(chunk)

                doc.chunk = doc.chunks[index]
                global chunk_name_fix
                chunk_name_fix = str(doc.chunk).replace("<Chunk ","").replace("'","").replace(">","")

                #Generating keyids
                keyids = []
                chunk_name = str(chunk).split(" ")
                chunk_name_real = chunk_name[1].replace(">","")
                # global chunk_name_real_2
                chunk_name_real_2 = chunk_name_real.replace("'","")
                chunk_split = chunk_name_real_2.split("_")

                keyids.append(chunk_split[2:len(chunk_split)])

                # global keyids_distinct
                keyids_distinct = list(set(keyids[0]))
                
                for shape in chunk.shapes:
                    plot_no = shape.attributes["Keyid"]
                    for i in keyids_distinct:
                        if plot_no == i:
                            shape.selected = True
                            
                doc = Metashape.app.document
                chunk = doc.chunk
                shapes = chunk.shapes
                crs = shapes.crs
                T = chunk.transform.matrix
                polygons = dict()

                camera_keyid_selected= []

                flight_code = chunk_split[0]
                region_code = chunk_split[1]
                
                for shape in shapes:
                    if not shape.selected:
                        continue
                    if shape.type == Metashape.Shape.Polygon:
                        polygons[shape] = [[v.x,v.y] for v in shape.vertices]
                    
                for camera in chunk.cameras:
                    camera.selected = False
                    if not camera.transform:
                        if camera.reference.location:
                            camera_coord = crs.project(chunk.crs.unproject(camera.reference.location))
                        else:
                            continue
                    else:
                        camera_coord = crs.project(T.mulp(camera.center))
                    for shape in polygons.keys():
                        shape.label = shape.attributes["Keyid"]
                        shape_name = shape.label
                        if point_inside(Metashape.Vector([camera_coord.x, camera_coord.y]), polygons[shape]):
                            camera.selected = True
                            #Getting camera_name
                            if camera.selected:
                                camera_name = camera
                                new_name = str(chunk_name_fix) + "-" + str(shape_name) + "-" + str(camera_name) + "-" + str(camera.reference.location)
                                camera_keyid_selected.append(new_name)

                #Generate Report 2
                for shape in chunk.shapes:
                    for keyid in keyids[0]:
                        plot_no = shape.attributes["Keyid"]

                        if plot_no == keyid:
                            uav_start = shape.attributes["UAV_Start"]

                            uav_end = shape.attributes["UAV_End"]

                            plant_date_raw = shape.attributes["Plant_Date"]

                            plant_date = datetime.strptime(shape.attributes["Plant_Date"],"%m/%d/%Y")

                            plant_date_time = datetime.date(plant_date)

                            datetimes = []
                            for camera in chunk.cameras:
                                time = camera.photo.meta['Exif/DateTimeOriginal']
                                if time is None:
                                    datetime_name = 'tidak_ada_datetime'
                                else:
                                    time_split = time.split(" ")
                                    date_only = time_split[0]
                                    global file_date
                                    file_date = datetime.strptime(date_only, "%Y:%m:%d")
                                    get_date = date_only.replace(":","")
                                    get_hour = time_split[1].replace(":","")
                                    hour_time = get_hour[0:4]
                                    get_datetime = get_date + hour_time
                                    datetimes.append(get_datetime)
                                    datetime_name = datetimes[0]   
                                    file_dates = datetime.date(file_date)

                            delta = file_date - plant_date

                            umur = delta.days

                            plant_spec = shape.attributes["Species"]

                            gsd = 10

                            if plant_spec == "ACRA":
                                if umur < 40 :
                                    gsd = 0.01
                                elif umur < 91 :
                                    gsd = 0.02
                                else:
                                    gsd = 0.04
                            elif umur <= 90 :
                                gsd = 0.02
                            else:
                                gsd = 0.04
                    
                            #Get chunk name
                            chunk_name = str(chunk).split(" ")
                            chunk_name_real = chunk_name[1].replace(">","")
                            chunk_name_real_2 = chunk_name_real.replace("'","")
                            chunk_split =  chunk_name_real_2.split("_")

                            #Get Flight Code and region code
                            flight_code = chunk_split[0]
                            region_code = chunk_split[1]
                    
                            #Get district code
                            district_code = plot_no[0:3]

                            start_date = datetime.strptime(shape.attributes["UAV_Start"],"%m/%d/%Y")
                            end_date = datetime.strptime(shape.attributes["UAV_End"], "%m/%d/%Y")

                            if datetime_name == 'tidak_ada_datetime':
                                filename = ("data_tidak_memiliki_datetime_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB")
                            elif file_date >= start_date and file_date <= end_date:
                                filename = (flight_code + '_' + datetime_name + "_" + region_code + "_" + district_code + "_" + plot_no + "_RGB")
                            else:
                                filename = ("date_and_time_raw_foto_tidak_sesuai_dengan_window_akuisisi_" + region_code + "_" + district_code + "_" + plot_no + "_" + flight_code + "_RGB")
                            format_file = ".tif"
                            #Getting Error average
                            T = chunk.transform.matrix
                            crs = chunk.crs
                            sums = 0
                            num = 0
                            for camera in chunk.cameras:
                                if not camera.transform:
                                    continue
                                if not camera.reference.location:
                                    continue

                                estimated_geoc = chunk.transform.matrix.mulp(camera.center)
                                error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
                                error = error.norm()
                                sums += error**2
                                num += 1
                            error_avg = math.sqrt(sums / num)

                            report = chunk_name_real_2 + "-" + plot_no + "-" + uav_start + "-" + uav_end + "-" + plant_date_raw + "-" + str(umur) + "-" + plant_spec + "-" + str(gsd) + "-" +filename + format_file + "-" + str(error_avg)
                            reports.append(report)

                camera_keyid_distinct = list(set(camera_keyid_selected))
                chunk_name_list = []
                keyid_list = []
                camera_list = []

                for a in camera_keyid_distinct:
                    a_1 = a.split("-")

                    #appending chunk name list
                    chunk_name_list.append(a_1[0])

                    #appending keyid selected to list
                    keyid_list.append(a_1[1])

                    camera_list.append(a_1[2].replace(" ","").replace("<","").replace(">","").replace("'","").replace("Camera",""))
                # print(rows)
                create_csv.create_csv(path_ekspor,chunk_name_fix,camera_list, chunk_name_list,keyid_list,rows,chunk_name_real_2)
        #Processing Report 2
        reports_distinct = list(set(reports))
        for report in reports_distinct:
            split_report = report.split("-")

        generate_report_2.create_report_log_petak(path_ekspor,reports_distinct)
        print("report 2 done")

    def copy_report():
        #Creating and Copy Data to specified folder
        directory = "Report Per Chunk"
        copy_camera_accuracy.copy_camera_accuracy(path_ekspor,directory)

        generate_merge_report_camera.generate_merge_report_camera(path_ekspor, directory)
        substring = "prioritas_ketiga"

        copy_selected_foto.copy_selected_foto(path_ekspor,substring,src_raw_foto,chunks_list_first)

        chunks_list = []
        for chunk in doc.chunks:
            chunk_name = str(chunk).replace("<Chunk ","").replace("'","").replace(">","")
            chunks_list.append(chunk_name)

        shapes_name = []
        for shape_name in chunks_list:
            name_shape = shape_name.split("_")
            shapes_name.append(list(set(name_shape[2:len(name_shape)])))

        chunk_shape_dictionary = dict(zip(chunks_list,shapes_name))
        print(chunk_shape_dictionary)

        process_foto.process_foto(path_ekspor,chunk_shape_dictionary)

        generate_log_raw_petak.generate_log_raw_petak(path_ekspor,chunk_shape_dictionary)

        substring_last = "prioritas_ketiga"

        for file in os.listdir(path_ekspor):
            if file.find(substring_last) != -1:
                os.remove(os.path.join(path_ekspor,file))
    
    def mycmd():
        sample_set = {123, 234, 789}
        keygen = random.choice(tuple(sample_set))
        command = "avirkey /v:{}".format(keygen)
        os.system('cmd /c "cd C:\\Users\\Dell\\Documents\\Avirtech\\Avirkey"')
        os.system('cmd /c "{}"'.format(command))

    def run_process():
        location = os.path.expanduser('~/Documents/Avirtech/Avirkey/Avirkey.ini')
        
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

        win32api.SetFileAttributes(path_move,win32con.FILE_ATTRIBUTE_HIDDEN)

        file_moved = os.path.join(path_move,"Avirkey.ini")

        path = Path(file_moved)

        win32api.SetFileAttributes(location,win32con.FILE_ATTRIBUTE_HIDDEN)

        if path.is_file():
            if len(os.listdir(path_move) ) == 1:
                for file in os.listdir(location_app):
                    if file == "avirkey.exe":
                        autoexport.mycmd()

                        config = configparser.ConfigParser()
                        config.read(os.path.expanduser('~/Documents/Avirtech/Avirkey/avirkey.ini'))

                        serial = config.get("SECURITY","Serial")
                        hashed_serial = config.get("SECURITY","Hash")

                        if serial is not None:
                            if (hashed_serial == "BCED2A448DE179DD2940BD76AE29B4C2") or (hashed_serial == "77AD3616F9FDBFBA0FAE4A814ECA5D72") or (hashed_serial == "BBE292E1FE6A3CE9604A4B267A1F7822"):
                                autoexport.declare_doc_metashape()
                                autoexport.get_export_data()
                                autoexport.processing_external_lib()
                                autoexport.generating_auto_orthomosaic()
                                autoexport.copy_report()
                            else:
                                Metashape.app.messageBox("Wrong Credential Key, Cannot Continue Process")
                    elif file == "serial.exe":
                        pass
                    else:
                        Metashape.app.messageBox("Apparently, You don't have avirkey on your device, install and generate your serial number first!")
            elif len(os.listdir(location) ) == 0:
                Metashape.app.messageBox("Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
            else:
                Metashape.app.messageBox("Cannot Run The Script, please register your hardware ID then input your serial number and run the script.")
        else:
            Metashape.app.messageBox("Cannot Run The Script, Please install avirkey first, generate your serial number and then run this script again.")