import math
from numpy import ones, vstack
from numpy.linalg import lstsq


def cap_value(number, cap_number):
    """Cap a number to a certain threshold
            
            Args:
                number (float): Input number
                cap_number (float): Max number
            
            Returns:
                float: Capped number
            """
    if number > cap_number:
        return cap_number
    else:
        return number


# TODO maybe put all these into a class?


def calculate_distance_two_points(point_1, point_2):
    """Calculates distance between two given points
    
    Args:
        point_1 (tuple): Tuple with coordinates for point 1
        point_2 (tuple): Tuple with coordinates for point 2
    
    Returns:
        float: Distance as a float
    """
    # TODO maybe move to utils?
    x1 = point_1[0]
    y1 = point_1[1]
    x2 = point_2[0]
    y2 = point_2[1]

    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def train_linear_two_points(point_1, point_2):
    """Trains a linear model based on two points
    
    Args:
        point_1 (tuple): Tuple with coordinates for point 1
        point_2 (tuple): Tuple with coordinates for point 2
    
    Returns:
        dict: Dict with slope and intercept
    """

    points = [point_1, point_2]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords, ones(len(x_coords))]).T
    m, c = lstsq(A, y_coords)[0]

    output_dict = {"slope": m, "intercept": c}

    return output_dict


def apply_linear_model(value, model_dict):
    """Apply a linear model to a value
    
    Args:
        value (float): Input value
        model_dict (dict): Dict with slope and intercept
    
    Returns:
        float: Output value
    """
    output_value = model_dict["intercept"] + model_dict["slope"] * value

    return output_value

