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
    
    def getSelectedCategories(self, selectedCategories, data):
        finalCategories = []
        if "All" not in selectedCategories and len(selectedCategories) != 0:
            categories = selectedCategories
        else: 
            categories = self.getAllCategories()
        
        for i in categories:
            if i.lower() == "food":
                finalCategories.append(data.food)
            if i.lower() == "furniture":
                finalCategories.append(data.furniture)
            if i.lower() == "tech":
                finalCategories.append(data.tech)
            if i.lower() == "drugs":
                finalCategories.append(data.drugs)
            if i.lower() == "transport":
                finalCategories.append(data.transport)
            if i.lower() == "flights":
                finalCategories.append(data.flights)
            if i.lower() == "music":
                finalCategories.append(data.music)
            if i.lower() == "shopping":
                finalCategories.append(data.shopping)
            if i.lower() == "gas":
                finalCategories.append(data.gas)
            if i.lower() == "others":
                finalCategories.append(data.others)
            
        return finalCategories[0]

 
    
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
