import json
# import os

# # this mode , usefull for when whole code write in main.py , if changed structure of project , better use of singleton design
# class loadLange:

#     def __init__(self) -> None:
        

#         with open('strings.json', "r") as file:
#             # load the JSON data from the file
#             data = json.load(file)
#             for key, value in data.items():

#                 setattr(self, key, value)



class Struct:
    """The recursive class for building and representing objects with."""

    def __init__(self, obj):
        
        for k, v in obj.items():
            if isinstance(v, dict):
                setattr(self, k, Struct(v))
            else:
                setattr(self, k, v)

    def __getitem__(self, val):
        return self.__dict__[val]

    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v)) for (k, v) in self.__dict__.items()))


with open('strings.json', "r") as file:
    obj = json.load(file)

loadStrings = Struct(obj)