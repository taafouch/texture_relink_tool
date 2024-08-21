import pytest
from texture_relink import main


@pytest.fixture
def mock_maya_main_window(monkeypatch):
    class MockMainWindow:
        pass

    monkeypatch.setattr("texture_relink.maya_utils.maya_main_window", lambda: MockMainWindow())


@pytest.fixture
def mock_texture_relink_window(monkeypatch):
    class MockTextureRelinkWindow:
        def __init__(self, parent=None):
            self.parent = parent

        @classmethod
        def get_instance(cls, parent=None):
            return cls(parent)

        def show(self):
            pass

        def raise_(self):
            pass

        def activateWindow(self):
            pass

    monkeypatch.setattr("texture_relink.main.TextureRelinkWindow", MockTextureRelinkWindow)


def test_main(mock_maya_main_window, mock_texture_relink_window):
    main.main()


if __name__ == "__main__":
    pytest.main()