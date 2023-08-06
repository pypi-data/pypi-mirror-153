from functools import wraps

import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

from utilitys.params import RunOpts, ParamEditor, ShortcutParameter
from utilitys.widgets import EasyWidget


class LAST_RESULT:
    """Just for testing purposes"""

    value = None


def printResult(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        QtWidgets.QMessageBox.information(
            QtWidgets.QApplication.desktop(),
            "Function Run!",
            f"Func result: {LAST_RESULT.value}",
        )

    return wrapper


@printResult
def funcOutsideClassUpdateOnBtn(a=5, b=6):
    """Function description. This will appear in the hover menu."""
    LAST_RESULT.value = a + b


class MyClass(ParamEditor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registerFunc(funcOutsideClassUpdateOnBtn)

        self.registerFunc(self.updateOnChanging, runOpts=RunOpts.ON_CHANGING)
        self.registerFunc(self.updateOnChanged, runOpts=RunOpts.ON_CHANGED)
        self.registerFunc(
            self.updateOnBtnOrChanged,
            runOpts=[RunOpts.ON_BUTTON, RunOpts.ON_CHANGING, RunOpts.ON_CHANGED],
        )
        self.registerFunc(self.updateOnBtn, btnOpts={"value": "Ctrl+C"})
        self.registerFunc(self.hasCondition)

    @printResult
    def updateOnChanging(self, a=5, b=6, c="string"):
        """
        :param a:
          pType: slider
          limits: [0, 15]
          step: 0.15
        """
        LAST_RESULT.value = f"a={a}, b={b}, c={c}"

    @printResult
    def updateOnBtn(self, boolOp=False):
        LAST_RESULT.value = str(boolOp)

    @printResult
    def updateOnChanged(self, f=5, g="six\nseven"):
        """
        :param f:
          pType: int
          step: 3
          limits: [0, 17]
        :param g:
          pType: text
        """
        LAST_RESULT.value = f"f={f}, g={g}"

    @printResult
    def updateOnBtnOrChanged(self, lstOp="five"):
        """
        :param lstOp:
          pType: list
          limits: ['five', 'six', 'seven']
        """
        LAST_RESULT.value = lstOp

    @printResult
    def updateOnApply(self, fileOp="./"):
        """
        :param fileOp:
          pType: filepicker
          helpText: "File picker can either select existing or non-existing files,
            folders, or multiple files depending on specified configurations."
        """
        LAST_RESULT.value = fileOp

    @printResult
    def hasCondition(self, a=5, b=4):
        """
        :param a:
        :param b:
          condition: a > 0
        """


def run():
    app = pg.mkQApp()

    ShortcutParameter.setRegistry(createIfNone=True)

    editor = MyClass()
    win = EasyWidget.buildMainWin([editor.dockContentsWidget])
    win.show()
    app.exec_()


if __name__ == "__main__":
    run()
