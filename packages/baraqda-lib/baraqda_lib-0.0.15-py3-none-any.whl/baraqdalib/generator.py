import csv
import random
import os
from typing import List, Dict
import pkgutil


class Generator:
    """Generating data with real distribution given in loaded files. To call functions simply use Generator.generate()."""
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Dict[str, list]]] = dict(dict(dict()))  # create empty dict
        self._list_of_files: Dict[str, list] = dict()

        self._list_of_files = {'PL': ['age.csv', 'blood_type.csv', 'cities_pops.txt', 'eyes.csv', 'female_first_name.csv', 'female_second_name.csv', 'female_surname.csv',
                      'hair.csv', 'male_first_name.csv', 'male_second_name.csv', 'male_surname.csv']}

    def draw(self, lang: str, data_type: str, count: int = 1, sep: str = ' ') -> List[str]:  # return table with weighted draw
        """Drawing a results from given file, returing list with len(list) = counter

        Parameters:
        lang (str): two letters shortcut for country
        data_type (str): name of file from which data should be generated
        count (int): default is 1. How many records should be generated
        sep (str): default is single space. Set separators for columns in files

        Returns:
        list: Returning list of generated data.
        """
        try:
            return random.choices(self._data[lang][data_type]['values'],
                                  weights=self._data[lang][data_type]['weights'],
                                  k=count)
        except KeyError:  # run normal generation when error occurred
            self.generate(lang, data_type, count, sep)

    def search_files(self, path, sep, lang) -> None:
        """Searching for files in given list of filenames

        Parameters:
        sep (str): separator of columns in files
        lang (str): Two letters shortcut for country

        Returns: None
        """
        self._data[lang] = {}
        for file in self._list_of_files[lang]:
            filename = file.split('.')[0]
            self._data[lang][filename] = {}  # create dict with key filename
            self.read_files(os.path.join('data/PL', file), sep, lang, filename)

    def read_files(self, filepath: str, separator: str, lang: str, filename: str) -> None:
        """Reading files into class variable self._data

        Parameters:
        filepath (str): Filepath for a file
        separator (str): Separator of columns in files
        lang (str): Two letters shortcut for country
        filename (str): Filename

        Returns: None
        """
        # read files and store data from them
        files = pkgutil.get_data(__package__, filepath)
        file = csv.reader(files.decode('utf-8').splitlines(), delimiter='\t')
        temp_list = []
        keys = []
        keys = next(file)
        weights_index = keys.index('weights')
        for i in range(len(keys)):  # create lists to store values
            temp_list.append([])
        for row in file:
            if row[weights_index] == 'weights':
                pass
            else:
                temp_tab = row
                temp_tab[weights_index] = int(temp_tab[weights_index])
                for t, item in zip(temp_tab, temp_list):
                    item.append(t)
        for k, v in zip(keys, temp_list):
            self._data[lang][filename][k] = v

    def generate(self, lang: str, data_type: str, counter: int = 1, sep: str = ' ') -> List[str]:
        """Generating data with reading files. This is recommended way of using.

        Parameters:
        lang (str): two letters shortcut for country
        data_type (str): name of file from which data should be generated
        counter (int): default is 1. How many records should be generated
        sep (str): default is single space. Set separators for columns in files

        Returns:
        list: Returning list of generated data.
        """
        # check if key lang exist
        try:
            self._data[lang]
        except KeyError:
            path = os.path.join('baraqdalib', 'data', lang)  # create path to subdirectories
            self.search_files(path, sep, lang)  # search files in directory
            try:  # check if key lang exist after search for directory
                self._data[lang]
            except KeyError:
                print(f'Data not provided for {lang}!')
                return []

        # check if key data_type exist
        try:
            self._data[lang][data_type]
        except KeyError:
            path = os.path.join('baraqdalib', 'data', lang)  # create path to subdirectories
            self.search_files(path, sep, lang)  # search files in directory
            try:  # check if key data_type exist after search and reading files
                self._data[lang][data_type]
            except KeyError:
                print(f'Data not provided for {lang}, {data_type}!')
                return []
        return self.draw(lang, data_type, counter, sep)  # generate weighted dataw

    def access_data(self, lang: str, data_type: str) -> Dict[str, list]:
        """Access data which are readed from files. Helpful when you
        want to make sure that your files are in correct format

        Parameters:
        lang (str): Two letters shortcut for country
        data_type (str): Name of file from which data should be generated

        Returns:
        Dict: Returning dictionary with loaded data in class instance
        """
        try:  # check if keys lang, data_type exists
            self._data[lang][data_type]
        except KeyError:
            print(f'No data for {lang}, {data_type}')
        else:
            return self._data[lang][data_type]
