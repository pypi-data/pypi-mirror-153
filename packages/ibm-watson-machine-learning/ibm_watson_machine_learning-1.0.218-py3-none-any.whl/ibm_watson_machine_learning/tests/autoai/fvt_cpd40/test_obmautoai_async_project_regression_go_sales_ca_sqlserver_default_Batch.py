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

import ibm_boto3
from ibm_watson_machine_learning.preprocessing import DataJoinGraph
from ibm_watson_machine_learning.helpers.connections import DataConnection, ContainerLocation, FSLocation, \
    DatabaseLocation
from ibm_watson_machine_learning.tests.utils import is_cp4d, save_data_to_container, get_db_credentials
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import AbstractTestOBM, \
    AbstractTestBatch

from ibm_watson_machine_learning.utils.autoai.errors import WrongDataJoinGraphNodeName

from ibm_watson_machine_learning.utils.autoai.enums import PredictionType, Metrics, RegressionAlgorithms


class TestAutoAIRemote(AbstractTestOBM, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """
    HISTORICAL_RUNS_CHECK = False
    cos_resource = None

    input_data_filenames = ["go_1k.csv", "go_daily_sales.csv"]

    input_data_path = './autoai/data/go_sales_1k/'

    input_node_names = [name.replace('go_', 'node_').split('.')[0] for name in input_data_filenames]

    schema_name = "connections"
    table_names = ["go_1k", "go_daily_sales"]

    SPACE_ONLY = False

    BATCH_DEPLOYMENT_WITH_DA = False
    BATCH_DEPLOYMENT_WITH_CDA = True
    BATCH_DEPLOYMENT_WITH_CA_DA = False
    BATCH_DEPLOYMENT_WITH_CA_CA = False

    OPTIMIZER_NAME = "Go Sales OBM test sdk"

    target_space_id: str = None

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        desc='test description',
        prediction_type=PredictionType.REGRESSION,
        prediction_column='Quantity',
        scoring=Metrics.ROOT_MEAN_SQUARED_LOG_ERROR,
        include_only_estimators=[RegressionAlgorithms.SnapDT, RegressionAlgorithms.RIDGE]
    )

    def test_00b_prepare_COS_instance_and_connection(self):
        TestAutoAIRemote.db_credentials = get_db_credentials('sqlserver')
        connection_details = self.wml_client.connections.create({
            'datasource_type': self.wml_client.connections.get_datasource_type_uid_by_name('sqlserver'),
            'name': 'POSTGRES Connection to DB for python API tests',
            'properties': self.db_credentials
        })

        TestAutoAIRemote.connection_id = self.wml_client.connections.get_uid(connection_details)
        self.assertIsInstance(self.connection_id, str)

    def test_01_create_multiple_data_connections__connections_created(self):
        TestAutoAIRemote.data_connections = []
        for file, node_name, table_name in zip(self.input_data_filenames, self.input_node_names, self.table_names):
            conn = DataConnection(
                data_join_node_name=node_name,
                connection_asset_id=self.connection_id,
                location=DatabaseLocation(
                    schema_name=self.schema_name,
                    table_name=table_name
                )
            )
            TestAutoAIRemote.data_connections.append(conn)

        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connections)
        self.assertGreater(len(TestAutoAIRemote.data_connections), 0)
        self.assertIsNone(self.results_connection)

    def test_02_create_data_join_graph__graph_created(self):
        data_join_graph = DataJoinGraph()
        data_join_graph.node(name="node_daily_sales")
        data_join_graph.node(name="node_1k", main=True)

        data_join_graph.edge(from_node="node_daily_sales", to_node="node_1k",
                             from_column=["Product number"], to_column=["Product number"])

        TestAutoAIRemote.data_join_graph = data_join_graph

        print(f"data_join_graph: {data_join_graph}")


if __name__ == '__main__':
    unittest.main()
