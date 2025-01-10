import pandas as pd
import os

class Data:
    def __init__(self, file):
        self.df = pd.read_excel(f"Finance Statements/{file}", usecols=[2, 3, 7, 11])
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
                return [True, listToCheck[i]]
        return [False, False] 
    
    def convertToLatin(self, text : str):
        bulgarianToLatin = {
            'а': 'a', 'А': 'A',
            'б': 'b', 'Б': 'B',
            'в': 'v', 'В': 'V',
            'г': 'g', 'Г': 'G',
            'д': 'd', 'Д': 'D',
            'е': 'e', 'Е': 'E',
            'ж': 'zh', 'Ж': 'Zh',
            'з': 'z', 'З': 'Z',
            'и': 'i', 'И': 'I',
            'й': 'y', 'Й': 'Y',
            'к': 'k', 'К': 'K',
            'л': 'l', 'Л': 'L',
            'м': 'm', 'М': 'M',
            'н': 'n', 'Н': 'N',
            'о': 'o', 'О': 'O',
            'п': 'p', 'П': 'P',
            'р': 'r', 'Р': 'R',
            'с': 's', 'С': 'S',
            'т': 't', 'Т': 'T',
            'у': 'u', 'У': 'U',
            'ф': 'f', 'Ф': 'F',
            'х': 'h', 'Х': 'H',
            'ц': 'ts', 'Ц': 'Ts',
            'ч': 'ch', 'Ч': 'Ch',
            'ш': 'sh', 'Ш': 'Sh',
            'щ': 'sht', 'Щ': 'Sht',
            'ъ': 'a', 'Ъ': 'A',
            'ь': 'y', 'Ь': 'Y',
            'ю': 'yu', 'Ю': 'Yu',
            'я': 'ya', 'Я': 'Ya'
        }

        
        table  = str.maketrans(bulgarianToLatin)
        return text.translate(table)

    def appendDataCategories(self, listToCheck, category, description, data, descriptionInLatin):
        data.append(self.categoriseRows(listToCheck, description)[1])
        data.append(category)
        data.append(descriptionInLatin)

        return data
    
    def makeCategories(self):
        # Categories to check
        superMarkets = ["edeka", "lidl", "kaufland", "nah und gut", "rewe", "aldi", "billa"]
        furnitureStores = ["ikea", "poco", "jysk"]
        techStores = ["media markt", "technopolis"]
        drugStores = ["dm", "rossman"]
        transportCompanies = ["miles", "lime"]
        flightCompanies = ["ryanair"]
        musicStores = ["muziker", "mmg"]
        shoppingStores = ["h&m", "c&a"]
        gasStations = ["omv", "shell"]

        # Initialize category lists
        self.food = []
        self.furniture = []
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
            data = [row["Price"], row["Date"]]
            descriptionInLatin = self.convertToLatin(str(description))


            if (self.categoriseRows(superMarkets, description))[0]:
                data = self.appendDataCategories(superMarkets, "Food", description, data, descriptionInLatin)
                self.food.append(data)

            elif (self.categoriseRows(furnitureStores, description))[0]:
                data = self.appendDataCategories(furnitureStores, "Furniture", description, data, descriptionInLatin)
                self.furniture.append(data)

            elif self.categoriseRows(techStores, description)[0]:
                data = self.appendDataCategories(techStores, "Tech", description, data, descriptionInLatin)
                self.tech.append(data)

            elif self.categoriseRows(drugStores, description)[0]:
                data = self.appendDataCategories(drugStores, "Drugs", description, data, descriptionInLatin)
                self.drugs.append(data)

            elif self.categoriseRows(transportCompanies, description)[0]:
                data = self.appendDataCategories(transportCompanies, "Transport", description, data, descriptionInLatin)
                self.transport.append(data)

            elif self.categoriseRows(flightCompanies, description)[0]:
                data = self.appendDataCategories(flightCompanies, "Flights", description, data, descriptionInLatin)
                self.flights.append(data)

            elif self.categoriseRows(musicStores, description)[0]:
                data = self.appendDataCategories(musicStores, "Music", description, data, descriptionInLatin)
                self.music.append(data)    

            elif self.categoriseRows(shoppingStores, description)[0]:
                data = self.appendDataCategories(shoppingStores, "Shopping", description, data, descriptionInLatin)

                self.shopping.append(data)  

            elif self.categoriseRows(gasStations, description)[0]:
                data = self.appendDataCategories(gasStations, "Gas", description, data, descriptionInLatin)
                self.gas.append(data)    
            
            else:
                data.append("Other")
                data.append("Other")
                data.append(descriptionInLatin)
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
