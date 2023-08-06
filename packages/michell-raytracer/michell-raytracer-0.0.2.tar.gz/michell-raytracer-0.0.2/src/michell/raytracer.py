"""Raytracer object implemention allowing to set render
with different parameters."""

import numpy as np
from progressbar import ProgressBar
import michell.utils as u

class Raytracer:
    """Describes raytracer object implementing rendering functionality of package."""
    def __init__(
        self,
        scene,
        resolution,
        limits,
        linear=False,
        curvature=1.5
    ):
        self.scene = scene
        self.resolution = resolution
        (self.step, self.border) = limits
        self.linear = linear
        self.curvature = curvature
        self.points, self.directions = self.scene.camera.calc_starting_vectors(resolution)
        self.distances = self.scene.sdf_matrix(self.points)
        self.steps = u.count_steps(self.distances, self.step)

    def nonlinear_rays(self):
        """Returns matrices of new origins and directions (m, n, 3)
        based on old ones and matrix of steps (m, n, 1). Uses relativistic
        geodesic paths for rays."""
        areal_velocity = np.cross(self.points, self.directions)
        square_areal_velocity = np.einsum('...i,...i', areal_velocity, areal_velocity)
        self.points = self.points + self.directions * self.steps
        accel = (
            u.matrix_normalization(self.points) *
            (
                -abs(self.curvature) * square_areal_velocity /
                np.power(np.einsum('...i,...i', self.points, self.points), 2.5)
            )[:,:,np.newaxis,]
        )
        self.directions = u.matrix_normalization(self.directions + accel * self.steps)

    def linear_rays(self):
        """Returns matrices of new origins and directions (m, n, 3)
        based on old ones and matrix of steps (m, n, 1). Uses linear
        paths for rays."""
        self.points = self.points + self.directions * self.steps

    def rays_march(self):
        """Returns matrices of new origins and directions (m, n, 3)
        based on old ones and matrix of steps (m, n, 1). Choses
        between linear and non linear methods of calculating
        ray paths."""
        if self.linear:
            return self.linear_rays()
        return self.nonlinear_rays()

    def calc_image(self):
        """Returns matrix of resulting image (m, n, 3)."""
        image = np.zeros(self.points.shape)
        for entity in self.scene.entities:
            entity_mask = (
                np.ones(self.points.shape) -
                np.abs(np.sign(np.round(entity.sdf_matrix(self.points),5)))
            )
            entity_colors = entity.get_colors(self.points)
            image += entity_colors * entity_mask
        return image

    def render(self):
        """Starts rendering process. Shows progress bar. Returns resulting image after finishing
        of rendering process."""
        progress = u.count_progress(self.distances)

        print("Calculating paths of rays:")
        progress_bar = ProgressBar(maxval = 100).start()
        max_iterations = 6 * self.border / self.step
        iterations = 0
        while (progress < 100) and iterations < max_iterations:
            self.rays_march()
            self.distances = self.scene.sdf_matrix(self.points)
            self.steps = u.count_steps(self.distances, self.step)
            progress = u.count_progress(self.distances)
            progress_bar.update(int(progress))
            iterations += 1
        progress_bar.update(100)
        progress_bar.finish()
        print("Wait. Scene are being painted...")
        return self.calc_image()
