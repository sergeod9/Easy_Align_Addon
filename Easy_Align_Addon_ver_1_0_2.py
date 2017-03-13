# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Easy Align",
    "author":"Georges Dahdouh",
    "version":(1,0,0),
    "blender":(2,7,8),
    "location":"View 3D > Property Shelf",
    "description":"Align mesh objects origins and mesh to selected axis",
    "warning":"",
    "category" : "Align"
}

import bpy
from bpy.props import *

Axis = [('0','X',""),
        ('1','Y',""),
        ('2','Z',"")
        ]

ax_prop = EnumProperty \
(
items = Axis,
name ="",
description = "Set the Axis",
default = '2'
)

snap_items = [('0','To Grid',''),
            ('1','To Cursor',''),
            ('2','To Cursor (offset)',''),
            ('3','To Active','')
            ]
            
snap_enum = EnumProperty \
(
items = snap_items,
name ="",
description = "Snap to"
)
            
invert_ax = BoolProperty \
(name = "Maximum",
description = "Set to Maximum",
default = False
)

invert_active_ax = BoolProperty \
(name = "Active Maximum",
description = "Set active to Maximum for Exclusively Align Objects",
default = True
)

median_prop = BoolProperty \
(name = "Median",
description = "Align origin using median vertices coordniates",
default = False
)

local_prop = BoolProperty \
(name = "Local",
description = "Use local coordinates, default is global",
default = False
)
    
flex_prop = FloatProperty \
(name = "Flexibility",
description = "The higher the value, the more flexible alignment is in Blender units",
default = 0.01,
step = 1,
min = 0.0
)

class Easy_A_OP(bpy.types.Operator):
    """Set origin to selected axi"""
    bl_idname = "object.easy_a"
    bl_label = "Easy Align"
    bl_options = {'REGISTER','UNDO'}

    def execute(self,context):
        
                            
        lt_selected =[] 
        vlist = []       
        C = bpy.context 
        D = bpy.data
        O = bpy.ops
        area = context.area
        current_m = C.object.mode
        areaAnchor = area.type
        S = C.selected_objects
        active_ob = C.active_object
        ax_prop = int(context.object.set_enum_prop)
        invert_ax = context.object.set_maximum
        median_prop = context.object.set_median
        flex_prop = context.object.flexibility
        local_prop = context.object.set_local
        original_cursor = list(C.scene.cursor_location)

        if bpy.context.object.type == 'MESH':
            current_m = context.object.mode
            if  current_m == 'EDIT':
                context.object.update_from_editmode()
                bpy.ops.object.mode_set(mode = 'OBJECT')

            
            for i in S:
                if i.type == "MESH":
                    lt_selected.append(i)
                    
            for act_loop in lt_selected:
                vertGlob=[]
                O.object.select_all(action="DESELECT")
                C.scene.objects.active = act_loop
                act_loop.select = True
                O.object.mode_set(mode = 'EDIT') 
                O.mesh.select_mode(type='VERT')
                O.mesh.select_all(action = 'DESELECT')
                O.object.mode_set(mode = 'OBJECT')
                mw = C.active_object.matrix_world
                vert = C.active_object.data.vertices
                vertGlob = [mw * v.co for v in vert]
                
                if local_prop:
                    vertGlob = [v.co for v in vert]

                if invert_ax:
                    sel_ax = max([v[ax_prop] for v in vertGlob])
                else:
                    sel_ax = min([v[ax_prop] for v in vertGlob])
                    
                for v in vert:
                    vlist = list(mw * v.co)
                    if local_prop:
                        vlist = list(v.co)
                    if vlist[ax_prop] >= (sel_ax - flex_prop) and vlist[ax_prop] <= (sel_ax + flex_prop) :
                        v.select = True
                    else:
                        v.select = False
                        
                area.type = 'VIEW_3D'
                O.object.mode_set(mode = 'EDIT')
                O.view3d.snap_cursor_to_selected()
                context.object.update_from_editmode()
                O.object.mode_set(mode = 'OBJECT')
                O.object.origin_set(type='ORIGIN_CURSOR')
                
                if median_prop:
                    O.object.origin_set(type = 'ORIGIN_GEOMETRY')
                    O.view3d.snap_cursor_to_active()
                    C.space_data.cursor_location[ax_prop]= sel_ax
                    O.object.origin_set(type='ORIGIN_CURSOR')
                    
                area.type = areaAnchor
                
            C.scene.cursor_location = original_cursor
            
            for i in range(len(S)):
                if S[i].name != active_ob:
                    S[i].select = True
                    
            C.scene.objects.active = active_ob
            O.object.mode_set(mode = current_m)
            
        return {"FINISHED"}
    
