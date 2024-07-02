# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['src\\porting-advisor.py'],
    pathex=[],
    binaries=[],
    datas=[('src\\advisor\\rules\\*.json', 'advisor\\rules'), ('src\\advisor\\tools\\graviton-ready-java\\target\\*', 'advisor\\tools\\graviton-ready-java\\target'), ('src\\advisor\\templates\\template.html', 'advisor\\templates'), ('.venv\\lib\\site-packages\\certifi\\cacert.pem', 'certifi')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['readline', 'pyinstaller', 'pyinstaller-hooks-contrib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.binaries -= TOC([
    ('api-ms-win-core-console-l1-1-0.dll', None, None), 
    ('api-ms-win-core-datetime-l1-1-0.dll', None, None), 
    ('api-ms-win-core-debug-l1-1-0.dll', None, None), 
    ('api-ms-win-core-errorhandling-l1-1-0.dll', None, None), 
    ('api-ms-win-core-fibers-l1-1-0.dll', None, None), 
    ('api-ms-win-core-file-l1-1-0.dll', None, None), 
    ('api-ms-win-core-file-l1-2-0.dll', None, None), 
    ('api-ms-win-core-file-l2-1-0.dll', None, None), 
    ('api-ms-win-core-handle-l1-1-0.dll', None, None), 
    ('api-ms-win-core-heap-l1-1-0.dll', None, None), 
    ('api-ms-win-core-interlocked-l1-1-0.dll', None, None), 
    ('api-ms-win-core-libraryloader-l1-1-0.dll', None, None), 
    ('api-ms-win-core-localization-l1-2-0.dll', None, None), 
    ('api-ms-win-core-memory-l1-1-0.dll', None, None), 
    ('api-ms-win-core-namedpipe-l1-1-0.dll', None, None), 
    ('api-ms-win-core-processenvironment-l1-1-0.dll', None, None), 
    ('api-ms-win-core-processthreads-l1-1-0.dll', None, None), 
    ('api-ms-win-core-processthreads-l1-1-1.dll', None, None), 
    ('api-ms-win-core-profile-l1-1-0.dll', None, None), 
    ('api-ms-win-core-rtlsupport-l1-1-0.dll', None, None), 
    ('api-ms-win-core-string-l1-1-0.dll', None, None), 
    ('api-ms-win-core-synch-l1-1-0.dll', None, None), 
    ('api-ms-win-core-synch-l1-2-0.dll', None, None), 
    ('api-ms-win-core-sysinfo-l1-1-0.dll', None, None), 
    ('api-ms-win-core-timezone-l1-1-0.dll', None, None), 
    ('api-ms-win-core-util-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-conio-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-convert-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-environment-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-filesystem-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-heap-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-locale-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-math-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-process-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-runtime-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-stdio-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-string-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-time-l1-1-0.dll', None, None), 
    ('api-ms-win-crt-utility-l1-1-0.dll', None, None), 
    ('libffi-7.dll', None, None), 
    ('ucrtbase.dll', None, None),
    ('vcruntime140.dll', None, None)
    ])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='porting-advisor-win-x64',
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
    name='porting-advisor-win-x64',
)
