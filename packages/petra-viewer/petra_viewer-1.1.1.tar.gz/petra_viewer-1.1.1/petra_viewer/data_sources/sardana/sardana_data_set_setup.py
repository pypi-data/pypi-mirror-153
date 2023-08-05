# Created by matveyev at 13.08.2021
from petra_viewer.data_sources.sardana.sardana_data_set import SETTINGS
from petra_viewer.data_sources.base_classes.base_2d_detector_setup import Base2DDetectorSetup
from petra_viewer.gui.datasource_setup_sardana_ui import Ui_SardanaSetup
from petra_viewer.utils.utils import refresh_combo_box

WIDGET_NAME = 'SardanaScanSetup'


class SardanaScanSetup(Base2DDetectorSetup):
    """
    SETTINGS = {'enable_mask': False,
                'loaded_mask': None,
                'loaded_mask_info': {'file': ''},
                'enable_ff': False,
                'loaded_ff': None,
                'loaded_ff_info': {'file': ''},
                'enable_fill': False,
                'fill_radius': 7,
                'atten_correction': 'on',
                'atten_param': 'atten',
                'inten_correction': 'on',
                'inten_param': 'eh_c01',
                }
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        """
        """
        super(SardanaScanSetup, self).__init__(main_window)

        self._ui.le_door_address.setText(SETTINGS['door_address'])

        self._ui.cmb_attenuator.addItems(SETTINGS['all_params'])
        self._ui.cmb_attenuator.setEnabled(SETTINGS['atten_correction'])
        if SETTINGS['atten_param'] not in SETTINGS['all_params']:
            self._ui.cmb_attenuator.addItem(SETTINGS['atten_param'])
        refresh_combo_box(self._ui.cmb_attenuator, SETTINGS['atten_param'])
        self._ui.rb_atten_on.setChecked(SETTINGS['atten_correction'])
        self._ui.rb_atten_off.setChecked(not SETTINGS['atten_correction'])

        self._ui.cmb_intensity.addItems(SETTINGS['all_params'])
        self._ui.cmb_intensity.setEnabled(SETTINGS['inten_correction'])
        if SETTINGS['inten_param'] not in SETTINGS['all_params']:
            self._ui.cmb_intensity.addItem(SETTINGS['inten_param'])
        refresh_combo_box(self._ui.cmb_intensity, SETTINGS['inten_param'])
        self._ui.rb_inten_on.setChecked(SETTINGS['inten_correction'])
        self._ui.rb_inten_off.setChecked(not SETTINGS['inten_correction'])

        self._ui.bg_intensity.buttonClicked.connect(
            lambda button: self._ui.cmb_intensity.setEnabled(button == self._ui.rb_inten_on))
        self._ui.bg_attenuator.buttonClicked.connect(
            lambda button: self._ui.cmb_attenuator.setEnabled(button == self._ui.rb_atten_on))

    # ----------------------------------------------------------------------
    def _my_ui(self):

        return Ui_SardanaSetup()

    # ----------------------------------------------------------------------
    def _my_settings(self):

        return SETTINGS

    # ----------------------------------------------------------------------
    def get_settings(self):

        settings = super(SardanaScanSetup, self).get_settings()

        if self._ui.le_door_address.text() != '':
            settings['door_address'] = str(self._ui.le_door_address.text())

        if self._ui.rb_atten_on.isChecked():
            settings['atten_param'] = str(self._ui.cmb_attenuator.currentText())

        if self._ui.rb_atten_on.isChecked():
            settings['inten_param'] = str(self._ui.cmb_intensity.currentText())

        return {'SARDANA': settings}

