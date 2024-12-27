class Helper:
    def __init__(self):
        pass

    def getAllCategories(self):
        return [
        "All",
        "Food", 
        "Furnitare",
        "Tech", 
        "Drugs",
        "Transport",
        "Flights", 
        "Music", 
        "Shopping",
        "Gas" ,
        "Others"]
    
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
