"""The catenoid between two rings: pull the rings apart, the waist narrows, past h/R ~ 1.3255 the film snaps.

  blender -b -P catenoid.py -- out=DIR/f%05d.png first=0 last=599 [KEY=VALUE ...]

Ring radius R = 1, axis vertical. Separation schedule hr=F:V,F:V,... (h/R per output frame, smoothstep between keys).
While a catenoid exists, the film is the stable (fat) branch a cosh(z/a), a from cosh x = (2R/h) x, x = h/(2a)
(the same equations as docs/catenoid.js). From frame `snap` on, the rings stop at h/R = hr_final (> 1.3255) and the
film follows the axisymmetric curvature flow r_t = r_zz/(1+r_z^2) - 1/r (docs/catenoid.js, Profile.step) until
the neck pinches (r < 0.02 R), paced by visual progress over `flow` frames; then the two halves flatten into disks
over `split` frames. Per-frame data (h/R, film area over two-disk area, phase, ring screen positions) goes to meta=PATH.
"""
import bpy, bmesh, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

opt = C.args()
first, last = int(opt.get("first", 0)), int(opt.get("last", 599))
fps = float(opt.get("fps", 24))

# ---- catenoid mathematics (as in docs/catenoid.js) ----
XSTAR = 1.2
for _ in range(60):
    XSTAR -= (math.tanh(XSTAR) - 1 / XSTAR) / (1 / math.cosh(XSTAR) ** 2 + 1 / XSTAR ** 2)
HR_MAX = 2 * XSTAR / math.cosh(XSTAR)


def stable_a(h, R=1.0):
    k = 2 * R / h; f = lambda x: math.cosh(x) - k * x
    if f(XSTAR) > 0: return None
    lo, hi = 1e-9, XSTAR
    for _ in range(100):
        m = (lo + hi) / 2
        if f(lo) * f(m) <= 0: hi = m
        else: lo = m
    return h / (2 * (lo + hi) / 2)


def cat_area(a, h):
    x = h / (2 * a); return math.pi * a * a * (2 * x + math.sinh(2 * x))


M = int(opt.get("M", 161))


def profile_area(z, r):
    return float(np.sum(math.pi * (r[1:] + r[:-1]) * np.hypot(np.diff(z), np.diff(r))))


def flow_run(h, a0):
    """curvature flow from the stretched last catenoid; returns a list of profiles up to the pinch"""
    z = np.linspace(-h / 2, h / 2, M); r = a0 * np.cosh(z / a0 * (h_snap / h))      # stretched: the rings moved apart
    r[0] = r[-1] = 1.0
    dz = h / (M - 1); dt = 0.2 * dz * dz; out = [r.copy()]
    for it in range(400000):
        rz = (r[2:] - r[:-2]) / (2 * dz); rzz = (r[2:] - 2 * r[1:-1] + r[:-2]) / dz ** 2
        r[1:-1] = r[1:-1] + dt * (rzz / (1 + rz * rz) - 1 / np.maximum(r[1:-1], 1e-4))
        if it % 25 == 0: out.append(r.copy())
        if r.min() < 0.02: out.append(r.copy()); break
    return z, out


def sched(key, default):
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


HR = sched("hr", 0.8)
snap = int(opt.get("snap", 10 ** 9)); flow_frames = int(opt.get("flow", 72)); split = int(opt.get("split", 8))
hr_final = float(opt.get("hr_final", 1.335))
h_snap = HR(snap - 1) if snap < 10 ** 9 else None
if snap < 10 ** 9:
    a_snap = stable_a(h_snap) or stable_a(HR_MAX - 1e-6)
    zf, flows = flow_run(hr_final, a_snap)
    # pace the flow by visual change: cumulative max |dr| between stored profiles
    dch = np.array([0.0] + [float(np.abs(flows[i] - flows[i - 1]).max()) + 1e-6 for i in range(1, len(flows))])
    prog = np.cumsum(dch); prog /= prog[-1]
    print(f"flow: {len(flows)} stored profiles to the pinch; h/R final {hr_final}; snap from h/R {h_snap:.5f}")

# ---- scene ----
scene = C.setup(opt)
light = opt.get("light", "studio")
dp, bg = C.softbox_world(scene, float(opt.get("soft", 2.2)), float(opt.get("lo", 0.45)), float(opt.get("hi", 0.75)))
cam = C.Cam(scene, dp, light)


