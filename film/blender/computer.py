"""The soap computer: pins between two glass plates, film walls relaxing to a locally shortest network.

  blender -b -P computer.py -- traj=A.json[,B.json] out=DIR/f%05d.png first=0 last=239 [KEY=VALUE ...]

Each trajectory is a recorded relaxation of one measured dip (film/sims/steiner_traj.mjs: the same seeded dip that
tools/success.mjs scores). Rig k sits at x = offs[k] and starts forming at frame starts[k]; it is lifted out of the
soap over `lift` frames (the walls grow down from the top plate) and relaxes over dur[k] frames, paced by visual
progress. Walls are vertical thin films between the plates; their thickness (nm) drains toward the bottom plate and
is stirred by slow 4D noise. Optional 120-degree arcs at the settled junctions glow during frames arcs=F0:F1.
Per-frame overlay data (screen positions of pins, junctions, network length) goes to meta=PATH.
"""
import bpy, bmesh, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

opt = C.args()
H = float(opt.get("H", 0.42))                     # plate gap (pin circumradius 1)
trajs = [json.load(open(p)) for p in opt["traj"].split(",")]
K = len(trajs)
offs = [float(x) for x in opt.get("offs", ",".join(str(2.5 * (k - (K - 1) / 2)) for k in range(K))).split(",")]
starts = [int(x) for x in opt.get("starts", ",".join("0" for _ in trajs)).split(",")]
durs = [int(x) for x in opt.get("dur", ",".join("240" for _ in trajs)).split(",")]
lift = int(opt.get("lift", 30))
arcs = [int(x) for x in opt["arcs"].split(":")] if "arcs" in opt else None
first, last = int(opt.get("first", 0)), int(opt.get("last", 239))
fps = float(opt.get("fps", 24))

scene = C.setup(opt)
dp, bg = C.softbox_world(scene, float(opt.get("soft", 2.4)), float(opt.get("lo", 0.5)), float(opt.get("hi", 0.7)))
cam = C.Cam(scene, dp, opt.get("light", "studio"))
col = scene.collection


# ---- trajectory pacing: frame -> (step index, fraction) by cumulative visual change ----
def pacing(tr):
    fr = tr["frames"]; c = [0.0]
    for k in range(1, len(fr)):
        a, b = fr[k - 1], fr[k]
        if len(a["jx"]) == len(b["jx"]) and a["edges"] == b["edges"]:
            d = max([math.hypot(p["x"] - q["x"], p["y"] - q["y"]) for p, q in zip(a["jx"], b["jx"])] or [0.0])
        else:
            d = 0.06
        c.append(c[-1] + min(d, 0.2) + 1e-5)
    return [x / c[-1] for x in c]


def state(tr, prog, u):
    """network at visual progress u in [0,1]: list of segment endpoints (x, y) and junction points"""
    import bisect
    fr = tr["frames"]; k = min(len(fr) - 1, bisect.bisect_left(prog, u))
    a = fr[max(0, k - 1)]; b = fr[k]
    if k > 0 and len(a["jx"]) == len(b["jx"]) and a["edges"] == b["edges"] and prog[k] > prog[k - 1]:
        s = (u - prog[k - 1]) / (prog[k] - prog[k - 1])
        jx = [{"x": p["x"] + s * (q["x"] - p["x"]), "y": p["y"] + s * (q["y"] - p["y"])} for p, q in zip(a["jx"], b["jx"])]
        edges, L = b["edges"], a["L"] + s * (b["L"] - a["L"])
    else:
        jx, edges, L = b["jx"], b["edges"], b["L"]
    n = len(tr["pins"]); P = lambda i: tr["pins"][i] if i < n else jx[i - n]
    return [(P(e[0]), P(e[1])) for e in edges], jx, edges, L


def ease(t):
    t = min(1.0, max(0.0, t)); return 1 - (1 - t) ** 1.6


