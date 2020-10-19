import os
import hashlib
import csv


def gen_sha1(path, abspath=True):
    sha1 = hashlib.sha1()
    with open(path, 'rb') as hashFile:
        buffer = hashFile.read()
        sha1.update(buffer)
        if abspath is True:
            print(f'{os.path.abspath(path)} : {sha1.hexdigest()}')
            return os.path.abspath(path), sha1.hexdigest()
        else:
            print(f'{path} : {sha1.hexdigest()}')
            return path, sha1.hexdigest()


class dir_sum:
    def __init__(self, dir_path='.', gitignore=True, gitignore_path=None):
        self.dirPath = dir_path
        self.gitignorePath = gitignore_path
        self.gitignore = gitignore
        if gitignore_path is None:
            self.gitignorePath = os.path.join(dir_path, '.gitignore')


    def checksum_dir(self, csv_write, abspath, csv_filename):
        if self.gitignore:
            try:
                with open(self.gitignorePath, 'r') as ignoreFile:
                    ignoreList = ignoreFile.readlines()

                    for index, line in enumerate(ignoreList):
                        if line.startswith('#') or line == "\n":
                            del ignoreList[index]
                        ignoreList[index] = line.rstrip("\n")
                print(ignoreList)
            except FileNotFoundError:
                print(".gitignore Not Found")

        if csv_write:
            with open(f'{csv_filename}.csv', 'w+'):
                pass

        for item in os.listdir(self.dirPath):
            hashCheckCondition = False
            if self.gitignore:
                for ignoreItem in ignoreList:
                    if ignoreItem == item:
                        hashCheckCondition = True

            if hashCheckCondition:
                continue
            if not os.path.isdir(item):
                if abspath:
                    filePath = os.path.abspath(os.path.join(self.dirPath, item))
                else:
                    filePath = item
                try:
                    output = gen_sha1(os.path.join(self.dirPath, item), abspath)
                    if csv_write:
                        with open(f'{csv_filename}.csv', 'a') as csvFile:
                            csvWriter = csv.writer(csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            csvWriter.writerow(output)
                except PermissionError as e:
                    print(f"Error; Could not hash {filePath} : Permission Error")
                    print(e)


    def recursive_checksum_dir(self, csv_write, abspath, csv_filename):
        if csv_write:
            with open(f'{csv_filename}.csv', 'w+'):
                pass

        for root, subdir, files in os.walk(self.dirPath, topdown=True):
            for file in files:
                if abspath:
                    filePath = os.path.abspath(os.path.join(root, file))
                else:
                    filePath = (os.path.join(root, file))
                try:
                    output = gen_sha1(os.path.join(root, file), abspath)
                    if csv_write:
                        with open(f'{csv_filename}.csv', 'a') as csvFile:
                            csvWriter = csv.writer(csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            csvWriter.writerow(output)

                except PermissionError as e:
                    print(f"Error; Could not hash {filePath} : Permission Error")
                    print(e)


if __name__ == '__main__':
    Tracer = dir_sum('D:\\PycharmProjects\\Tracer')
    Tracer.checksum_dir(True, True, 'Tracer')
