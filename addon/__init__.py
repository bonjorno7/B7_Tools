from . import ops
from . import ui


def register():
    ops.register()
    ui.register()


def unregister():
    ui.unregister()
    ops.unregister()
