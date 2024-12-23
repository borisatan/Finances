import pandas as pd
import os

class Data:
    food = []
    furnitare = []
    tech = []
    drugs = []
    transport = []
    flights = []
    music = []
    shopping = []
    gas = []
    others = []

    def __init__(self, file):
        self.df = pd.read_excel(f"finance_statements/{file}", usecols=[2, 3, 7, 11])

        
    def removeNanRows(self):
        self.df = self.df.rename(columns={"Unnamed: 2" : "Currency", "Unnamed: 3" : "Price", "Unnamed: 7" : "Date", "Unnamed: 11" : "Description"}, errors="raise")
        NANRowIndexes = []

        for i in range(len(self.df)):
            price = self.df.at[i, "Price"]

            if str(price).lower() == "nan":
                NANRowIndexes.append(i)

            try:
                float(price)
            except:
                NANRowIndexes.append(i)   

        self.df = self.df.drop(NANRowIndexes)

        return self.df


# REINDEX EACH ROW START = 0, END = len(df)

    def reindex(self, df):
        j = 0
        for i, row in df.iterrows():
            df = df.rename(index={i : j})
            j += 1

        # CHECK IF EACH TRANSACTION IS IN BGN

        # for i in range(len(df)):
        #     currency = df.at[i, "Currency"]

        #     if str(currency) != "BGN":
        #         print("Transaction not in lev")

        return df


    def categoriseRows(self, listToCheck, value):
        for i in range(len(listToCheck)):

            if str(listToCheck[i]).lower() in str(value).lower():
                return True

        return False    


# LISTS TO CHECK

    def makeCategories(self):
        # CATEGORIES TO CHECK
        superMarkets = ["edeka", "lidl", "kaufland", "nah und gut", "rewe", "aldi", "billa"]
        furnitareStores = ["ikea", "poco", "jysk"]
        techStores = ["media markt", "technopolis"]
        drugStores = ["dm", "rossman"]
        transportCompanies = ["miles", "lime"]
        flightCompanies = ["ryanair"]
        musicStores = ["muziker", "mmg"]
        shoppingStores = ["h&m", "c&a"]
        gasStations = ["omv", "shell"]

        # END RESULTS

        for i, row in self.df.iterrows():
            row = row.to_list()
            description = row[3]
            row.insert(0, i)

            data = row[0:4] # index, currency, price, date

            if self.categoriseRows(superMarkets, description):
                self.food.append(data)

            elif self.categoriseRows(furnitareStores, description):
                self.furnitare.append(data)

            elif self.categoriseRows(techStores, description):
                self.tech.append(data)

            elif self.categoriseRows(drugStores, description):
                self.drugs.append(data)

            elif self.categoriseRows(transportCompanies, description):
                self.transport.append(data)

            elif self.categoriseRows(flightCompanies, description):
                self.flights.append(data)

            elif self.categoriseRows(musicStores, description):
                self.music.append(data)    

            elif self.categoriseRows(shoppingStores, description):
                self.shopping.append(data)  

            elif self.categoriseRows(gasStations, description):
                self.gas.append(data)    
            
            else:
                self.others.append(data)    


    def sortByMonth(self, months: list ): # [start, end] or [] for all
        # DROP NOT MATCHING MONTHS
        df = self.df

        if months:
            rowsNotInMonth = []

            for i, j in enumerate(df.loc[:, "Date"]):
                date = j.split(".")

                if int(date[1]) < months[0] or int(date[1]) > months[1]:
                    rowsNotInMonth.append(i)

            df = df.drop(rowsNotInMonth)
            df = self.reindex(df)

        self.makeCategories()
        return df # create a new object to store the month values so that the originals don't get messed up
    

    def printCategories(self, categoriesToPrint: list): # PRINT CERTAIN CATEGORIES
        if len(categoriesToPrint) > 0: 
            for j, category in enumerate(categoriesToPrint):
                print(f"Category index {j}: ")
                for i in category:
                    print(i)
    
        else: # IF NO CATEGORIES PRINT ALL
            for i, row in self.df.iterrows():
                row = row.to_list()
                row.insert(0, i)
                data = row[0:4]
                print(data)    
