#!/usr/bin/env python

import sys
from setuptools import setup,find_packages
import versioneer
from _datalad_buildsupport.setup import (
    BuildManPage,
)

cmdclass = versioneer.get_cmdclass()
cmdclass.update(build_manpage=BuildManPage)

if __name__ == '__main__':
    setup(name='datalad-lgpdextension',
        packages = (find_packages()),
        version='0.4.0',
        description = 'Datalad extension to apply lgpd patterns',
        author = 'Messias Silva',
        author_email = 'messias.oliveira2011@hotmail.com',
        url = 'https://github.com/messiasoliveira/lgpdextension-datalad.git',
        download_url = 'https://github.com/messiasoliveira/lgpdextension-datalad/archive/refs/tags/version.tar.gz',
        keywords = ['lgpd', 'datalad', 'extension'],
        classifiers = [],
    )