import os

import pytest
from time import sleep, time
import numpy as np
from PyQt5 import QtWidgets
from mock import MagicMock

import AsapoWorker
from AsapoWorker.data_handler import serialize_ndarray
from unittest.mock import create_autospec

from petra_viewer.main_window import PETRAViewer
from petra_viewer.data_sources.asapo.asapo_data_set import ASAPODataSet
from petra_viewer.utils.option_parser import get_options

TIMEOUT_FOR_FILE_OPEN = 5


# ----------------------------------------------------------------------
@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(os.path.dirname(os.path.dirname(request.fspath.dirname)))
    yield
    os.chdir(request.config.invocation_dir)


# ----------------------------------------------------------------------
@pytest.fixture
def message_data():
    return create_message_data((10, 5))


# ----------------------------------------------------------------------
@pytest.fixture
def viewer(message_data):

    app = QtWidgets.QApplication([os.getcwd() + 'data_viewer.py', '--tests'])
    if app is None:
        app = QtWidgets.QApplication([os.getcwd() + 'data_viewer.py', '--tests'])

    main = PETRAViewer(get_options(['--tests']))

    ASAPODataSet._setup_receiver = MagicMock(return_value=True)
    ASAPODataSet.receiver = create_autospec(AsapoWorker.asapo_receiver.SerialAsapoReceiver)
    ASAPODataSet.receiver.set_start_id = MagicMock(return_value=True)
    ASAPODataSet.meta_only = False
    ASAPODataSet._mode = 'file'
    ASAPODataSet.receiver.get_next = MagicMock(return_value=message_data)
    ASAPODataSet.receiver.get_current_size = MagicMock(return_value=10)

    yield main


# ----------------------------------------------------------------------
def create_message_data(shape):
    data = serialize_ndarray(np.ones(shape)).getvalue()
    mdata = {'_id': 1,
             'size': 5392,
             'name': 'processed/tmp/20211015T_111706/mod_0_msg_0.h5',
             'timestamp': 1634289427969925572,
             'source': '192.168.1.27:20493',
             'buf_id': 0, 'dataset_substream': 0,
             'meta': {},
             'stream': '29',
             'data_source': 'test011_5_100_50'}
    return data, mdata


# ----------------------------------------------------------------------
def _load_stream(viewer):

    viewer.data_pool.open_stream("test007", "1", {})
    start_time = time()
    while viewer.data_pool.open_file_in_progress and time() - start_time < TIMEOUT_FOR_FILE_OPEN:
        sleep(0.1)  # sleep for sometime to open stream

    assert not viewer.data_pool.open_file_in_progress


# ----------------------------------------------------------------------
def test_load_stream(change_test_dir, viewer, message_data):

    _load_stream(viewer)

    assert len(viewer.data_pool._files_data) == 1
    assert 'test007/1' in viewer.data_pool._files_data
    assert viewer.data_pool._files_data['test007/1']._data_shape == [10, 10, 5]
    assert len(viewer.data_pool._files_data['test007/1']._additional_data['metadata']) == 1
    assert viewer.data_pool._files_data['test007/1']._additional_data['metadata'][0] == message_data[1]

    selection = viewer.data_pool.get_section("test007/1")
    assert len(selection) == 3
    assert selection[0]['range_limit'] == 3
    assert selection[1]['range_limit'] == 0


# ----------------------------------------------------------------------
def test_add_file(change_test_dir, viewer, message_data):

    _load_stream(viewer)

    viewer.frame_view.add_file("test007/1", "second")
    assert viewer.frame_view.current_file() == "test007/1"
    assert viewer.data_pool.get_all_axes_limits() == [[0, 9], [0, 9], [0, 4]]

