import basilisk as bsk
import glm
import random

engine = bsk.Engine()
scene = bsk.Scene(engine)
# scene.sky = None

# Load meshes
sphere_mesh = bsk.Mesh('models/sphere.obj')
monkey_mesh = bsk.Mesh('models/monkey.obj')

# Load images
floor_albedo = bsk.Image('textures/floor_albedo.png')
floor_normal = bsk.Image('textures/floor_normal.png')
mud_albedo   = bsk.Image('textures/mud.png')
mud_normal   = bsk.Image('textures/mud_normal.png')
cloth_albedo = bsk.Image('textures/cloth_albedo.png')
cloth_normal = bsk.Image('textures/cloth_normal.png')
landscape = bsk.Image('textures/landscape.png')

# Load materials
floor     = bsk.Material(texture=floor_albedo, normal=floor_normal, roughness=.25, specular=2, clearcoat=1, anisotropic=.25)
mud       = bsk.Material(texture=mud_albedo, normal=mud_normal, roughness=.5, specular=2, clearcoat=.5)
cloth     = bsk.Material(texture=cloth_albedo, normal=cloth_normal, roughness=.8, specular=1.5, clearcoat=.8, clearcoat_gloss=.6)
emissive  = bsk.Material(emissive_color=(500, 500, 500))
black     = bsk.Material(color=(20, 20, 20))
landscape = bsk.Material(texture=landscape)

# Add nodes to the scene
node = bsk.Node(mesh=sphere_mesh, rotation=(0, 3.14, 0), material=cloth)
scene.add(node)
scene.add(bsk.Node(position=(0, -3, 0), scale=(10, .25, 10), material=floor))

# Set the shader to one with a more agressive gradient
blinnPhongShader = bsk.Shader(engine, frag='shader/blinnPhong.frag')
scene.shader = blinnPhongShader

# Set the lights (just looks better with this shader)
scene.light_handler.directional_lights = scene.light_handler.directional_lights[:-1]
scene.light_handler.write(scene.shader)

# Color Quantization tools
dither_shader = bsk.Shader(engine, 'shader/frame.vert', 'shader/dither.frag')
dither_renderer = bsk.Framebuffer(engine)
low_res = bsk.Framebuffer(engine, scale=.2, linear_filter=False)
dither_fbo = bsk.Framebuffer(engine, dither_shader, scale=.2, linear_filter=False)


# r = 50
# for i in range(1000):
#     scene.add(bsk.Node(position=[random.randrange(-r, r) for i in range(3)], rotation=[random.randrange(5, r) for i in range(3)], scale=(.1, .1, .1), material=emissive))

while engine.running:
    scene.update()

    dither_shader.write('textureSize', glm.vec2(engine.win_size) * .2)
    dither_renderer.bind(scene.frame.output_buffer.texture, 'screenTexture', 0)
    dither_renderer.render(low_res, auto_bind=False)
    low_res.render(dither_fbo)
    dither_fbo.render()

    engine.update(render=False)