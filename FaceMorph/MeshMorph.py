import eos
import numpy as np

def main():
    
    sharepath = "C:\\Users\\Mikael\\Documents\\GitHub\\Hackstreet-Boys\\FaceMorph\\"
    path = "C:\\Users\\Mikael\\Documents\\GitHub\\Hackstreet-Boys\\"
    landmarks = read_pts(path + "FaceAlign\\facepts.pts")
    image_width = 1280 # Make sure to adjust these when using your own images!
    image_height = 720

    model = eos.morphablemodel.load_model(sharepath + "share\\sfm_shape_3448.bin")
    blendshapes = eos.morphablemodel.load_blendshapes(sharepath + "share\\expression_blendshapes_3448.bin")
    # Create a MorphableModel with expressions from the loaded neutral model and blendshapes:
    morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
                                                                        color_model=eos.morphablemodel.PcaModel(),
                                                                        vertex_definitions=None,
                                                                        texture_coordinates=model.get_texture_coordinates())
    landmark_mapper = eos.core.LandmarkMapper(sharepath + "share\\ibug_to_sfm.txt")
    edge_topology = eos.morphablemodel.load_edge_topology(sharepath + "share\\sfm_3448_edge_topology.json")
    contour_landmarks = eos.fitting.ContourLandmarks.load(sharepath + "share\\ibug_to_sfm.txt")
    model_contour = eos.fitting.ModelContour.load(sharepath + "share\\sfm_model_contours.json")

    (mesh, pose, shape_coeffs, blendshape_coeffs) = eos.fitting.fit_shape_and_pose(morphablemodel_with_expressions,
        landmarks, landmark_mapper, image_width, image_height, edge_topology, contour_landmarks, model_contour)

    # Now you can use your favourite plotting/rendering library to display the fitted mesh, using the rendering
    # parameters in the "pose" variable.

    # Or for example extract the texture map, like this:
    # import cv2
    # image = cv2.imread("../bin/data/image_0010.png")
    # isomap = eos.render.extract_texture(mesh, pose, image)
    
    p = path + "FaceMeshOutput\\FaceMesh.obj"
    eos.core.write_obj(mesh,p)

def read_pts(filename):
    """A helper function to read the 68 ibug landmarks from a .pts file."""
    lines = open(filename).read().splitlines()
    lines = lines[3:71]

    landmarks = []
    ibug_index = 1  # count from 1 to 68 for all ibug landmarks
    for l in lines:
        coords = l.split()
        landmarks.append(eos.core.Landmark(str(ibug_index), [float(coords[0]), float(coords[1])]))
        ibug_index = ibug_index + 1

    return landmarks

if __name__ == "__main__":
    main()