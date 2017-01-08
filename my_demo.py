#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from sr_factory.sr_image_factory import SRImageFactory

__autor__ = 'Kyosuke Yamamoto (kyon)'
__date__ = '08 Jan 2017'

if __name__ == '__main__':
    image = Image.open(sys.argv[1])
    sr_image = SRImageFactory.create_sr_image(image)
    reconstructed_sr_image = sr_image.reconstruct(2, 'iccv09')
    reconstructed_sr_image.save('/tmp/sisr.png', 'png')
    print 'saved as /tmp/sisr.png'
