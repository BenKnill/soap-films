# Blender renders of the relaxed films

1. `node blender/export_meshes.js`: relaxes the tetrahedron and cube films with the page's own minimiser (`docs/surface.js`). It writes `blender/tetra.json` and `blender/cube.json`, each with vertices, triangles, a film-thickness field in nm, the wires, the triple lines and the junctions.
2. `Blender -b -P blender/render_frame.py -- cube out.png 160` renders it in Cycles on the Metal GPU.
   - The film is a Principled BSDF with IOR 1.0 (air on both sides) and a thin film of IOR 1.33. The "thick" vertex attribute drives the film's thickness, and Cycles computes the interference colours.
   - Lighting follows soap-film photography: a black background behind the film and a large soft light behind the camera.
   - Environment variables: `YAW`, `PITCH`, `DIST` and `SOFTBOX` (the light's strength).

A 1280×720 frame at 160 samples takes about 25 s on this Mac.
