# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Libe57(CMakePackage):
    """Software Tools for Managing E57 Point Cloud Files"""

    homepage = 'http://libe57.org'
    url = "https://github.com/hlrs-vis/libe57/archive/refs/tags/v1.1.334.tar.gz"
    git = "https://github.com/hlrs-vis/libe57.git"

    maintainers = ['aumuell']

    version('master', preferred=False, branch='master')
    version("1.1.337", sha256="093bf48e8be73af95778d1f587da0d10c6fa6c013d54431750400cb565f44f83")
    version("1.1.336", sha256="a61d28adb2943aab61348c114bfb8a6f565386f9bca2695864ab53d33874e1f4")
    version("1.1.335", sha256="2e612aa0bb1c8f4659ca6dbcc8f918344e90cfa0334e16532016cfb24566f545")
    version("1.1.334", sha256="ff15ce1d2d9572daedbe990755800ea5fb0ef5dfbd8b9db9d679e73c43996bc4")
    version("1.1.333", sha256="f8fe8e329fb75c48bea5e45cad46cb011a62f3005cb1551cdc183e98253cfd44")

    depends_on('cmake@3.3:', type='build')
    depends_on('boost+multithreaded')
    depends_on('xerces-c')

    def test(self):
        """Perform smoke tests on the installed package."""
        self.run_test('e57validate', [], [], installed=True,
                      purpose=reason, skip_missing=True, work_dir='.')
