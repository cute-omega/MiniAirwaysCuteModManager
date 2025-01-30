# update_version.py
import datetime, os, sys, logging

rc_filename = "version.rc"
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_version():
    rc_content = """#include <winver.h>
VS_VERSION_INFO VERSIONINFO
 FILEVERSION     {0}, {1}, {2}, {3}
 PRODUCTVERSION  {0}, {1}, {2}, {3}
 FILEOS          VOS_NT_WINDOWS32
 FILETYPE        VFT_APP
BEGIN
  BLOCK "StringFileInfo"
  BEGIN
    BLOCK "040904b0"
    BEGIN
      VALUE "FileDescription",  "迷你空管 Cute Mod 管理器"
      VALUE "FileVersion",      "{0}.{1}.{2}.{3}"
      VALUE "ProductName",      "Mini Airways Cute Mod Manager"
      VALUE "ProductVersion",   "{0}.{1}.{2}.{3}"
      VALUE "CompanyName",      "Cute Omega"
      VALUE "LegalCopyright",   "Open Source by GPLv3 © 2025 - {4}"
    END
  END
  BLOCK "VarFileInfo"
  BEGIN
    VALUE "Translation", 0x0409, 1200
  END
END"""

    if not os.path.isfile(rc_filename):
        major = 0
        minor = 0
        patch = 0
        build = 0
    else:
        # 读取当前版本号
        with open(rc_filename, encoding="utf-8") as f:
            old_version = f.readlines()[12].strip().split(" ")[-1].strip('"')
            logging.debug(f"{old_version=}")
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
