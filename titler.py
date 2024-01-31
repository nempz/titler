import os 
import shutil
import platform

from bs4 import BeautifulSoup

serija = input("Ime serije?: ")

def main():
    createFolder()
    

def createFolder():
    systemOS = platform.system()
    if systemOS == "Linux":
        folderName = f"/home/nempz/{serija}"
    elif systemOS == "Windows":
        folderName = f"E:\\movies\{serija}"
    else:
        print(f"Unsupported operating system: {systemOS}")
        return

    files = os.listdir(folderName) 
    for i in files:
        if os.path.isfile(os.path.join(folderName, i)):
            newFolderPath = os.path.join(folderName, i.split(".")[0])
            
            # Create a folder
            os.mkdir(newFolderPath)

            # Copy the file to the new folder
            shutil.move(os.path.join(folderName, i), newFolderPath)


if __name__ == "__main__":
    main()