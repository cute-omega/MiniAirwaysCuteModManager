from typing import NoReturn
from flask import Flask, request
import json, os, logging

CONFIG_FILENAME = "cute_mod_manager_settings.json"
config: dict[str, str] = {
    "game folder": r"C:\Program Files (x86)\Steam\steamapps\common\Mini Airways"
}
PORT = 55000


class Mod:
    def __init__(self, name, version, filename, status) -> None:
        self.name = name
        self.version = version
        self.filename = filename
        self.status = status

    def dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "filename": self.filename,
            "status": self.status,
        }

    def __str__(self) -> str:
        return json.dumps(self.dict())


plugin_folder = ""
app = Flask(__name__)
mods: list[Mod] = []
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    # filename=os.path.splitext(__file__)[0] + ".log",
)


def load_mods() -> list[Mod] | None:
    def __get_version_number(file_path) -> str:
        from win32com.client import Dispatch

        """获取文件版本信息"""
        information_parser = Dispatch("Scripting.FileSystemObject")
        version = information_parser.GetFileVersion(file_path)
        return version

    if os.path.isdir(plugin_folder):
        result = []
        for f in os.listdir(plugin_folder):
            if f.endswith(".dll") or f.endswith(".dll.disabled"):
                result.append(
                    Mod(
                        f.removesuffix(".dll.disabled").removesuffix(".dll"),
                        __get_version_number(os.path.join(plugin_folder, f)),
                        f,
                        "启用" if f.endswith(".dll") else "禁用",
                    )
                )
        return result
    else:
        return None


def __static_file(file_path):
    def __resource_path(relative_path):
        import sys

        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    with open(__resource_path(file_path), encoding="utf-8") as f:
        return f.read()


@app.route("/index.css")
def index_css():
    return __static_file("index.css")


@app.route("/", methods=["GET"])
def index():
    return __static_file("index.html")


@app.route("/contact")
def contact():
    return __static_file("contact.html")


@app.route("/enable", methods=["POST"])
def enable_mod():
    name: str = os.path.join(plugin_folder, request.args["filename"])
    for mod in mods:
        if mod.name == name:
            os.rename(mod.filename, mod.filename.removesuffix(".disabled"))
            return "ok"
    return "not found"


@app.route("/disable", methods=["POST"])
def disable_mod():
    name: str = os.path.join(plugin_folder, request.args["name"])
    for mod in mods:
        if mod.name == name:
            os.rename(mod.filename, mod.filename + ".disabled")
            return "ok"
    return "not found"


@app.route("/mods", methods=["GET"])
def get_mods():
    global mods
    mods = load_mods()
    mods_dict_list = []
    for mod in mods:
        mods_dict_list.append(mod.dict())
    return json.dumps(mods_dict_list)


@app.route("/delete", methods=["POST"])
def delete_mod():
    name = request.args["name"]
    path = ""
    for mod in mods:
        if mod.name == name:
            path = os.path.join(plugin_folder, mod.filename)
    os.remove(path)
    return "ok"


@app.route("/path", methods=["POST"])
def path():
    global config, plugin_folder
    config["game folder"] = request.args["path"]
    with open(CONFIG_FILENAME, "w", encoding="utf-8") as f:
        json.dump(config, f)
    plugin_folder = os.path.join(config["game folder"], "BepInEx", "plugins")
    return "ok"


def main() -> NoReturn:
    global config, plugin_folder
    import socket

    # 检查端口是否被占用
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", PORT)) == 0:
            logging.info("端口占用，假定为程序已经在运行。无论如何均需退出。")
            import win32api

            win32api.MessageBoxW(
                0,
                "端口被占用，可能因为程序已经在运行。如果程序已在运行，请在浏览器中打开127.0.0.1:55000以打开程序界面",
                "错误",
                0,
            )
            exit()

    if not os.path.exists(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, "w", encoding="utf-8") as f:
            json.dump(config, f)
    with open(CONFIG_FILENAME, encoding="utf-8") as f:
        config = json.load(f)
        plugin_folder = os.path.join(config["game folder"], "BepInEx", "plugins")

    # os.system(f"start http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, debug=True)


if __name__ == "__main__":
    main()
