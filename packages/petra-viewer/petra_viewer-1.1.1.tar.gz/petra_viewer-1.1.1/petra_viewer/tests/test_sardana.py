import os

import h5py
import pytest

from time import sleep, time
import numpy as np
from PyQt5 import QtWidgets

from mock import MagicMock

from petra_viewer.main_window import PETRAViewer
from petra_viewer.utils.option_parser import get_options

TIMEOUT_FOR_FILE_OPEN = 500000

x_dim = 100
y_dim = 200
z_dim = 11


# ----------------------------------------------------------------------
def generate_fake_data():

    frame = np.zeros((y_dim, x_dim))
    for ind in range(y_dim):
        frame[ind] = np.cos(np.linspace(0, 2*np.pi, x_dim))
    for ind in range(x_dim):
        frame[:, ind] *= np.cos(np.linspace(0, 2*np.pi, y_dim))

    data_cube = np.zeros((z_dim, y_dim, x_dim))
    for ind, scale in enumerate(np.cos(np.linspace(0, 2*np.pi, z_dim))):
        data_cube[ind] = frame*scale

    return data_cube


# ----------------------------------------------------------------------
def generate_fake_file():

    data = {'scan': {'data': {'lmbd' : None,
                             'point_nb': np.arange(11),
                             'omega': np.linspace(1, 2, 11)}
                    },
            'entry': {'instrument':{'detector': {'data': generate_fake_data()}}}
            }

    data_set = MagicMock()
    data_set.filename = 'test'
    data_set.__getitem__.side_effect = data.__getitem__
    data_set.__iter__.side_effect = data.__iter__

    return data_set


# ----------------------------------------------------------------------
@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(os.path.dirname(os.path.dirname(request.fspath.dirname)))
    yield
    os.chdir(request.config.invocation_dir)


# ----------------------------------------------------------------------
@pytest.fixture
def viewer():

    h5py.File = MagicMock(return_value=generate_fake_file())
    os.listdir = MagicMock(return_value=['test.nxs'])

    app = QtWidgets.QApplication([os.getcwd() + 'data_viewer.py', '--tests'])
    if app is None:
        app = QtWidgets.QApplication([os.getcwd() + 'data_viewer.py', '--test'])

    main = PETRAViewer(get_options(['--tests']))

    yield main


# ----------------------------------------------------------------------
def _load_file(viewer, file_name="test007.nxs"):

    viewer.data_pool.open_file(file_name, 'sardana')
    start_time = time()
    while viewer.data_pool.open_file_in_progress and time() - start_time < TIMEOUT_FOR_FILE_OPEN:
        sleep(0.1)  # sleep for sometime to open stream

    assert not viewer.data_pool.open_file_in_progress


# ----------------------------------------------------------------------
def test_load_file(change_test_dir, viewer):

    _load_file(viewer)

    assert len(viewer.data_pool._files_data) == 1
    assert 'test007' in viewer.data_pool._files_data
    assert viewer.data_pool._files_data['test007']._data_shape == (z_dim, y_dim, x_dim)
    assert viewer.data_pool._files_data['test007']._scan_length == z_dim
    possible_axes = viewer.data_pool._files_data['test007'].get_possible_axis_units(0)
    assert 'point_nb' in possible_axes and 'omega' in possible_axes
    assert np.all(viewer.data_pool._files_data['test007']._get_axis(0) == np.arange(11))
    viewer.data_pool._files_data['test007'].set_axis_units(0, 'omega')
    assert np.all(viewer.data_pool._files_data['test007']._get_axis(0) == np.linspace(1, 2, 11))
    assert viewer.data_pool._files_data['test007']._detector_folder == 'test/lmbd'
    assert viewer.data_pool._files_data['test007']._detector == 'lmbd'


