import bpy


class MainPanel(bpy.types.Panel):
    bl_idname = 'B7_PT_MainPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = 'B7 Tools'


    def draw(self, context):
        layout = self.layout
        layout.ui_units_x = 8
        column = layout.column()

        column.label(text='High Poly', icon='MESH_GRID')
        box = column.box()
        col = box.column(align=True)

        op = col.operator('b7.add_modifier', text='Mirror', icon='MOD_MIRROR')
        op.modifier, op.settings = 'MIRROR', 'HIGH_POLY'
        op = col.operator('b7.add_modifier', text='Weighted Normal', icon='MOD_NORMALEDIT')
        op.modifier, op.settings = 'WEIGHTED_NORMAL', 'HIGH_POLY'
        op = col.operator('b7.add_modifier', text='Triangulate', icon='MOD_TRIANGULATE')
        op.modifier, op.settings = 'TRIANGULATE', 'HIGH_POLY'

        column.separator()

        column.label(text='Low Poly', icon='MESH_PLANE')
        box = column.box()
        col = box.column(align=True)

        op = col.operator('b7.add_modifier', text='Weighted Normal', icon='MOD_NORMALEDIT')
        op.modifier, op.settings = 'WEIGHTED_NORMAL', 'LOW_POLY'
        op = col.operator('b7.add_modifier', text='Triangulate', icon='MOD_TRIANGULATE')
        op.modifier, op.settings = 'TRIANGULATE', 'LOW_POLY'
        op = col.operator('b7.add_modifier', text='Mirror', icon='MOD_MIRROR')
        op.modifier, op.settings = 'MIRROR', 'LOW_POLY'

        column.separator()

        column.label(text='Import', icon='IMPORT')
        box = column.box()
        col = box.column(align=True)

        op = col.operator('b7.import_export', text='FBX', icon='IMPORT').mode = 'IMPORT_FBX'
        op = col.operator('b7.import_export', text='GLB', icon='IMPORT').mode = 'IMPORT_GLB'
        op = col.operator('b7.import_export', text='OBJ', icon='IMPORT').mode = 'IMPORT_OBJ'
        op = col.operator('b7.import_export', text='STL', icon='IMPORT').mode = 'IMPORT_STL'

        column.separator()

        column.label(text='Export', icon='EXPORT')
        box = column.box()
        col = box.column(align=True)

        op = col.operator('b7.import_export', text='FBX', icon='EXPORT').mode = 'EXPORT_FBX'
        op = col.operator('b7.import_export', text='GLB', icon='EXPORT').mode = 'EXPORT_GLB'
        op = col.operator('b7.import_export', text='OBJ', icon='EXPORT').mode = 'EXPORT_OBJ'
        op = col.operator('b7.import_export', text='STL', icon='EXPORT').mode = 'EXPORT_STL'


def popover(self, context):
    self.layout.popover(MainPanel.bl_idname, text='', icon='SCRIPT')


def register():
    bpy.utils.register_class(MainPanel)
    bpy.types.VIEW3D_MT_editor_menus.append(popover)


def unregister():
    bpy.types.VIEW3D_MT_editor_menus.remove(popover)
    bpy.utils.unregister_class(MainPanel)