# ---- materials ----
def wall_thickness(nt):
    tc = nt.nodes.new("ShaderNodeTexCoord"); sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    u = C.math_node(nt, "SUBTRACT", 1.0, C.math_node(nt, "DIVIDE", sep.outputs["Z"], H, clamp=True))   # 0 top .. 1 bottom
    base = C.math_node(nt, "ADD", C.math_node(nt, "MULTIPLY", C.math_node(nt, "POWER", u, 1.3), float(opt.get("dbot", 760)) - float(opt.get("dtop", 330))), float(opt.get("dtop", 330)))
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.noise_dimensions = "4D"; nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 3.0; nz.inputs["Distortion"].default_value = 0.6
    tv = C.value_node(nt, "time"); nt.links.new(tv.outputs[0], nz.inputs["W"])
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (1.0, 1.0, 2.6)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs[0], nz.inputs["Vector"])
    mod = C.math_node(nt, "ADD", 1.0, C.math_node(nt, "MULTIPLY", C.math_node(nt, "SUBTRACT", nz.outputs["Fac"], 0.5), 0.55))
    return C.math_node(nt, "MULTIPLY", base, mod)


soap, _ = (C.film_material_clear if opt.get("light", "studio") == "studio" else C.film_material)("soap", wall_thickness)
glass = C.faint_glass("glass", float(opt.get("glassrefl", 0.004)), float(opt.get("glassfres", 0.06)))
copper = C.metal("copper", (0.72, 0.30, 0.16, 1), 0.3)
water, _ = C.principled("border", **{"Base Color": (1, 1, 1, 1), "Roughness": 0.0, "IOR": 1.33, "Transmission Weight": 1.0})
arcm = bpy.data.materials.new("arc"); arcm.use_nodes = True
an = arcm.node_tree; [an.nodes.remove(x) for x in list(an.nodes) if x.type != "OUTPUT_MATERIAL"]
em = an.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.86, 0.45, 1)
an.links.new(em.outputs[0], next(x for x in an.nodes if x.type == "OUTPUT_MATERIAL").inputs["Surface"])


def box(name, cx, cy, cz, sx, sy, sz, mat):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co.x = cx + v.co.x * sx; v.co.y = cy + v.co.y * sy; v.co.z = cz + v.co.z * sz
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(mat); col.objects.link(ob); return ob


def cylinder(name, x, y, z0, z1, r, mat, seg=32):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=z1 - z0)
    for v in bm.verts: v.co.x += x; v.co.y += y; v.co.z += (z0 + z1) / 2
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(mat); col.objects.link(ob); return ob


rigs = []
pt = float(opt.get("plate", 0.035))
for k, tr in enumerate(trajs):
    ox = offs[k]
    xs = [p["x"] for p in tr["pins"]]; ys = [p["y"] for p in tr["pins"]]
    W = max(xs) - min(xs) + 0.7; D = max(ys) - min(ys) + 0.7
    if opt.get("plates", "1") == "1":
        box(f"bottom{k}", ox, 0, -pt / 2, W, D, pt, glass)
        box(f"top{k}", ox, 0, H + pt / 2, W, D, pt, glass)
    for i, p in enumerate(tr["pins"]):
        cylinder(f"pin{k}_{i}", ox + p["x"], p["y"], -0.01, H + 0.01, float(opt.get("pinr", 0.03)), copper)
    me = bpy.data.meshes.new(f"walls{k}"); ob = bpy.data.objects.new(f"walls{k}", me); ob.data.materials.append(soap); col.objects.link(ob)
    bm_ = bpy.data.meshes.new(f"borders{k}"); bo = bpy.data.objects.new(f"borders{k}", bm_); bo.data.materials.append(water); col.objects.link(bo)
    am = bpy.data.meshes.new(f"arcs{k}"); ao = bpy.data.objects.new(f"arcs{k}", am); ao.data.materials.append(arcm); col.objects.link(ao)
    rigs.append(dict(tr=tr, prog=pacing(tr), ox=ox, walls=me, borders=bm_, arcs=am))


