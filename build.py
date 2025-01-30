# update_version.py
import json, datetime, os, sys

rc_filename = "version.rc"


def update_version():
    rc_content = """
#include <winver.h>
VS_VERSION_INFO VERSIONINFO
 FILEVERSION     {0}
 PRODUCTVERSION  {0}
 FILEOS          VOS_NT_WINDOWS32
 FILETYPE        VFT_APP
BEGIN
  BLOCK "StringFileInfo"
  BEGIN
    BLOCK "040904b0"
    BEGIN
      VALUE "FileDescription",  "迷你空管 Cute Mod 管理器"
      VALUE "FileVersion",      "{0}"
      VALUE "ProductName",      "Mini Airways Cute Mod Manager"
      VALUE "ProductVersion",   "{0}"
      VALUE "CompanyName",      "Cute Omega"
      VALUE "LegalCopyright",   "Open Source by GPLv3 © 2025 - {1}"
    END
  END
  BLOCK "VarFileInfo"
  BEGIN
    VALUE "Translation", 0x0409, 1200
  END
END
"""

    if not os.path.isfile(rc_filename):
        major = 0
        minor = 0
        patch = 0
        build = 0
    else:
        # 读取当前版本号
        with open(rc_filename) as f:
            old_version = f.readlines()[2].strip().split()[-1]
            major, minor, patch, build = map(int, old_version.split("."))

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

    new_version = f"{major}.{minor}.{patch}.{build}"

    # 生成 version.rc 文件
    with open(rc_filename, "w", encoding="utf-8") as f:
        f.write(rc_content.format(new_version, datetime.datetime.now().year))
    return new_version


def main():
    print("检测版本...")
    new_version = update_version()
    print("新版本：", new_version)
    print("开始打包...")
    os.system(
        f"""pyinstaller -F -w ^
  --add-data "index.html;." ^
  --add-data "index.css;." ^
  --add-data "contact.html;." ^
  --exclude-module "mod_manager_settings.json" ^
  --hidden-import=win32com.client ^
  --version-file={rc_filename} ^
  MiniAirwaysCuteModManager.py"""
    )
    print("打包完成！可执行文件在 dist 文件夹中")


if __name__ == "__main__":
    main()
