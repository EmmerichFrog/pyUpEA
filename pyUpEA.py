import requests
import json
import shutil
from clint.textui import progress
import os
import re
import glob
from natsort import natsorted
import sys

def queryGithubLatestRelease(apiUrl):
    response = requests.get(apiUrl)
    print(response)
    responseJson = response.json()
    version = responseJson.get("tag_name")
    downloadLink = responseJson.get("assets")[0].get("browser_download_url")
    
    return version, downloadLink
 
def getGithubLatestRelease(url, path, version):
    r = requests.get(url, stream=True)
    pathFilename = os.path.join(path, "Yuzu_EA"+ version + ".AppImage")
    with open(pathFilename, 'wb') as f:
        totalLength = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=65536), expected_size=(totalLength/65536) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
    downloadedSize = os.stat(pathFilename).st_size
    print("Expected size:\t", totalLength)
    print("Actual size:\t", downloadedSize)
    try:
        os.remove(os.path.join(path, "yuzu.AppImage")) 
    except:
        print("No symlink, skipping deletion")    
    if totalLength == downloadedSize:            
        os.symlink(pathFilename, os.path.join(path, "yuzu.AppImage"))   
        print("Creating symlink")
    else:
        print("Size mismatch")

def currentVersionCheck(latestVersion, downloadUrl):
    allAppimages = natsorted((glob.glob(os.path.join(path, "Yuzu_EA*.AppImage"))))
    for idx, i in enumerate(allAppimages):
        allAppimages[idx] = os.path.basename(allAppimages[idx])
    
    if allAppimages == []:
        latestAppimage = ""
        currentVersion = ""
    else:    
        latestAppimage = allAppimages[-1]
        currentVersion = "".join(re.findall("\d+", latestAppimage))
    
    latestVersion = "".join(re.findall("\d+", latestVersion))
    print(latestAppimage, currentVersion, latestVersion)
    
    if currentVersion == "":
        getGithubLatestRelease(downloadUrl, path, latestVersion)
    elif latestVersion > currentVersion:
        bkName = currentVersion + ".bak"
        shutil.move(os.path.join(path, latestAppimage), os.path.join(path, latestAppimage+".bak"))
        getGithubLatestRelease(downloadUrl, path, latestVersion)
    else:
        print("Up to date")

    
if __name__ == "__main__":
    apiUrl = "https://api.github.com/repos/pineappleEA/pineapple-src/releases/latest"
    
    try:
        path = sys.argv[1]
    except:
        path = os.getcwd()        
    if path == "":
        path = os.getcwd()
    print(path)
    
    try:
        returned = queryGithubLatestRelease(apiUrl)
    except:
        print("Can't connect")
        sys.exit(0)

    latestVersion = returned[0]
    downloadUrl = returned[1]
    
    currentVersionCheck(latestVersion, downloadUrl)
    