def thickness(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    hv = C.value_node(nt, "half_h", 0.5)
    u = C.math_node(nt, "DIVIDE", C.math_node(nt, "SUBTRACT", hv.outputs[0], sep.outputs["Z"]),
                    C.math_node(nt, "MULTIPLY", hv.outputs[0], 2.0), clamp=True)                     # 0 top ring .. 1 bottom
    base = C.math_node(nt, "ADD", float(opt.get("dtop", 280)), C.math_node(nt, "MULTIPLY", C.math_node(nt, "POWER", u, 1.3), float(opt.get("dbot", 820)) - float(opt.get("dtop", 280))))
    tv = C.value_node(nt, "time")
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.noise_dimensions = "4D"; nz.inputs["Scale"].default_value = 1.6
    nz.inputs["Detail"].default_value = 3.0; nz.inputs["Distortion"].default_value = 0.8
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"]); nt.links.new(tv.outputs[0], nz.inputs["W"])
    mod = C.math_node(nt, "ADD", 1.0, C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", nz.outputs["Fac"], 0.5), 0.5))
    return C.math_node(nt, "MULTIPLY", base, mod)


soap, _ = (C.film_material_clear if light == "studio" else C.film_material)("soap", thickness)
disk_m, _ = (C.film_material_clear if light == "studio" else C.film_material)("disk", lambda nt: C.math_node(nt, "ADD", 0.0, float(opt.get("ddisk", 520))))
wire = C.metal("wire", (0.55, 0.56, 0.60, 1), 0.25)
me = bpy.data.meshes.new("film"); film = bpy.data.objects.new("film", me); film.data.materials.append(soap); scene.collection.objects.link(film)
rings = []
for k in range(2):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0 + 0.016, minor_radius=float(opt.get("wire", 0.022)), major_segments=192, minor_segments=20)
    o = bpy.context.active_object
    for p in o.data.polygons: p.use_smooth = True
    o.data.materials.append(wire); rings.append(o)
S_SEG = int(opt.get("seg", 160))


def set_surface(parts):
    """parts: list of (z array, r array, material index); builds one revolved mesh"""
    bm = bmesh.new()
    for z, r in parts:
        ringsv = []
        for i in range(len(z)):
            row = [bm.verts.new((r[i] * math.cos(2 * math.pi * j / S_SEG), r[i] * math.sin(2 * math.pi * j / S_SEG), z[i])) for j in range(S_SEG)]
            ringsv.append(row)
        for i in range(len(z) - 1):
            for j in range(S_SEG):
                j1 = (j + 1) % S_SEG
                try: bm.faces.new((ringsv[i][j], ringsv[i][j1], ringsv[i + 1][j1], ringsv[i + 1][j]))
                except ValueError: pass
    bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True


nt = soap.node_tree
tnode, hnode = nt.nodes["time"], nt.nodes["half_h"]
dist, pitch, yaw0, yawr, lens = float(opt.get("dist", 6.4)), float(opt.get("pitch", 14)), float(opt.get("yaw", 0)), float(opt.get("yawrate", 0.05)), float(opt.get("lens", 50))
DISTS = sched("dist", dist); PITCHS = sched("pitch", pitch)


def per_frame(f):
    tnode.outputs[0].default_value = f / fps * float(opt.get("flowrate", 0.05))
    if f < snap:
        h = HR(f); a = stable_a(h) or stable_a(HR_MAX - 1e-9)
        nz = int(opt.get("nz", 121)); z = np.linspace(-h / 2, h / 2, nz); r = a * np.cosh(z / a)
        set_surface([(z, r)]); phase = "catenoid"; area = cat_area(a, h)
    else:
        h = hr_final; s = f - snap
        if s < flow_frames:
            u = (s / flow_frames) ** 1.0; i = int(np.searchsorted(prog, u)); i = min(i, len(flows) - 1)
            r = flows[i]; set_surface([(zf, r)]); phase = "flow"; area = profile_area(zf, r)
        else:
            r = flows[-1]; i0 = int(np.argmin(r)); t = min(1.0, (s - flow_frames + 1) / max(1, split)); t = 1 - (1 - t) ** 2
            zu = zf[i0:] + t * (h / 2 - zf[i0:]); zl = zf[:i0 + 1] + t * (-h / 2 - zf[:i0 + 1])
            set_surface([(zu, r[i0:]), (zl, r[:i0 + 1])]); phase = "split" if t < 1 else "disks"
            area = profile_area(zu, r[i0:]) + profile_area(zl, r[:i0 + 1])
    hnode.outputs[0].default_value = h / 2
    rings[0].location = (0, 0, h / 2); rings[1].location = (0, 0, -h / 2)
    cam.aim((0, 0, 0), DISTS(f), yaw0 + yawr * f, PITCHS(f), lens)
    return {"hr": round(h, 5), "area_ratio": round(area / (2 * math.pi), 5), "phase": phase,
            "top": cam.project(scene, [(0, 0, h / 2)])[0], "bottom": cam.project(scene, [(0, 0, -h / 2)])[0],
            "right": cam.project(scene, [(1.05, 0, 0)])[0]}


C.render_frames(scene, range(first, last + 1), opt["out"], per_frame, opt.get("meta"))
print("DONE catenoid", opt["out"], "HR_MAX", HR_MAX)
