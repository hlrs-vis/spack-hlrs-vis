# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Vistle(CMakePackage, ROCmPackage, CudaPackage):
    """Vistle is a tool for visualization of scientific data in VR.

    This package does not include the VR features.
    Notable features are distributed workflows and low-latency remote
    visualization."""

    homepage = 'https://www.vistle.io'
    url = "https://github.com/vistle/vistle/releases/download/v2023.9/vistle-v2023.9.tar.gz"
    git = "https://github.com/vistle/vistle.git"

    maintainers = ['aumuell']

    version('master', branch='master', submodules=True)
    version("2025.1", sha256="dff98a584006ad5096694d3b16d35f545a9393afd4d35a76edce72e7a87a2a9f")
    version("2024.2", sha256="1d2959ea56b6e8fcf617f9772f34801c66ce7b86e0d61dbe2813a1b6c7e16b18")
    version("2024.1.1", sha256="2bf644061d85dcc0e09b9af244da2795bcbb74e586ef35552f856d1ffbfbdc7f")
    version("2023.9", sha256="6ab328c3bb1ffb2763823792376be6b373eb5d81315771aa22746b489a0721b2")
    version('2021.10', tag='v2021.10', submodules=True)
    version('2020.9', tag='v2020.9', submodules=True)
    version('2020.8', commit='aaf99ff79145c10a6ba4754963266244b1481660', submodules=True)
    version('2020.2', commit='3efd1e7718d30718a6f7c0cddc3999928dc02a9d', submodules=True)
    version('2020.1', tag='v2020.1', submodules=True)
    version('2019.9', tag='v2019.9', submodules=True)

    variant('python', default=True, description='Enable Python support')
    variant('tui', default=True, description='Install interactive command line interface')
    variant('catalyst', default=False, description='Enable in-situ simulation interface')
    variant('qt', default=True, description='Build graphical workflow editor relying on Qt')
    variant('qt5', default=False, description='Build graphical workflow editor relying on Qt 5')
    variant('embree', default=True, description='Enable remote rendering')
    variant('vtk', default=True, description='Enable reading VTK data')
    variant('foam', default=True, description='Enable reading OpenFOAM data')
    variant('netcdf', default=True, description='Enable reading of WRF data')
    variant('pnetcdf', default=True, description='Enable reading of e.g. MPAS data')
    variant('hdf5', default=True, description='Enable reading of HDF5 based data formats')
    variant('xdmf', default=False, description='Enable reading of SeisSol data')
    variant('osg', default=True, description='Build renderer relying on OpenSceneGraph')
    variant('assimp', default=True, description='Enable reading of polygonal models (.obj, .stl, ...)')
    variant('proj', default=True, description='Enable MapDrape module for carthographic coordinate mappings')
    variant('gdal', default=True, description='Enable IsoHeightSurface module for carthographic coordinate mappings')
    variant('cgal', default=True, description='Enable DelaunayTriangulation module for triangulations of point clouds')

    variant('multi', default=True, description='Use a process per module')
    variant('double', default=False, description='Use double precision scalars')
    variant('large', default=False, description='Use 64-bit indices')

    variant('static', default=False, description='Do not build shared libraries')
    variant('dev', default=True, description='Install internal 3rd party dependencies for linking to Vistle')
    variant('boostmpi', default=False, description='Do not use internal copy of Boost.MPI')
    variant('cuda', default=False, description='Build with CUDA')
    variant('vtkm', default=True, description='Do not use internal copy of VTK-m')
    variant('kokkos', default=False, description='Use Kokkos backend for internal VTK-m', when='~vtkm')
    variant('rocm', default=False, description='Use rocm-enabled Kokkos backend for internal VTK-m', when='~vtkm')
    variant('openmp', default=True, description='Use OpenMP (including within Kokkos)')

    conflicts('%gcc@:4.99')
    depends_on('cmake@3.3:', type='build')
    depends_on('git', type='build')

    with when("+openmp"):
        depends_on('llvm-openmp', when='platform=darwin')
    depends_on('tbb', when="~openmp")

    extends('python', when='+python')

    depends_on('python@2.7:', when='+python', type=('build', 'link', 'run'))
    depends_on('py-installer', when='+python+xdmf', type=('build'))
    conflicts('+tui', '~python', msg='Python is required to interpret user input')
    depends_on('py-ipython', when='+tui', type=('run'))

    depends_on('mpi')
    depends_on('hwloc')
    depends_on('botan')
    depends_on('boost+atomic+thread+exception+log+locale+math+random+timer+filesystem+date_time+program_options+serialization+system+iostreams+chrono+regex@1.59:')
    depends_on('boost+pic', when='+static')
    depends_on('boost+mpi', when='+boostmpi')
    depends_on('fmt')

    depends_on("libcatalyst +conduit", when="+catalyst")

    with when("+vtkm"):
        depends_on('vtk-m@2 +fpic')
        depends_on("vtk-m +64bitids", when="+large")
        depends_on("vtk-m ~64bitids", when="~large")
        conflicts("+kokkos")

    depends_on("kokkos +rocm", when="+kokkos +rocm")
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
                "kokkos amdgpu_target=%s" % amdgpu_value,
                when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
                )

    depends_on("hip@3.7:", when="+rocm")
    # CUDA thrust is already include in the CUDA pkg
    depends_on("rocthrust", when="@2.1: +kokkos+rocm")

    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="~kokkos", msg="VTK-m does not support HIP without Kokkos")
    #conflicts("+rocm", when="+virtuals", msg="VTK-m does not support virtual functions with ROCm")

    with when("+rocm"):
        depends_on('kokkos +rocm')
        conflicts('+cuda')
    with when("+cuda"):
        depends_on('cuda')
        conflicts('+rocm')
        depends_on("kokkos +cuda", when="+kokkos")

    depends_on('netcdf-c +hdf4') # hdf4 for MPAS
    depends_on('netcdf-cxx4', when='+netcdf')
    depends_on('parallel-netcdf', when='+pnetcdf')
    depends_on('hdf5', when='+hdf5')
    depends_on('xdmf3', when='+xdmf')

    depends_on('zstd')
    depends_on('lz4')
    depends_on('snappy', when='@:2024')

    with when("+foam"):
        depends_on('zlib-api')
        depends_on('libzip')
        depends_on('libarchive')

    with when("+vtk"):
        depends_on('vtk')
        depends_on('tinyxml2')

    depends_on('assimp', when='+assimp')

    depends_on('cgal', when='+cgal')
    depends_on('gdal', when='+gdal')
    depends_on('proj', when='+proj')
    depends_on('proj@:7', when='+proj@:2021.10')

    depends_on('openscenegraph@3.4:', when='+osg')
    depends_on('glew', when='+osg')
    depends_on('glu', when='+osg')

    depends_on('jpeg', when='+embree')
    depends_on('embree+ispc', when='+embree')
    depends_on('ispc', when='+embree', type='build')

    with when("+qt5"):
        depends_on('qt', when='+qt')
    with when("~qt5"):
        depends_on('qt-base', when='+qt')
        depends_on('qt-svg', when='+qt', type="run")

    def setup_build_environment(self, env):
        """Remove environment variables that let CMake find packages outside the spack tree."""
        env.set('ARCHSUFFIX','spack')
        env.unset('EXTERNLIBS')
        env.unset('COVISEDIR')
        env.unset('COVISEDESTDIR')
        env.unset('COVISE_PATH')

    def setup_run_environment(self, env):
        env.set('VISTLE_ROOT', self.prefix)
        if self.spec.satisfies('+python'):
            env.prepend_path("PYTHONPATH", self.prefix.lib)

    def cmake_args(self):
        """Populate cmake arguments for Vistle."""
        spec = self.spec

        args = []

        args.append('-DVISTLE_PEDANTIC_ERRORS=OFF')

        if '+static' in spec:
            args.extend([
                '-DVISTLE_BUILD_SHARED=OFF',
                '-DVISTLE_MODULES_SHARED=OFF'
            ])

        args.append(self.define('VISTLE_INTERNAL_BOOST_MPI', not spec.satisfies('+boostmpi')))
        args.append(self.define('VISTLE_INTERNAL_VTKM', not spec.satisfies('+vtkm')))
        if not spec.satisfies('+vtkm'):
            args.append(self.define_from_variant('VISTLE_USE_CUDA', 'cuda'))
            use_kokkos = spec.satisfies("+kokkos") or spec.satisfies("+rocm")
            args.append(self.define('VISTLE_USE_KOKKOS', use_kokkos))

            # hip support
            if "+rocm" in spec:
                args.append(self.builder.define_hip_architectures(self))
                if "+kokkos" in spec:
                    hipcc = self.spec['hip'].prefix.bin.join('hipcc')
                    args.append(self.define('CMAKE_CXX_COMPILER', str(hipcc)))
        
        args.append(self.define('VISTLE_COLOR_DIAGNOSTICS', 'OFF'))
        args.append(self.define_from_variant('VISTLE_USE_OPENMP', 'openmp'))

        args.append(self.define_from_variant('VISTLE_MULTI_PROCESS', 'multi'))
        args.append(self.define_from_variant('VISTLE_DOUBLE_PRECISION', 'double'))
        args.append(self.define_from_variant('VISTLE_64BIT_INDICES', 'large'))

        args.append(self.define_from_variant('VISTLE_INSTALL_3RDPARTY', 'dev'))

        return args