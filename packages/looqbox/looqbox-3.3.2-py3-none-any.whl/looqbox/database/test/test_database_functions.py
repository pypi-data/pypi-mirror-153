import unittest

from looqbox.database.database_functions import sql_in
from looqbox.database.database_functions import sql_between
from looqbox.database.database_functions import _sql_replace_parameters


class TestSQLFunctions(unittest.TestCase):

    def test_sql_in(self):
        """
        Test sql_in function
        """
        par1 = [1, 2, 3, 4, 5]
        query1 = "select * from database where 1=1 " + sql_in("and par1 in", par1)
        correct_query1 = "select * from database where 1=1 and par1 in (1, 2, 3, 4, 5)"

        par2 = [1, 2, 3]
        par3 = 1
        query2 = "select * from database where 1=1 " + sql_in("and par2 in", par2) + \
                 sql_in(" and par3 in", par3)
        correct_query2 = "select * from database where 1=1 and par2 in (1, 2, 3) and par3 in (1)"

        self.assertEqual(query1, correct_query1)
        self.assertEqual(query2, correct_query2)

    def test_sql_between(self):
        """
        Test sql_between function
        """
        par1 = [1, 2]
        query1 = "select * from database where 1=1" + sql_between(" and par1", par1)
        correct_query1 = "select * from database where 1=1 and par1 between 1 and 2"

        par2 = ['2018-01-01', '2018-02-02']
        query2 = "select * from database where 1=1" + sql_between(" and date", par2)
        correct_query2 = "select * from database where 1=1 and date between '2018-01-01' and '2018-02-02'"

        par3 = ['2018-01-01']
        par4 = [1, 2, 3, 4]
        self.assertEqual(query1, correct_query1)
        self.assertEqual(query2, correct_query2)
        with self.assertRaises(Exception):
            "select * from database where 1=1" + sql_between(" and date", par3)
            "select * from database where 1=1" + sql_between(" and date", par4)

    def test_replace_parameters(self):
        """
        Test _sql_replace_parameters
        """
        query = "select * from database where x = `1` and z = `3` and y = `2`"
        replace_parameters = [30, "2019-01-01", "matheus"]
        expected_query = 'select * from database where x = "30" and z = "matheus" and y = "2019-01-01"'
        test_query = _sql_replace_parameters(query, replace_parameters, replace_with_quotes=True)
        
        self.assertEqual(expected_query, test_query)


if __name__ == '__main__':
    unittest.main()
