"""
    by Carsten Richter

    These classes define measurement geometries.
    Based on the EmptyGeometry it should be easy to define new geometries,

    contains all movements of the Huber diffractometer
    (vertical and horizontal)
"""
import collections
import xrayutilities as xu
from numpy import isscalar

class EmptyGeometry(object):
    """
        Abstract container for diffractometer angles
    """
    sample_rot = collections.OrderedDict()
    detector_rot = collections.OrderedDict()
    offsets = collections.defaultdict(float)

    # defines whether these motors are used. otherwise set to zero.
    usemotors = set()

    inc_beam = [1,0,0]

    def __init__(self, **kwargs):
        """
            Initialize diffractometer geomtry.

            Inputs: all motor names from self.sample_rot and self.detector_rot
                True  -- use motor
                False -- discard
        """
        usemotors = self.usemotors
        for motor in kwargs:
            usemotors.add(motor) if kwargs[motor] else usemotors.discard(motor)

    def getQconversion(self, inc_beam = None):
        if inc_beam is None:
            inc_beam = self.inc_beam
        sample_rot = [v for (k,v) in self.sample_rot.items() if k in self.usemotors]
        detector_rot = [v for (k,v) in self.detector_rot.items() if k in self.usemotors]
        qc = xu.experiment.QConversion(sample_rot, detector_rot, inc_beam)
        return qc

    def set_offsets(self, **kwargs):
        """
            Set offset for each motor to be subtracted from its position.
            Motors identified by keyword arguments.
        """
        for kw in kwargs:
            if kw in self.sample_rot or kw in self.detector_rot:
                self.offsets[kw] = float(kwargs[kw])


class AreaDetector(object):
    """
        The Base class.
        This is temporary until proper nexus classes are implemented
    """
    def __init__(self, directions, pixsize, pixnum, mask=None, chunks=None):
        if isscalar(pixsize):
            pixsize = (pixsize, pixsize)
        if isscalar(pixnum):
            pixnum = (pixnum, pixnum)
        self.directions = directions
        self.pixsize = pixsize
        self.pixnum  = pixnum
        self.mask = mask
        self.chunks = pixnum if chunks is None else chunks # for h5py

    @staticmethod
    def correct_image(image):
        pass # to be implemented for each detector


class P23SixC(EmptyGeometry):
    def __init__(self, **kwargs):
        ### geometry of diffractometer
        ### x downstream; z upwards; y to the "outside" (righthanded)
        ### maintain the correct order: outer to inner rotation!
        self.sample_rot['omega_t'] = 'y-' # check mu is not 0
        self.sample_rot['mu'] = 'z-' # check mu is not 0
        self.sample_rot['omega'] = 'y-'
        self.sample_rot['chi'] = 'x-'
        self.sample_rot['phi'] = 'y+'

        self.detector_rot['gamma'] = 'z-'
        self.detector_rot['delta'] = 'y-'

        self.inc_beam = [1,0,0]

        # defines whether these motors are used. otherwise set to zero
        #   typical defaults, can be overridden during __init__:
        self.usemotors = set(('omega', 'chi', 'phi', 'gamma', 'delta'))
        super(P23SixC, self).__init__(**kwargs)


class Lambda(AreaDetector):
    alias = shortalias = "lmbd"
    def __init__(self, mask=None):
        super(Lambda, self).__init__(directions=("y+", "z-"),
                                      pixsize=55e-6,
                                      pixnum=(516,1556),
                                      mask=mask,
                                      chunks=(258, 389) # e.g. for hdf5 writing
                                     )
    @staticmethod
    def correct_image(image):
        pass


