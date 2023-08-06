#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.

import argparse
from argparse import RawTextHelpFormatter
import asyncio
from contextlib import closing, suppress
from enum import Enum
import json
import logging
import os
import signal
import pandas as pd
import sys
import time

from datarobot.mlops.common import config
from datarobot.mlops.common.enums import SpoolerType, MLOpsSpoolAction, DataType
from datarobot.mlops.common.exception import DRCommonException
from datarobot.mlops.common.exception import DRConfigKeyAlreadyAssigned
from datarobot.mlops.common.exception import DRNotFoundException
from datarobot.mlops.constants import Constants
from datarobot.mlops.metric import SerializationConstants
from datarobot.mlops.spooler.record_spooler_factory import RecordSpoolerFactory

from .client import MLOpsClient
from .enums import DatasetSourceType, ExitCode
from .exception import DRMLOpsConnectedException
from .upload_tracker import MLOpsUploadTracker


logger = logging.getLogger(__name__)


class EV:
    """Class to define environment variables used throughout the program."""

    MLOPS_SERVICE_URL = "MLOPS_SERVICE_URL"
    MLOPS_API_TOKEN = "MLOPS_API_TOKEN"

    MLOPS_MODEL_ID = "MLOPS_MODEL_ID"
    MLOPS_MODEL_PACKAGE_ID = "MLOPS_MODEL_PACKAGE_ID"
    MLOPS_DATASET_ID = "MLOPS_DATASET_ID"
    MLOPS_TRAINING_DATASET_ID = "MLOPS_TRAINING_DATASET_ID"
    MLOPS_HOLDOUT_DATASET_ID = "MLOPS_HOLDOUT_DATASET_ID"
    MLOPS_DEPLOYMENT_ID = "MLOPS_DEPLOYMENT_ID"
    MLOPS_DEPLOYMENT_LABEL = "MLOPS_DEPLOYMENT_LABEL"
    MLOPS_PREDICTION_ENVIRONMENT_ID = "MLOPS_PREDICTION_ENVIRONMENT_ID"


class Subjects:
    MAIN_COMMAND = "mlops-cli"
    PERF_TEST = "perf"
    PREDICTIONS = "predictions"
    ACTUALS = "actuals"
    MODEL = "model"
    DATASET = "dataset"
    DEPLOYMENT = "deployment"
    PREDICTION_ENVIRONMENT = "prediction-environment"
    SERVICE_STATS = "service-stats"

    ALL_SUBJECTS = [PERF_TEST, PREDICTIONS, ACTUALS, MODEL, DATASET, DEPLOYMENT,
                    PREDICTION_ENVIRONMENT, SERVICE_STATS]


class Actions:
    UPLOAD = "upload"
    DOWNLOAD = "download"
    CREATE = "create"
    GET = "get"
    LIST = "list"
    DELETE = "delete"
    REPLACE = "replace"
    REPORT = "report"
    RUN = "run"
    DEPLOY = "deploy"
    GET_MODEL = "get-model"

    ALL_ACTIONS = [UPLOAD, DOWNLOAD, CREATE, GET, LIST, DELETE, REPLACE,
                   REPORT, RUN, DEPLOY, GET_MODEL]

    PERF_ACTIONS = [RUN]
    PREDICTIONS_ACTIONS = [UPLOAD, GET, REPORT]
    ACTUALS_ACTIONS = [REPORT]
    MODEL_ACTIONS = [DOWNLOAD, CREATE, GET, LIST, DELETE, REPLACE, DEPLOY]
    DATASET_ACTIONS = [UPLOAD, GET, LIST, DELETE]
    DEPLOYMENT_ACTIONS = [GET, LIST, DELETE, GET_MODEL]
    PREDICTION_ENVIRONMENT_ACTIONS = [CREATE, GET, LIST, DELETE]
    SERVICE_STATS_ACTIONS = [GET]


SUPPORTED_ACTIONS = {
    Subjects.PERF_TEST: Actions.PERF_ACTIONS,
    Subjects.PREDICTIONS: Actions.PREDICTIONS_ACTIONS,
    Subjects.ACTUALS: Actions.ACTUALS_ACTIONS,
    Subjects.MODEL: Actions.MODEL_ACTIONS,
    Subjects.DATASET: Actions.DATASET_ACTIONS,
    Subjects.DEPLOYMENT: Actions.DEPLOYMENT_ACTIONS,
    Subjects.PREDICTION_ENVIRONMENT: Actions.PREDICTION_ENVIRONMENT_ACTIONS,
    Subjects.SERVICE_STATS: Actions.SERVICE_STATS_ACTIONS,
}


class ArgumentsOptions:
    VERBOSE = "--verbose"
    QUIET = "--quiet"
    JSON = "--json"
    TERSE = "--terse"
    PREDICTION_ENVIRONMENT_ID = "--prediction-environment-id"
    DEPLOYMENT_ID = "--deployment-id"
    MODEL_ID = "--model-id"
    MODEL_PACKAGE_ID = "--model-package-id"
    DEPLOYMENT_LABEL = "--deployment-label"
    DATASET_ID = "--dataset-id"
    TRAINING_DATASET_ID = "--training-dataset-id"
    HOLDOUT_DATASET_ID = "--holdout-dataset-id"
    JSON_CONF = "--json-config"
    OUTPUT_DIRECTORY = "--output-dir"
    MLOPS_SERVICE = "--mlops-url"
    MLOPS_API_TOKEN = "--api-token"
    VERIFY_SSL = "--verify-ssl"
    INPUT = "--input"
    COUNT = "--count"
    ROWS = "--rows"
    TARGET_COL = "--target-col"
    PREDICTION_COLS = "--prediction-cols"
    ASSOC_ID = "--assoc-id-col"
    PREDICTION_TIME = "--prediction-time"
    TIMESTAMP_COL = "--timestamp-col"
    ACTED_ON_COL = "--acted-on-col"
    ACTUAL_VALUE_COL = "--actual-value-col"
    DRY_RUN = "--dry-run"
    STATUS_FILE = "--status-file"
    REASON = "--reason"
    WAIT = "--wait"
    TIMEOUT = "--timeout"
    FILESYSTEM_DIR = "--filesystem-directory"
    CLASS_NAMES = "--class-names"
    FROM_SPOOL = "--from-spool"
    SEARCH = "--search"
    LIMIT = "--limit"
    NUM_CONCURRENT_REQUESTS = "--num-concurrent-requests"


class RunMode(Enum):
    PERF_TEST = Subjects.PERF_TEST
    PREDICTIONS = Subjects.PREDICTIONS
    ACTUALS = Subjects.ACTUALS
    MODEL = Subjects.MODEL
    DATASET = Subjects.DATASET
    DEPLOYMENT = Subjects.DEPLOYMENT
    PREDICTION_ENVIRONMENT = Subjects.PREDICTION_ENVIRONMENT
    SERVICE_STATS = Subjects.SERVICE_STATS

    @staticmethod
    def list_all():
        all_subjects = ""
        for m in RunMode:
            all_subjects = "{} {}".format(all_subjects, m.value)
        return all_subjects


REPLACEMENT_REASONS = ["ACCURACY", "DATA_DRIFT", "ERRORS", "SCHEDULED_REFRESH", "SCORING_SPEED",
                       "OTHER"]


common_fields_keys = SerializationConstants.GeneralConstants
deployment_stats_keys = SerializationConstants.DeploymentStatsConstants
predictions_data_keys = SerializationConstants.PredictionsDataConstants
external_events_keys = SerializationConstants.EventConstants
config_keys = config.ConfigConstants


