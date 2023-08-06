from baraqdalib import Generator
import csv
import random
from typing import List, Dict
import pkgutil

class Addresses:
    """Class Addresses for generating polish fake address but with true distribution"""
    def __init__(self):
        self.address_generator = Generator()

        self.streets_file_name: str = 'streets.csv'
        self.cities_file_name: str = 'cities.csv'
        self.cities_pops_data: str = 'cities_pops'
        self.cities_pops_file_name: str = 'cities_pops.csv'

        self._postal_code: List[List[str, str]] = list(list())
        self._streets: List[List[str, str]] = list(list())
        self._cities: List[List[str, str]] = list(list())

        self.sep: str = '\t'

        self._set_streets()
        self._set_cities()
        self._set_codes()

    def _set_codes(self):   # Setting self._postal_code variable with list from 'postal_codes.csv'
        """Get postal codes from file postal_codes.csv and save in self._postal_code list

        Parameters : None

        Returns: None
        """
        codesFile = pkgutil.get_data(__package__, 'addressData/postal_codes.csv')
        codes = csv.reader(codesFile.decode('utf-8-sig').splitlines(), delimiter=';')
        for code in codes:
            self._postal_code.append([code[2], code[0]])

    def _set_cities(self):   # Setting self.cities variable with list from self.cities_file_name
        """Get cities names  from file cities.csv and save in self._cities list

        Parameters : None

        Returns: None
        """
        citiesFile = pkgutil.get_data(__package__, 'addressData/cities.csv')
        cities = csv.reader(citiesFile.decode('utf-8-sig').splitlines(), delimiter=';')
        for sym in cities:
            self._cities.append(sym)

    def _set_streets(self):  # Setting self.streets variable with list from self.cities_file_name
        """Get street names from file streets.csv and save in self._streets list

        Parameters : None

        Returns: None
        """
        streetsFile = pkgutil.get_data(__package__, 'addressData/streets.csv')
        streets_csv = csv.reader(streetsFile.decode('utf-8-sig').splitlines())
        for row in streets_csv:
            self._streets.append([row[4], (row[6] + ' ' + row[8] + ' ' + row[7]).replace('  ', ' ')])

    def generate(self, counter: int = 1, lang: str = 'PL'):   # Generating from Generator class
        """ Generating address with city, street, street number,  and postal code

        Parameters:
        counter (int): Default is 1. You can specify how much addreses you want to generate
        lang (str): Default is 'PL'. By this argument you can choose from wchich country addresses should be generated.

        Returns:
        Dict(Dict()): returning generated addresses in nested dictionary for easy access

        """
        generated_cities = self.address_generator.generate(lang, self.cities_pops_data, counter, self.sep)
        address: Dict[Dict[str, str]] = dict(dict())
        for city, address_id in zip(generated_cities, range(len(generated_cities))):
            sym = self.get_sym_city(city)
            street = self.get_streets(int(sym))
            postal_code = self.get_code(str(city))
            address.update({str(address_id): {'street': street, 'city': city, 'postal_code': postal_code}})
        return address

    def get_code(self, city: str):  # Searching for city in postal_codes returning it's value
        """Search and return postal code for a given city

        Parameters:
        city (str): Name of the city

        Returns:
        str: Returns postal code
        """
        codes = list()
        for code in self._postal_code:
            if code[0] == city:
                codes.append(code[1])
        if codes:
            return random.choice(codes)
        return 'No city in file'

    def get_sym_city(self, city: str):    # Searching for city in cities and returning sym
        """Searching for city in cities and returning sym (indentificator)

        Parameters:
        city (str): name of city for searching

        Returns:
        str : return sym for searching city
        """
        for sym in self._cities:
            if sym[1] == city:
                return sym[0]
        return 'No city in file'

    def get_streets(self, city_sym: int):    # Returning streets for city sym
        """ Generate random street for given city sym (identificator) that is in this city.

        Parameters:
        city_sym (int): number of city syn

        Returns:
        str: returns random street
        """
        if city_sym != 'No city in file':   # If city_sym isn't set as a 'No city in file' generating address
            streets = []
            streets_dump = []
            for row in self._streets:   # Reading streets
                if row[0] == city_sym:      # Checking if city is in list
                    streets.append(row[1])
                elif row[0] != 'SYM' and row[0] != city_sym:    # Checking if city isn't in list and isn't header 'SYM'
                    if 287400 % int(row[0]):        # Decimation of list of streets from which we generate
                        streets_dump.append(row[1])
            if not streets:
                return random.choice(streets_dump) + ' ' + str((round(random.lognormvariate(1.6, 2)) + 1) % 200)    # Generating address if city isn't in file
            return random.choice(streets) + ' ' + str((round(random.lognormvariate(1.6, 2)) + 1) % 200)     # Generating address if city is in file
        else:
            return city_sym       # If city_sym is set as a 'No city in file' returning this string
