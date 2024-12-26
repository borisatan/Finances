import pandas as pd
import os

class Data:
    def __init__(self, file):
        self.df = pd.read_excel(f"finance_statements/{file}", usecols=[2, 3, 7, 11])
        self.removeNanRows()

        self.makeCategories()


    def removeNanRows(self):
        self.df = self.df.rename(columns={"Unnamed: 2": "Currency", "Unnamed: 3": "Price", "Unnamed: 7": "Date", "Unnamed: 11": "Description"}, errors="raise")
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


    def categoriseRows(self, listToCheck : list, value : str):
        for i in range(len(listToCheck)):
            if str(listToCheck[i]).lower() in str(value).lower():
                return True
        return False 

    def makeCategories(self):
        # Categories to check
        superMarkets = ["edeka", "lidl", "kaufland", "nah und gut", "rewe", "aldi", "billa"]
        furnitareStores = ["ikea", "poco", "jysk"]
        techStores = ["media markt", "technopolis"]
        drugStores = ["dm", "rossman"]
        transportCompanies = ["miles", "lime"]
        flightCompanies = ["ryanair"]
        musicStores = ["muziker", "mmg"]
        shoppingStores = ["h&m", "c&a"]
        gasStations = ["omv", "shell"]

        # Initialize category lists
        self.food = []
        self.furnitare = []
        self.tech = []
        self.drugs = []
        self.transport = []
        self.flights = []
        self.music = []
        self.shopping = []
        self.gas = []
        self.others = []

        # Categorize each row based on description
        for i, row in self.df.iterrows():
            description = row["Description"]
            data = [row["Currency"], row["Price"], row["Date"], row["Description"]]

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


    def getExpensesByMonth(self, months: list = None):
        """ Returns total expenses per month (1-12). If months is None, all data will be considered. """
        monthlyExpenses = {month: 0 for month in range(1, 13)}  # Initialize all months to 0

        # Iterate through rows and categorize expenses by month
        for i, row in self.df.iterrows():
            date = row["Date"]
            try:
                month = int(date.split(".")[1])  # Extract month from Date column (MM.YYYY format)
                price = -1 * float(row["Price"])  # Assuming "Price" is a positive amount, expenses are negative
                if months:
                    if month in months:
                        monthlyExpenses[month] += price
                else:
                    monthlyExpenses[month] += price
            except Exception as e:
                print(f"Error processing row {i}: {e}")

        return monthlyExpenses

    def printCategories(self, categoriesToPrint: list = None):
        """ Prints out the categories. If categoriesToPrint is specified, only those are printed. """
        if categoriesToPrint:
            for category in categoriesToPrint:
                print(f"Category: {category}")
                for entry in getattr(self, category):
                    print(entry)
        else:
            # If no categories specified, print all data
            for i, row in self.df.iterrows():
                print(row.to_list())

