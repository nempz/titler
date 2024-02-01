import os 
import shutil
import platform
import requests
import zipfile
from bs4 import BeautifulSoup

folder = input("Naziv foldera?: ")
serija = input("Ime serije?: ")


def main():
    folderPath = createFolder()
    findSubtitle(folderPath)
    
def createFolder():
    systemOS = platform.system()
    if systemOS == "Linux":
        folderName = f"/home/nempz/{folder}"
    elif systemOS == "Windows":
        folderName = f"E:\\movies\{folder}"
    else:
        print(f"Unsupported operating system: {systemOS}")
        return

    files = os.listdir(folderName)
    files.sort()

    for index, fileName in enumerate(files, start=1):
        if os.path.isfile(os.path.join(folderName, fileName)):
            newFolderPath = os.path.join(folderName, f"Epizoda {index}")
            
            # Create a folder
            os.mkdir(newFolderPath)

            # Copy the file to the new folder
            shutil.move(os.path.join(folderName, fileName), newFolderPath)

    return folderName

def findSubtitle(folderPath):
    currentPage = 1

    while True:
        searchUrl = f"https://rs.titlovi.com/prevodi/?prevod={serija}&pg={currentPage}"
        response = requests.get(searchUrl)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            subtitleLinks = soup.select(".subtitleContainer [data-id]")

            if subtitleLinks:
                for index, link in enumerate(subtitleLinks, start=1):
                    dataID = link["data-id"]
                    episodeInfo = link.select_one(".s0xe0y").get_text(strip=True)
                    print(f"{index}. data-id: {dataID}, {episodeInfo}")

                print("0. Sledeca strana")
                print("-1. Zavrsi pretragu")

                choiceIndex = getUserChoice(len(subtitleLinks))
                if choiceIndex == 0:
                    currentPage += 1
                elif choiceIndex == -1:
                    break
                elif 1 <= choiceIndex <= len(subtitleLinks):
                    chosenSubtitle = subtitleLinks[choiceIndex - 1]["data-id"]
                    subtitleDownload(chosenSubtitle, folderPath) 
                    break
                else:
                    print("Nevazeci izbor. Pokusajte ponovo.")
            else:
                print("Titl nije pronadjen")
                break
        else:
            print(f"Titl nije pronadjen. HTTP Status Code: {response.status_code}")
            break


def getUserChoice(maxIndex):
    while True:
        try:
            choiceIndex = int(input("Odaberite titl (Unesite redni broj ili 0 za sledecu stranicu, -1 za izlaz.): "))
            if -1 <= choiceIndex <= maxIndex:
                return choiceIndex
            else:
                print("Nevazeci izbor. Pokusajte ponovo.")
        except ValueError:
            print("Nevazeci unos. Unesite broj.")
    


def subtitleDownload(subID, folderPath):
    subtitleUrl = f"https://rs.titlovi.com/download/?type=1&mediaid={subID}"
    
    downloadsFolder = os.path.expanduser("~" + os.sep + "Downloads")
    
    zipFilePath = os.path.join(downloadsFolder, f"{serija}_subtitles.zip")
    
    response = requests.get(subtitleUrl)

    if response.status_code == 200:
        with open(zipFilePath, "wb") as zip_file:
            zip_file.write(response.content)

        unzipSubtitle(zipFilePath, folderPath)
    else:
        print(f"Neuspesno preuzimanje titla. HTTP Status Code: {response.status_code}")
    
    
def unzipSubtitle(zipFilePath, extractFolder):
    os.makedirs(extractFolder, exist_ok=True)

    with zipfile.ZipFile(zipFilePath, "r") as zip_ref:
        zip_ref.extractall(extractFolder)

    print(f"Titl uspesno raspakovan u: {extractFolder}")


if __name__ == "__main__":
    main()