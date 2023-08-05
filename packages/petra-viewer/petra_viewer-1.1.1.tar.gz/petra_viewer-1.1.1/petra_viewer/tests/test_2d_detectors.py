import numpy as np

from petra_viewer.tests.test_sardana import _load_file, z_dim, y_dim, x_dim, generate_fake_data, viewer, change_test_dir


def test_2d_functionality(change_test_dir, viewer):

    _load_file(viewer)

    section = viewer.data_pool.get_section('test007')
    for axis, axis_lim in enumerate([z_dim, y_dim, x_dim]):
        assert section[axis]['max'] == axis_lim - 1
        assert section[axis]['range_limit'] == axis_lim

    for axis, axis_lim in enumerate([z_dim, y_dim, x_dim]):
        assert viewer.data_pool.get_max_frame_along_axis('test007', axis) == axis_lim - 1

    viewer.data_pool.set_axis_units('test007', 0, 'omega')
    omega = np.linspace(1, 2, 11)
    assert viewer.data_pool.get_frame_for_value('test007', 0, omega[2]) == 2
    assert viewer.data_pool.get_value_for_frame('test007', 0, 2) == omega[2]
    viewer.data_pool.set_axis_units('test007', 0, 'point_nb')

    fake_data_cube = generate_fake_data()
    old_max = [section[axis]['max'] for axis in range(3)]

    for section_axis, do_rotate, axes_set in zip([0, 0, 1, 2],
                                                 [True, False, False, True],
                                                 [['Z', 'Y', 'X'], ['Z', 'X', 'Y'], ['X', 'Z', 'Y'], ['Y', 'X', 'Z']]):
        for ind, axis in enumerate(axes_set):
            section[ind]['axis'] = axis

        viewer.data_pool.save_section('test007', section)
        cut_data = np.sum(fake_data_cube.take(indices=[0], axis=section_axis), axis=section_axis)
        if do_rotate:
            cut_data = np.transpose(cut_data)
        data, q_rect = viewer.data_pool.get_2d_picture('test007')
        assert np.all(np.isclose(data, cut_data))
        assert int(q_rect.width()) == cut_data.shape[0] - 1
        assert int(q_rect.height()) == cut_data.shape[1] - 1
        assert int(q_rect.x()) == 0
        assert int(q_rect.y()) == 0

        section[section_axis]['integration'] = True
        section[section_axis]['max'] = 4
        viewer.data_pool.save_section('test007', section)

        cut_data = np.sum(fake_data_cube.take(indices=range(0, 5), axis=section_axis), axis=section_axis)
        if do_rotate:
            cut_data = np.transpose(cut_data)
        data, q_rect = viewer.data_pool.get_2d_picture('test007')
        assert np.all(np.isclose(data, cut_data))

        for axis in range(3):
            section[axis]['max'] = 4
        viewer.data_pool.save_section('test007', section)

        cut_data = np.sum(fake_data_cube[:5, :5, :5], axis=section_axis)
        if do_rotate:
            cut_data = np.transpose(cut_data)

        data, q_rect = viewer.data_pool.get_2d_picture('test007')
        assert np.all(np.isclose(data, cut_data))

        for ind, lim in enumerate(old_max):
            section[ind]['max'] = lim
        section[section_axis]['integration'] = False

        viewer.data_pool.save_section('test007', section)


def test_roi_functionality(change_test_dir, viewer):

    _load_file(viewer)

    viewer.frame_view.add_file("test007", "second")

    ind, roi_key, dims = viewer.data_pool.add_new_roi()

    assert viewer.data_pool.get_roi_key(ind) == roi_key
    assert viewer.data_pool.get_roi_index(roi_key) == ind

    assert viewer.data_pool.roi_parameter_changed(roi_key, 1, 'pos', y_dim*3) == y_dim - 2
    assert viewer.data_pool.roi_parameter_changed(roi_key, 1, 'pos', -10) == 0
    assert viewer.data_pool.roi_parameter_changed(roi_key, 1, 'width', y_dim * 3) == y_dim - 1

    assert viewer.data_pool.roi_parameter_changed(roi_key, 1, 'width', 25) == 25
    assert viewer.data_pool.roi_parameter_changed(roi_key, 1, 'pos', 15) == 15
    assert viewer.data_pool.roi_parameter_changed(roi_key, 2, 'pos', 15) == 15
    assert viewer.data_pool.roi_parameter_changed(roi_key, 2, 'width', 25) == 25

    fake_data_cube = generate_fake_data()
    assert np.all(np.isclose(fake_data_cube[:, 15:40, 15:40], viewer.data_pool.get_roi_cut('test007', roi_key)))

    axis, plot = viewer.data_pool.get_roi_plot('test007', roi_key)
    assert np.all(np.isclose(np.sum(np.sum(fake_data_cube[:, 15:40, 15:40], axis=2), axis=1), plot))

