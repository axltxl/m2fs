# -*- mode: python ; coding: utf-8 -*-
# python spec file used by pyinstaller in order
# to get us a Windows executable file

import os


block_cipher = None

basedir = os.getcwd()
target_script = f"{basedir}/windows/m2fs.win64.py"
simconnect_dll = f"{basedir}/windows/SimConnect.dll"
config_file = f"{basedir}/examples/generic/config.py"


a = Analysis(
    [target_script],
    pathex=[basedir],
    binaries=[(simconnect_dll, ".")],
    datas=[(config_file, ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="m2fs",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="m2fs",
)
