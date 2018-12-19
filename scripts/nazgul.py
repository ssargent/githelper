import glob
import os
import random

import fire
from prettytable import PrettyTable


class nazgul(object):
    """ A simple way of modifing files at random to break comparisons """

    def corrupt(self, directory, percent, textToAdd):
        searchPath = "{0}\**\*.cshtml".format(directory)
        files = glob.glob(searchPath, recursive=True)

        target = int(round(len(files) / percent))
        print("Found {} Files, Corrupting {}".format(len(files), target))

        x = PrettyTable()
        x.field_names = ["7h3 c0rrup73d"]
        x.align = 'l'

        for y in range(target):
            randIndex = random.randint(0, len(files) - 1)
            fileToCorrupt = files[randIndex]

            with open(fileToCorrupt, "a") as openFile:
                openFile.write(textToAdd)

            x.add_row([fileToCorrupt])

        print(x)


if __name__ == '__main__':
    fire.Fire(nazgul)
