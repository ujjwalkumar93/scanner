import os
import re

class Company_name:
    @staticmethod
    def name():
        file_location = os.path.join(os.getcwd(), 'media', 'text')
        with open(file_location, 'r+') as fl:
            for line in fl:
                name = re.search(r'ENTERPRISESIndustrial (\S+)', line)
                try:
                    if name:
                        print(name)
                    else:
                        print("Name not found")
                except:
                    print('exception handeled')
        return name


