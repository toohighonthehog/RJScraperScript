import rjscanmodule.rjgeneral as rjgen

#SOURCE_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/General/"
SOURCE_DIRECTORY = "/home/rjohnson/multimedia/Other/RatedFinalJ/Censored/08/"
#TARGET_DIRECTORY = "/home/rjohnson/vscode/git/RJScraperScript/misc/General/"
FILE = "MIAD-283"

print (rjgen.prate_directory(SOURCE_DIRECTORY, 10))
print (rjgen.prate_directory(SOURCE_DIRECTORY, "Names"))

#shutil.move(SOURCE_DIRECTORY + FILE, TARGET_DIRECTORY + FILE)