import os
import subprocess
from .vendor.remi import gui, server


# Mock database
db = {
    "apps": [
        {
            "label": "Maya 2016",
            "exe": r"c:\program files\autodesk\maya2016\bin\maya.exe",
            "icon": "File_Spool_2_64.png",
        },
        {
            "label": "Maya 2018",
            "exe": r"c:\program files\autodesk\maya2018\bin\maya.exe",
            "icon": "File_Spool_2_64.png",
        },
        {
            "label": "NukeX 11v3",
            "exe": "nuke",
            "icon": "File_Plugin_64.png",
        },
        {
            "label": "Mari 2018",
            "exe": "mari",
            "icon": "App_Workspaces_64.png",
        },
        {
            "label": "Photoshop",
            "exe": "photoshop",
            "icon": "App_ImageEditor_64.png",
        },
    ],
    "projects": {
        "Alita": {"assets": {}, "shots": {}},
        "Batman Dark Knight": {"assets": {}, "shots": {}},
        "Batman Begins": {
            "assets": {
                "Bruce Wayne": None,
                "Batman": None,
                "Bat Claw": None,
                "Bat Mobile": None,
            },
            "shots": {
                "1000": None,
                "2000": None,
                "2500": None,
                "2600": None,
                "3100": None,
                "5100": None,
                "5200": None,
                "5700": None,
                "5800": None,
                "5850": None,
                "6500": None,
                "6800": None,
            }
        },
        "Hulk": {
            "assets": {},
            "shots": {},
        },
        "Spiderman": {
            "assets": {},
            "shots": {},
        }
    }
}


class AppButton(gui.HBox):
    def __init__(self, app, *args, **kwargs):
        super(AppButton, self).__init__(*args, **kwargs)
        self.type = "li"

        icon = gui.Image("res/" + app["icon"], width=32)
        button = gui.Button(app["label"])

        # Must be appended prior to connected,
        # else a AttributeError is thrown
        self.append(button)
        button.append(icon)

        button.onclick.connect(self.on_clicked)

        self._app = app
        self._button = button

    def on_clicked(self, widget):
        print(self._app["exe"] + " Clicked!")
        subprocess.Popen([
            self._app["exe"]
        ])


class MyApp(server.App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(__file__), "res")
        super(MyApp, self).__init__(*args, static_file_path=res_path)

    def main(self):
        panels = {
            "page": gui.HBox(),
            "window": gui.VBox(),
            "side": gui.VBox(height="100%", width=300),
            "container": gui.HBox(height="100%",
                                  width=500),
        }

        widgets = {
            "apps": gui.GridBox(),
            "header": gui.Label("Avalon Launcher"),
            "selection": gui.Label("Nothing selected"),
            "tree": gui.TreeView(height="100%", width=250),
        }

        def append_recursive(root, parent):
            for key, value in sorted(root.items()):
                item = gui.TreeItem(key)
                parent.append(item)

                if isinstance(value, dict):
                    append_recursive(value, item)
                else:
                    item.onclick.connect(self.on_item_clicked)

        append_recursive(db["projects"], widgets["tree"])

        for key, value in panels.items():
            value.attributes["object-name"] = key

        for key, value in widgets.items():
            value.attributes["object-name"] = key

        widgets["apps"].define_grid(("ab",
                                     "cd",
                                     "ef",
                                     "gh"))

        for index, app in enumerate(db["apps"]):
            widgets["apps"].append({"abcdefgh"[index]: AppButton(app)})

        panels["side"].append(widgets["selection"])
        panels["side"].append(widgets["apps"])

        panels["container"].style.update({"align-items": "start"})
        panels["window"].style.update({"align-items": "start"})
        panels["container"].append(widgets["tree"])
        panels["container"].append(panels["side"])

        panels["window"].append(widgets["header"])
        panels["window"].append(panels["container"])

        panels["page"].append(panels["window"])

        self.panels = panels
        self.widgets = widgets

        return panels["page"]

    def on_item_clicked(self, widget):
        tree = self.widgets["tree"]
        selection = self.widgets["selection"]

        previous = tree.attributes.get("current-selection")

        if previous:
            previous.attributes.pop("selected", None)

        widget.attributes["selected"] = True
        tree.attributes["current-selection"] = widget
        selection.set_text(widget.get_text())


if __name__ == "__main__":
    import sys

    try:
        server.start(
            MyApp,
            debug=True,
            address="0.0.0.0",
            port=8081,
            start_browser=False,
            multiple_instance=False,
            update_interval=0.1,
        )

    except KeyboardInterrupt:
        sys.exit(0)
