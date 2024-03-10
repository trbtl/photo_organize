
# 1 - Import
import os
import shutil
import hashlib
from datetime import datetime
from PIL import Image
import PySimpleGUI as sg

source_folder = ""
target_folder = ""


def get_best_date(file_path):
    exif_date = None
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                date_str = exif_data[36867].strip()  # Remove leading/trailing whitespace
                if date_str:
                    exif_date = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except (IOError, AttributeError, KeyError, ValueError):
        pass
    
    file_date = datetime.fromtimestamp(os.path.getctime(file_path))
    
    return exif_date or file_date

def copy_photos_by_best_date(window, source_folder, target_folder, method):
    text_stream = ""
    xDate = datetime.now()
    xYear = xDate.year
    xMonth = xDate.month
    xDay = xDate.day
    xHour = xDate.hour
    xMinute = xDate.minute 
    xSecond  = xDate.second
    activityFile = target_folder +  "Activity"  + str(xYear) + str(xMonth) + str(xDay) + str(xHour) + str(xMinute)  + str(xSecond) + ".txt"
    # Define the file path with the path to your text file
    txtfile_path = "skipped_files.txt"
    # List of file extensions to process
    extensions_to_process = ['jpg', 'jpeg', 'bmp', 'gif', 'png', '.heic']
    # Add your logic for processing files with the current file_extension
    for root, _, files in os.walk(source_folder):
        for file in files:

            # event, values = window.read()
            # if event == '_CANCEL_KEY_':
            #     break
            # elif event == None:
            #     pass

            # Get the file extension from the file
            file_extension = os.path.splitext(file)[1][1:].lower()
            # Check if the file extension is in the list of extensions to process
            if file_extension in extensions_to_process:
                # print(file)
                file_path = os.path.join(root, file)
                best_date = get_best_date(file_path)
                year = best_date.year
                # convert the month number to month string 
                if best_date.month == 1:
                    month = "January"
                elif best_date.month == 2:
                    month = "Feburary"
                elif best_date.month == 3:
                    month = "March"
                elif best_date.month == 4:
                    month = "April"
                elif best_date.month == 5:
                    month = "May"
                elif best_date.month == 6:
                    month = "June"
                elif best_date.month == 7:
                    month = "July"
                elif best_date.month == 8:
                    month = "August"
                elif best_date.month == 9:
                    month = "September"
                elif best_date.month == 10:
                    month = "October"
                elif best_date.month == 11:
                    month = "November"
                elif best_date.month == 12:
                    month = "December"
                else:
                    month = best_date.month
                day = best_date.day
                # build the destination folder structure 
                destination_folder = os.path.join(target_folder, str(year), str(month), str(day))

                # check if the two files have the same file name, do they have the same file contents 
                if os.path.exists(os.path.join(destination_folder, file)):
                    print("Hashing: -->" + file_path)
                    # get the hash of the source file 
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    # get the hash of the destination duplicate file
                    destination_file_path = os.path.join(destination_folder, file)
                    with open(destination_file_path, 'rb') as df:
                        destination_file_hash = hashlib.sha256(df.read()).hexdigest()
                    # if they have the same content, rename the source file 
                    if file_hash == destination_file_hash:
                      file = "_" + file

                # one last check for duplicate file names
                if not os.path.exists(os.path.join(destination_folder, file)):
                    # print(os.path.join(destination_folder, file))
                    try:
                        os.makedirs(destination_folder, exist_ok=True)
                        # copy or move
                        if method == 'True':
                            # copy
                            shutil.copy(file_path, os.path.join(destination_folder, file))
                            print("Copied file: ", os.path.join(destination_folder, file))
                            with open(activityFile, 'a') as fActivity:
                            # add the filename to the text file
                                fActivity.write("Copied file: " + file_path.replace("/","\\") + "\n    -->  " + destination_folder.replace("/","\\") + "\\" + file + "\n")
                            text_stream = "Copied file: " + file_path.replace("/","\\") + "\n    -->  " + destination_folder.replace("/","\\") + "\\" + file + "\n" + text_stream
                        else:
                            # move
                            shutil.move(file_path, os.path.join(destination_folder, file))
                            print("Moved file: ", os.path.join(destination_folder, file))
                            with open(activityFile, 'a') as fActivity:
                            # add the filename to the text file
                                fActivity.write("Moved file: " + file_path.replace("/","\\") + "\n    -->  " + destination_folder.replace("/","\\") + "\\" + file + "\n")
                            text_stream = "Moved file: " + file_path.replace("/","\\") + "\n    -->  " + destination_folder.replace("/","\\") + "\\" + file + "\n" + text_stream
                        # update the multiline display 
                        window["-TEXT-"].update(text_stream)
                        window.refresh ()
                    except (IOError, AttributeError, KeyError, ValueError):
                        # Open the file in append mode ('a'). This will create the file if it doesn't exist or append to its content if it does
                        with open(txtfile_path, 'a') as f:
                            # add the filename to the text file
                            f.write(file_path + '\n    -->  ' + IOError + ', ' + AttributeError + ', ' +  KeyError + ', ' +  ValueError + '\n') 
                        # add the filename to the activityFile file
                        with open(activityFile, 'a') as fActivity:
                            fActivity.write("Skipped file: " + file_path.replace("/","\\") + "  -->  Already exists!\n")
                        # skip the file that errored and continue on
                        pass
                else:
                    print("Skipping: " + os.path.join(destination_folder, file).replace("/","\\")  +  ' -->  Already exists!')
                    # add the filename to the text file
                    with open(txtfile_path, 'a') as f:
                        f.write("Skipped file: " + file_path.replace("/","\\") + "  -->  Already exists!\n")  # Ensure a newline character for separate lines
                    # add the filename to the activityFile file
                    with open(activityFile, 'a') as fActivity:
                        fActivity.write("Skipped file: " + file_path.replace("/","\\") + "  -->  Already exists!\n")
                    # update the multiline display
                    text_stream = "Skipped file: " + file_path.replace("/","\\") + "\n    -->  Already exists!\n" + text_stream
                    window["-TEXT-"].update(text_stream)  
                    window.refresh ()

        window["-TEXT-"].update("\nDone!\n\n" + text_stream)
        window.refresh ()                   
 
