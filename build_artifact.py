#! /usr/bin/python3

from jonchki import cli_args
from jonchki import install

import glob
import os
import subprocess


tPlatform = cli_args.parse()
print('Building for %s' % tPlatform['platform_id'])


# --------------------------------------------------------------------------
# -
# - Configuration
# -

# Get the project folder. This is the folder of this script.
strCfg_projectFolder = os.path.dirname(os.path.realpath(__file__))

# This is the complete path to the testbench folder. The installation will be
# written there.
strCfg_workingFolder = os.path.join(
    strCfg_projectFolder,
    'build',
    tPlatform['platform_id']
)

# -
# --------------------------------------------------------------------------

astrCMAKE_COMPILER = None
astrCMAKE_PLATFORM = None
strMake = None
astrEnv = None

if tPlatform['host_distribution_id'] == 'ubuntu':
    if tPlatform['distribution_id'] == 'ubuntu':
        # Build on linux for linux.
        # It is currently not possible to build for another version of the OS.
        if tPlatform['distribution_version'] != tPlatform['host_distribution_version']:
            raise Exception('The target Ubuntu version must match the build host.')

        if tPlatform['cpu_architecture'] == tPlatform['host_cpu_architecture']:
            # Build for the build host.

            astrCMAKE_COMPILER = []
            astrCMAKE_PLATFORM = []
            strMake = 'make'

        elif tPlatform['cpu_architecture'] == 'armhf':
            # Build on linux for raspberry.

            astrCMAKE_COMPILER = [
                '-DCMAKE_TOOLCHAIN_FILE=%s/cmake/toolchainfiles/toolchain_ubuntu_armhf.cmake' % strCfg_projectFolder
            ]
            astrCMAKE_PLATFORM = [
                '-DJONCHKI_PLATFORM_DIST_ID=%s' % tPlatform['distribution_id'],
                '-DJONCHKI_PLATFORM_DIST_VERSION=%s' % tPlatform['distribution_version'],
                '-DJONCHKI_PLATFORM_CPU_ARCH=%s' % tPlatform['cpu_architecture']
            ]
            strMake = 'make'

        elif tPlatform['cpu_architecture'] == 'arm64':
            # Build on linux for arm64.

            # Install the build dependencies.
            astrDeb = [
                'libcrypt1:arm64',
                'libcrypt-dev:arm64'
            ]
            install.install_foreign_debs(astrDeb, strCfg_workingFolder, strCfg_projectFolder)

            # This is terrible, but there was no way to pass the include and library paths as parameters to the openresty
            # build scripts.
            if os.path.exists('/usr/aarch64-linux-gnu/lib/libcrypt.a') is not True:
                os.symlink(
                    os.path.join(
                        strCfg_workingFolder,
                        'packages/usr/lib/aarch64-linux-gnu/libcrypt.a'
                    ),
                    '/usr/aarch64-linux-gnu/lib/libcrypt.a'
                )
            if os.path.exists('/usr/aarch64-linux-gnu/include/crypt.h') is not True:
                os.symlink(
                    os.path.join(
                        strCfg_workingFolder,
                        'packages/usr/include/crypt.h'
                    ),
                    '/usr/aarch64-linux-gnu/include/crypt.h'
                )

            astrCMAKE_COMPILER = [
                '-DCMAKE_TOOLCHAIN_FILE=%s/cmake/toolchainfiles/toolchain_ubuntu_arm64.cmake' % strCfg_projectFolder
            ]
            astrCMAKE_PLATFORM = [
                '-DJONCHKI_PLATFORM_DIST_ID=%s' % tPlatform['distribution_id'],
                '-DJONCHKI_PLATFORM_DIST_VERSION=%s' % tPlatform['distribution_version'],
                '-DJONCHKI_PLATFORM_CPU_ARCH=%s' % tPlatform['cpu_architecture']
            ]
            strMake = 'make'

        elif tPlatform['cpu_architecture'] == 'riscv64':
            # Build on linux for riscv64.

            astrCMAKE_COMPILER = [
                '-DCMAKE_TOOLCHAIN_FILE=%s/cmake/toolchainfiles/toolchain_ubuntu_riscv64.cmake' % strCfg_projectFolder
            ]
            astrCMAKE_PLATFORM = [
                '-DJONCHKI_PLATFORM_DIST_ID=%s' % tPlatform['distribution_id'],
                '-DJONCHKI_PLATFORM_DIST_VERSION=%s' % tPlatform['distribution_version'],
                '-DJONCHKI_PLATFORM_CPU_ARCH=%s' % tPlatform['cpu_architecture']
            ]
            strMake = 'make'

        else:
            raise Exception('Unknown CPU architecture: "%s"' % tPlatform['cpu_architecture'])

    else:
        raise Exception('Unknown distribution: "%s"' % tPlatform['distribution_id'])

else:
    raise Exception(
        'Unknown host distribution: "%s"' %
        tPlatform['host_distribution_id']
    )

# Create the folders if they do not exist yet.
astrFolders = [
    strCfg_workingFolder
]
for strPath in astrFolders:
    if os.path.exists(strPath) is not True:
        os.makedirs(strPath)

# ---------------------------------------------------------------------------
#
# Build openresty.
#
astrCmd = [
    'cmake',
    '-DCMAKE_INSTALL_PREFIX=""',
    '-DPRJ_DIR=%s' % strCfg_projectFolder,
    '-DWORKING_DIR=%s' % strCfg_workingFolder
]
astrCmd.extend(astrCMAKE_COMPILER)
astrCmd.extend(astrCMAKE_PLATFORM)
astrCmd.append(strCfg_projectFolder)
strCwd = os.path.join(strCfg_workingFolder)
subprocess.check_call(' '.join(astrCmd), shell=True, cwd=strCwd, env=astrEnv)
subprocess.check_call('%s pack' % strMake, shell=True, cwd=strCwd, env=astrEnv)
