# -*- coding: utf-8 -*-
# @author: Wenting Tu
# @email: wtugmail@163.com
# @date: 2022/06
"""
==========
datasets: Datasets in pytima
==========
"""

class TimaDataset(object):

    def __init__(self):
        """Common Datasets in pytima"""
        '''
        series_data: pandas.DataFrame, columns为[FcstUnit_{dim1}, FcstUnit_{dimM}, ... , Time, TimeBucket, FcstTarget]
        horizen_data: pandas.DataFrame, columns为[FcstUnit_{dim1}, FcstUnit_{dimM}, ... , Time, TimeBucket]
        {dim}_data: columns为[FcstUnit_{dim}, {attribute1}, ...] }
        '''
        self.series_data = None
        self.horizen_data = None
        pass
