import openride as ride

from dataclasses import dataclass
from typing import Optional

import time
import numpy as np



@dataclass
class Hero:
    bounding_box:ride.BoundingBox = ride.BoundingBox(ride.Point(0,0,0.8), rotation=ride.Rotation(), size=ride.Size(2.3,0.9,0.8))
    max_velocity:float = 50.0

    def __post_init__(self):
        self.velocity:float = 0.0
        self.acceleration:float = 0.0
        self.steering:float = 0.0


    def update(self, dt:float):

        steering = self.steering / abs(self.velocity + 1)

        x, y, yaw, v = rear_axle_kinematic_model(
            self.bounding_box.position.x, self.bounding_box.position.y, self.bounding_box.rotation.yaw,
            self.velocity, dt, self.acceleration, steering, self.bounding_box.size.x*2, 0.5,
        )

        self.bounding_box.position.x = x
        self.bounding_box.position.y = y
        self.bounding_box.rotation.yaw = yaw
        self.velocity = min((v, self.max_velocity))


    def on_key_press(self, key_event:ride.KeyEvent):

        if key_event.key == 'w' or key_event.key == 'Up':
            self.acceleration = 25.0
        if key_event.key == 's' or key_event.key == 'Down':
            self.acceleration = -25.0

        if key_event.key == 'a' or key_event.key == 'Left':
            self.steering = 4.0
        if key_event.key == 'd' or key_event.key == 'Right':
            self.steering = -4.0


    def on_key_release(self, key_event:ride.KeyEvent):
        if key_event.key in ['w','s','Up','Down']:
            self.acceleration = 0.0
        if key_event.key in ['a','d','Left','Right']:
            self.steering = 0.0


    def collides(self, colliders:ride.BoundingBoxCollection) -> Optional[int]:
        for index, collider in enumerate(colliders):
            if ride.bird_eye_view_distance(self.bounding_box, collider) == 0.0:
                return index


    def respawn(self):
        self.bounding_box = ride.BoundingBox(ride.Point(0,0,0.8), rotation=ride.Rotation(), size=ride.Size(2.3,0.9,0.8))
        self.velocity = 0.0
        self.acceleration = 0.0
        self.steering = 0.0


def rear_axle_kinematic_model(x0, y0, yaw0, v0, dt, acceleration, wheel_angle, wheelbase, drag):
    x = x0 + (v0 * np.cos(yaw0) * dt)
    y = y0 + (v0 * np.sin(yaw0) * dt)
    v = v0 + (acceleration * dt)
    v -= v0 * drag * dt
    yaw = yaw0 + (v0 * np.tan(wheel_angle) / wheelbase * dt)
    return x, y, yaw, v


@dataclass
class City:
    size:float = 200
    building_width:float = 25
    road_width:float = 15

    def __post_init__(self):
        self.buildings = ride.BoundingBoxCollection()
        self.traffic_cones = ride.BoundingBoxCollection()
        self.generate_buildings()
        self.generate_traffic_cones()


    def generate_buildings(self, fill_ratio:float=0.9):
        for x in range(-self.size, self.size, self.building_width+self.road_width):
            for y in range(-self.size, self.size, self.building_width+self.road_width):
                if np.random.random() > fill_ratio: continue
                height = np.random.random()*15+5
                building = ride.BoundingBox(
                    ride.Point(x,y,height), 
                    size=ride.Size(self.building_width/2,self.building_width/2,height)
                )
                self.buildings.append(building)
        offset = self.size % (self.building_width + self.road_width) + (self.building_width + self.road_width)/2
        self.buildings = self.buildings.transform(ride.Transform(ride.Point(0, offset)))


    def spawn_traffic_cone(self):
        x = np.random.random()*2*self.size - self.size
        y = np.random.random()*2*self.size - self.size
        box = ride.BoundingBox(ride.Point(x, y, 0.5), size=ride.Size(0.5,0.5,0.5))
        for building in self.buildings:
            if ride.bird_eye_view_distance(box, building) == 0.0:
                self.spawn_traffic_cone()
        self.traffic_cones.append(box)


    def generate_traffic_cones(self, density:float=0.01):
        amount = int(density * self.size ** 2)
        for _ in range(amount):
            self.spawn_traffic_cone()


def main():

    hero = Hero()
    city = City(size=220)

    viewer = ride.Viewer(mouse_camera_interactions=False)
    viewer.draw_grid(extent=city.size+40)
    viewer.hud.toggle_fps_count()
    viewer.interactor.set_callback(ride.Event.KeyPressEvent, hero.on_key_press)
    viewer.interactor.set_callback(ride.Event.KeyReleaseEvent, hero.on_key_release)

    score = 0

    t = time.time()
    while True:
        dt = time.time() - t
        t = time.time()

        if hero.collides(city.buildings):
            hero.respawn()
            viewer.camera.follow(hero.bounding_box, spring=0)
            score -= 5

        collision_index = hero.collides(city.traffic_cones)
        if collision_index:
            city.traffic_cones.pop(collision_index)
            city.spawn_traffic_cone()
            score += 1

        score = max((score, 0))

        hero.update(dt)
        viewer.camera.follow(hero.bounding_box, spring=0.8)

        viewer.draw_model(ride.SubCategory.Car, hero.bounding_box, color=(0.7,0.6,0.35))
        [viewer.draw_bounding_box(building, color=(0.5, 0.5, 0.6)) for building in city.buildings if viewer.camera.is_in_front(building.position)]
        [viewer.draw_model(ride.Category.TrafficCone, cone, color=(0.9, 0.2, 0.1), number_polygons=200) for cone in city.traffic_cones if viewer.camera.is_in_front(cone.position)]

        viewer.hud.add('score', score)
        viewer.update()


if __name__ == "__main__":
    main()