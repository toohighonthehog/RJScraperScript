import os, shutil

#SOURCE_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/General/"
SOURCE_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/08/"
TARGET_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/General/"
FILE = "MIAD-283"

shutil.move(SOURCE_DIRECTORY + FILE, TARGET_DIRECTORY + FILE)