class MLOpsCliArgParser:
    SUBJECT_KEYWORD = "subject"
    ACTION_KEYWORD = "action"

    parser = None

    @staticmethod
    def _is_valid_file(arg):
        abs_path = os.path.abspath(arg)
        if not os.path.exists(arg):
            raise argparse.ArgumentTypeError("The file {} does not exist.".format(arg))
        else:
            return os.path.realpath(abs_path)

    @staticmethod
    def _register_arg_version(*parsers):
        for parser in parsers:
            parser.add_argument(
                "--version", action="version",
                version="%(prog)s {version}".format(version=Constants.MLOPS_VERSION)
            )

    @staticmethod
    def _register_arg_verbose(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.VERBOSE, action="store_true", default=False,
                help="Set logging to DEBUG level"
            )

    @staticmethod
    def _register_arg_quiet(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.QUIET, action="store_true", default=False,
                help="Set logging to ERROR level"
            )

    @staticmethod
    def _register_arg_json(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.JSON, action="store_true", default=False,
                help="Return JSON as output for create/get/list/delete/deploy"
            )

    @staticmethod
    def _register_arg_terse(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.TERSE, action="store_true", default=False,
                help="Only return ID(s) as output for create/get/list/delete/deploy"
            )

    @staticmethod
    def _register_arg_subject(*parsers):
        for parser in parsers:
            parser.add_argument(
                dest=MLOpsCliArgParser.SUBJECT_KEYWORD,
                choices=Subjects.ALL_SUBJECTS
            )

    @staticmethod
    def _register_arg_action(*parsers):
        for parser in parsers:
            parser.add_argument(
                dest=MLOpsCliArgParser.ACTION_KEYWORD,
                choices=Actions.ALL_ACTIONS
            )

    @staticmethod
    def _register_arg_reason(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.REASON, default="OTHER", choices=REPLACEMENT_REASONS
            )

    @staticmethod
    def _register_arg_deployment_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.DEPLOYMENT_ID,
                default=os.environ.get(EV.MLOPS_DEPLOYMENT_ID, None),
                help="Deployment ID to use for monitoring model predictions "
                "(env: {})".format(EV.MLOPS_DEPLOYMENT_ID),
            )

    @staticmethod
    def _register_arg_pe_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.PREDICTION_ENVIRONMENT_ID,
                default=os.environ.get(EV.MLOPS_PREDICTION_ENVIRONMENT_ID, None),
                help="Prediction Environment ID "
                     "(env: {})".format(EV.MLOPS_PREDICTION_ENVIRONMENT_ID),
            )

    @staticmethod
    def _register_arg_deployment_label(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.DEPLOYMENT_LABEL,
                default=os.environ.get(EV.MLOPS_DEPLOYMENT_LABEL, None),
                help="Deployment label to use when creating a deployment "
                "(env: {})".format(EV.MLOPS_DEPLOYMENT_LABEL),
            )

    @staticmethod
    def _register_arg_model_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.MODEL_ID,
                default=os.environ.get(EV.MLOPS_MODEL_ID, None),
                help="Model ID to use for model package creation or prediction monitoring "
                "(env: {})".format(EV.MLOPS_MODEL_ID),
            )

    @staticmethod
    def _register_arg_model_package_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.MODEL_PACKAGE_ID,
                default=os.environ.get(EV.MLOPS_MODEL_PACKAGE_ID, None),
                help="Model package ID to use for model package deployment "
                "(env: {})".format(EV.MLOPS_MODEL_PACKAGE_ID),
            )

    @staticmethod
    def _register_arg_dataset_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.DATASET_ID,
                default=os.environ.get(EV.MLOPS_DATASET_ID, None),
                help="Dataset ID to use for AI catalog operations "
                "(env: {})".format(EV.MLOPS_DATASET_ID),
            )

    @staticmethod
    def _register_arg_training_dataset_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.TRAINING_DATASET_ID,
                default=os.environ.get(EV.MLOPS_TRAINING_DATASET_ID, None),
                help="Dataset ID to use for training set model package creation "
                "(env: {})".format(EV.MLOPS_TRAINING_DATASET_ID),
            )

    @staticmethod
    def _register_arg_holdout_dataset_id(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.HOLDOUT_DATASET_ID,
                default=os.environ.get(EV.MLOPS_HOLDOUT_DATASET_ID, None),
                help="Dataset ID to use for holdout set model package creation "
                "(env: {})".format(EV.MLOPS_HOLDOUT_DATASET_ID),
            )

    @staticmethod
    def _register_arg_json_conf(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.JSON_CONF,
                help="JSON configuration to use for object creation",
            )

    @staticmethod
    def _register_arg_output_dir(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.OUTPUT_DIRECTORY,
                dest="output_dir",
                default="/tmp/",
                help="Output directory to write model package file to",
            )

    @staticmethod
    def _register_arg_mlops_service(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.MLOPS_SERVICE,
                dest="mlops_service_url",
                default=os.environ.get(EV.MLOPS_SERVICE_URL, None),
                help="MLOps service URL to use (env: {})".format(EV.MLOPS_SERVICE_URL),
            )

    @staticmethod
    def _register_arg_mlops_api_token(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.MLOPS_API_TOKEN,
                dest="mlops_api_token",
                default=os.environ.get(EV.MLOPS_API_TOKEN, None),
                help="MLOps API Token to use for connecting (env: {})".format(EV.MLOPS_API_TOKEN),
            )

    @staticmethod
    def _register_arg_verify_ssl(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.VERIFY_SSL,
                dest="verify_ssl",
                default=True,
                help="Verify SSL connection to DataRobot MLOps",
            )

    @staticmethod
    def _register_arg_search(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.SEARCH,
                dest="search",
                default=None,
                help="Search filter to use when listing items",
            )

    @staticmethod
    def _register_arg_limit(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.LIMIT,
                dest="limit",
                default=None,
                help="Maximum items to return when listing items",
            )

    @staticmethod
    def _register_arg_input(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.INPUT,
                default=None,
                type=MLOpsCliArgParser._is_valid_file,
                help="Path to an input dataset",
            )

    @staticmethod
    def _register_arg_wait(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.WAIT,
                default=False,
                action="store_true",
                help="Wait for request to MLOps to complete",
            )

    @staticmethod
    def _register_arg_timeout(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.TIMEOUT,
                default=120,
                type=int,
                help="Timeout value for connection in seconds (default: %(default)s s)",
            )

    @staticmethod
    def _register_arg_count(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.COUNT,
                default=5,
                type=int,
                help="Number of iterations; depends on the context in which it is called",
            )

    @staticmethod
    def _register_arg_rows(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.ROWS,
                default=-1,
                type=int,
                help="Number of rows to use from input file",
            )

    @staticmethod
    def _register_target_col(*parsers, default_value=None):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.TARGET_COL,
                default=default_value,
                type=str,
                help="Name of target column in input data",
            )

    @staticmethod
    def _register_prediction_cols(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.PREDICTION_COLS,
                default=None,
                nargs="+",
                type=str,
                help="Name of prediction column(s) in input data",
            )

    @staticmethod
    def _register_class_names(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.CLASS_NAMES,
                default=None,
                nargs="+",
                type=str,
                help="Name of classes for classification data",
            )

    @staticmethod
    def _register_prediction_time(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.PREDICTION_TIME,
                type=int,
                default=10,
                help="Time it took to compute predictions in milliseconds "
                "(default: %(default)s ms)",
            )

    @staticmethod
    def _register_assoc_id_col(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.ASSOC_ID,
                type=str,
                help="Name of association ID column in input data",
            )

    @staticmethod
    def _register_actual_value_col(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.ACTUAL_VALUE_COL,
                type=str,
                help="Name of actual value column in input data",
            )

    @staticmethod
    def _register_acted_on_col(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.ACTED_ON_COL,
                default=None,
                type=str,
                help="Name of was-acted-on column in input data",
            )

    @staticmethod
    def _register_timestamp_col(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.TIMESTAMP_COL,
                default=None,
                type=str,
                help="Name of timestamp column in input data",
            )

    @staticmethod
    def _register_dry_run(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.DRY_RUN,
                action="store_true",
                default=False,
                help="Dry run; no actual requests will be sent to DataRobot MLOps"
            )

    @staticmethod
    def _register_status_file(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.STATUS_FILE,
                default=None,
                help="Path to file tracking status of upload",
            )

    @staticmethod
    def _register_from_spool(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.FROM_SPOOL,
                action="store_true",
                default=False,
                help="Report prediction data from spooler"
            )

    @staticmethod
    def _register_filesystem_dir(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.FILESYSTEM_DIR,
                default=os.environ.get(config_keys.FILESYSTEM_DIRECTORY.name, None),
                help="Path to filesystem spool directory",
            )

    @staticmethod
    def _register_arg_num_concurrent_requests(*parsers):
        for parser in parsers:
            parser.add_argument(
                ArgumentsOptions.NUM_CONCURRENT_REQUESTS,
                default=1,  # 1 concurrent request => synchronous
                type=int,
                help="Number of concurrent requests for async reporting",
            )

    @staticmethod
    def _gen_parser(subcommand, help_msg, description=None):
        subparser = MLOpsCliArgParser._subparsers.add_parser(subcommand,
                                                             help=help_msg,
                                                             description=description,
                                                             formatter_class=RawTextHelpFormatter)
        MLOpsCliArgParser._parsers[subcommand] = subparser
        return subparser

    @staticmethod
    def _add_perf_subcommand(parser):
        MLOpsCliArgParser._register_arg_input(parser)
        MLOpsCliArgParser._register_arg_count(parser)
        MLOpsCliArgParser._register_arg_rows(parser)

    @staticmethod
    def _add_predictions_subcommand(parser):
        MLOpsCliArgParser._register_prediction_time(parser)
        MLOpsCliArgParser._register_filesystem_dir(parser)
        MLOpsCliArgParser._register_from_spool(parser)
        MLOpsCliArgParser._register_arg_num_concurrent_requests(parser)

    @staticmethod
    def _add_actuals_subcommand(parser):
        MLOpsCliArgParser._register_arg_wait(parser)

        MLOpsCliArgParser._register_actual_value_col(parser)
        MLOpsCliArgParser._register_acted_on_col(parser)
        MLOpsCliArgParser._register_timestamp_col(parser)

    @staticmethod
    def _add_model_subcommand(parser):
        # for model deployment only
        MLOpsCliArgParser._register_arg_deployment_label(parser)

        # for model download only
        MLOpsCliArgParser._register_arg_output_dir(parser)

        # for model package creation only
        MLOpsCliArgParser._register_arg_training_dataset_id(parser)
        MLOpsCliArgParser._register_arg_holdout_dataset_id(parser)

        # for model replacement only
        MLOpsCliArgParser._register_arg_reason(parser)

    @staticmethod
    def get_arg_parser():
        parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description="""
        A command line tool for interacting with DataRobot MLOps app.
        All commands require --mlops-service-url and --mlops-api-token or that
        MLOPS_SERVICE_URL and MLOPS_API_TOKEN are set as environment variables.

        Usage is <subject> <action> followed by options. For example:

          # create a prediction environment
          prediction-environment create --json-config <>

          # get information about a prediction environment
          prediction-environment get --prediction-environment-id <>

          # delete a prediction environment (must not have any deployments)
          prediction-environment delete --prediction-environment-id <>

          # upload a dataset into the AI catalog
          dataset upload --input <>

          # delete a dataset from the AI catalog
          dataset delete --dataset-id <>

          # create an external model package
          model create --json-config <> --training-dataset-id <> --holdout-dataset-id <>

          # get model package metadata
          model get --model-package-id <>

          # deploy a model package
          model deploy --model-package-id <> --deployment-label <>

          # download the current model artifact from a deployment (for non-external models only)
          model download --deployment-id <>

          # delete a model package
          model delete --model-package-id <>

          # get metadata about a deployment
          deployment get --deployment-id <>

          # delete a deployment
          deployment delete --deployment-id <>

          # upload a ScoringCode classification csv file
          predictions report --prediction-cols <col1> <col2> --input <> --class-names <c1> <c2>

          # upload a spool file
          predictions report --from-spool

          # upload a scoring file to a deployment
          predictions upload --input <> --target-col <> --class-names <>

          # upload an actuals file to a deployment
          actuals report --input <> --actual-value-col <> --assoc-id-col <>

          # measure performance
          perf run --input <> --target-col <> --class-names <> --deployment-id <> --model-id <>
        """)
        MLOpsCliArgParser._register_arg_version(parser)
        MLOpsCliArgParser._register_arg_verbose(parser)
        MLOpsCliArgParser._register_arg_quiet(parser)
        MLOpsCliArgParser._register_arg_json(parser)
        MLOpsCliArgParser._register_arg_terse(parser)

        MLOpsCliArgParser._register_arg_mlops_service(parser)
        MLOpsCliArgParser._register_arg_mlops_api_token(parser)
        MLOpsCliArgParser._register_arg_verify_ssl(parser)

        MLOpsCliArgParser._register_arg_subject(parser)
        MLOpsCliArgParser._register_arg_action(parser)

        MLOpsCliArgParser._parsers = parser

        # multi-use parameters
        MLOpsCliArgParser._register_arg_deployment_id(parser)
        MLOpsCliArgParser._register_arg_pe_id(parser)
        MLOpsCliArgParser._register_arg_model_id(parser)
        MLOpsCliArgParser._register_arg_model_package_id(parser)
        MLOpsCliArgParser._register_target_col(parser)
        MLOpsCliArgParser._register_prediction_cols(parser)
        MLOpsCliArgParser._register_class_names(parser)
        MLOpsCliArgParser._register_dry_run(parser)
        MLOpsCliArgParser._register_status_file(parser)
        MLOpsCliArgParser._register_assoc_id_col(parser)
        MLOpsCliArgParser._register_arg_json_conf(parser)
        MLOpsCliArgParser._register_arg_dataset_id(parser)
        MLOpsCliArgParser._register_arg_timeout(parser)
        MLOpsCliArgParser._register_arg_search(parser)
        MLOpsCliArgParser._register_arg_limit(parser)

        MLOpsCliArgParser._add_perf_subcommand(parser)
        MLOpsCliArgParser._add_predictions_subcommand(parser)
        MLOpsCliArgParser._add_actuals_subcommand(parser)
        MLOpsCliArgParser._add_model_subcommand(parser)
        return parser


