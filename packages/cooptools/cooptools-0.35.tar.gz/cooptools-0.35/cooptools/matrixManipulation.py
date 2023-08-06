import numpy as np

def rotation_unit_vector(axis: np.array):
    return axis / (axis ** 2).sum() ** 0.5

def translationMatrix(dx=0, dy=0, dz=0):
    """ Return matrix for translation along vector (dx, dy, dz). """
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                    [0, 0, 0, 1]])

def scaleMatrix(sx=0, sy=0, sz=0):
    """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])

def rotateXMatrix(radians):
    """ Return matrix for rotating about the x-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c, s, 0],
                     [0, -s, c, 0],
                     [0, 0, 0, 1]])

def rotateYMatrix(radians):
    """ Return matrix for rotating about the y-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, 0, -s, 0],
                     [0, 1, 0, 0],
                     [s, 0, c, 0],
                     [0, 0, 0, 1]])

def rotateZMatrix(radians):
    """ Return matrix for rotating about the z-axis by 'radians' radians """
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c, s, 0, 0],
                     [-s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def rotateAroundAxis(rotationPoint, rotationAxis, radians):
    """http://www.fastgraph.com/makegames/3drotation/"""
    c = np.cos(radians)
    s = np.sin(radians)
    t = 1 - np.cos(radians)
    u = rotationAxis[0]
    v = rotationAxis[1]
    w = rotationAxis[2]


    ''' Build the transposes into the matrix'''
    x=rotationPoint[0]
    y=rotationPoint[1]
    z= rotationPoint[2]
    calculated_matrix = np.array([[u**2 + (v**2 + w**2) * c, u*v*t-w*s,              u*w*t+v*s,              (x*(v**2 + w**2) - u*(y*v + z*w))*t + (y*w-z*v)*s],
                                 [u*v*t + w*s,              v**2 + (u**2 + w**2)*c, v*w*t-u*s,              (y*(u**2 + w**2) - v*(x*u + z*w))*t + (z*u-x*w)*s],
                                 [u*w*t - v*s,              v*w*t + u*s,            w**2 + (u**2 + v**2)*c, (z*(u**2 + v**2) - w*(x*u + y*v))*t + (x*v-y*u)*s],
                                 [0,                        0,                      0,                      1]])

    return calculated_matrix

def get_grid_rotation_matrix(rotation_axis_x, rotation_axis_z, x_rot_rads, z_rot_rads):
    # Rot Z
    orientation = np.array([0, 0, 1])
    ruv = rotation_unit_vector(orientation)
    matrixz = rotateAroundAxis((rotation_axis_x, rotation_axis_z, 0), ruv, z_rot_rads)

    # Rot X
    orientation = np.array([1, 0, 0])
    ruv = rotation_unit_vector(orientation)
    matrixx = rotateAroundAxis((rotation_axis_x, rotation_axis_z, 0), ruv,
                                  x_rot_rads)
    matrix = matrixx.dot(matrixz)
    return matrix



    # translationM = translationMatrix(-rotationPoint[0], -rotationPoint[1], -rotationPoint[2])
    # print (f"translationM: \n{translationM}")
    # # return translationM
    # translationMInv = translationMatrix(rotationPoint[0], rotationPoint[1], rotationPoint[2])
    #
    #
    # matrix =  np.array([[t * u ** 2 + c,    t * u * v - s * w,  t * u * w + s * v,  0],
    #                     [t * u * v + s * w, t * v**2 + c,       t*v*w-s*u,          0],
    #                     [t*u*w - s*v,       t*v*w+s*u,          t*w**2+c,           0],
    #                     [0,                 0,                  0,                  1]])
    #
    #
    # # return matrix
    # with np.printoptions(precision=3, suppress=True):
    #     print(f"Rotation \n{matrix}")
    #     print(matrix.dot(translationM))
    #     finalTransform = translationMInv.dot(matrix.dot(translationM))
    #     # finalTransform = translationM.dot(matrix).dot(translationMInv)
    #     print(f"Final Transform: \n{finalTransform}")
    #
    #     print(f"clc: {calculated_matrix}")
    #     print(f"mat: {finalTransform}")
    #
    # return finalTransform


def rotateAroundPoint( point, rotationVector):

    translationM = translationMatrix(-point[0], -point[1], -point[2])


    translationMInv = translationMatrix(point[0], point[1], point[2])
    rX = rotateXMatrix(rotationVector[0])
    rY = rotateYMatrix(rotationVector[1])
    rZ = rotateZMatrix(rotationVector[2])

    return translationM.dot(rX.dot(rY.dot(rZ.dot(translationMInv))))

def scaleAroundPoint(point, scalarVector):
    translationM = translationMatrix(-point[0], -point[1], -point[2])
    translationMInv = translationMatrix(point[0], point[1], point[2])
    scaleM = scaleMatrix(*scalarVector)
    matrix = translationMInv.dot(scaleM.dot(translationM))

    with np.printoptions(precision=3, suppress=True):
        print(f"Scalar \n{matrix}")
    return matrix


