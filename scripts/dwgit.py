import ftplib
import glob
import os
import shutil
import uuid
import zlib
from pathlib import Path

import fire
from prettytable import PrettyTable


class dwgit(object):
    """ A simple tool for comparing dw to git 

        ./dwgit compare --dwdirectory=/path/to/your/dw/files/folder --gitdirectory=/path/to/your/git/files/folder

        - This will compare files on the disk.  

        ./dwgit ftpcompare --address=mysite.com --username=corey --password=cmft --serverpath=files --gitdirectory=/path/to/your/git/files/folder

        - This will ftp the files down and then do the disk based comparison.

        ./dwgit getFtpFile  

        - You cannot call this directly.

    """

    def ftpcompare(self, address, username, password, serverpath, gitdirectory, deleteWorkDir=True):
        searchPath = "{0}\**\*.*".format(gitdirectory)
        files = glob.glob(searchPath, recursive=True)
        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        workdir = os.path.join(currentDirectory, str(uuid.uuid4()))
        os.mkdir(workdir)
        ftp = ftplib.FTP(host=address)
        ftp.login(user=username, passwd=password)

        ftp.cwd(serverpath)
        print(workdir)
        for file in files:
            normalizedPath = file.replace(gitdirectory, "")
            self.getFtpFile(ftp, normalizedPath, workdir)

        ftp.quit()
        self.compare(workdir, gitdirectory)

        if(deleteWorkDir):
            shutil.rmtree(workdir)

    def getFtpFile(self, ftp, file, workdir):
        try:
            fileName = os.path.basename(file)
            fdirectory = os.path.dirname(file)
            localfileName = os.path.join(workdir, fdirectory[1:], fileName)

            if(os.path.exists(os.path.dirname(localfileName)) != True):
                os.makedirs(os.path.dirname(localfileName))
            ftp.cwd(fdirectory[1:])
            ftp.retrbinary("RETR " + fileName, open(localfileName, 'wb').write)
            ftp.cwd("/Files")
        except:
            print("Unable to find {}".format(file))

    def compare(self, dwdirectory, gitdirectory):
        searchPath = "{0}\**\*.*".format(gitdirectory)
        files = glob.glob(searchPath, recursive=True)
        print("Git Folder: {}".format(gitdirectory))
        print("DW Folder: {}".format(dwdirectory))

        x = PrettyTable()
        x.field_names = ["Differences"]
        x.align = 'l'
        dwFolder = Path(dwdirectory)

        for file in files:
            normalizedPath = file.replace(gitdirectory, "")
            dwPath = dwFolder / normalizedPath[1:]

            if dwPath.exists():
                with open(dwPath, 'rb') as dwFile:
                    dwFileSignature = zlib.adler32(dwFile.read())

            else:
                print("Looking for {} in {}".format(
                    normalizedPath, dwdirectory))
                dwFileSignature = -1
                break

            with open(file, 'rb') as gitFile:
                gitFileSignature = zlib.adler32(gitFile.read())

            if gitFileSignature != dwFileSignature:
                if dwFileSignature == -1:
                    normalizedPath = "{} [File Missing]".format(normalizedPath)
                x.add_row([normalizedPath])

        print(x)


if __name__ == '__main__':
    fire.Fire(dwgit)