class Easy_A_Object_OP(bpy.types.Operator):
    """Align Selected to Active"""
    bl_idname = "object.easy_a_sel_to_active"
    bl_label = "Selected to Active"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self,context):
        C = bpy.context 
        D = bpy.data
        O = bpy.ops
        sel = bpy.context.selected_objects
        act = bpy.context.active_object
        invert_ax = context.object.set_maximum
        area = context.area
        areaAnchor = area.type
        current_m = C.object.mode
        if bpy.context.object.type == 'MESH':
            current_m = context.object.mode
            if  current_m == 'EDIT':
                context.object.update_from_editmode()
                bpy.ops.object.mode_set(mode = 'OBJECT')
            
        if len(sel)>=2:
            for i in sel:
                if i == act:
                    i.select = False
                    sel.remove(act)
                    Easy_A_OP.execute(self,context)
            O.object.select_all(action = "DESELECT")
            act.select = True
            if invert_ax:
                C.object.set_maximum = False
                Easy_A_OP.execute(self,context)
                C.object.set_maximum = True
            else:
                C.object.set_maximum = True
                Easy_A_OP.execute(self,context)
                C.object.set_maximum = False
                
            O.object.select_all(action = "DESELECT")
            
            for i in sel:
                i.select = True
                O.view3d.snap_selected_to_active()
            act.select = True
            O.object.mode_set(mode = current_m)
            area.type = areaAnchor
                        
        return {"FINISHED"}

class Easy_A_Object_OP_EXCL(bpy.types.Operator):
    """Align Selected to Active exclusively using chosen axis"""
    bl_idname = "object.easy_a_sel_to_active_excl"
    bl_label = "Selected to Active"
    bl_options = {'REGISTER','UNDO'}
    
    def execute(self,context):
        C = bpy.context 
        D = bpy.data
        O = bpy.ops
        sel = bpy.context.selected_objects
        act = bpy.context.active_object
        invert_ax = context.object.set_maximum
        onlySel = []
        area = context.area
        areaAnchor = area.type

        vlist = []   
        vertGlob=[]   
        current_m = C.active_object.mode
        ax_prop = int(context.object.set_enum_prop)
        median_prop = context.object.set_median
        flex_prop = context.object.flexibility
        local_prop = context.object.set_local
        active_maximum = context.object.set_active_maximum
        original_cursor = list(C.scene.cursor_location) 

        if  current_m == 'EDIT':
            context.object.update_from_editmode()
            bpy.ops.object.mode_set(mode = 'OBJECT')
                    
        if len(sel)>=2:
            for i in sel:
                if i != act:
                    onlySel.append(i)
            for v in onlySel:
                O.object.select_all(action="DESELECT")
                v.select = True
                Easy_A_OP.execute(self,context)

                
            O.object.select_all(action="DESELECT")
            act.select = True
            O.object.mode_set(mode = 'EDIT') 
            context.object.update_from_editmode()
            O.mesh.select_mode(type='VERT')
            O.mesh.select_all(action = 'DESELECT')
            O.object.mode_set(mode = 'OBJECT')
            mw = C.active_object.matrix_world
            vert = C.active_object.data.vertices
            vertGlob = [mw * v.co for v in vert]
            
            if local_prop:
                local_prop == False

            if not active_maximum:
                sel_ax = min([v[ax_prop] for v in vertGlob])
            elif active_maximum and not invert_ax:
                sel_ax = max([v[ax_prop] for v in vertGlob])
            else:
                sel_ax = max([v[ax_prop] for v in vertGlob])
                
            for v in vert:
                vlist = list(mw * v.co)
                if local_prop:
                    vlist = list(v.co)
                if vlist[ax_prop] >= (sel_ax - flex_prop) and vlist[ax_prop] <= (sel_ax + flex_prop) :
                    v.select = True
                else:
                    v.select = False
            vertGlob = [mw*v.co for v in vert]
            area.type = 'VIEW_3D'
            O.object.mode_set(mode = 'EDIT')
            O.view3d.snap_cursor_to_selected()
            context.object.update_from_editmode()
            O.object.mode_set(mode = 'OBJECT')
            O.object.mode_set(mode = current_m)
            for i in onlySel:
                C.scene.objects.active = i
                i.location[ax_prop]= bpy.context.scene.cursor_location[ax_prop]
            for v in sel:
                v.select = True
                
            
            area.type = areaAnchor
            C.scene.cursor_location = original_cursor
            C.scene.objects.active = act
            
                        
        return {"FINISHED"}

