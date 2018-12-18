import fire
import glob
import hashlib
import zlib
from pathlib import Path
from prettytable import PrettyTable


class dwgit(object):
    """ A simple tool for comparing dw to git """

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
                dwFileSignature = -1

            with open(file, 'rb') as gitFile:
                gitFileSignature = zlib.adler32(gitFile.read()) 
                

            if gitFileSignature != dwFileSignature:
                if dwFileSignature == -1:
                    normalizedPath = "{} [File Missing]".format(normalizedPath)
                x.add_row([normalizedPath])
        
        print(x)


if __name__ == '__main__':
    fire.Fire(dwgit)
