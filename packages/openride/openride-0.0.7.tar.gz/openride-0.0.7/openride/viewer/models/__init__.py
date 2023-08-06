from openride.core.categories import Category, SubCategory
from openride.core.rotation import Rotation

from typing import List, Union

import glob
import os
import numpy as np

FILEPATH = os.path.dirname(os.path.abspath(__file__))



DEFAULT_MODELS = {
    Category.Vehicle: f"{FILEPATH}/cars/Aston_martin.stl",
    Category.Pedestrian: f"{FILEPATH}/pedestrians/default_male.stl",
    Category.Cyclist: f"{FILEPATH}/cyclists/bicycle2.stl",
    Category.TrafficCone: f"{FILEPATH}/traffic_cones/cone.stl",

    SubCategory.Car: f"{FILEPATH}/cars/Aston_martin.stl",
    SubCategory.Van: f"{FILEPATH}/vans/volkswagen_transporter.stl",
    SubCategory.Bus: f"{FILEPATH}/buses/ShortSchoolBus.stl",
    SubCategory.Truck: f"{FILEPATH}/trucks/Truck2.stl",
    SubCategory.Motorcycle: f"{FILEPATH}/motorcycles/kawaski.stl",
}



DIRECTORIES = {
    Category.Vehicle: f"{FILEPATH}/cars",
    Category.Pedestrian: f"{FILEPATH}/pedestrians",
    Category.Cyclist: f"{FILEPATH}/cyclists",
    Category.TrafficCone: f"{FILEPATH}/traffic_cones",

    SubCategory.Car: f"{FILEPATH}/cars",
    SubCategory.Van: f"{FILEPATH}/vans",
    SubCategory.Bus: f"{FILEPATH}/buses",
    SubCategory.Truck: f"{FILEPATH}/trucks",
    SubCategory.Motorcycle: f"{FILEPATH}/motorcycles",
}



def get_model_files(category:Union[Category, SubCategory]) -> List[str]:
    directory = DIRECTORIES.get(category)
    if not directory: return []
    return glob.glob(f"{directory}/*")



MODEL_ROTATIONS = {

    'jeep_renegate.stl': Rotation(yaw=np.pi/2),
    'Aston_martin.stl': Rotation(yaw=np.pi),
    'chevrolet_camaro_ss.stl': Rotation(yaw=np.pi/2),
    'chevrolet_corvette_zr1.stl': Rotation(yaw=np.pi/2),
    'dodge_challenger.stl': Rotation(yaw=np.pi/2),
    'mitsubishi_lancer_evolution.stl': Rotation(yaw=np.pi/2),
    'nissan_skyline_gtr.stl': Rotation(yaw=np.pi/2),
    'shelby_mustang_gt350r.stl': Rotation(yaw=np.pi/2),
    'tesla_model_3.stl': Rotation(yaw=np.pi/2),
    'volkswagen_golf_gti.stl': Rotation(yaw=np.pi/2),
    'chopper_reduziert.stl': Rotation(roll=np.pi/2),
    'ducati.stl': Rotation(yaw=np.pi/2),
    'kawaski.stl': Rotation(yaw=np.pi/2),

    'volkswagen_transporter.stl': Rotation(yaw=np.pi/2),
    'vw_transporter2.stl': Rotation(yaw=np.pi/2),

    'Fire_Truck.stl': Rotation(),
    'trashtruck.stl': Rotation(),
    'Truck2.stl': Rotation(),

    'ShortSchoolBus.stl': Rotation(),

    'default_male.stl': Rotation(roll=np.pi/4, pitch=0, yaw=np.pi/2),
    'sophie_walk.stl': Rotation(roll=np.pi/2, yaw=np.pi/2),
    'tyler_walk.stl': Rotation(roll=np.pi/2, yaw=np.pi/2),
    'woman_stand.stl': Rotation(yaw=np.pi/2),
    'default_female.stl': Rotation(yaw=np.pi/2),
    'vahlen_stand.stl': Rotation(yaw=np.pi/2),

    'bicycle.stl': Rotation(),
    'bicycle2.stl': Rotation(),

}