class Snap_to_OP(bpy.types.Operator):
    bl_idname = "object.snap_to_operator"
    bl_label = "Snap to"
    bl_options = {'REGISTER','UNDO'}
   
    def execute(self,context):
        
        snap_enum = int(context.object.snap_to)
        
        if snap_enum == 0:
            bpy.ops.view3d.snap_selected_to_grid()
        if snap_enum == 1:
            bpy.ops.view3d.snap_selected_to_cursor(use_offset = False)
        if snap_enum == 2:
            bpy.ops.view3d.snap_selected_to_cursor(use_offset = True)
        if snap_enum == 3:
            bpy.ops.view3d.snap_selected_to_active()
        
        return {"FINISHED"}
    
        
class Easy_A_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Easy Align"
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object is not None and bpy.context.active_object.type == "MESH"
    
    def draw(self, context):
        
        layout = self.layout
        box = layout.box()
        col = box.row().column()
        col.operator("object.easy_a", "Align Origin")
        col.label("Default Minimum")
        row = box.row()
        col.prop(context.object, "set_maximum")
        col.prop(context.object, "set_median")
        col.prop(context.object, "set_local")
        col.prop(context.object, "set_enum_prop")
        col.prop(context.object,"flexibility")
        col = box.row().column()
        col.label("Selected to Active")
        col.operator("object.easy_a_sel_to_active","Align Objects")
        split = col.split()
        col.label ("Align Objects Exclusively")
        col.operator("object.easy_a_sel_to_active_excl","Exclusively Align Objects")
        col.prop(context.object,"set_active_maximum")
        
        
        split = layout.split()
        
        row = layout.row()
        row.operator("object.origin_set","Set Origin")
        row.operator("object.snap_to_operator","Snap")
        row.prop(context.object,"snap_to")


def register():
    bpy.utils.register_class(Easy_A_panel)
    bpy.utils.register_class(Easy_A_OP)
    bpy.utils.register_class(Easy_A_Object_OP)
    bpy.utils.register_class(Easy_A_Object_OP_EXCL)
    bpy.utils.register_class(Snap_to_OP)
    bpy.types.Object.set_enum_prop = ax_prop
    bpy.types.Object.set_maximum = invert_ax
    bpy.types.Object.set_active_maximum = invert_active_ax
    bpy.types.Object.set_median = median_prop
    bpy.types.Object.set_local = local_prop
    bpy.types.Object.snap_to = snap_enum
    bpy.types.Object.flexibility = flex_prop

def unregister():
    bpy.utils.unregister_class(Easy_A_panel)
    bpy.utils.unregister_class(Easy_A_OP)
    bpy.utils.unregister_class(Easy_A_Object_OP)
    bpy.utils.unregister_class(Easy_A_Object_OP_EXCL)
    bpy.utils.unregister_class(Snap_to_OP)
    del bpy.types.Object.set_enum_prop
    del bpy.types.Object.set_maximum
    del bpy.types.Object.set_median
    del bpy.types.Object.set_local
    del bpy.types.Object.snap_to
    del bpy.types.Object.flexibility
    del bpy.types.Object.set_active_maximum 
    
if __name__ == "__main__":
    register()  
