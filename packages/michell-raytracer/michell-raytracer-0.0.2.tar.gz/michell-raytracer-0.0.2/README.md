# Michell's Raytracer

Simple relativistic nonlinear raytracer named after John Michell,
the first man to think about existence of black holes (he called
them "dark stars").

It uses Schwarzschild's metric to implement calculations of rays
paths near black hole.

Here are example of how to use this package:

```
import matplotlib.pyplot as plt
import numpy as np
from michell.raytracer import Raytracer
from michell.scene import Camera, Sphere, Ring, Scene
from michell.textures import ColorTexture, ImageTexture

blackhole_texture = ColorTexture(np.array([0, 0, 0]))
background_texture = ImageTexture("space.jpg")
ring_texture = ImageTexture("rings.jpeg")

blackhole = Sphere(np.array([0, 0, 0]), 1, blackhole_texture)
background = Sphere(np.array([0, 0, 0]), 8, background_texture, inverse=True)
ring = Ring(np.array([0, 0, 0]), (1.5, 4), np.array([0, 1, 0]), ring_texture)

camera = Camera(np.array([-7,0.5,0]), np.array([0, 0, 0]), np.array([0, 1, 0]), np.pi / 3)

scene = Scene(camera)

scene.push_entity(blackhole)
scene.push_entity(ring)
scene.push_entity(background)

raytracer = Raytracer(scene, (300, 200), (0.16, 8), curvature=3)

plt.imsave('output.png', raytracer.render())
```

Firstly we create textures for scene entities. Then we create scene entities.
Next step is to create camera and scene. The last one before making raytracer
is to push entities created earlier to scene's list of entities. And finally
we create raytracer for rendering the scene we created few lines ago.

**REMEMBER** to put sphere in <0, 0, 0> to correctly render black hole.