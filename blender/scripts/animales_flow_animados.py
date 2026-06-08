import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 3000
scene.frame_set(1)
scene.render.fps = 30
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    scene.render.engine = 'BLENDER_EEVEE'

world = scene.world or bpy.data.worlds.new("World")
scene.world = world
world.color = (0.015, 0.018, 0.025)

def make_mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    return m

mat_sand = make_mat("mat_sand", (0.42, 0.32, 0.22, 1))
mat_dark = make_mat("mat_dark", (0.04, 0.045, 0.055, 1))
mat_black = make_mat("mat_black", (0.015, 0.015, 0.018, 1))
mat_white = make_mat("mat_white", (0.90, 0.88, 0.82, 1))
mat_seal = make_mat("mat_seal", (0.17, 0.20, 0.24, 1))
mat_seal_light = make_mat("mat_seal_light", (0.36, 0.39, 0.42, 1))
mat_red = make_mat("mat_red", (0.62, 0.10, 0.13, 1))
mat_blue = make_mat("mat_blue", (0.08, 0.22, 0.48, 1))
mat_gold = make_mat("mat_gold", (0.85, 0.66, 0.22, 1))
mat_green = make_mat("mat_green", (0.18, 0.55, 0.26, 1))
mat_purple = make_mat("mat_purple", (0.42, 0.20, 0.62, 1))
mat_cyan = make_mat("mat_cyan", (0.12, 0.62, 0.72, 1))
mat_eye = make_mat("mat_eye", (0.02, 0.02, 0.025, 1))
mat_nose = make_mat("mat_nose", (0.04, 0.035, 0.035, 1))

