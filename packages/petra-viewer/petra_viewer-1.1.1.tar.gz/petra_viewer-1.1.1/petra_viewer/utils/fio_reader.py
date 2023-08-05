# Taken from HasyUtils

import numpy as np

class fioColumn:
    '''
    the class represents a column of a FIO file. The first column is the
    x-axis which is used by all columns, name_in, e.g. test_00001_C1
    '''

    def __init__(self, name_in):
        self.name = name_in
        lst = self.name.split('_')
        if len(lst) > 1:
            self.deviceName = lst[-1]
            if self.deviceName.find("0") == 0:
                self.deviceName = "ScanName"
        else:
            self.deviceName = "n.n."
        self.x = []
        self.y = []
        return


class fioReader:
    '''
    represents an entire file with several columns
    input:   name of the .fio file (or .dat or .iint)
             flagMCA: if True, the x-axis are channel numbers
    returns: object containing:
        self.comments
        self.user_comments
        self.parameters
        self.columns
        self.fileName

    The string 'None' appearing in a column is interpreted as '0.'
    '''

    def __init__(self, fileName, flagMCA=False):
        '''
        flagMCA: don't be too smart and try to guess it.
        '''
        self.comments = []
        self.user_comments = []
        self.parameters = {}
        self.columns = []
        self.fileName = fileName
        self.flagMCA = flagMCA
        self.isImage = None
        #
        # /home/p12user/dirName/gen_00001.fio -> gen_00001
        #
        self.scanName = self.fileName.split("/")[-1].split(".")[0]
        if fileName.endswith('.fio'):
            self._readFio()
        else:
            raise ValueError("fioReader: format not identified, %s" % fileName)

        return

    def _readFio(self):
        '''
        !
        ! user comments
        !
        %c
        comments
        %p
        parameterName = parameterValue
        %d
        Col 1 AU_ALO_14_0001  FLOAT
        Col 2 AU_ALO_14_0001  FLOAT
        Col 3 AU_ALO_14_0001_RING  FLOAT
        data data data etc.
        '''
        try:
            inp = open(self.fileName, 'r')
        except IOError as e:
            raise ValueError("fioReader.fioReader._readFio: failed to open %s" % self.fileName)
            return False
        lines = inp.readlines()
        inp.close()
        flagComment = 0
        flagParameter = 0
        flagData = 0
        lineCount = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.find("!") == 0:
                self.user_comments.append(line)
                flagComment, flagParameter, flagData = False, False, False
            elif line.find("%c") == 0:
                flagComment, flagParameter, flagData = True, False, False
                continue
            elif line.find("%p") == 0:
                flagComment, flagParameter, flagData = False, True, False
                continue
            elif line.find("%d") == 0:
                flagComment, flagParameter, flagData = False, False, True
                continue
            #
            if flagComment:
                self.comments.append(line)
            #
            # parName = parValue
            #
            if flagParameter:
                lst = line.split("=")
                self.parameters[lst[0].strip()] = lst[1].strip()
            if not flagData:
                continue
            #
            # height and width indicate that we are reading an image
            #
            if self.isImage is None:
                if 'width' in self.parameters and 'height' in self.parameters:
                    self.isImage = True
                else:
                    self.isImage = False
            lst = line.split()
            if lst[0] == "Col":
                #
                # the 'Col 1 ...' description does not create a
                # new FIO_dataset because it contains the x-axis for all
                #
                if not self.flagMCA and not self.isImage:
                    #
                    # the first column contains the independent variable (motor position)
                    #
                    if lst[1] == "1":
                        self.motorName = lst[2]
                    else:
                        self.columns.append(fioColumn(lst[2]))
                #
                # MCA and image files have one colum only
                #
                else:
                    if self.isImage:
                        self.motorName = lst[2]
                    if self.flagMCA:
                        self.motorName = "Channels"
                    self.columns.append(fioColumn(lst[2]))
            else:
                if not self.flagMCA and not self.isImage:
                    for i in range(1, len(self.columns) + 1):
                        self.columns[i - 1].x.append(float(lst[0]))
                        #
                        # some column may be 'None' - try to continue anyway
                        #
                        if lst[i].lower() == 'none':
                            self.columns[i - 1].y.append(float(0.))
                        else:
                            self.columns[i - 1].y.append(float(lst[i]))
                elif self.flagMCA:
                    for i in range(0, len(self.columns)):
                        self.columns[i].x.append(float(lineCount))
                        #
                        # some column may be 'None' - try to continue anyway
                        #
                        if lst[i].lower() == 'none':
                            self.columns[i].y.append(float(0.))
                        else:
                            self.columns[i].y.append(float(lst[i]))
                #
                # image, one column only
                #
                elif self.isImage:
                    self.columns[0].x.append(float(lst[0]))

            lineCount += 1
        if self.isImage:
            if len(self.columns) != 1:
                raise ValueError(" fioReader.reasdFio: isImage and len( self.columns) != 1")
            if len(self.columns[0].y) is not 0:
                raise ValueError(" fioReader.readFio: isImage and len( self.columns[0].y) is not 0")
            if int(self.parameters['width']) * int(self.parameters['height']) != len(self.columns[0].x):
                raise ValueError(" fioReader.reasdFio: isImage and width*height != len(x)")
            xlocal = np.asarray(self.columns[0].x, dtype=np.float64)
            self.columns[0].x = xlocal[:]

        return True