def main():
    # 2 - Layout
    sg.theme('SystemDefault1')
    layout = [
                [sg.Text('Enter source folder:')],
                [sg.In(size=(70, 1), enable_events=True, key="_SOURCE_FOLDER_"), sg.FolderBrowse()],
                [sg.Radio('Copy files', 'group1', size=(12, 1), key='_R1_', default=True), 
                 sg.Radio('Move files', 'group1', size=(12, 1), key='_R2_')],
                [sg.Text('Enter destination folder:')],
                [sg.In(size=(70, 1), enable_events=True, key="_DESTINATION_FOLDER_"), sg.FolderBrowse()],
                [sg.Button('Start', key='_START_KEY_', size=(12, 1)), 
                 sg.Button('Exit', key='_EXIT_KEY_', size=(12, 1)),
                 sg.Button('Cancel', key='_CANCEL_KEY_', size=(12, 1), visible=False)],
                [sg.Multiline(size=(80, 30), key="-TEXT-", do_not_clear=False)]
            ]

    # 3 - Window
    window = sg.Window('Photo Organizer', layout)
    
    # 4 - Event loop / handling
    while True:
        event, values = window.read()
        if event == '_START_KEY_':
            print(event, values)
            source_folder = str(values["_SOURCE_FOLDER_"])
            target_folder = str(values["_DESTINATION_FOLDER_"])
            method = str(values["_R1_"])
            if source_folder and target_folder:
                # window['_CANCEL_KEY_'].update(visible = True)
                copy_photos_by_best_date(window, source_folder, target_folder, method) 
                # window['_CANCEL_KEY_'].update(visible = False)
                # clear the source and destination fields
                source_folder = ""
                # target_folder = ""
                window["_SOURCE_FOLDER_"].update("")
                # window["_DESTINATION_FOLDER_"].update("")
                window.refresh ()
            else:
                sg.popup('Alert!', 'Please enter both "Source" and "Destination" folers!')

        if event == '_EXIT_KEY_' or event == sg.WIN_CLOSED:
            # out of the loop
            break  

    # 5 - Close
    window.close()

if __name__ == '__main__':
    main()
