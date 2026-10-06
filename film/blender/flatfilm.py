"""A vertical soap film in a rectangular wire frame: drainage bands, slow swirls, a black film, a pop.

  blender -b -P flatfilm.py -- out=DIR/f%05d.png first=0 last=239 [light=day|sodium] [KEY=VALUE ...]

Thickness (nm) in film coordinates u (0 at the top wire, 1 at the bottom): d = (dtop + (dbot - dtop) u'^1.4) * thin,
where u' is u stirred by slow 4D noise and `thin` falls with film time (bands slide down as the film drains). A
common black film (about 12 nm) spreads down from the top while u' < black(t). The pop is a hole growing from a point.
Schedules (per output frame, linear between keys): thin=F:V,F:V..., black=F:V,..., hole=F:V,..., time=F:V,...
Camera: dist=F:V,..., yaw=F:V,..., pitch, lens. light=day uses Cycles' thin film; light=sodium the one-wavelength
Airy reflectance at 589.3 nm.
"""
import bpy, bmesh, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

opt = C.args()
first, last = int(opt.get("first", 0)), int(opt.get("last", 239))
FW, FH = float(opt.get("fw", 1.6)), float(opt.get("fh", 1.0))
light = opt.get("light", "day")


def sched(key, default):
    """'F:V,F:V' -> piecewise-linear (smoothstep-eased) function of the frame"""
    if key not in opt: return lambda f: default
    if ":" not in opt[key]: return lambda f, v=float(opt[key]): v
    pts = sorted((float(a), float(b)) for a, b in (kv.split(":") for kv in opt[key].split(",")))
    def g(f):
        if f <= pts[0][0]: return pts[0][1]
        for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
            if f <= f1:
                s = (f - f0) / (f1 - f0); s = s * s * (3 - 2 * s); return v0 + s * (v1 - v0)
        return pts[-1][1]
    return g


scene = C.setup(opt)
dp, bg = C.softbox_world(scene, float(opt.get("soft", 2.6)), float(opt.get("lo", 0.45)), float(opt.get("hi", 0.75)))
cam = C.Cam(scene, dp, "full")


