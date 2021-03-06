__author__ = 'Sherwin'

import math
import sys
import sr_util.profiler
from sr_dataset import SRDataSet
from sr_util import sr_image_util

DEFAULT_RECONSTRUCT_LEVEL = 6
ALPHA = 2 ** (1.0/5)

class ICCV09(object):

    def __init__(self):
        self._method_type = "iccv09"
        self._kernel = sr_image_util.create_gaussian_kernel()

    def get_method_type(self):
        return self._method_type

    @sr_util.profiler.profiler
    def reconstruct(self, ratio, sr_image):
        """Reconstruct the SR image by the given ratio.

        @param ratio: reconstruct ratio
        @type ratio: float
        @param sr_image: original SR image
        @type sr_image: L{sr_image.SRImage}
        @return: reconstructed SR image
        @rtype: L{sr_image.SRImage}
        """
        sr_dataset = SRDataSet.from_sr_image(sr_image)
        reconstructed_sr_image = sr_image
        construct_level = int(math.log(ratio, ALPHA) + 0.5)
        print 'construct_level:', construct_level
        r = ALPHA
        for level in range(construct_level):
            reconstructed_sr_image = self._reconstruct(r, reconstructed_sr_image, sr_dataset)
            print 'size:', reconstructed_sr_image.size,
            reconstructed_sr_image = sr_image_util.back_project(reconstructed_sr_image, sr_image,
                                                                3, level+1)
            new_sr_dataset = SRDataSet.from_sr_image(reconstructed_sr_image)
            sr_dataset.merge(new_sr_dataset)
            print "Reconstructing %.2f%%" % (float(level+1) / construct_level * 100)
        return reconstructed_sr_image

    def _reconstruct(self, ratio, sr_image, sr_dataset):
        """Reconstruct a SRImage using the given SRDataset by the given ratio.

        @param ratio: reconstruct ratio
        @type ratio: float
        @param sr_image: original SRImage
        @type sr_image: L{sr_image.SRImage}
        @param sr_dataset:
        @type sr_dataset: L{sr_dataset.SRDataset}
        @return: reconstructed SRImage
        @rtype: L{sr_image.SRImage}
        """
        resized_sr_image = sr_image.resize(ratio)
        patches_without_dc, patches_dc = sr_image_util.get_patches_from(resized_sr_image, interval=4)
        high_res_patches_without_dc = sr_dataset.parallel_query(patches_without_dc)
        high_res_patches = high_res_patches_without_dc + patches_dc
        high_res_data = sr_image_util.unpatchify(high_res_patches, resized_sr_image.size, self._kernel)
        resized_sr_image.putdata(high_res_data)
        return resized_sr_image

