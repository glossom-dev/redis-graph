import unittest
import redis


class FlowTestsBase(unittest.TestCase):
    RUN_TIME_ROW_INDEX = 4

    @classmethod
    def setUpClass(cls):
        cls.redis_con = redis.Redis(host='localhost', port=6379)

    def _assert_only_expected_resuls_are_in_actual_results(self,
                                                           actual_result,
                                                           query_info):
        actual_result_set = actual_result.result_set[1:]

        # assert num resuls
        self.assertEqual(len(actual_result_set), len(query_info.expected_result))

        # assert actual values vs expected values
        for res in query_info.expected_result:
            self.assertTrue(res in actual_result_set,
                            'The item %s is NOT in the actual result\n'
                            'The actual result: %s\nThe expected result: %s' %
                            (str(res), str(actual_result_set), str(query_info.expected_result)))

    def _assert_actual_results_contained_in_expected_results(self,
                                                             actual_result,
                                                             query_info,
                                                             num_contained_results):
        actual_result_set = actual_result.result_set[1:]

        # assert num results
        self.assertEqual(len(actual_result_set), num_contained_results)

        # assert actual values vs expected values
        expected_result = query_info.expected_result
        count = len([res for res in expected_result if res in actual_result_set])

        # assert number of different results is as expected
        self.assertEqual(count,
                         num_contained_results,
                         'The actual result is: %s\nThe expected result is: %s' %
                         (str(actual_result_set), str(query_info.expected_result)))

    def _assert_run_time(self, actual_result, query_info):
        run_time_string = actual_result.statistics[self.RUN_TIME_ROW_INDEX]
        actual_run_time = float(run_time_string.split(': ')[1].split(' milliseconds')[0])
        self.assertLessEqual(actual_run_time,
                             query_info.max_run_time_ms,
                             'Maximum runtime for query \"%s\" was: %s, but shoud be %s' %
                             (query_info.description, str(query_info.max_run_time_ms), str(actual_run_time)))