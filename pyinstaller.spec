from kivy_deps import sdl2, glew  # noqa


block_cipher = None

a = Analysis(
    ['main.py'],
    binaries=[],
    datas=[
        ('*.kv', '.'),
        ('assets', 'assets'),
        ('screens/*.kv', 'screens'),
        ('widgets/*.kv', 'widgets'),
        ('translations', 'translations'),
    ],
    hiddenimports=[
        'babel.numbers',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.binaries = [
    binary for binary in a.binaries
    if not binary[1].lower().startswith(r'c:\windows')
]

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(path) for path in (
        sdl2.dep_bins
        + glew.dep_bins
    )],
    [],
    name='app',
    icon='assets/icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=['vcruntime140.dll'],
    runtime_tmpdir=None,
    console=False,
)

# vim: se syntax=python:
