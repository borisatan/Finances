class Helper:
    def __init__(self):
        pass

    def getAllCategories(self):
        return [
        "All",
        "Food", 
        "Furniture",
        "Tech", 
        "Drugs",
        "Transport",
        "Flights", 
        "Music", 
        "Shopping",
        "Gas" ,
        "Others"]
    
    def appendAllItems(self, finalPurchases, dataToAppend):
        for i in dataToAppend:
            finalPurchases.append(i)

        return finalPurchases    

    def getSelectedCategories(self, selectedCategories, data):
        finalPurchases = []
        if not ("All" in selectedCategories) and len(selectedCategories) != 0:
            categories = selectedCategories
        else: 
            categories = self.getAllCategories()

            
        for i in categories:
            if i.lower() == "food":
                finalPurchases = self.appendAllItems(finalPurchases, data.food)
            if i.lower() == "furniture":
                finalPurchases = self.appendAllItems(finalPurchases, data.furniture)
            if i.lower() == "tech":
                finalPurchases = self.appendAllItems(finalPurchases, data.tech)
            if i.lower() == "drugs":
                finalPurchases = self.appendAllItems(finalPurchases, data.drugs)
            if i.lower() == "transport":
                finalPurchases = self.appendAllItems(finalPurchases, data.transport)
            if i.lower() == "flights":
                finalPurchases = self.appendAllItems(finalPurchases, data.flights)
            if i.lower() == "music":
                finalPurchases = self.appendAllItems(finalPurchases, data.music)
            if i.lower() == "shopping":
                finalPurchases = self.appendAllItems(finalPurchases, data.shopping)
            if i.lower() == "gas":
                finalPurchases = self.appendAllItems(finalPurchases, data.gas)
            if i.lower() == "others":
                finalPurchases = self.appendAllItems(finalPurchases, data.others)

        return finalPurchases

 
    
    def getMonthsDictionary(self):
        values = [i for i in range(1, 13)]
        keys = self.getAllMonths()[1:]

        return dict(zip(keys, values))
    
    def getAllMonths(self):
        return ["All", "Jan", "Feb", 'Mar', "Apr", 'May', "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def getAvailableMonths(self, data):
        # Get the months available in the file
        availableMonths = data.df["Date"].apply(lambda x: x.split(".")[1]).unique()
        availableMonths = sorted(map(int, availableMonths))  # Sort months numerically
        return availableMonths
