import unittest
import os
from baraqdalib.addresses import Addresses


class AddressesTestCase(unittest.TestCase):
    def test_sym(self):
        os.chdir('../')
        a = Addresses()
        self.assertEqual([a.get_sym_city('Piorunów'), a.get_sym_city('Regut'), a.get_sym_city('Tłuste'), a.get_sym_city('Brzozówka'),
                          a.get_sym_city('Siemierz Górny'), a.get_sym_city('Horyszów-Nowa Kolonia')],
                         ['307', '1063', '2536', '1146', '896829', '898030'])


if __name__ == '__main__':
    unittest.main()
