"""Useful classes for scene modeling."""

import numpy as np
import michell.utils as u

class BaseEntity:
    """Base class for every entity on scene."""

    def __init__(
        self,
        position
    ):
        self.position = position

    def get_position(self):
        """Returns position of entity."""
        return self.position

    def set_position(self, position):
        """Sets new position of entity."""
        self.position = position

    def move_position(self, direction):
        """Moves entity by direction."""
        self.position += direction

    def sdf_matrix(self, matrix_of_points):
        """Returns matrix of distances (m, n, 1) from points of
        matrix of points (m, n, 3) to entity."""
        return np.abs(matrix_of_points - self.position)

class Camera(BaseEntity):
    """Describes camera using for scene rendering. Has four settings.
    position - 3-vector describing its place on scene.
    look_at - 3-vector describing point it should look at on scene.
    top - 3-vector describing direction where top of camera is placed.
          shouldn't be parallel to look_at.
    fov - field of view presented in radians."""

    def __init__(
        self,
        position,
        look_at,
        top,
        fov
    ):
        super().__init__(position)
        self.look_at = look_at
        self.top = top
        self.fov = fov
        self.directions = np.array([])
        self.origins = np.array([])

    def calc_starting_vectors(self, resolution):
        """Returns two matrices of starting points and directions."""
        width, height = resolution
        orientation = self.look_at - self.position
        screen_normal = u.vector_normalization(orientation) * 0.1
        vector_u = u.vector_normalization(np.cross(screen_normal, self.top))
        vector_v = u.vector_normalization(np.cross(vector_u, screen_normal))
        pixel = 2*np.tan(self.fov / 2) * 0.1 / height
        scanline_start = (
            self.position +
            screen_normal +
            (width / 2) *
            pixel *
            vector_u +
            (height / 2) *
            pixel *
            vector_v
        )
        points = np.fromfunction(
            lambda i, j, _: scanline_start - pixel * vector_v * i - pixel * vector_u * j,
            (height, width, 3)
        )
        directions = u.matrix_normalization(points - self.position)
        return points, directions

class TexturedEntity(BaseEntity):
    """Describes class of entities with textures."""

    def __init__(
        self,
        position,
        texture
    ):
        super().__init__(position)
        self.texture = texture

    def map_entity(self, point):
        """Converts points to 2d coordinates of entities surface"""

    def get_colors(self, points):
        """Returns matrix of colors (m, n, 3) using color function."""
        return np.apply_along_axis(lambda x: self.texture.get_color(self.map_entity(x)), 2, points) 

class Sphere(TexturedEntity):
    """Describes sphere with its position and radius."""

    def __init__(
        self,
        position,
        radius,
        texture,
        inverse=False
    ):
        super().__init__(position, texture)
        self.radius = radius
        self.inverse = inverse

    def get_radius(self):
        """Returns radius of sphere."""
        return self.radius

    def set_radius(self, radius):
        """Sets radius of sphere."""
        self.radius = radius

    def increase_radius(self, increase):
        """Increases radius of sphere."""
        self.radius += increase

    def sdf_matrix(self, matrix_of_points):
        """Returns matrix of distances (m, n, 1) from matrix of points to sphere's surface."""
        sign = 1
        if self.inverse:
            sign = -1
        return sign * (
            np.apply_over_axes(
                lambda  x, a: np.linalg.norm(x, axis=a),
                matrix_of_points - self.position,
                [2]
            ) - self.radius
        )

    def map_entity(self, point):
        p_x, p_y, p_z = point
        p_r = np.sqrt(p_x**2 + p_y**2 + p_z**2)
        p_theta = np.arccos(p_y / p_r) / np.pi
        p_phi = np.arctan2(p_x, p_z)
        if p_phi < 0:
            p_phi = 2 * np.pi + p_phi
        p_phi = p_phi / (2 * np.pi)
        return p_theta, p_phi       

class Ring(TexturedEntity):
    """Describes ring with its position two radiuses and normal vector."""

    def __init__(
        self,
        position,
        radiuses,
        normal_vector,
        texture
    ):
        super().__init__(position, texture)
        self.small_radius, self.big_radius = radiuses
        self.normal_vector = normal_vector

    def get_big_radius(self):
        """Returns big radius of ring."""
        return self.big_radius

    def set_big_radius(self, big_radius):
        """Sets big radius of ring."""
        self.big_radius = big_radius

    def increase_big_radius(self, increase):
        """Increases big radius of ring."""
        self.big_radius += increase

    def get_small_radius(self):
        """Returns small radius of ring."""
        return self.small_radius

    def set_small_radius(self, small_radius):
        """Sets small radius of ring."""
        self.small_radius = small_radius

    def increase_small_radius(self, increase):
        """Increases small radius of ring."""
        self.small_radius += increase

    def get_normal_vector(self):
        """Returns normal vector of ring."""
        return self.normal_vector

    def set_normal_vector(self, normal_vector):
        """Sets new normal vector of ring."""
        self.normal_vector = normal_vector

    def move_normal_vector(self, direction):
        """Move normal vector of ring by direction."""
        self.normal_vector += direction

    def sdf_matrix(self, matrix_of_points):
        """Returns matrix of distances (m,n,1) from matrix of points to ring's surface."""
        distance_vectors = u.projections_on_plane(
            matrix_of_points - self.position,
            self.normal_vector
        )
        distances = np.apply_over_axes(
            lambda  x, a: np.linalg.norm(x, axis=a),
            distance_vectors, [2]
        )
        over = (
            (distances >= self.small_radius) &
            (distances <= self.big_radius) * 1
        ) * np.abs(np.linalg.norm(matrix_of_points - distance_vectors, axis=2))[:,:,np.newaxis,]
        inner_points = u.matrix_normalization(distance_vectors) * self.small_radius
        below = (
            (distances < self.small_radius) * 1 *
            np.abs(np.linalg.norm(matrix_of_points - inner_points, axis=2))[:,:,np.newaxis,]
        )
        outer_points = u.matrix_normalization(distance_vectors) * self.big_radius
        upper = (
            (distances > self.big_radius) * 1 *
            np.abs(np.linalg.norm(matrix_of_points - outer_points, axis=2))[:,:,np.newaxis,]
        )
        return over + below + upper

    def map_entity(self, point):
        p_x, _, p_z = point
        radius = (
            (np.linalg.norm(point) - self.small_radius) %
            (self.big_radius - self.small_radius)
        ) / (self.big_radius - self.small_radius)
        p_phi = np.arctan2(p_x, p_z)
        if p_phi < 0:
            p_phi = 2 * np.pi + p_phi
        p_phi = p_phi / (2 * np.pi)
        return radius, p_phi


class Scene:
    """Describes scene to render."""
    def __init__(
        self,
        camera
    ):
        self.camera = camera
        self.entities = []

    def push_entity(self, entity):
        """Pushes new entity to the list."""
        self.entities.append(entity)

    def pop_entity(self):
        """Pops out last entity from the list."""
        entity = self.entities[-1]
        del self.entities[-1]
        return entity

    def sdf_matrix(self, points):
        """Returns matrix of minimal distances (m, n, 1) to objects' surfaces from
        points of input matrix (m, n, 3)."""
        distances = np.ones((points.shape[0],points.shape[1], 1)) * np.inf
        for entity in self.entities:
            new_distances = entity.sdf_matrix(points)
            distances = np.minimum(distances, new_distances)
        return distances
