# UTF-8
#
# For more details about fixed file info 'ffi' see:
# https://learn.microsoft.com/en-us/windows/win32/menurc/vs-versioninfo-resource <wrong url>

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 9, 0, 4),  # 文件版本号
    prodvers=(0, 9, 0, 4),  # 产品版本号
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',  # 语言和编码（简体中文-UTF-8）
          [
            StringStruct('FileDescription', '迷你空管 Cute Mod 管理器'),  # 文件描述
            StringStruct('FileVersion', '0.9.0.4'),         # 文件版本（字符串）
            StringStruct('ProductName', 'Mini Airways Cute Mod Manager'),     # 产品名称
            StringStruct('ProductVersion', '0.9.0.4'),      # 产品版本（字符串）
            StringStruct('CompanyName', 'Cute Omega'),    # 公司名称
            StringStruct('LegalCopyright', 'Open Source by GPLv3 © 2025 - 2025')  # 版权信息
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x409, 1200])])  # 英语-UTF16
  ]
)