def set_walls(rig, segs, jx, zb):
    verts, faces = [], []
    ox = rig["ox"]
    for a, b in segs:
        L = math.hypot(b["x"] - a["x"], b["y"] - a["y"])
        if L < 1e-6 or zb >= H - 1e-4: continue
        i = len(verts)
        verts += [(ox + a["x"], a["y"], zb), (ox + b["x"], b["y"], zb), (ox + b["x"], b["y"], H), (ox + a["x"], a["y"], H)]
        faces.append((i, i + 1, i + 2, i + 3))
    me = rig["walls"]; me.clear_geometry(); me.from_pydata(verts, [], faces); me.update()
    # Plateau borders: thin water columns where three walls meet
    bm = bmesh.new()
    if zb < H - 1e-3:
        for J in jx:
            g = bmesh.ops.create_cone(bm, cap_ends=False, segments=12, radius1=0.006, radius2=0.006, depth=H - zb)
            for v in g["verts"]: v.co.x += ox + J["x"]; v.co.y += J["y"]; v.co.z += (H + zb) / 2
    bm.to_mesh(rig["borders"]); bm.free()


def set_arcs(rig, jx, edges, strength):
    tr = rig["tr"]; n = len(tr["pins"]); ox = rig["ox"]; bm = bmesh.new()
    if strength > 0:
        P = lambda i: tr["pins"][i] if i < n else jx[i - n]
        for j, J in enumerate(jx):
            nb = [e[1] if e[0] == n + j else e[0] for e in edges if n + j in e]
            if len(nb) != 3: continue
            ang = sorted(math.atan2(P(v)["y"] - J["y"], P(v)["x"] - J["x"]) for v in nb)
            for t in range(3):
                a0 = ang[t]; a1 = ang[(t + 1) % 3] + (2 * math.pi if t == 2 else 0)
                r, w, z = 0.11, 0.008, H + pt + 0.003
                m = 24; ring = []
                for s in range(m + 1):
                    a = a0 + 0.12 + (a1 - a0 - 0.24) * s / m
                    ring.append((bm.verts.new((ox + J["x"] + (r - w) * math.cos(a), J["y"] + (r - w) * math.sin(a), z)),
                                 bm.verts.new((ox + J["x"] + (r + w) * math.cos(a), J["y"] + (r + w) * math.sin(a), z))))
                for s in range(m): bm.faces.new((ring[s][0], ring[s + 1][0], ring[s + 1][1], ring[s][1]))
    bm.to_mesh(rig["arcs"]); bm.free()
    em.inputs["Strength"].default_value = 6.0 * strength


tnode = soap.node_tree.nodes["time"]
cx = float(opt.get("cx", 0.0)); DIST = C.sched(opt, "dist", 4.6); pitch = float(opt.get("pitch", 52))
yaw0, yawr = float(opt.get("yaw", -18)), float(opt.get("yawrate", 0.04))
lens = float(opt.get("lens", 50)); tz = float(opt.get("tz", H / 2))


def per_frame(f):
    tnode.outputs[0].default_value = f / fps * float(opt.get("flow", 0.05))
    cam.aim((cx, 0, tz), DIST(f), yaw0 + yawr * f, pitch, lens)
    info = {"rigs": []}
    for k, rig in enumerate(rigs):
        tau = (f - starts[k]) / durs[k]
        if f < starts[k]:
            set_walls(rig, [], [], H); set_arcs(rig, [], [], 0); info["rigs"].append(None); continue
        lf = min(1.0, (f - starts[k]) / max(1, lift)); zb = H * (1 - (1 - (1 - lf) ** 2))
        segs, jx, edges, L = state(rig["tr"], rig["prog"], ease(tau))
        set_walls(rig, segs, jx, zb)
        a = 0.0
        if arcs and arcs[0] <= f <= arcs[1]:
            a = min(1.0, (f - arcs[0]) / 12, (arcs[1] - f) / 12)
        set_arcs(rig, jx, edges, a)
        n = len(rig["tr"]["pins"])
        info["rigs"].append(dict(L=round(L, 5), settled=tau >= 1, arcs=round(a, 3),
                                 pins=cam.project(scene, [(rig["ox"] + p["x"], p["y"], H + pt) for p in rig["tr"]["pins"]]),
                                 jx=cam.project(scene, [(rig["ox"] + J["x"], J["y"], H + pt) for J in jx]),
                                 centre=cam.project(scene, [(rig["ox"], 0, H + pt)])[0]))
    return info


C.render_frames(scene, range(first, last + 1), opt["out"], per_frame, opt.get("meta"))
print("DONE computer", opt["out"])