def smooth(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    obj.select_set(False)

def sphere(name, radius, loc, scale, material, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=radius, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    smooth(obj)
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def cyl(name, radius, depth, loc, rot, material, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = rot
    obj.data.materials.append(material)
    smooth(obj)
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def cone(name, radius1, depth, loc, rot, material, parent=None):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=radius1, radius2=0.01, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = rot
    obj.data.materials.append(material)
    smooth(obj)
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def torus(name, major, minor, loc, rot, material, parent=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    smooth(obj)
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def empty(name, loc, parent=None):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=loc)
    obj = bpy.context.object
    obj.name = name
    if parent:
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
    return obj

def key(obj, frame, loc=None, rot=None, scale=None):
    scene.frame_set(frame)
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert(data_path="location", frame=frame)
    if rot is not None:
        obj.rotation_euler = rot
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert(data_path="scale", frame=frame)

def interp(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'SINE'

bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=7.5, depth=0.08, location=(0, 0, -0.04))
arena = bpy.context.object
arena.name = "arena_limpia"
arena.data.materials.append(mat_sand)
smooth(arena)

torus("borde_rojo", 7.4, 0.12, (0, 0, 0.10), (0, 0, 0), mat_red)
torus("borde_dorado", 7.4, 0.035, (0, 0, 0.24), (0, 0, 0), mat_gold)
torus("borde_interno", 5.4, 0.025, (0, 0, 0.04), (0, 0, 0), mat_cyan)

for i in range(18):
    a = math.radians(i * 20)
    x = math.cos(a) * 6.6
    y = math.sin(a) * 6.6
    cyl("luz_baja", 0.035, 0.45, (x, y, 0.24), (0, 0, 0), mat_gold)

main_ball = sphere("pelota_grande", 1.25, (0, 0, 1.25), (1, 1, 1), mat_blue)
torus("pelota_banda_1", 1.27, 0.035, (0, 0, 1.25), (math.radians(90), 0, 0), mat_gold)
torus("pelota_banda_2", 1.27, 0.035, (0, 0, 1.25), (0, math.radians(90), 0), mat_gold)
torus("pelota_banda_3", 1.27, 0.025, (0, 0, 1.25), (0, 0, 0), mat_red)

seal_root = empty("seal_root", (0, 0, 2.55))
body_ctrl = empty("body_ctrl", (0, 0, 2.55), seal_root)
head_ctrl = empty("head_ctrl", (0, 0, 2.55), seal_root)
flipper_ctrl = empty("flipper_ctrl", (0, 0, 2.55), seal_root)
tail_ctrl = empty("tail_ctrl", (0, 0, 2.55), seal_root)

body = sphere("body", 0.78, (0, 0, 2.62), (1.05, 0.85, 1.55), mat_seal, body_ctrl)
belly = sphere("belly", 0.50, (0.15, 0, 2.72), (0.85, 0.70, 1.10), mat_seal_light, body_ctrl)
chest = sphere("chest", 0.55, (0.05, 0, 3.35), (0.95, 0.78, 1.10), mat_seal, body_ctrl)
head = sphere("head", 0.43, (0.10, 0, 4.03), (0.95, 0.86, 1.00), mat_seal, head_ctrl)
snout = sphere("snout", 0.17, (0.36, 0, 3.93), (1.25, 0.65, 0.70), mat_white, head_ctrl)
nose = sphere("nose", 0.052, (0.52, 0, 3.98), (1.0, 0.65, 0.55), mat_nose, head_ctrl)
eye_l = sphere("eye_l", 0.048, (0.28, 0.13, 4.13), (0.55, 0.40, 0.85), mat_eye, head_ctrl)
eye_r = sphere("eye_r", 0.048, (0.28, -0.13, 4.13), (0.55, 0.40, 0.85), mat_eye, head_ctrl)

flipper_l = cyl("flipper_l", 0.105, 0.78, (-0.05, 0.70, 2.92), (math.radians(102), 0, math.radians(20)), mat_seal, flipper_ctrl)
flipper_r = cyl("flipper_r", 0.105, 0.78, (-0.05, -0.70, 2.92), (math.radians(102), 0, math.radians(-20)), mat_seal, flipper_ctrl)
tail_l = cyl("tail_l", 0.075, 0.50, (-0.28, 0.22, 2.03), (math.radians(35), math.radians(28), math.radians(25)), mat_seal, tail_ctrl)
tail_r = cyl("tail_r", 0.075, 0.50, (-0.28, -0.22, 2.03), (math.radians(-35), math.radians(28), math.radians(-25)), mat_seal, tail_ctrl)

for y in [0.08, 0.02, -0.04]:
    cyl("whisker_l", 0.006, 0.42, (0.55, 0.18 + y, 3.94 + y * 0.4), (0, math.radians(88), math.radians(8)), mat_white, head_ctrl)
    cyl("whisker_r", 0.006, 0.42, (0.55, -0.18 - y, 3.94 + y * 0.4), (0, math.radians(88), math.radians(-8)), mat_white, head_ctrl)

juggle_1 = sphere("malabar_1", 0.14, (0, 0, 4.90), (1, 1, 1), mat_red)
juggle_2 = sphere("malabar_2", 0.14, (0, 0, 4.90), (1, 1, 1), mat_green)
juggle_3 = sphere("malabar_3", 0.14, (0, 0, 4.90), (1, 1, 1), mat_purple)

curve_mat = mat_cyan
for offset in [-0.5, 0.0, 0.5]:
    curve = bpy.data.curves.new("arco_malabar", "CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 24
    spl = curve.splines.new("POLY")
    spl.points.add(24)
    for i in range(25):
        u = i / 24
        x = -0.55 + 1.10 * u
        y = offset * 0.15
        z = 4.55 + math.sin(u * math.pi) * 1.15
        spl.points[i].co = (x, y, z, 1)
    curve.bevel_depth = 0.01
    obj = bpy.data.objects.new("arco_visual", curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(curve_mat)

bpy.ops.object.light_add(type='AREA', location=(0, -3, 7))
light = bpy.context.object
light.name = "main_light"
light.data.energy = 2600
light.data.size = 6

for name, loc, color, energy in [
    ("spot_foca", (0, -2.8, 6.2), (0.95, 0.98, 1.0), 1600),
    ("luz_lateral_azul", (-4, -3, 3.5), (0.35, 0.60, 1.0), 400),
    ("luz_lateral_calida", (4, -3, 3.5), (1.0, 0.78, 0.45), 400),
]:
    bpy.ops.object.light_add(type='SPOT', location=loc)
    sp = bpy.context.object
    sp.name = name
    sp.data.energy = energy
    sp.data.color = color
    sp.rotation_euler = (math.radians(65), 0, 0)

bpy.ops.object.camera_add(location=(0, -7.6, 4.4), rotation=(math.radians(67), 0, 0))
camera = bpy.context.object
camera.name = "camera_main"
scene.camera = camera

for f in range(1, 3001, 8):
    t = f / 30.0
    balance = math.sin(t * 2.35)
    balance_fast = math.sin(t * 4.7)
    breath = abs(math.sin(t * 1.15))
    ball_shift_x = 0.10 * math.sin(t * 1.2)
    ball_shift_y = 0.05 * math.sin(t * 0.8)

    key(main_ball, f, loc=(ball_shift_x, ball_shift_y, 1.25), rot=(math.radians(t * 24), math.radians(t * 38), math.radians(6 * math.sin(t * 0.7))), scale=(1.0 + 0.015 * abs(balance), 1.0, 1.0 - 0.012 * abs(balance)))

    key(seal_root, f, loc=(ball_shift_x, ball_shift_y, 2.55 + 0.070 * math.sin(t * 2.4)), rot=(math.radians(4.0 * balance_fast), math.radians(2.5 * math.sin(t * 1.05)), math.radians(7.5 * balance)))
    key(body_ctrl, f, loc=(0, 0, 2.55 + 0.025 * math.sin(t * 3.1)), rot=(math.radians(3.0 * math.sin(t * 2.8)), math.radians(2.0 * balance), math.radians(-5.0 * balance)), scale=(1.0 + 0.018 * breath, 1.0, 1.0 - 0.012 * breath))
    key(head_ctrl, f, loc=(0, 0, 2.55), rot=(math.radians(9.0 * math.sin(t * 1.25)), math.radians(6.0 * math.sin(t * 0.95)), math.radians(-8.0 * balance)))
    key(flipper_ctrl, f, loc=(0, 0, 2.55), rot=(math.radians(2.0 * math.sin(t * 2.0)), 0, math.radians(-4.0 * balance)))
    key(tail_ctrl, f, loc=(0, 0, 2.55), rot=(math.radians(3.0 * math.sin(t * 2.6)), 0, math.radians(10.0 * math.sin(t * 3.4))))

    key(flipper_l, f, rot=(math.radians(102 + 24 * math.sin(t * 3.5)), 0, math.radians(20 + 26 * math.sin(t * 3.8))))
    key(flipper_r, f, rot=(math.radians(102 - 24 * math.sin(t * 3.5)), 0, math.radians(-20 - 26 * math.sin(t * 3.8))))
    key(tail_l, f, rot=(math.radians(35 + 12 * math.sin(t * 4.1)), math.radians(28), math.radians(25 + 16 * math.sin(t * 4.4))))
    key(tail_r, f, rot=(math.radians(-35 - 12 * math.sin(t * 4.1)), math.radians(28), math.radians(-25 - 16 * math.sin(t * 4.4))))

    for index, obj in enumerate([juggle_1, juggle_2, juggle_3]):
        phase = index * 2.094
        x = 0.58 * math.sin(t * 2.55 + phase)
        y = 0.04 * math.cos(t * 1.1 + phase)
        z = 4.55 + 1.15 * abs(math.sin(t * 2.55 + phase))
        scale = 1.0 + 0.10 * abs(math.sin(t * 2.55 + phase))
        key(obj, f, loc=(x, y, z), rot=(math.radians(t * 120), math.radians(t * 90), 0), scale=(scale, scale, scale))

    cam_x = 0.30 * math.sin(t * 0.10)
    cam_y = -7.6 + 0.25 * math.sin(t * 0.08)
    cam_z = 4.4 + 0.12 * math.sin(t * 0.12)
    key(camera, f, loc=(cam_x, cam_y, cam_z), rot=(math.radians(67 + 0.8 * math.sin(t * 0.09)), 0, math.radians(1.0 * math.sin(t * 0.08))))

for obj in [
    main_ball, seal_root, body_ctrl, head_ctrl, flipper_ctrl, tail_ctrl,
    flipper_l, flipper_r, tail_l, tail_r,
    juggle_1, juggle_2, juggle_3, camera
]:
    interp(obj)

scene.frame_set(1)
print("Escena corregida: foca centrada, pelota grande, malabarismo, equilibrio y animacion limpia.")