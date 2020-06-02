import bpy, bmesh, math
from . import utils


class AddModifier(bpy.types.Operator):
    bl_idname = 'b7.add_modifier'
    bl_label = 'Add Modifier'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}
    bl_description = utils.description(
        'First remove modifiers of the chosen type from selected objects',
        'Then add the chosen modifier to selected objects with the chosen settings',
    )


    modifier: bpy.props.EnumProperty(
        name='Modifier',
        description='What type of modifier to add',
        items=[
            ('WEIGHTED_NORMAL', 'Weighted Normal', 'Modify the direction of the surface normals using a weighting method'),
            ('TRIANGULATE', 'Triangulate', 'Convert all polygons to triangles'),
            ('MIRROR', 'Mirror', 'Mirror along the local X, Y, and/or Z axes, over the object origin'),
        ]
    )


    settings: bpy.props.EnumProperty(
        name='Settings',
        description='Which modifier settings to use',
        items=[
            ('HIGH_POLY', 'High Poly', 'Use modifier settings suited for high poly export'),
            ('LOW_POLY', 'Low Poly', 'Use modifier settings sutied for low poly export'),
        ]
    )


    axes: bpy.props.BoolVectorProperty(
        name = 'Axes',
        description='Which axes to mirror across',
        default=(True, False, False),
    )


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects


    #def draw(self, context):
    #    pass # TODO: Implement draw panel


    def execute(self, context):
        name = f'{utils.beautify(self.modifier)} - {utils.beautify(self.settings)}'

        if self.modifier == 'WEIGHTED_NORMAL':
            bpy.ops.object.shade_smooth()

        for obj in context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == self.modifier:
                    obj.modifiers.remove(mod)

            mod = obj.modifiers.new(name, self.modifier)
            mod.show_in_editmode = False
            mod.show_expanded = False

            if self.modifier == 'WEIGHTED_NORMAL':
                self.setup_weighted_normal(obj, mod)

            elif self.modifier == 'TRIANGULATE':
                self.setup_triangulate(obj, mod)

            elif self.modifier == 'MIRROR':
                self.setup_mirror(obj, mod)

        self.report({'INFO'}, name)
        return {'FINISHED'}


    def setup_weighted_normal(self, obj, mod):
        obj.data.use_auto_smooth = True

        if self.settings == 'LOW_POLY':
            obj.data.auto_smooth_angle = math.radians(180)
            mod.keep_sharp = True


    def setup_triangulate(self, obj, mod):
        mod.keep_custom_normals = True
        mod.quad_method = 'FIXED'
        mod.ngon_method = 'CLIP'


    def setup_mirror(self, obj, mod):
        mod.use_axis = self.axes
        mod.use_bisect_axis = self.axes

        use_mirror_vertex_groups = True

        if self.settings == 'LOW_POLY':
            mod.use_mirror_merge = False
            mod.use_clip = False

        elif self.settings == 'HIGH_POLY':
            mod.use_mirror_merge = True
            mod.use_clip = True

        mod.offset_u = 1
        mod.offset_v = 0

        if self.settings == 'LOW_POLY':
            bm = bmesh.new()
            bm.from_mesh(obj.data)

            for index, axis in enumerate(self.axes):
                if not axis:
                    continue

                geom = bm.verts[:] + bm.edges[:] + bm.faces[:]

                plane_no = [0, 0, 0]
                plane_no[index] = 1

                # TODO: Rotate normal with object's rotation_euler

                bmesh.ops.bisect_plane(bm, geom=geom, dist=0, plane_co=obj.location, plane_no=plane_no, clear_inner=True)

            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)

            bm.to_mesh(obj.data)
            bm.free()


class ImportExport(bpy.types.Operator):
    bl_idname = 'b7.import_export'
    bl_label = 'Import Export'
    bl_options = {'REGISTER', 'INTERNAL'}
    bl_description = 'Import / Export of FBX / GLB / OBJ / STL'


    mode: bpy.props.EnumProperty(
        name='Type',
        description='Which file type to import or export',
        items=[
            ('IMPORT_FBX', 'Import FBX', 'Import FBX file'),
            ('IMPORT_GLB', 'Import glTF', 'Import glTF 2.0 file'),
            ('IMPORT_OBJ', 'Import OBJ', 'Import Wavefront OBJ file'),
            ('IMPORT_STL', 'Import STL', 'Import STL file'),
            ('EXPORT_FBX', 'Export FBX', 'Export selected objects as FBX'),
            ('EXPORT_GLB', 'Export glTF', 'Export selected objects as glTF 2.0'),
            ('EXPORT_OBJ', 'Export OBJ', 'Export selected objects as Wavefront OBJ'),
            ('EXPORT_STL', 'Export STL', 'Export selected objects as STL'),
        ]
    )


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'


    def execute(self, context):
        objects = len(context.selected_objects)

        if self.mode == 'IMPORT_FBX':
            bpy.ops.import_scene.fbx('INVOKE_DEFAULT')
        elif self.mode == 'IMPORT_GLB':
            bpy.ops.import_scene.gltf('INVOKE_DEFAULT')
        elif self.mode == 'IMPORT_OBJ':
            bpy.ops.import_scene.obj('INVOKE_DEFAULT')
        elif self.mode == 'IMPORT_STL':
            bpy.ops.import_mesh.stl('INVOKE_DEFAULT')

        elif self.mode == 'EXPORT_FBX':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, object_types={'MESH'})
            #self.report({'INFO'}, f'Exported {objects} objects as FBX')

        elif self.mode == 'EXPORT_GLB':
            bpy.ops.export_scene.gltf('INVOKE_DEFAULT', use_selection=True, export_apply=True)
            #self.report({'INFO'}, f'Exported {objects} objects as glTF 2.0 (binary)')

        elif self.mode == 'EXPORT_OBJ':
            bpy.ops.export_scene.obj('INVOKE_DEFAULT', use_selection=True)
            #self.report({'INFO'}, f'Exported {objects} objects as Wavefront OBJ')

        elif self.mode == 'EXPORT_STL':
            bpy.ops.export_mesh.stl('INVOKE_DEFAULT', use_selection=True)
            #self.report({'INFO'}, f'Exported {objects} objects as STRL')

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AddModifier)
    bpy.utils.register_class(ImportExport)


def unregister():
    bpy.utils.unregister_class(ImportExport)
    bpy.utils.unregister_class(AddModifier)
