import unittest
from collections import Counter
from baraqdalib import Generator


class MyTestCase(unittest.TestCase):

    def test_first_name(self):  # check if generated name are from given data
        p = Generator()
        p._data = {'PL': {
                        'male_names': {
                            'values': ['Filip', 'Jakub', 'Kacper', 'Marek', 'Pawel', 'Szymon'],
                            'weights': [200, 600, 3200, 4600, 2345, 123]}
                        }
                    }
        name = p.generate('PL', 'male_names', 1)[0]
        assert name
        self.assertIsInstance(name, str)
        self.assertIn(name, p._data['PL']['male_names']['values'])

    def test_weighed_random(self):  # check if generated data are weighted
        p = Generator()
        p._data = {'PL': {
                        'male_names': {
                            'values': ['Filip', 'Jakub', 'Kacper', 'Marek', 'Pawel', 'Szymon'],
                            'weights': [200, 600, 3200, 4600, 2345, 123]}
                        }
                    }
        weights_in_percent = []
        names = p.generate('PL', 'male_names', 10000)
        names_counts = Counter(names)
        names_count_az = {}
        for i in sorted(names_counts):
            names_count_az[i] = names_counts[i]
        names_counts_az_weighs = list(names_count_az.values())
        for i in range(len(names_counts_az_weighs)):
            names_counts_az_weighs[i] = round(int(names_counts_az_weighs[i])/10000, 3)
            weights_in_percent.append(round(p._data['PL']['male_names']['weights'][i] / sum(p._data['PL']['male_names']['weights']), 3))

        for i in range(len(names_counts_az_weighs)):
            self.assertAlmostEqual(names_counts_az_weighs[i], weights_in_percent[i], delta=0.02)


if __name__ == '__main__':
    unittest.main()