class MLOpsCSVSplitter:
    def __init__(self, filename, chunk_size, skip_rows=0):
        self.filename = filename
        self.chunk_size = chunk_size
        self.skip_rows = skip_rows
        # Because we want to skip 'n' rows, but still want to keep the header (as it contains the
        # column names), we skip rows from range 1 to that offset)
        self.headers = pd.read_csv(filename, nrows=1).columns.tolist()
        logger.info("Reading input data after skipping '{}' rows".format(self.skip_rows))
        self.reader = pd.read_csv(
            filename, skiprows=range(1, self.skip_rows), chunksize=self.chunk_size
        )
        self._next_chunk = None
        self._current_row = self.skip_rows

    def get_columns(self):
        return self.headers

    def get_data_chunks(self):
        # Using generator pattern, especially because we are dealing with several GBs of files
        # This will limit the memory usage.
        for chunk in self.reader:
            self._current_row += self.chunk_size
            yield chunk

    def get_current_row(self):
        return self._current_row

    def get_chunk_size(self):
        return self.chunk_size

    def _get_next_chunk(self):
        self._next_chunk = next(self.reader, None)
        if self._next_chunk is not None:
            self._current_row += self.chunk_size

    def is_all_data_reported(self):
        if self._next_chunk is not None:
            return False
        self._get_next_chunk()
        return self._next_chunk is None

    def get_next_chunk_to_report(self):
        if self._next_chunk is None:
            self._get_next_chunk()
        if self._next_chunk is not None:
            chunk = self._next_chunk
            self._get_next_chunk()
            return chunk
        else:
            return None


class MLOpsCSVBatchSplitter(MLOpsCSVSplitter):
    # Batch Splitter can chop big, 100K
    BATCH_CHUNK_SIZE = 100 * 1000

    def __init__(self, filename, skip_rows=0):
        super(MLOpsCSVBatchSplitter, self).__init__(filename, self.BATCH_CHUNK_SIZE, skip_rows)


