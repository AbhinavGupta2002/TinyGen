from pathlib import Path
import promptFunctions
import imghdr

def getFiles(dirName, fileContent):
    for filePath in Path(dirName).iterdir():
        if filePath.is_file():
            with open(filePath, 'r', encoding='latin-1') as file:
                if imghdr.what(str(filePath)) is None: # filter out images
                    fileContent[str(filePath)] = file.read()
        else:
            filePath.name != ".git" and getFiles(filePath, fileContent) # ignore files under .git

def modifyFiles(files):
    for fileData in files:
        with open(fileData.name, 'w') as file:
            file.write(fileData.content)

def isValidFileNames(allFiles, modifiedFiles):
    for file in modifiedFiles:
        if not file.name in allFiles:
            return False
    return True

def updateFileContent(allFiles, modifiedFiles):
    for file in modifiedFiles:
        allFiles[file.name] = file.content

promptGenerator = {
    "getResponse": promptFunctions.getResponse,
    "getReflection": promptFunctions.getReflection,
    "getRevision": promptFunctions.getRevision
}