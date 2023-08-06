import os
from unittest import TestCase

from configservice import Config, MissingEnviron, ErrorFlagTrue


class TestCore(TestCase):

    def test__load_env(self):
        # set an env to work with.

        os.environ['TEST_ME_X'] = '1'

        c = Config()

        # Test simple recall.
        res = c.get_env('TEST_ME_X')
        self.assertEqual('1', res)

        # Test default value
        res = c.get_env('THIS_DOESNT_EXIST',
                        default_value='A')
        self.assertEqual('A', res)

        # Test default value where the key does exist (should take the key instead)
        res = c.get_env('TEST_ME_X',
                        default_value='A')
        self.assertEqual('1', res)

        # Test test mode responses section.
        ######### TEST MODES ############
        c._test_mode = True
        # Test simple recall.
        res = c.get_env('TEST_ME_X', test_response='test_res')
        self.assertEqual('test_res', res)

        # Test assigned value where no value assigned
        res = c.get_env('TEST_ME_X',
                        default_value=24,
                        test_response='test_res')
        self.assertEqual('1', res)
        c._test_mode = False
        ######### End Test Mode Section ############

        ######## Check error states. ############

        with self.assertRaises(MissingEnviron) as e:
            res = c.get_env('THIS_DOESNT_EXIST', error_flag=True)

        with self.assertRaises(ErrorFlagTrue) as e:
            res = c.get_env('THIS_DOESNT_EXIST', error_flag=True, default_value='1')

        ###### Check data conversion ###########
        # Test integer
        os.environ['TEST_ME_X'] = '1'
        res = c.get_env('TEST_ME_X', data_type_convert='int')
        self.assertEqual(1, res)

        # Test float
        os.environ['TEST_ME_X'] = '1.11'
        res = c.get_env('TEST_ME_X', data_type_convert='float')
        self.assertEqual(1.11, res)

        # Test Bool
        os.environ['TEST_ME_X'] = '1'
        res = c.get_env('TEST_ME_X', data_type_convert='bool')
        self.assertTrue(res)

        os.environ['TEST_ME_X'] = 'True'
        res = c.get_env('TEST_ME_X', data_type_convert='bool')
        self.assertTrue(res)

        os.environ['TEST_ME_X'] = '0'
        res = c.get_env('TEST_ME_X', data_type_convert='bool')
        self.assertFalse(res)

        os.environ['TEST_ME_X'] = 'false'
        res = c.get_env('TEST_ME_X', data_type_convert='bool')
        self.assertFalse(res)

        # Test list
        os.environ['TEST_ME_X'] = 'a,b,c,d'
        res = c.get_env('TEST_ME_X', data_type_convert='list')
        golden = ['a', 'b', 'c', 'd']
        self.assertListEqual(golden, res)

        # Test list int
        os.environ['TEST_ME_X'] = '1,2,3,4,5'
        res = c.get_env('TEST_ME_X', data_type_convert='list_int')
        golden = [1, 2, 3, 4, 5]
        self.assertListEqual(golden, res)

        # Test list float
        os.environ['TEST_ME_X'] = '1.2,2,3.6,4.6,5'
        res = c.get_env('TEST_ME_X', data_type_convert='list_float')
        golden = [1.2, 2, 3.6, 4.6, 5]
        self.assertListEqual(golden, res)

        # Test default value int

        res = c.get_env('TEST_ME_NO', default_value='3', data_type_convert='int')
        self.assertEqual(3, res)

        # Test default value int
        c._test_mode = True
        res = c.get_env('TEST_ME_NO', test_response='2', default_value='3', data_type_convert='int')
        self.assertEqual(3, res)

        # Test default value int
        c._test_mode = True
        res = c.get_env('TEST_ME_NO', test_response='2', data_type_convert='int')
        self.assertEqual(2, res)
