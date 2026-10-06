"""Shared Cycles setup for the episode-4 film shots (run inside Blender 5.x).

Soap-film photography lighting: the world is black ahead of the camera and a big soft light sits behind it, so every
part of a film reflects something bright and the background stays black. Films are Principled BSDFs with IOR 1.0
(air on both sides) and a thin film of IOR 1.33; Cycles computes the interference colours itself from the film
thickness in nanometres. The sodium-lamp look is the same reflection with one wavelength (589.3 nm), computed from
the Airy reflectance in shader nodes, because Cycles' thin film is evaluated in RGB.
"""
import bpy, math, os, sys, json

N_WATER, NA_NM = 1.33, 589.3
NA_COLOR = (1.0, 0.55, 0.035)          # linear RGB of the sodium D line on screen
R_FRESNEL = (N_WATER - 1) / (N_WATER + 1)
F_AIRY = 4 * R_FRESNEL ** 2 / (1 - R_FRESNEL ** 2) ** 2


def args():
    """KEY=VALUE options after '--'"""
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return dict(a.split("=", 1) for a in argv if "=" in a)


def sched(opt, key, default):
    """option 'F:V,F:V,...' -> smoothstep-eased piecewise-linear function of the frame; a plain number is constant"""
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


def setup(opt):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    rw, rh = map(int, opt.get("res", "1920x1080").split("x"))
    scene.render.engine = "CYCLES"; cy = scene.cycles
    cy.samples = int(opt.get("samples", 64)); cy.use_denoising = opt.get("denoise", "1") == "1"
    if cy.use_denoising:
        cy.denoiser = "OPENIMAGEDENOISE"
        try: cy.denoising_use_gpu = opt.get("dngpu", "1") == "1"
        except Exception as e: print("no GPU denoise option:", e)
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = float(opt.get("adapt", 0.01))
    cy.max_bounces = 32; cy.transparent_max_bounces = 32; cy.transmission_bounces = 24; cy.glossy_bounces = 8
    cy.diffuse_bounces = 2; cy.caustics_reflective = False; cy.caustics_refractive = False
    cy.sample_clamp_indirect = 20.0
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("METAL", "CUDA"):
        try:
            prefs.compute_device_type = kind; prefs.get_devices()
        except Exception:
            continue
        gpus = [d for d in prefs.devices if d.type == kind]
        if gpus:
            for d in prefs.devices: d.use = d.type == kind
            cy.device = "GPU"; print("Cycles device:", kind, [d.name for d in gpus]); break
    else:
        print("GPU not available: rendering on the CPU")
    scene.render.resolution_x, scene.render.resolution_y = rw, rh
    scene.render.resolution_percentage = int(opt.get("pct", 100))
    scene.view_settings.view_transform = "AgX"; scene.view_settings.look = opt.get("look", "AgX - Medium High Contrast")
    scene.view_settings.exposure = float(opt.get("exposure", 0.0))
    scene.render.image_settings.file_format = "PNG"; scene.render.image_settings.color_depth = "8"
    scene.render.use_persistent_data = True
    scene.render.film_transparent = False
    return scene


