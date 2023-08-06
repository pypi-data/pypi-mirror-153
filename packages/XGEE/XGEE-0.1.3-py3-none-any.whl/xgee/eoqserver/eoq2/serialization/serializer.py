'''
 Bjoern Annighoefer 2019
'''

class Serializer:
    def Ser(self,val):
        pass
    def Des(self,code):
        pass
    def serialize(self,val):
        return self.Ser(val) #legacy support
    def deserialize(self,code):
        return self.Des(code) #legacy support
    
    
    

    