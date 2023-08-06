from pyqtgraph.Qt import QtWidgets, QtCore

from examples.parameditor import MyClass, LAST_RESULT


def test_default_use(monkeypatch):
    pe = MyClass()
    with monkeypatch.context() as m:
        m.setattr(QtWidgets.QMessageBox, "information", lambda *args: None)

        for proc, params in pe.procToParamsMapping.items():
            lowerName = proc.name.lower()
            if "btn" in lowerName:
                assert params.child("Run")
            if params.hasChildren():
                paramToChange = params.children()[0]
                old = LAST_RESULT.value
                if "changed" in lowerName:
                    paramToChange.sigValueChanged.emit(
                        paramToChange, paramToChange.value()
                    )
                    assert LAST_RESULT.value != old
                if "changing" in lowerName:
                    LAST_RESULT.value = old
                    paramToChange.sigValueChanging.emit(
                        paramToChange, paramToChange.value()
                    )
                    assert LAST_RESULT.value != old
