import logging
from typing import NoReturn
from flask import Flask, request
import json, os

CONFIG_FILENAME = "cute_mod_manager_settings.json"
config: dict[str, str] = {
    "game folder": r"C:\Program Files (x86)\Steam\steamapps\common\Mini Airways"
}
plugin_folder = ""
app = Flask(__name__)
mods: dict[str, dict[str, str]] = {}
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=os.path.splitext(__file__)[0] + ".log",
)


def load_mods() -> dict[str, dict[str, str]] | None:
    def __get_version_number(file_path) -> str:
        from win32com.client import Dispatch

        """获取文件版本信息"""
        information_parser = Dispatch("Scripting.FileSystemObject")
        version = information_parser.GetFileVersion(file_path)
        return version

    if os.path.isdir(plugin_folder):
        result = {}
        for f in os.listdir(plugin_folder):
            if f.endswith(".dll") or f.endswith(".dll.disabled"):
                result[f.removesuffix(".dll.disabled").removesuffix(".dll")] = {
                    "filename": f,
                    "status": "启用" if f.endswith(".dll") else "禁用",
                    "version": __get_version_number(os.path.join(plugin_folder, f)),
                }
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

    with open(__resource_path(file_path), "r", encoding="utf-8") as f:
        return f.read()


@app.route("/index.css", methods=["GET"])
def index_css():
    return __static_file("index.css")


@app.route("/", methods=["GET"])
def index():
    return __static_file("index.html")


@app.route("/contact")
def contact():
    return __static_file("contact.html")


@app.route("/enable", methods=["POST"])
def enableMod():
    name: str = os.path.join(plugin_folder, request.form.get("name"))
    os.rename(mods[name]["filename"], mods[name]["filename"].removesuffix(".disabled"))
    return "ok"


@app.route("/disable", methods=["POST"])
def disableMod():
    name: str = os.path.join(plugin_folder, request.form.get("name"))
    os.rename(mods[name]["filename"], mods[name]["filename"] + ".disabled")
    return "ok"


@app.route("/mods", methods=["GET"])
def getMods():
    global mods
    mods = load_mods()
    return json.dumps(
        [
            {
                "name": k,
                "filename": v["filename"],
                "status": v["status"],
                "version": v["version"],
            }
            for k, v in mods
        ]
    )


@app.route("/delete", methods=["POST"])
def deleteMod():
    name = request.form.get("name")
    path: str = os.path.join(plugin_folder, mods[name]["filename"])
    os.remove(path)
    return "ok"


@app.route("/path", methods=["POST"])
def path():
    global config, plugin_folder
    config["game folder"] = request.form.get("path")
    with open(CONFIG_FILENAME, "w") as f:
        json.dump(config, f)
    plugin_folder = os.path.join(config["game folder"], "BepInEx", "plugins")
    return "ok"


def main() -> NoReturn:
    global config, plugin_folder
    if not os.path.exists(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, "w") as f:
            json.dump(config, f)
    with open(CONFIG_FILENAME, "r") as f:
        config = json.load(f)
        plugin_folder = os.path.join(config["game folder"], "BepInEx", "plugins")
    os.system("start http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
