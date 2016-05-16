# -*- mode: python -*-

block_cipher = None


a = Analysis(['login.py'],
             pathex=['/home/mirror/\xe6\xa1\x8c\xe9\x9d\xa2/pyse/test/\xe6\xa8\xa1\xe6\x8b\x9f\xe7\x99\xbb\xe5\xbd\x95\xe5\xbe\xae\xe6\x95\x99\xe5\x8a\xa1\xe7\xb3\xbb\xe7\xbb\x9f'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='login',
          debug=False,
          strip=False,
          upx=True,
          console=False )