def thickness(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    u = C.math_node(nt, "DIVIDE", C.math_node(nt, "SUBTRACT", FH / 2, sep.outputs["Z"]), FH)
    tv = C.value_node(nt, "time")
    # domain warp: a slow vector noise displaces the coordinates of the band noise, which marbles the bands
    w = nt.nodes.new("ShaderNodeTexNoise"); w.noise_dimensions = "4D"; w.inputs["Scale"].default_value = 1.1
    w.inputs["Detail"].default_value = 2.0
    nt.links.new(tc.outputs["Object"], w.inputs["Vector"]); nt.links.new(tv.outputs[0], w.inputs["W"])
    wc = nt.nodes.new("ShaderNodeVectorMath"); wc.operation = "SUBTRACT"; wc.inputs[1].default_value = (0.5, 0.5, 0.5)
    nt.links.new(w.outputs["Color"], wc.inputs[0])
    ws = nt.nodes.new("ShaderNodeVectorMath"); ws.operation = "SCALE"; ws.inputs["Scale"].default_value = float(opt.get("warp", 0.45))
    nt.links.new(wc.outputs[0], ws.inputs[0])
    wa = nt.nodes.new("ShaderNodeVectorMath"); wa.operation = "ADD"
    nt.links.new(tc.outputs["Object"], wa.inputs[0]); nt.links.new(ws.outputs[0], wa.inputs[1])
    n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.noise_dimensions = "4D"; n1.inputs["Scale"].default_value = 1.6
    n1.inputs["Detail"].default_value = 4.0; n1.inputs["Roughness"].default_value = 0.55; n1.inputs["Distortion"].default_value = 0.8
    nt.links.new(wa.outputs[0], n1.inputs["Vector"]); nt.links.new(tv.outputs[0], n1.inputs["W"])
    up = C.math_node(nt, "ADD", u, C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", n1.outputs["Fac"], 0.5), float(opt.get("stir", 0.30))))
    upc = C.math_node(nt, "MAXIMUM", up, 0.0)
    base = C.math_node(nt, "ADD", float(opt.get("dtop", 120)),
                       C.math_node(nt, "MULTIPLY", C.math_node(nt, "POWER", upc, 1.4), float(opt.get("dbot", 1250)) - float(opt.get("dtop", 120))))
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.noise_dimensions = "4D"; n2.inputs["Scale"].default_value = 7.0
    n2.inputs["Detail"].default_value = 2.0
    nt.links.new(tc.outputs["Object"], n2.inputs["Vector"]); nt.links.new(tv.outputs[0], n2.inputs["W"])
    fine = C.math_node(nt, "ADD", 1.0, C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", n2.outputs["Fac"], 0.5), 0.12))
    thin = C.value_node(nt, "thin", 1.0)
    d = C.math_node(nt, "MULTIPLY", C.math_node(nt, "MULTIPLY", base, fine), thin.outputs[0])
    # black film above u' < black: a sharp step down to ~12 nm
    blk = C.value_node(nt, "black", -1.0)
    step = C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", up, blk.outputs[0]), 60.0, clamp=True)   # 0 inside black
    return C.math_node(nt, "ADD", 12.0, C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", d, 12.0), step))


def hole_mask(nt):
    """1 where the film still exists; a hole of radius hole_r around (hx, hz)"""
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    dx = C.math_node(nt, "SUBTRACT", sep.outputs["X"], float(opt.get("hx", 0.25)))
    dz = C.math_node(nt, "SUBTRACT", sep.outputs["Z"], float(opt.get("hz", 0.30)))
    r = C.math_node(nt, "SQRT", C.math_node(nt, "ADD", C.math_node(nt, "MULTIPLY", dx, dx), C.math_node(nt, "MULTIPLY", dz, dz)))
    hr = C.value_node(nt, "hole_r", -1.0)
    return C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", r, hr.outputs[0]), 400.0, clamp=True)


if light == "sodium":
    m = C.sodium_material("soap", thickness, float(opt.get("nagain", 3.2)))
else:
    m, _ = C.film_material_clear("soap", thickness)
nt = m.node_tree; out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
surf = out.inputs["Surface"].links[0].from_socket
mix = nt.nodes.new("ShaderNodeMixShader"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
nt.links.new(hole_mask(nt), mix.inputs["Fac"]); nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(surf, mix.inputs[2])
nt.links.new(mix.outputs[0], out.inputs["Surface"])

# film: a plane in x-z facing -y
bm = bmesh.new()
vs = [bm.verts.new((sx * FW / 2, 0, sz * FH / 2)) for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
bm.faces.new(vs); me = bpy.data.meshes.new("film"); bm.to_mesh(me); bm.free()
film = bpy.data.objects.new("film", me); film.data.materials.append(m); scene.collection.objects.link(film)

# wire frame: a rounded-rectangle tube
wire = C.metal("wire", (0.36, 0.37, 0.40, 1), 0.3)
cu = bpy.data.curves.new("frame", "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = float(opt.get("wire", 0.014)); cu.bevel_resolution = 6
sp = cu.splines.new("POLY"); rc = 0.05; pts = []
for cx, cz, a0 in ((FW / 2 - rc, FH / 2 - rc, 0), (-FW / 2 + rc, FH / 2 - rc, 90), (-FW / 2 + rc, -FH / 2 + rc, 180), (FW / 2 - rc, -FH / 2 + rc, 270)):
    for k in range(9):
        a = math.radians(a0 + 90 * k / 8); pts.append((cx + rc * math.cos(a), 0, cz + rc * math.sin(a)))
sp.points.add(len(pts) - 1)
for i, p in enumerate(pts): sp.points[i].co = (*p, 1)
sp.use_cyclic_u = True
fo = bpy.data.objects.new("frame", cu); fo.data.materials.append(wire); scene.collection.objects.link(fo)
# a handle below the frame
h = bpy.data.curves.new("handle", "CURVE"); h.dimensions = "3D"; h.bevel_depth = 0.02; h.bevel_resolution = 6
hs = h.splines.new("POLY"); hs.points.add(1); hs.points[0].co = (0, 0, -FH / 2, 1); hs.points[1].co = (0, 0, -FH / 2 - 1.5, 1)
ho = bpy.data.objects.new("handle", h); ho.data.materials.append(wire); scene.collection.objects.link(ho)

S = {k: sched(k, d) for k, d in (("thin", 1.0), ("black", -1.0), ("hole", -1.0), ("time", 0.0), ("dist", 3.4),
                                   ("yaw", 0.0), ("pitch", 4.0), ("tx", 0.0), ("tz", 0.0), ("lens", 50.0))}
fps = float(opt.get("fps", 24)); flow = float(opt.get("flow", 0.035))
V = lambda name: nt.nodes[name].outputs[0]


def per_frame(f):
    V("time").default_value = S["time"](f) if "time" in opt else f / fps * flow
    V("thin").default_value = S["thin"](f); V("black").default_value = S["black"](f); V("hole_r").default_value = S["hole"](f)
    cam.aim((S["tx"](f), 0, S["tz"](f)), S["dist"](f), S["yaw"](f), S["pitch"](f), S["lens"](f))
    return {"thin": round(S["thin"](f), 4), "black": round(S["black"](f), 4), "hole": round(S["hole"](f), 4)}


C.render_frames(scene, range(first, last + 1), opt["out"], per_frame, opt.get("meta"))
print("DONE flatfilm", opt["out"])