class MLOpsCSVJSONSplitter(MLOpsCSVSplitter):
    # JSON Post is 10k at a time
    JSON_CHUNK_SIZE = 10000

    def __init__(self, filename, skip_rows=0):
        super(MLOpsCSVJSONSplitter, self).__init__(filename, self.JSON_CHUNK_SIZE, skip_rows)


class MLOpsCli:
    def __init__(self, options):
        self.options = options
        # self.logger = CMRunner._config_logger(runtime.options)
        self.run_mode = RunMode(options.subject)
        self.raw_arguments = sys.argv
        self.csv_splitter = None
        self.status_tracker = None
        self.mclient = None

    def create_mclient(self):
        self.mclient = MLOpsClient(service_url=self.options.mlops_service_url,
                                   api_key=self.options.mlops_api_token,
                                   verify=self.options.verify_ssl,
                                   dry_run=self.options.dry_run)

    def delete_mclient(self):
        if self.mclient is not None:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.mclient.shutdown())

    async def _check_deployment_stats_perf(self):
        logger.info("\n\ndeployment stats performance:")
        start_time = time.time()
        request_num = self.options.count
        for _ in range(0, request_num):
            request_start_time = time.time()
            res = await self.mclient.report_deployment_stats(
                self.options.deployment_id, self.options.model_id, 1, 10
            )
            request_end_time = time.time()
            request_elapsed_ms = (request_end_time - request_start_time) * 1000
            logger.info("request: {} time {:.1f}ms".format(res, request_elapsed_ms))

        end_time = time.time()
        elapsed_time = end_time - start_time
        per_request_ms = (elapsed_time * 1000.0) / request_num

        logger.info("report deployment stats: total: {:.3f}sec sec, per request {:.2f}ms"
                    .format(elapsed_time, per_request_ms))

    async def _check_prediction_data_perf(self):
        logger.info("prediction data performance:")
        start_time = time.time()
        request_num = self.options.count

        input_df = pd.read_csv(self.options.input)
        if self.options.rows > 0:
            input_df = input_df.head(self.options.rows)

        for _ in range(0, request_num):
            request_start_time = time.time()
            res, payload_size = await self.mclient.report_prediction_data(
                self.options.deployment_id,
                self.options.model_id,
                input_df,
                assoc_id_col=None,
                target_col=self.options.target_col,
                class_names=self.options.class_names
            )
            request_end_time = time.time()
            request_elapsed_ms = (request_end_time - request_start_time) * 1000
            logger.info("request: {} payload_size: {} time {:.1f}ms".format(
                res, payload_size, request_elapsed_ms))

        end_time = time.time()
        elapsed_time = end_time - start_time
        per_request_ms = (elapsed_time * 1000.0) / request_num

        logger.info("prediction data: total: {:.3f}sec sec, per request {:.2f}ms"
                    .format(elapsed_time, per_request_ms))

    async def _perf_run_async(self):
        await self._check_deployment_stats_perf()
        await self._check_prediction_data_perf()

    def perf_run(self):
        check_required_parameter(self.options.input, "INPUT", ArgumentsOptions.INPUT)
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        check_required_parameter(self.options.model_id, EV.MLOPS_MODEL_ID,
                                 ArgumentsOptions.MODEL_ID)
        check_required_parameter(self.options.target_col, None, ArgumentsOptions.TARGET_COL)
        check_required_parameter(self.options.class_names, None, ArgumentsOptions.CLASS_NAMES)

        self.create_mclient()
        logger.info("Running performance test:")
        logger.info("MLOps service: {}".format(self.options.mlops_service_url))
        logger.info("Deployment ID: {}".format(self.options.deployment_id))
        logger.info("Model ID:      {}".format(self.options.model_id))
        logger.info("Target:        {}".format(self.options.target_col))
        logger.info("Classes:       {}".format(self.options.class_names))
        logger.info("Input:         {}".format(self.options.input))
        logger.info("Count:         {}".format(self.options.count))
        logger.info("Rows:          {}".format(self.options.rows))

        self.event_loop.run_until_complete(self._perf_run_async())
        self.delete_mclient()

    def _log_report_status(self, input_df, row_offset):
        logger.info("Reporting predictions:")
        logger.debug("MLOps service: {}".format(self.options.mlops_service_url))
        logger.debug("Input:         {}".format(self.options.input))
        logger.info("Input rows:     {}".format(len(input_df)))
        logger.info("Input cols:     {}".format(len(input_df.columns)))
        logger.info("Row Offset:     {}".format(row_offset))
        logger.debug("Dry run:       {}".format(self.options.dry_run))
        logger.debug("Status File:   {}".format(self.status_tracker.get_status_file()))

    async def _report_predictions_connected_lib(self, input_df, row_offset):
        self._log_report_status(input_df, row_offset)

        request_start_time = time.time()
        res, payload_size = await self.mclient.report_prediction_data(
            self.options.deployment_id,
            self.options.model_id,
            input_df,
            assoc_id_col=self.options.assoc_id_col,
            target_col=self.options.target_col,
            prediction_cols=self.options.prediction_cols,
            class_names=self.options.class_names,
            dry_run=self.options.dry_run
        )
        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time) * 1000

        await self.mclient.report_deployment_stats(
            self.options.deployment_id,
            self.options.model_id,
            len(input_df),
            self.options.prediction_time,
            dry_run=self.options.dry_run
        )
        logger.debug("Row offset: {} payload_size: {} time {:.1f}ms"
                     .format(row_offset, payload_size, request_elapsed_ms))

    def _get_association_ids(self, input_df):
        # TODO: method never called...delete? otherwise, change print -> logger
        if self.options.assoc_id_col is None:
            print("No association ID column set")
            return None

        if self.options.assoc_id_col not in input_df.columns:
            raise Exception(
                "Association ID feature '{}' is not present in the input data".format(
                    self.options.assoc_id_col
                )
            )

        return input_df[self.options.assoc_id_col].tolist()

    def _report_predictions_async(self):
        self.event_loop.run_until_complete(self._data_dispatcher())

    async def _data_dispatcher(self):
        num_rows, iteration = self.status_tracker.get_status()
        tasks = list()
        for input_df_chunk in self.csv_splitter.get_data_chunks():
            tasks.append(
                asyncio.create_task(
                    self._report_predictions_connected_lib(input_df_chunk, num_rows)
                )
            )
            num_rows = self.csv_splitter.get_current_row()
            if len(tasks) == self.options.num_concurrent_requests:
                break

        while not self.csv_splitter.is_all_data_reported():
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                tasks.remove(task)
                # num_rows += task.result()
                # iteration += 1
                # self.status_tracker.update_status(num_rows, iteration)
                input_df_chunk = self.csv_splitter.get_next_chunk_to_report()
                if input_df_chunk is None:
                    continue
                num_rows = self.csv_splitter.get_current_row()
                new_task = asyncio.create_task(
                    self._report_predictions_connected_lib(input_df_chunk, num_rows)
                )
                tasks.append(new_task)
                logger.debug("Added new task to report rows from {} to {}".format(
                    num_rows, num_rows + self.csv_splitter.get_chunk_size()
                ))

        # No more data to report, all tasks submitted, but lets wait for their completion
        logger.info("Done with submitting all tasks; waiting for them to finish now.")
        await asyncio.wait(tasks)
        logger.info("Done reporting all data.")

    async def _report_predictions_from_spooler(self, record, spooler):
        data_type = record.get_data_type()
        payload = record.get_payload()
        request_start_time = time.time()
        if data_type == DataType.DEPLOYMENT_STATS:
            await self.mclient.report_deployment_stats(
                record.get_deployment_id(),
                payload[common_fields_keys.MODEL_ID_FIELD_NAME],
                payload[deployment_stats_keys.NUM_PREDICTIONS_FIELD_NAME],
                payload[deployment_stats_keys.EXECUTION_TIME_FIELD_NAME],
                payload[common_fields_keys.TIMESTAMP_FIELD_NAME],
                dry_run=self.options.dry_run
            )
        elif data_type == DataType.PREDICTIONS_DATA:
            df, assoc_id, predictions, class_names = [None] * 4
            if predictions_data_keys.FEATURES_FIELD_NAME in payload:
                df = pd.DataFrame.from_dict(payload[predictions_data_keys.FEATURES_FIELD_NAME])
            if predictions_data_keys.ASSOCIATION_IDS_FIELD_NAME in payload:
                assoc_id = payload[predictions_data_keys.ASSOCIATION_IDS_FIELD_NAME]
            if predictions_data_keys.PREDICTIONS_FIELD_NAME in payload:
                predictions = payload[predictions_data_keys.PREDICTIONS_FIELD_NAME]
            if predictions_data_keys.CLASS_NAMES_FIELD_NAME in payload:
                class_names = payload[predictions_data_keys.CLASS_NAMES_FIELD_NAME]
            await self.mclient.report_prediction_data(
                record.get_deployment_id(),
                payload[common_fields_keys.MODEL_ID_FIELD_NAME],
                df,
                association_ids=assoc_id,
                predictions=predictions,
                class_names=class_names,
                timestamp=payload[common_fields_keys.TIMESTAMP_FIELD_NAME],
                dry_run=self.options.dry_run
            )

            row_count = df.shape[0] if df is not None else len(predictions)
        else:
            logger.warn("Connected client does not handle data type: '{}'".format(data_type.name))

        if spooler.enable_dequeue_ack_record:
            spooler.ack_records([record.get_id()])

        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time) * 1000
        if data_type == DataType.DEPLOYMENT_STATS:
            logger.debug("Reporting stats predictions: {} execution time: {}".format(
                payload[deployment_stats_keys.NUM_PREDICTIONS_FIELD_NAME],
                payload[deployment_stats_keys.EXECUTION_TIME_FIELD_NAME]
            ))
        elif data_type == DataType.PREDICTIONS_DATA:
            logger.debug("Reporting feature data, row count: {}".format(row_count))
        logger.debug("Reporting latency: {:.1f}ms".format(request_elapsed_ms))

    def report_predictions_from_spool(self):
        self.create_mclient()
        try:
            spooler_type = config.get_config_default(
                config.ConfigConstants.SPOOLER_TYPE,
                SpoolerType.FILESYSTEM.name
            )
            # If the user has already set the config explicitly, don't worry about it.
            with suppress(DRConfigKeyAlreadyAssigned):
                # Set max number of request per dequeue call, to number of concurrent request
                config.set_config_safely(
                    config.ConfigConstants.SPOOLER_DEQUEUE_MAX_RECORDS_PER_CALL,
                    self.options.num_concurrent_requests
                )
            spooler = RecordSpoolerFactory().create(SpoolerType[spooler_type])
            spooler.set_config()
            spooler.open(action=MLOpsSpoolAction.DEQUEUE)

            # Some exceptions (like KeyboardInterrupt) don't work as expected inside the
            # event-loop so setup the spooler here and make sure it gets closed.
            with closing(spooler):
                self.event_loop.run_until_complete(self._spool_data_dispatcher(spooler))
        finally:
            self.delete_mclient()

    async def _spool_data_dispatcher(self, spooler):
        tasks = list()
        total_records = 0
        log_interval_sec = 180
        start_time = time.time()
        next_log_time = start_time + log_interval_sec

        while not spooler.empty():
            record_list = spooler.dequeue()
            total_records += len(record_list)
            for record in record_list:
                tasks.append(
                    asyncio.create_task(self._report_predictions_from_spooler(record, spooler))
                )
            if len(tasks) == self.options.num_concurrent_requests:
                break

        while not spooler.empty() and tasks:
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                tasks.remove(task)
                record_list = spooler.dequeue()
                total_records += len(record_list)
                for record in record_list:
                    new_task = asyncio.create_task(
                        self._report_predictions_from_spooler(record, spooler)
                    )
                    tasks.append(new_task)
            if time.time() >= next_log_time:  # log updated metrics every couple of minutes
                elapsed = time.time() - start_time
                logger.info("Records processed so far: %s", total_records)
                logger.info("Current Throughput: %.02f (records/s)", total_records / elapsed)
                next_log_time = time.time() + log_interval_sec

        runtime = time.time() - start_time
        logger.info("Runtime: %.02f minutes", runtime / 60)
        logger.info("Total records processed: %s", total_records)
        logger.info("Overall Throughput: %.02f (records/s)", total_records / runtime)
        # No more data to report, all tasks submitted, but let's wait for their completion
        logger.info("Done with submitting all tasks; waiting for them to finish now.")

        if tasks:
            await asyncio.wait(tasks)
        logger.info("Done reporting all data.")

    def _check_columns(self, columns):
        if self.options.prediction_cols is not None:
            for prediction_col in self.options.prediction_cols:
                if prediction_col not in columns:
                    raise DRCommonException(
                        "Prediction column {} not found in input file.".format(prediction_col))
            if self.options.class_names is not None:
                if len(self.options.class_names) != len(self.options.prediction_cols):
                    raise DRCommonException(
                        "The number of class names and prediction columns must match.")
        if self.options.target_col is not None:
            if self.options.target_col not in columns:
                raise DRCommonException(
                    "Target column {} not found in input file.".format(self.options.target_col))
        if self.options.assoc_id_col is not None:
            if self.options.assoc_id_col not in columns:
                raise DRCommonException(
                    "Association ID column {} not found in input file."
                    .format(self.options.assoc_id_col))

    def report_predictions(self):
        check_required_parameter(self.options.input, None, ArgumentsOptions.INPUT)
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        check_required_parameter(self.options.model_id, EV.MLOPS_MODEL_ID,
                                 ArgumentsOptions.MODEL_ID)

        logger.debug("Reporting predictions:")
        logger.debug("MLOps service:         {}".format(self.options.mlops_service_url))
        logger.debug("Input:                 {}".format(self.options.input))
        logger.debug("Target column:         {}".format(self.options.target_col))
        logger.debug("Prediction column(s):  {}".format(self.options.prediction_cols))
        logger.debug("Classes:               {}".format(self.options.class_names))
        logger.debug("Assoc Id column:       {}".format(self.options.assoc_id_col))
        logger.debug("Dry run:               {}".format(self.options.dry_run))

        if self.options.status_file:
            self.status_tracker = MLOpsUploadTracker(self.options.status_file)
        else:
            self.status_tracker = MLOpsUploadTracker()
        skip_rows, _ = self.status_tracker.get_status()
        try:
            self.csv_splitter = MLOpsCSVJSONSplitter(self.options.input, skip_rows=skip_rows)
            self._check_columns(self.csv_splitter.get_columns())
        except (pd.errors.EmptyDataError, DRCommonException) as e:
            self._log_error_and_exit(e, ExitCode.DEFAULT.value)

        try:
            self.create_mclient()
            self._report_predictions_async()
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def get_prediction_stats(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        self.create_mclient()
        self._log_get_action("deployment", self.options.deployment_id, "prediction stats")
        try:
            stats = self.mclient.get_prediction_stats(self.options.deployment_id,
                                                      self.options.model_id)
            self._print_resource_received(self.options.deployment_id, stats)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def get_service_stats(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        self.create_mclient()
        if self.options.model_id is None:
            self._log_get_action("deployment", self.options.deployment_id, "service stats")
        else:
            self._log_get_action("deployment", self.options.deployment_id,
                                 "service stats for model ID {}".format(self.options.model_id))
        try:
            stats = self.mclient.get_service_stats(
                self.options.deployment_id, self.options.model_id)
            self._print_resource_received(self.options.deployment_id, stats)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def report_actuals(self):
        check_required_parameter(self.options.deployment_id, None, ArgumentsOptions.DEPLOYMENT_ID)
        check_required_parameter(self.options.input, None, ArgumentsOptions.INPUT)
        check_required_parameter(self.options.actual_value_col, None,
                                 ArgumentsOptions.ACTUAL_VALUE_COL)
        check_required_parameter(self.options.assoc_id_col, None, ArgumentsOptions.ASSOC_ID)

        self.create_mclient()

        input_df = pd.read_csv(self.options.input)

        logger.info("Reporting actuals:")
        logger.info("MLOps service:         {}".format(self.options.mlops_service_url))
        logger.info("Deployment ID:         {}".format(self.options.deployment_id))
        logger.info("Input:                 {}".format(self.options.input))
        logger.info("Input rows:            {}".format(len(input_df)))
        logger.info("Actual value column:   {}".format(self.options.actual_value_col))
        logger.info("Assoc ID column:       {}".format(self.options.assoc_id_col))
        logger.info("Was-acted-on column:   {}".format(self.options.acted_on_col))
        logger.info("Timestamp column:      {}".format(self.options.timestamp_col))

        def progress_callback(total_nr_actuals, nr_actuals_sent, request_time):
            logger.info("Actuals sent: {} / {} : {:.3f} sec"
                        .format(nr_actuals_sent, total_nr_actuals, request_time))

        request_start_time = time.time()
        ret_val = \
            self.mclient.submit_actuals_from_dataframe(
                self.options.deployment_id,
                input_df,
                assoc_id_col=self.options.assoc_id_col,
                actual_value_col=self.options.actual_value_col,
                was_act_on_col=self.options.acted_on_col,
                timestamp_col=self.options.timestamp_col,
                progress_callback=progress_callback,
                wait_for_result=self.options.wait,
                timeout=self.options.timeout
            )
        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time)
        logger.debug("request: {} : time {:.2f} sec".format(ret_val, request_elapsed_ms))
        self.delete_mclient()

    def _generate_temp_csv_filename(self, iteration):
        prefix = "/tmp/" + os.path.basename(self.options.input).replace(".csv", "")
        return prefix + str(iteration) + ".csv"

    async def _upload_scoring_dataset_batch(self, input_df, row_offset, iteration):
        """ Upload a scoring dataset and associate it with a deployment. """
        # This is just the filename generated and issued for display in "AI Catalog"; there is no
        # actual file written to disk.  Dataframe is streamed to the MLOps in CSV format.
        csv_file_name = self._generate_temp_csv_filename(iteration)
        logger.info("Set scoring dataset:")
        logger.debug("MLOps service: {}".format(self.options.mlops_service_url))
        logger.info("Deployment ID:  {}".format(self.options.deployment_id))
        logger.info("Model ID:       {}".format(self.options.model_id))
        logger.info("Target:         {}".format(self.options.target_col))
        logger.info("Classes:        {}".format(self.options.class_names))
        logger.debug("Input:         {}".format(self.options.input))
        logger.info("Input rows:     {}".format(len(input_df)))
        logger.info("Input cols:     {}".format(len(input_df.columns)))
        logger.info("Row Offset:     {}".format(row_offset))
        logger.debug("Dry run:       {}".format(self.options.dry_run))
        logger.debug("Status File:   {}".format(self.status_tracker.get_status_file()))
        logger.debug("CSV FileName:  {}".format(csv_file_name))

        if len(input_df) < 1:
            logger.debug("All rows already uploaded.")
            return

        request_start_time = time.time()
        dataset_id = self.mclient.upload_dataframe(
            input_df, csv_file_name, dry_run=self.options.dry_run
        )
        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time) * 1000
        logger.debug("Upload done: time {:.1f}ms".format(request_elapsed_ms))

        request_start_time = time.time()
        self.mclient.associate_deployment_dataset(
            self.options.deployment_id,
            dataset_id,
            DatasetSourceType.SCORING,
            dry_run=self.options.dry_run
        )
        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time) * 1000
        logger.debug("Association done: time {:.1f}ms".format(request_elapsed_ms))

        # Remove the dataset after association is done
        self.mclient.soft_delete_dataset(dataset_id)

        request_start_time = time.time()
        res, payload_size = await self.mclient.report_prediction_data(
            self.options.deployment_id,
            self.options.model_id,
            input_df,
            target_col=self.options.target_col,
            class_names=self.options.class_names,
            dry_run=self.options.dry_run,
        )
        request_end_time = time.time()
        request_elapsed_ms = (request_end_time - request_start_time) * 1000
        logger.debug("request: {} payload_size: {} time {:.1f}ms"
                     .format(res, payload_size, request_elapsed_ms))

    async def _upload_scoring_dataset_async(self):
        if self.options.status_file:
            self.status_tracker = MLOpsUploadTracker(self.options.status_file)
        else:
            self.status_tracker = MLOpsUploadTracker()
        skip_rows, iteration = self.status_tracker.get_status()
        csv_splitter = MLOpsCSVBatchSplitter(self.options.input, skip_rows=skip_rows)
        num_rows = skip_rows
        for input_df_chunk in csv_splitter.get_data_chunks():
            await self._upload_scoring_dataset_batch(input_df_chunk, num_rows, iteration)
            num_rows += input_df_chunk.shape[0]
            self.status_tracker.update_status(num_rows, iteration)
            iteration += 1

    def upload_scoring_dataset(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        check_required_parameter(self.options.model_id, EV.MLOPS_MODEL_ID,
                                 ArgumentsOptions.MODEL_ID)
        check_required_parameter(self.options.target_col, None, ArgumentsOptions.TARGET_COL)
        check_required_parameter(self.options.input, "INPUT", ArgumentsOptions.INPUT)
        self.create_mclient()
        try:
            self.event_loop.run_until_complete(self._upload_scoring_dataset_async())
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def upload_dataset(self):
        check_required_parameter(self.options.input, None, ArgumentsOptions.INPUT)
        self.create_mclient()
        dataset = self.options.input
        logger.info("Uploading dataset - {}. This may take some time...".format(dataset))
        try:
            if self.options.timeout:
                dataset_id = self.mclient.upload_dataset(dataset, timeout=self.options.timeout)
            else:
                dataset_id = self.mclient.upload_dataset(dataset)
            self._print_resource_generic_action(dataset_id)
            logger.info("Dataset uploaded. Dataset ID {}.".format(dataset_id))
        except Exception as e:
            feature_drift_error_message = (
                "Dataset upload failed. You won't see Feature Drift reports in UI.")
            logger.error(feature_drift_error_message)
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED)
        finally:
            self.delete_mclient()

    def get_dataset(self):
        check_required_parameter(self.options.dataset_id, EV.MLOPS_DATASET_ID,
                                 ArgumentsOptions.DATASET_ID)
        self.create_mclient()
        self._log_get_action("dataset", self.options.dataset_id)
        try:
            info = self.mclient.get_dataset(self.options.dataset_id)
            self._print_resource_received(self.options.dataset_id, info)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def list_datasets(self):
        self.create_mclient()
        self._log_list_action("dataset")
        params = None
        # TODO: using any limit seems to return 0 results
        if self.options.limit:
            params = {"limit": self.options.limit}

        try:
            all_results = self.mclient.list_datasets(params)
            # datasets don't have a name filter, so do that here
            if self.options.search:
                filtered_results = []
                for result in all_results:
                    if self.options.search in result.get("name"):
                        filtered_results.append(result)
            else:
                filtered_results = all_results
            self._print_resources_listed(filtered_results, "datasetId")
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def delete_dataset(self):
        check_required_parameter(self.options.dataset_id, None, ArgumentsOptions.DATASET_ID)
        self.create_mclient()
        self._log_delete_action("dataset", self.options.dataset_id)
        try:
            self.mclient.soft_delete_dataset(self.options.dataset_id)
            self._print_resource_generic_action(self.options.dataset_id)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def download_model_package(self):
        check_required_parameter(self.options.deployment_id, "MLOPS_DEPLOYMENT_ID",
                                 ArgumentsOptions.DEPLOYMENT_ID)

        self.create_mclient()
        logger.debug("Downloading current model package:")
        logger.debug("MLOps service:          {}".format(self.options.mlops_service_url))
        logger.debug("Deployment ID:          {}".format(self.options.deployment_id))
        logger.debug("Output directory:       {}".format(self.options.output_dir))

        mlpkg_path = self.mclient.download_dr_current_model_package(
            self.options.deployment_id, self.options.output_dir
        )

        logger.debug("Model Package path     {}".format(mlpkg_path))

        self.delete_mclient()

    def get_model_package(self):
        check_required_parameter(self.options.model_package_id, EV.MLOPS_MODEL_PACKAGE_ID,
                                 ArgumentsOptions.MODEL_PACKAGE_ID)
        self.create_mclient()
        self._log_get_action("model package", self.options.model_package_id)
        try:
            info = self.mclient.get_model_package(self.options.model_package_id)
            self._print_resource_received(self.options.model_package_id, info)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def list_model_packages(self):
        self.create_mclient()
        self._log_list_action("model package")
        try:
            info = self.mclient.list_model_packages(self.get_list_params())
            self._print_resources_listed(info)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def delete_model_package(self):
        check_required_parameter(self.options.model_package_id, EV.MLOPS_MODEL_PACKAGE_ID,
                                 ArgumentsOptions.MODEL_PACKAGE_ID)
        self.create_mclient()
        self._log_delete_action("model package", self.options.model_package_id)
        try:
            # until we support a real delete, we just archive.
            self.mclient.archive_model_package(self.options.model_package_id)
            self._print_resource_generic_action(self.options.model_package_id)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def _read_json_config(self, config_file):
        config_path = os.path.abspath(config_file)
        with open(config_path, "r") as f:
            info = json.loads(f.read())
        return info

    def create_model_package(self):
        check_required_parameter(self.options.json_config, None, ArgumentsOptions.JSON_CONF)
        self.create_mclient()
        logger.info("Creating model package:")
        logger.debug("MLOps service:         {}".format(self.options.mlops_service_url))
        logger.info("Model config:           {}".format(self.options.json_config))

        model_info = self._read_json_config(self.options.json_config)
        if self.options.model_id is not None:
            model_info["modelId"] = self.options.model_id
            logger.debug("Model ID:              {}".format(self.options.model_id))

        # if specified, add training_data to model configuration
        if (self.options.training_dataset_id is not None
                or self.options.holdout_dataset_id is not None):
            datasets = {}
            if self.options.training_dataset_id is not None:
                datasets["trainingDataCatalogId"] = self.options.training_dataset_id
                logger.debug("Training dataset ID:   {}".format(self.options.training_dataset_id))
            if self.options.holdout_dataset_id is not None:
                datasets["holdoutDataCatalogId"] = self.options.holdout_dataset_id
                logger.debug("Holdout dataset ID:    {}".format(self.options.holdout_dataset_id))
            model_info["datasets"] = datasets
        try:
            model_pkg_id = self.mclient.create_model_package(model_info)
            self._print_resource_generic_action(model_pkg_id)
            logger.info("Created model package ID {}.".format(model_pkg_id))
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def deploy_model_package(self):
        check_required_parameter(self.options.model_package_id, EV.MLOPS_MODEL_PACKAGE_ID,
                                 ArgumentsOptions.MODEL_PACKAGE_ID)
        self.create_mclient()
        logger.info("Deploying model package to prediction environment. This may take some time...")
        logger.debug("MLOps service:            {}".format(self.options.mlops_service_url))
        logger.info("Model package ID:          {}".format(self.options.model_package_id))
        logger.info("Deployment label:          {}".format(self.options.deployment_label))
        logger.info("Prediction Environment ID: {}".format(self.options.prediction_environment_id))
        try:
            deployment_id = self.mclient.deploy_model_package(
                self.options.model_package_id,
                self.options.deployment_label,
                prediction_environment_id=self.options.prediction_environment_id
            )
            self._print_resource_generic_action(deployment_id)
            logger.info("Model package deployed. Deployment ID {}.".format(deployment_id))

            logger.info("Updating deployment settings for deployment ID {}.".format(deployment_id))
            self.mclient.update_deployment_settings(
                deployment_id,
                target_drift=True,
                feature_drift=True,
                timeout=600
            )
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def replace_model_package(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        check_required_parameter(self.options.model_package_id, EV.MLOPS_MODEL_PACKAGE_ID,
                                 ArgumentsOptions.MODEL_PACKAGE_ID)
        self.create_mclient()
        logger.info("Replacing model package in a deployment:")
        logger.debug("MLOps service:        {}".format(self.options.mlops_service_url))
        logger.info("Model package ID:      {}".format(self.options.model_package_id))
        logger.info("Deployment ID:         {}".format(self.options.deployment_id))
        logger.info("Reason:                {}".format(self.options.reason))
        try:
            self.mclient.replace_model_package(self.options.deployment_id,
                                               self.options.model_package_id,
                                               self.options.reason)
            logger.debug("Model package replaced on deployment {}".format(
                self.options.deployment_id))
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def delete_deployment(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        self.create_mclient()
        self._log_delete_action("deployment", self.options.deployment_id)
        try:
            self.mclient.delete_deployment(self.options.deployment_id, self.options.wait)
            self._print_resource_generic_action(self.options.deployment_id)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def get_deployment(self):
        check_required_parameter(self.options.deployment_id, EV.MLOPS_DEPLOYMENT_ID,
                                 ArgumentsOptions.DEPLOYMENT_ID)
        self.create_mclient()
        self._log_get_action("deployment", self.options.deployment_id)
        try:
            info = self.mclient.get_deployment(self.options.deployment_id)
            if self.options.action == Actions.GET_MODEL:
                model_id = info["model"]["id"]
                self._print_resource_received(model_id, info)
            else:
                self._print_resource_received(self.options.deployment_id, info)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def list_deployments(self):
        self.create_mclient()
        self._log_list_action("deployment")
        try:
            info = self.mclient.list_deployments(self.get_list_params())
            self._print_resources_listed(info)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def create_prediction_environment(self):
        check_required_parameter(self.options.json_config, None, ArgumentsOptions.JSON_CONF)
        info = self._read_json_config(self.options.json_config)
        self.create_mclient()
        try:
            pe_id = self.mclient.create_prediction_environment(info)
            self._print_resource_generic_action(pe_id)
            logger.info("Created prediction environment ID {}.".format(pe_id))
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def get_prediction_environment(self):
        check_required_parameter(self.options.prediction_environment_id,
                                 EV.MLOPS_PREDICTION_ENVIRONMENT_ID,
                                 ArgumentsOptions.PREDICTION_ENVIRONMENT_ID)
        self.create_mclient()
        self._log_get_action("prediction environment", self.options.prediction_environment_id)
        try:
            info = self.mclient.get_prediction_environment(self.options.prediction_environment_id)
            self._print_resource_received(self.options.prediction_environment_id, info)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def list_prediction_environments(self):
        self.create_mclient()
        self._log_list_action("prediction environment")
        try:
            info = self.mclient.list_prediction_environments(self.get_list_params())
            self._print_resources_listed(info)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    def delete_prediction_environment(self):
        check_required_parameter(self.options.prediction_environment_id,
                                 EV.MLOPS_PREDICTION_ENVIRONMENT_ID,
                                 ArgumentsOptions.PREDICTION_ENVIRONMENT_ID)
        self.create_mclient()
        self._log_delete_action("prediction environment", self.options.prediction_environment_id)
        try:
            self.mclient.delete_prediction_environment(self.options.prediction_environment_id)
            self._print_resource_generic_action(self.options.prediction_environment_id)
        except DRNotFoundException as e:
            self._log_error_and_exit(e, ExitCode.DR_NOT_FOUND.value)
        except DRMLOpsConnectedException as e:
            self._log_error_and_exit(e, ExitCode.DR_CONNECTED.value)
        except Exception as e:
            self._log_error_and_exit(e, ExitCode.UNSPECIFIED.value)
        finally:
            self.delete_mclient()

    @staticmethod
    def _print_supported_actions(subject):
        actions = SUPPORTED_ACTIONS[subject]
        if len(actions) == 1:
            print("Supported {} action is: {}".format(subject, actions[0]))
        else:
            print("Supported {} actions are: {}".format(subject, ", ".join(actions)))
        raise SystemExit(ExitCode.INVALID_CLI_INPUT.value)

    def handle_predictions(self):
        if self.options.action == Actions.GET:
            self.get_prediction_stats()
        elif self.options.action == Actions.UPLOAD:
            self.upload_scoring_dataset()
        elif self.options.action == Actions.REPORT:
            if self.options.from_spool:
                self.report_predictions_from_spool()
            else:
                self.report_predictions()
        else:
            self._print_supported_actions(Subjects.PREDICTIONS)

    def handle_model(self):
        if self.options.action == Actions.CREATE:
            self.create_model_package()
        elif self.options.action == Actions.DEPLOY:
            self.deploy_model_package()
        elif self.options.action == Actions.REPLACE:
            self.replace_model_package()
        elif self.options.action == Actions.GET:
            self.get_model_package()
        elif self.options.action == Actions.LIST:
            self.list_model_packages()
        elif self.options.action == Actions.DOWNLOAD:
            self.download_model_package()
        elif self.options.action == Actions.DELETE:
            self.delete_model_package()
        else:
            self._print_supported_actions(Subjects.MODEL)

    def handle_deployment(self):
        if self.options.action == Actions.DELETE:
            self.delete_deployment()
        elif self.options.action == Actions.GET or self.options.action == Actions.GET_MODEL:
            self.get_deployment()
        elif self.options.action == Actions.LIST:
            self.list_deployments()
        else:
            self._print_supported_actions(Subjects.DEPLOYMENT)

    def handle_perf(self):
        if self.options.action == Actions.RUN:
            self.perf_run()
        else:
            self._print_supported_actions(Subjects.PERF_TEST)

    def handle_datasets(self):
        if self.options.action == Actions.UPLOAD:
            self.upload_dataset()
        elif self.options.action == Actions.DELETE:
            self.delete_dataset()
        elif self.options.action == Actions.GET:
            self.get_dataset()
        elif self.options.action == Actions.LIST:
            self.list_datasets()
        else:
            self._print_supported_actions(Subjects.DATASET)

    def handle_actuals(self):
        if self.options.action == Actions.REPORT:
            self.report_actuals()
        else:
            self._print_supported_actions(Subjects.ACTUALS)

    def handle_prediction_environment(self):
        if self.options.action == Actions.DELETE:
            self.delete_prediction_environment()
        elif self.options.action == Actions.GET:
            self.get_prediction_environment()
        elif self.options.action == Actions.LIST:
            self.list_prediction_environments()
        elif self.options.action == Actions.CREATE:
            self.create_prediction_environment()
        else:
            self._print_supported_actions(Subjects.PREDICTION_ENVIRONMENT)

    def handle_service_stats(self):
        if self.options.action == Actions.GET:
            self.get_service_stats()
        else:
            self._print_supported_actions(Subjects.SERVICE_STATS)

    def get_list_params(self):
        params = None
        if self.options.search or self.options.limit:
            params = {}
            if self.options.search:
                params["search"] = self.options.search
            if self.options.limit:
                params["limit"] = self.options.limit
        return params

    def _log_list_action(self, resource):
        logger.debug("Listing {} metadata...".format(resource))
        logger.debug("MLOps service:         {}".format(self.options.mlops_service_url))

    def _print_resources_listed(self, info, key="id"):
        """Print information for resources listed, according to output format."""
        if self.options.terse:
            for id in [result.get(key) for result in info]:
                print(id)
        elif self.options.json:
            print(json.dumps(info, indent=1))
        else:
            raise ValueError("Something went wrong. Output format not recognized.")

    def _log_get_action(self, resource, id, retrieved="metadata"):
        logger.debug("Retrieving {} for {} ID {}".format(retrieved, resource, id))
        logger.debug("MLOps service:          {}".format(self.options.mlops_service_url))

    def _print_resource_received(self, id, info):
        # TODO: this could technically be the same method as _print_list_resources;
        #       maybe just get 'id' from info object, instead of passing 'id' separately
        if self.options.terse:
            print(id)
        elif self.options.json:
            print(json.dumps(info, indent=1))
        else:
            raise ValueError("Something went wrong. Output format not recognized.")

    def _log_delete_action(self, resource, id):
        logger.info("Deleting {} ID {}...".format(resource, id))
        logger.debug("MLOps service:         {}".format(self.options.mlops_service_url))

    def _print_resource_generic_action(self, id):
        """Print information for a single resource, according to output format."""
        if self.options.terse:
            print(id)
        elif self.options.json:
            print(json.dumps({"id": id}, indent=1))
        else:
            raise ValueError("Something went wrong. Output format not recognized.")

    def _log_error_and_exit(self, error, exit_code):
        show_stack_trace = logger.isEnabledFor(logging.DEBUG)
        logger.critical("%s: %s", error.__class__.__name__, error, exc_info=show_stack_trace)
        raise SystemExit(exit_code) from None

    def run(self):
        self.event_loop = asyncio.get_event_loop()
        if self.run_mode == RunMode.PERF_TEST:
            self.handle_perf()
        elif self.run_mode == RunMode.PREDICTIONS:
            self.handle_predictions()
        elif self.run_mode == RunMode.ACTUALS:
            self.handle_actuals()
        elif self.run_mode == RunMode.DATASET:
            self.handle_datasets()
        elif self.run_mode == RunMode.MODEL:
            self.handle_model()
        elif self.run_mode == RunMode.DEPLOYMENT:
            self.handle_deployment()
        elif self.run_mode == RunMode.PREDICTION_ENVIRONMENT:
            self.handle_prediction_environment()
        elif self.run_mode == RunMode.SERVICE_STATS:
            self.handle_service_stats()
        else:
            print("No valid subject provided")
            raise SystemExit(ExitCode.INVALID_CLI_INPUT.value)


def check_required_parameter(option, env_name, parameter_name):
    if option is None:
        if env_name is None:
            print("Missing required parameter {}.".format(parameter_name))
        else:
            print("{} must be set via environment variable or via {} parameter.".format(
                env_name, parameter_name))
        raise SystemExit(ExitCode.INVALID_CLI_INPUT.value)


def determine_logging_level(options):
    if options.verbose and options.quiet:
        print("Please specify only one logging level from: {} | {}".format(
            ArgumentsOptions.VERBOSE, ArgumentsOptions.QUIET))
        raise SystemExit(ExitCode.INVALID_CLI_INPUT.value)
    if options.verbose:
        return logging.DEBUG
    if options.quiet:
        return logging.ERROR
    # By default, set logging level to INFO if no level specified
    return logging.INFO


def determine_output_format(options):
    if options.json and options.terse:
        print("Please specify only one output type from: {} (default) | {}".format(
            ArgumentsOptions.JSON, ArgumentsOptions.TERSE))
        raise SystemExit(ExitCode.INVALID_CLI_INPUT.value)
    # No changes needed if one or the other specified
    if options.json or options.terse:
        return
    # By default, set output format to JSON if no format specified
    options.json = True


def main():
    arg_parser = MLOpsCliArgParser.get_arg_parser()
    options = arg_parser.parse_args()

    check_required_parameter(options.mlops_service_url, EV.MLOPS_SERVICE_URL,
                             ArgumentsOptions.MLOPS_SERVICE)
    check_required_parameter(options.mlops_api_token, EV.MLOPS_API_TOKEN,
                             ArgumentsOptions.MLOPS_API_TOKEN)
    determine_output_format(options)
    logging_level = determine_logging_level(options)

    console_handler = logging.StreamHandler()
    simple_formatter = logging.Formatter("%(levelname)-8s  %(message)s")
    debug_formatter = logging.Formatter(
        "%(asctime)s,%(lineno)4d %(levelname)-8s %(name)s    %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    if logging_level == logging.DEBUG:
        console_handler.setFormatter(debug_formatter)
    else:
        console_handler.setFormatter(simple_formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging_level)

    # Setup signal handler so we can exit cleanly (i.e. delete lock files)
    def handle_term(*args):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, handle_term)

    mlops_cli = MLOpsCli(options)
    mlops_cli.run()
    exit(ExitCode.OK.value)


if __name__ == "__main__":
    main()
