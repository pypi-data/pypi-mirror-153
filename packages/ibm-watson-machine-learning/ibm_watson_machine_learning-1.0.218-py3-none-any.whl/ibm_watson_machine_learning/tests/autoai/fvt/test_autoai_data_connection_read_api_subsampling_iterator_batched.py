#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes.abstract_autoai_data_subsampling_iterator_batched import \
    AbstractAutoAISubsamplingIteratorBatched


class TestAutoAIRemote(AbstractAutoAISubsamplingIteratorBatched, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """

    def read_from_api(self, return_data_as_iterator, sample_size_limit, sampling_type, number_of_batch_rows,
                      return_subsampling_stats, experiment_metadata):
        params = {'use_flight': True,
                  'binary': sampling_type is None}

        if sampling_type is not None:
            params['sampling_type'] = sampling_type

        if experiment_metadata is not None:
            params['experiment_metadata'] = experiment_metadata

        if sample_size_limit is not None:
            params['sample_size_limit'] = sample_size_limit

        if return_data_as_iterator is not None:
            params['return_data_as_iterator'] = return_data_as_iterator

        if number_of_batch_rows is not None:
            params['number_of_batch_rows'] = number_of_batch_rows

        if return_subsampling_stats is not None:
            params['_return_subsampling_stats'] = return_subsampling_stats

        res = self.data_connections[0].read(**params)

        if return_subsampling_stats:
            self.assertEqual(type(res), tuple)
            res = res(0)

        if return_data_as_iterator:
            iterator = iter(res)
            data = next(iterator)
            return iterator, data
        else:
            data = res
            return None, data

if __name__ == '__main__':
    unittest.main()
