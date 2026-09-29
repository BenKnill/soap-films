"""Render a relaxed soap film (from export_meshes.js) in Cycles with physically based thin-film interference.

Usage: Blender -b -P blender/render_frame.py -- NAME [out.png] [samples]
The film is a Principled BSDF with IOR 1.0 (air on both sides) and a thin film of IOR 1.33 whose thickness comes
from the per-vertex attribute "thick" (nm), so Cycles computes the interference colours itself.
"""
import bpy, json, math, sys, os
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
NAME = argv[0] if argv else "cube"; HERE = os.path.dirname(os.path.abspath(__file__))
OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, "out", f"{NAME}.png"); SAMPLES = int(argv[2]) if len(argv) > 2 else 192
data = json.load(open(os.path.join(HERE, f"{NAME}.json")))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
# y-up (our meshes) → z-up (Blender)
yup = lambda v: (v[0], -v[2], v[1])

def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m, b

# the film
mesh = bpy.data.meshes.new("film"); mesh.from_pydata([yup(v) for v in data["V"]], [], data["tris"]); mesh.update()
for p in mesh.polygons: p.use_smooth = True
att = mesh.attributes.new("thick", "FLOAT", "POINT")
for i, d in enumerate(data["D"]): att.data[i].value = d
film = bpy.data.objects.new("film", mesh); scene.collection.objects.link(film)
fm, fb = principled("soap", **{"Base Color": (1, 1, 1, 1), "Metallic": 0.0, "Roughness": 0.0, "IOR": 1.0, "Transmission Weight": 1.0, "Thin Film IOR": 1.33})
at = fm.node_tree.nodes.new("ShaderNodeAttribute"); at.attribute_name = "thick"; at.attribute_type = "GEOMETRY"
fm.node_tree.links.new(at.outputs["Fac"], fb.inputs["Thin Film Thickness"])
film.data.materials.append(fm)

# wires, triple lines and junctions
def tube(pts, r, mat, name):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = r; cu.bevel_resolution = 4; cu.use_fill_caps = True
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for i, p in enumerate(pts): sp.points[i].co = (*yup(p), 1)
    ob = bpy.data.objects.new(name, cu); ob.data.materials.append(mat); scene.collection.objects.link(ob); return ob
metal, _ = principled("wire", **{"Base Color": (0.62, 0.64, 0.68, 1), "Metallic": 1.0, "Roughness": 0.22})
for k, (a, b) in enumerate(data["wires"]): tube([a, b], 0.03, metal, f"wire{k}")

# light, the way soap films are photographed: a black background behind the film and a big soft light behind the
# camera, so every part of the film reflects something bright. The world is bright for directions pointing back
# toward the camera's side and black for directions the camera looks into.
world = bpy.data.worlds.new("w"); scene.world = world; world.use_nodes = True; nt = world.node_tree
bg = nt.nodes["Background"]; tc = nt.nodes.new("ShaderNodeTexCoord"); dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"
ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.color_ramp.elements[0].position = 0.45; ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1); ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (1.0, 0.98, 0.95, 1)
mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -1; mr.inputs["From Max"].default_value = 1
nt.links.new(tc.outputs["Generated"], dp.inputs[0]); nt.links.new(dp.outputs["Value"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = float(os.environ.get("SOFTBOX", "1.6"))
# camera
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scene.collection.objects.link(cam); scene.camera = cam
yaw, pitch, dist = float(os.environ.get("YAW", "0.6")), float(os.environ.get("PITCH", "0.42")), float(os.environ.get("DIST", "7.6"))
cam.location = (dist * math.cos(pitch) * math.sin(yaw), -dist * math.cos(pitch) * math.cos(yaw), dist * math.sin(pitch))
tgt = bpy.data.objects.new("tgt", None); scene.collection.objects.link(tgt); c = cam.constraints.new("TRACK_TO"); c.target = tgt; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cam.data.lens = 50
fwd = [-cam.location[0] / dist, -cam.location[1] / dist, -cam.location[2] / dist]; dp.inputs[1].default_value = (-fwd[0], -fwd[1], -fwd[2])   # bright behind the camera

# render settings
scene.render.engine = "CYCLES"; cy = scene.cycles; cy.samples = SAMPLES; cy.use_denoising = True
cy.max_bounces = 48; cy.transparent_max_bounces = 64; cy.transmission_bounces = 48; cy.glossy_bounces = 12
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences; prefs.compute_device_type = "METAL"; prefs.get_devices()
    for d in prefs.devices: d.use = True
    cy.device = "GPU"
except Exception as e: print("GPU not available:", e)
scene.render.resolution_x, scene.render.resolution_y = 1280, 720
scene.view_settings.view_transform = "AgX"; scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.filepath = OUT; bpy.ops.render.render(write_still=True); print("wrote", OUT)
