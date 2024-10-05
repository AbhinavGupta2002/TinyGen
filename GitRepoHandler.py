import shutil
import git
import re
import os

class GitRepoHandler:
    def __init__(self, repoUrl):
        self.repoUrl = repoUrl
        self.userName, self.repoName, self.dirName = self.__extractGithubInfo()
        self.repo = None
    
    def clone(self):
        self.__clearRepo()
        self.repo = git.Repo.clone_from(self.repoUrl, self.dirName)
    
    def getDiff(self):
        return self.repo.git.diff()
    
    def __extractGithubInfo(self):
        pattern = r'^(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+)(?:\.git)?$'
        match = re.match(pattern, self.repoUrl)
        if match:
            userName = re.sub(r'(?<!^)(?=[A-Z])', '_', match.group(1)).lower()
            repoName = re.sub(r'(?<!^)(?=[A-Z])', '_', match.group(2)).lower()
            return userName, repoName, userName + "_" + repoName
        else:
            raise ValueError("Invalid GitHub URL format.")

    def __clearRepo(self):
        if os.path.isdir(self.dirName):
            shutil.rmtree(self.dirName)