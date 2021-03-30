class Seed(object):    
    def __init__(self, data):
        """Set seed data"""
        self.data = data
        
    def __str__(self):
        """Returns data as string representation of the seed"""
        return self.data
    __repr__ = __str__