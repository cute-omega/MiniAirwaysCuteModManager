# update_version.py
import datetime, os, sys, logging

rc_filename = "version.py"
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_version():
    rc_content = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# https://learn.microsoft.com/en-us/windows/win32/menurc/vs-versioninfo-resource <wrong url>

VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({0}, {1}, {2}, {3}),  # 文件版本号
    prodvers=({0}, {1}, {2}, {3}),  # 产品版本号
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
            StringStruct('FileVersion', '{0}.{1}.{2}.{3}'),         # 文件版本（字符串）
            StringStruct('ProductName', 'Mini Airways Cute Mod Manager'),     # 产品名称
            StringStruct('ProductVersion', '{0}.{1}.{2}.{3}'),      # 产品版本（字符串）
            StringStruct('CompanyName', 'Cute Omega'),    # 公司名称
            StringStruct('LegalCopyright', 'Open Source by GPLv3 © 2025 - {4}')  # 版权信息
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x409, 1200])])  # 英语-UTF16
  ]
)"""

    if not os.path.isfile(rc_filename):
        major = 0
        minor = 0
        patch = 0
        build = 0
    else:
        # 读取当前版本号
        with open(rc_filename, encoding="utf-8") as f:
            old_version = (
                f.readlines()[7]
                .strip()
                .replace("filevers=(", "")
                .replace("),  # 文件版本号", "")
            )
            logging.debug(f"{old_version=}")
            major, minor, patch, build = map(
                lambda x: int(x.strip()), old_version.split(",")
            )

    # 自动递增构建号（或根据需求自定义规则）
    for i in sys.argv:
        match i.lower():
            case "+major":
                major += 1
                minor = 0
                patch = 0
                build = 0
            case "+minor":
                minor += 1
                patch = 0
                build = 0
            case "+patch":
                patch += 1
                build = 0
            case _:
                build += 1

    # 生成 version.rc 文件
    with open(rc_filename, "w", encoding="utf-8") as f:
        f.write(
            rc_content.format(major, minor, patch, build, datetime.datetime.now().year)
        )
    return f"{major}.{minor}.{patch}.{build}"


def main():
    print("检测版本...")
    new_version = update_version()
    print("新版本：", new_version)
    cmd = f"""pyinstaller -F -w --add-data "index.html;." --add-data "index.css;." --add-data "contact.html;." --exclude-module "mod_manager_settings.json" --hidden-import=win32com.client --version-file={rc_filename} MiniAirwaysCuteModManager.py"""
    print(f"开始打包，命令行：{cmd}")
    os.system(cmd)
    print("打包完成！一切顺利的话可执行文件在 dist 文件夹中")


if __name__ == "__main__":
    main()
