import glob
import csv
import pandas as pd

# on définit le dossier sur lequel se baser
folder = "dumps/OGNreports/2/"

json_files = glob.glob(folder + "*.json")

# on concatène tous les fichiers json en un dataframe
tweets = pd.DataFrame()
for count,ele in enumerate(json_files,len(json_files)):
    tweets = pd.concat([tweets, pd.read_json(ele)])

# on écrit vers un fichier csv
tweets.to_csv(folder + "tweets_full.csv",index=False)