def softbox_world(scene, strength=1.6, lo=0.45, hi=0.75):
    """World light: bright for directions pointing back past the camera, black elsewhere (mode 'full'); or, in mode
    'below', bright below the horizon except in a cone around the camera's own view, so vertical films seen from
    above (whose mirror directions point down) catch light, while horizontal glass (mirroring upward) and the view
    straight through it stay dark. Cam.aim updates the direction vectors."""
    world = bpy.data.worlds.new("w"); scene.world = world; world.use_nodes = True; nt = world.node_tree
    bg = nt.nodes["Background"]; tc = nt.nodes.new("ShaderNodeTexCoord")
    dp = nt.nodes.new("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"
    nt.links.new(tc.outputs["Generated"], dp.inputs[0])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = lo; ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = hi; ramp.color_ramp.elements[1].color = (1.0, 0.98, 0.95, 1)
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = -1; mr.inputs["From Max"].default_value = 1
    nt.links.new(dp.outputs["Value"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    # mode 'below': brightness = [dir . fwd < cone] * [dir.z < horizon]
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    cone = math_node(nt, "MULTIPLY", math_node(nt, "SUBTRACT", 0.86, dp.outputs["Value"]), 5.0, clamp=True)
    below = math_node(nt, "MULTIPLY", math_node(nt, "SUBTRACT", 0.12, sep.outputs["Z"]), 4.0, clamp=True)
    lit = math_node(nt, "MULTIPLY", cone, below)
    lp = nt.nodes.new("ShaderNodeLightPath")
    studio = math_node(nt, "MULTIPLY", math_node(nt, "SUBTRACT", 1.0, lp.outputs["Is Camera Ray"]),
                       math_node(nt, "ADD", 0.75, math_node(nt, "MULTIPLY", sep.outputs["Z"], 0.25)))
    lit = math_node(nt, "ADD", math_node(nt, "MULTIPLY", lit, value_node(nt, "below_w", 1.0).outputs[0]),
                    math_node(nt, "MULTIPLY", studio, value_node(nt, "studio_w", 0.0).outputs[0]))
    sw = value_node(nt, "below_mode", 0.0)
    mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "FLOAT"
    nt.links.new(sw.outputs[0], mix.inputs["Factor"]); nt.links.new(ramp.outputs["Color"], mix.inputs["A"])
    nt.links.new(lit, mix.inputs["B"])
    warm = nt.nodes.new("ShaderNodeCombineColor")
    for i, c in enumerate((1.0, 0.98, 0.95)): nt.links.new(math_node(nt, "MULTIPLY", mix.outputs["Result"], c), warm.inputs[i])
    nt.links.new(warm.outputs[0], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = strength
    return dp, bg


class Cam:
    def __init__(self, scene, dp, mode="full"):
        self.cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); scene.collection.objects.link(self.cam)
        scene.camera = self.cam; self.cam.data.sensor_width = 36; self.dp = dp; self.mode = mode
        self.cam.data.clip_start = 0.01

    def aim(self, target, dist, yaw_deg, pitch_deg, lens=50.0, roll_deg=0.0):
        yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
        c = self.cam; c.data.lens = lens
        c.location = (target[0] + dist * math.cos(pitch) * math.sin(yaw), target[1] - dist * math.cos(pitch) * math.cos(yaw),
                      target[2] + dist * math.sin(pitch))
        fwd = [target[i] - c.location[i] for i in range(3)]; L = math.sqrt(sum(f * f for f in fwd)); fwd = [f / L for f in fwd]
        # rotation: look along fwd with world z up
        import mathutils
        q = mathutils.Vector(fwd).to_track_quat("-Z", "Y")
        c.rotation_mode = "QUATERNION"; c.rotation_quaternion = q
        if roll_deg:
            c.rotation_quaternion = q @ mathutils.Quaternion((0, 0, 1), math.radians(roll_deg))
        if self.mode == "horizontal":
            h = math.hypot(fwd[0], fwd[1]); self.dp.inputs[1].default_value = (-fwd[0] / h, -fwd[1] / h, 0.0)
        elif self.mode in ("below", "studio"):
            self.dp.inputs[1].default_value = tuple(fwd)
            wn = bpy.context.scene.world.node_tree.nodes
            wn["below_mode"].outputs[0].default_value = 1.0
            wn["below_w"].outputs[0].default_value = 1.0 if self.mode == "below" else 0.0
            wn["studio_w"].outputs[0].default_value = 1.0 if self.mode == "studio" else 0.0
        else:
            self.dp.inputs[1].default_value = (-fwd[0], -fwd[1], -fwd[2])     # bright behind the camera

    def project(self, scene, pts):
        from bpy_extras.object_utils import world_to_camera_view
        bpy.context.view_layer.update()
        rw, rh = scene.render.resolution_x, scene.render.resolution_y
        out = []
        for p in pts:
            v = world_to_camera_view(scene, self.cam, __import__("mathutils").Vector(p))
            out.append([round(v.x * rw, 2), round((1 - v.y) * rh, 2)])
        return out


def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m, b


def metal(name="wire", color=(0.62, 0.64, 0.68, 1), rough=0.22):
    return principled(name, **{"Base Color": color, "Metallic": 1.0, "Roughness": rough})[0]


def film_material(name, thickness_socket_builder, transmissive=True):
    """A thin-film soap material; thickness_socket_builder(nt) returns an output socket giving thickness in nm."""
    m, b = principled(name, **{"Base Color": (1, 1, 1, 1) if transmissive else (0, 0, 0, 1), "Metallic": 0.0,
                               "Roughness": 0.0, "IOR": 1.0, "Transmission Weight": 1.0 if transmissive else 0.0,
                               "Thin Film IOR": N_WATER})
    nt = m.node_tree
    nt.links.new(thickness_socket_builder(nt), b.inputs["Thin Film Thickness"])
    return m, b


def film_material_clear(name, thickness_socket_builder):
    """Thin film as transparency plus Cycles' thin-film specular on an opaque IOR-1.0 base (the reflection of a
    free film in air). Rays passing through stay camera rays, so the studio world stays black behind the film."""
    m, b = principled(name, **{"Base Color": (0, 0, 0, 1), "Metallic": 0.0, "Roughness": 0.0, "IOR": 1.0,
                               "Transmission Weight": 0.0, "Thin Film IOR": N_WATER})
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    nt.links.new(thickness_socket_builder(nt), b.inputs["Thin Film Thickness"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(b.outputs[0], add.inputs[0]); nt.links.new(tr.outputs[0], add.inputs[1]); nt.links.new(add.outputs[0], out.inputs["Surface"])
    return m, b


def faint_glass(name, refl=0.02, fres=0.08):
    """Glass that stays see-through for camera rays: transparency plus a weak Fresnel-weighted mirror."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    lw = nt.nodes.new("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.25
    g = nt.nodes.new("ShaderNodeBsdfGlossy"); g.inputs["Roughness"].default_value = 0.0
    k = math_node(nt, "ADD", refl, math_node(nt, "MULTIPLY", lw.outputs["Fresnel"], fres))
    cc = nt.nodes.new("ShaderNodeCombineColor")
    for i in range(3): nt.links.new(k, cc.inputs[i])
    nt.links.new(cc.outputs[0], g.inputs["Color"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(g.outputs[0], add.inputs[0]); nt.links.new(tr.outputs[0], add.inputs[1]); nt.links.new(add.outputs[0], out.inputs["Surface"])
    return m


def math_node(nt, op, a, b=None, clamp=False):
    n = nt.nodes.new("ShaderNodeMath"); n.operation = op; n.use_clamp = clamp
    for i, x in enumerate((a, b)):
        if x is None: continue
        if isinstance(x, (int, float)): n.inputs[i].default_value = x
        else: nt.links.new(x, n.inputs[i])
    return n.outputs[0]


def sodium_material(name, thickness_socket_builder, gain=1.6):
    """One-wavelength (589.3 nm) Airy reflectance of a water film, with the angle inside the film, as a glossy colour
    plus a transparent pass-through: bright and dark stripes, one per lambda/(2n) ~ 221 nm of thickness."""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    d = thickness_socket_builder(nt)
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    dot = nt.nodes.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    nt.links.new(geo.outputs["Incoming"], dot.inputs[0]); nt.links.new(geo.outputs["Normal"], dot.inputs[1])
    ci = math_node(nt, "ABSOLUTE", dot.outputs["Value"])
    s2 = math_node(nt, "SUBTRACT", 1.0, math_node(nt, "MULTIPLY", ci, ci))                      # sin^2 outside
    ct = math_node(nt, "SQRT", math_node(nt, "SUBTRACT", 1.0, math_node(nt, "DIVIDE", s2, N_WATER ** 2)))
    ph = math_node(nt, "MULTIPLY", math_node(nt, "MULTIPLY", d, ct), 2 * math.pi * N_WATER / NA_NM)
    s = math_node(nt, "SINE", ph); ss = math_node(nt, "MULTIPLY", s, s); fs = math_node(nt, "MULTIPLY", ss, F_AIRY)
    R = math_node(nt, "DIVIDE", fs, math_node(nt, "ADD", fs, 1.0))
    Rn = math_node(nt, "MULTIPLY", R, gain)              # raw reflectance (at most ~8 %), like the physical film
    rgb = nt.nodes.new("ShaderNodeCombineColor")
    for i, c in enumerate(NA_COLOR): nt.links.new(math_node(nt, "MULTIPLY", Rn, c), rgb.inputs[i])
    gl = nt.nodes.new("ShaderNodeBsdfGlossy"); gl.inputs["Roughness"].default_value = 0.0
    nt.links.new(rgb.outputs[0], gl.inputs["Color"])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    add = nt.nodes.new("ShaderNodeAddShader"); nt.links.new(gl.outputs[0], add.inputs[0]); nt.links.new(tr.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs["Surface"])
    return m


def value_node(nt, name, v=0.0):
    n = nt.nodes.new("ShaderNodeValue"); n.name = name; n.label = name; n.outputs[0].default_value = v
    return n


def render_frames(scene, frames, out_pattern, per_frame, meta_path=None):
    """per_frame(f) sets the scene for output frame f and may return a dict of overlay metadata.
    Existing non-empty frames are skipped (resumable)."""
    meta = {}
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
    import time
    for f in frames:
        path = out_pattern % f
        t_set = time.time(); info = per_frame(f); t_set = time.time() - t_set
        if info is not None: meta[str(f)] = info
        if os.path.exists(path) and os.path.getsize(path) > 0:
            continue
        t0 = time.time(); scene.render.filepath = path; bpy.ops.render.render(write_still=True)
        print(f"FRAME {f} {time.time() - t0:.1f}s (setup {t_set:.1f}s) -> {path}", flush=True)
        if meta_path and f % 24 == 0: json.dump(meta, open(meta_path, "w"))
    if meta_path: json.dump(meta, open(meta_path, "w"))
