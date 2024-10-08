# Arthur Gim
# 7/9/2024

# This is a program about generating load, axial, shear, and moment graphs based on external forces
# acted on an overhanging beam. An overhanging beam is one that is statically determinate
# and rests on two supports, a roller and a pin, located anywhere along the length of the beam.
# The graphs are generated based on the external point forces,
# moments, and distributed loads.

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy import integrate


# Pre: Accepts nothing. Only accepts either the string "metric" or the string "imperial"
# Post: This prompts the user to input what unit system they will be using
def unit_system_type():
    while True:
        unit_system = input('Please input the unit system you need '
                            '(Enter "metric" or "imperial"): ').strip().lower()
        if unit_system not in ["metric", "imperial"]:
            print("Invalid input. Please try again.")
        else:
            return unit_system


# Pre: Accepts nothing. Only accepts positive numbers and will reprompt the user if
#      they enter anything else
# Post: This prompts the user to input the length of the beam and then returns the length as a
# #     float value.
def beam_length():
    print()
    while True:
        try:
            inputted_length = float(input("Please input the length of the beam: "))
            if inputted_length <= 0:
                print("Invalid input. Length must be a positive number.")
            else:
                return inputted_length
        except ValueError:
            print("Invalid input. Please input only a number.")


# Pre: This takes in inputted_length
# Post: This gets information about the location of the supports.
#       The user can choose where to put the roller and the pin support.
#       The user will be repromted if the support is out of the range of the beam
#       or if they put in something that is not a number.
def support_locations_input(inputted_length):
    support_locations = []
    while True:
        try:
            roller_position = float(input("Please input the location of the roller support: "))
            if roller_position < 0 or roller_position > inputted_length:
                print("Invalid input. The roller must be along the beam.")
            else:
                support_locations.append(roller_position)
                break
        except ValueError:
            print("Invalid input. Please input only a number.")

    while True:
        try:
            pin_position = float(input("Please input the location of the pin support: "))
            if pin_position < 0 or pin_position > inputted_length:
                print("Invalid input. The pin must be along the beam.")
            else:
                support_locations.append(pin_position)
                break
        except ValueError:
            print("Invalid input. Please input only a number.")

    return support_locations


# Pre: Takes in inputtedLength to check if the inputted force is within bounds. 
#      It only accepts numbers and reprompts the user if they input
#      anything else.
# Post: This prompts the user to input the location of the horizontal point force and the direction
#       and magnitude. After that is done, it reprompts the user to add another force.
#       To end the input, the user can type 'done' and move on to the next prompt.
def point_horizontal_forces(inputted_length):
    print()
    h_forces = []  # This is an empty list to store the forces and locations the user inputs
    print("Please input the location of a horizontal point force "
          "or type 'done' if there are no more: ")
    while True:
        location_input = input("Enter the location of the force: ")
        if location_input.lower() == "done":
            break
        try:
            horizontal_force_location = float(location_input)
            if not (0 <= horizontal_force_location <= inputted_length):
                print("The location is not in the range of the beam. Please Try again.")
                continue
        except ValueError:
            print("Invalid input. Please input only a number.")      
            continue
                      
        try:
            print("For the direction, enter a positive number if the force is to the right "
                  "and a negative number if the force is to the left")
            horizontal_force_magnitude = float(input("Enter the magnitude and "
                                                     "direction of the force: "))
        except ValueError:
            print("Invalid input. Please input only a number.")
            continue

        horizontal_force_info = {"location": horizontal_force_location,
                                 "magnitude": horizontal_force_magnitude}
        # horizontalForce is a dictionary that stores the information for the location
        # and magnitude of a given force.
        h_forces.append(horizontal_force_info)
        
    return h_forces


# Pre: Takes in inputtedLength to check if the inputted force is within bounds.
#      It only accepts numbers and reprompts the user if they input
#      anything else.
# Post: This prompts the user to input the location of the vertical point force and the direction
#       and magnitude. After that is done, it reprompts the user to add another force.
#       To end the input, the user can type 'done' and move on to the next prompt.
def point_vertical_forces(inputted_length):
    print()
    v_forces = []  # This is an empty list to store the forces and locations the user inputs
    print("Please input the location of a vertical point force "
          "or type 'done' if there are no more: ")
    while True:
        location_input = input("Enter the location of the force: ")
        if location_input.lower() == "done":
            break
        try:
            vertical_force_location = float(location_input)
            if not (0 <= vertical_force_location <= inputted_length):
                print("The location is not in the range of the beam. Please Try again.")
                continue
        except ValueError:
            print("Invalid input. Please input only a number.")      
            continue
                      
        try:
            print("For the direction, enter a positive number if the force is upwards"
                  " and a negative number if the force is downwards")
            vertical_force_magnitude = float(input("Enter the magnitude and " 
                                                   "direction of the force: "))
        except ValueError:
            print("Invalid input. Please input only a number.")
            continue

        vertical_force_info = {"location": vertical_force_location,
                               "magnitude": vertical_force_magnitude}
        # vertical_force_info is a dictionary that stores the information for the location
        # and magnitude of a given force.
        v_forces.append(vertical_force_info)

    return v_forces


# Pre: Takes in inputtedLength to check if the inputted moment is within bounds.
#      It only accepts numbers and reprompts the user if they input
#      anything else.
# Post: This prompts the user to input the location of the bending point moment and the direction
#       and magnitude. After that is done, it reprompts the user to add another bending moment.
#       To end the input, the user can type 'done' and move on to the next prompt.
def point_moments(inputted_length):
    print()
    moments = []  # This is an empty list to store the forces and locations the user inputs
    print("Please input the location of a bending moment "
          "or type 'done' if there are no more: ")
    while True:
        location_input = input("Enter the location of the moment: ")
        if location_input.lower() == "done":
            break
        try:
            moment_location = float(location_input)
            if not (0 <= moment_location <= inputted_length):
                print("The location is not in the range of the beam. Please Try again.")
                continue
        except ValueError:
            print("Invalid input. Please input only a number.")      
            continue
                      
        try:
            print("For the direction, enter a positive number if the moment is counter-clockwise"
                  " and a negative number if the moment is clockwise")
            moment_magnitude = float(input("Enter the magnitude and " 
                                           "direction of the moment: "))
        except ValueError:
            print("Invalid input. Please input only a number.")
            continue

        moment_info = {"location": moment_location,
                       "magnitude": moment_magnitude}
        # moment_info is a dictionary that stores the information for the location
        # and magnitude of a given moment.
        moments.append(moment_info)

    return moments


# Pre: Takes in inputtedLength to check if the inputted moment is within bounds.
#      It only accepts numbers and reprompts the user if they input
#      anything else.
# Post: This prompts the user to input the interval of the distributed load and the
#       function. After that is done, it reprompts the user to add another distrbuted load.
#       To end the input, the user can type 'done' and move on to the next prompt.
def distributed_load(inputted_length):
    print()
    dist_loads = []  # This is an empty list to store the function and interval
    print("Please input the starting location of the "
          "Distributed Load or type 'done' if there are no more: ")
    while True:
        location_input = input("Enter the starting location: ")
        if location_input.lower() == "done":
            break
        try:
            start_location = float(location_input)
            if not (0 <= start_location <= inputted_length):
                print("The location is not in the range of the beam. Please Try again.")
                continue
        except ValueError:
            print("Invalid input. Please input only a number.")
            continue

        try:
            print("Please input the ending location of the Distributed Load: ")
            location_input = input("Enter the ending location: ")
            end_location = float(location_input)

            if end_location == start_location:
                print("The ending location cannot be the same as the starting location. "
                      "Please try again.")
                continue

            if not (start_location < end_location <= inputted_length):
                print("The location is not in the range of the beam or is "
                      "before the starting location. Please try again")
                continue
        except ValueError:
            print("Invalid input. Please input only a number.")
            continue

        try:
            print("Please input the distributed load function in a format"
                  " that matplotlib will be able to graph")
            x = sp.symbols('x')
            user_function_input = input("Enter the function: ")
            user_function = sp.sympify(user_function_input)

            # Check if the function is a valid expression and can be evaluated
            if not isinstance(user_function, (sp.Basic, float, int)):
                raise ValueError

            # Attempt to evaluate the function at some points to see if it's graphable
            test_point = (start_location + end_location) / 2
            evaluated_function = user_function.evalf(subs={x: test_point})

            # Ensure the evaluated function is a number
            if not isinstance(evaluated_function, (float, int, sp.Float, sp.Integer)):
                raise ValueError

            dist_info = {"start": start_location, "end": end_location, "function": user_function}
            # dist_info is a dictionary that stores the information for the interval
            # and function for a given distributed load.
            dist_loads.append(dist_info)

        except (sp.SympifyError, ValueError):
            print("Invalid function. Please enter a valid mathematical "
                  "function that matplotlib can graph.")
            print()
            continue

    return dist_loads


# Pre: Accepts the inputtedLength, horizontal forces, vertical forces, and point moments
#      (distributed loads will be programmed later) that the user already inputted
# Post: This calculates the reaction forces present at the supports and returns an array.
#       in RREF (which will be easy to extract the reaction values)
#       Future versions should use the distance between point A and B.
def solve_reaction_forces(h_forces, v_forces, moments, dist_loads, support_locations):
    rxn = np.empty(shape=(3, 4))
    # The following rows are hardcoded as that is always the form this system of equations
    # will be in. What is missing is the 4th column which will be solved for.

    roller_location = support_locations[0]
    pin_location = support_locations[1]
    # support_location[0] is where the ROLLER support is located
    # support_location[1] is where the PIN support is located

    row1_h = [1, 0, 0, 0]
    row2_v = [0, 1, 1, 0]
    row3_m = [0, roller_location, pin_location, 0]

    # This finds the sum of the inputted horizontal forces and then flips the sign to
    # allow it to be inputted as the solution to the system of equations.
    h_sum = 0
    for force in h_forces:
        h_sum += force['magnitude']
    row1_h[3] = -h_sum

    # This finds the sum of the inputted vertical forces and then flips the sign to
    # allow it to be inputted as the solution to the system of equations.
    v_sum = 0
    for force in v_forces:
        v_sum += force['magnitude']

    # This finds the sum of the inputted point moments
    m_sum = 0
    for moment in moments:
        m_sum += moment['magnitude']

    # This finds the moment about the LEFT most side of the beam
    force_cross_distance_sum = 0
    for f_x_d in v_forces:
        force_cross_distance_sum += f_x_d['location'] * f_x_d['magnitude']
    total_moment = -m_sum - force_cross_distance_sum
    #  We add this together to find the total_moment
    #  They must be negative because they are moved
    #  To the other side in RREF

    # This finds the vertical effect that the distributed loads have on the system.
    # They must be integrated one at a time and then added to the same row as the vertical forces
    x = sp.symbols('x')
    dist_v_sum = 0
    for load in dist_loads:
        dist_v_sum += sp.integrate(load['function'],
                                  (x, load['start'], load['end']))
    row2_v[3] = -v_sum + dist_v_sum

    # This finds the moment effect that the distributed loads have about point A
    dist_m_sum = 0
    for load in dist_loads:
        dist_m_sum += sp.integrate(load['function'] * x,
                                   (x, load['start'], load['end']))
    total_moment += dist_m_sum
    row3_m[3] = total_moment

    rxn[0] = row1_h
    rxn[1] = row2_v
    rxn[2] = row3_m

    # Convert to sympy Matrix
    A = sp.Matrix(rxn)

    # Convert to RREF
    rxn_RREF = A.rref()[0]

    # Convert the sympy Matrix to a numpy array
    rxn_RREF_array = np.array(rxn_RREF.evalf(4).tolist())

    return rxn_RREF_array


# Pre: This accepts the array from solveReactionForces
# Post: Finds the initial shear force form the array and puts it into a variable.
#       This stores the vertical force found at the pin support.
def find_roller_rxn(rxn_RREF_array):
    roller_rxn = (rxn_RREF_array[1, 3])
    # Initial shear force at the start of the beam. The value is located
    # at the 2nd row and 4th column of this array
    return roller_rxn


# Pre: This accepts teh array from solveReactionForces
# Post: Finds the final shear force from the array and puts it into a variable. This stores
#       the vertical force found at the roller support.
def find_pin_y_rxn(rxn_RREF_array):
    pin_y = (rxn_RREF_array[2, 3])
    # Initial shear force at the end of the beam. The value is located
    # at the 3rd row and 4th column of this array
    return pin_y


# Pre: This accepts the array from solveReactionForces
# Post:  Finds the initial axial force form the array and puts it into a variable.
def find_pin_x_rxn(rxn_RREF_array):
    pin_x = (rxn_RREF_array[0, 3])
    # Axial force at the pin support. The value is located
    # at the 1st row and 4th column of this array
    return pin_x


# Pre: Accepts h_forces, and initial_axial_force
# Post: This puts the total_h_forces into a list so that it can be easily used.
def find_total_h_forces(h_forces, pin_x, support_locations):
    total_h_forces = h_forces.copy()

    # Pin is located at support-locations[1]
    pin_x_location = support_locations[1]
    total_h_forces.append({'location': pin_x_location, 'magnitude': pin_x})

    return total_h_forces


# Pre: Accepts v_forces, initial_shear_force, inputtedLength, final_shear_force
# Post: This puts the total_v_forces into a list so that it can be easily used.
def find_total_v_forces(v_forces, roller_rxn, support_locations, pin_y):
    total_v_forces = v_forces.copy()

    # IMPORTANT: initial_shear_force_location is created so that when the supports are able
    #            to be moved around, the shear force at the support is not hard coded to be at zero
    roller_location = support_locations[0]
    pin_location = support_locations[1]
    total_v_forces.append({'location': roller_location, 'magnitude': roller_rxn})
    total_v_forces.append({'location': pin_location, 'magnitude': pin_y})

    return total_v_forces


# Pre: Accepts variable x, h_forces, initial_axial_force
# Post: This calculates the axial force at all points of x so that it can be plotted
def axial_force_at_point(x, total_h_forces):
    h = 0
    for force in total_h_forces:
        if x >= force["location"]:
            h -= force["magnitude"]

    return h


# Pre: Accepts variable x, v_forces, initial_shear_force
# Post: This calculates the shear force at all points of x so that it can be plotted
def shear_force_at_point(x, total_v_forces, dist_loads):
    V = 0
    for force in total_v_forces:
        if x >= force['location']:
            V += force['magnitude']

    # This was the previous version to handle constant functions only. I kept it
    # as it is easy to understand and it can be a reference
    # for load in dist_loads:
    #     if load['start'] <= x <= load['end']:
    #         V += -load['function'] * (x - load['start'])
    #     elif x > load['end']:
    #         V += -load['function'] * (load['end'] - load['start'])

    # This evaluates the function for each value of x
    for load in dist_loads:
        load_function = sp.lambdify(sp.symbols('x'), load['function'], modules='numpy')
        if load['start'] <= x <= load['end']:
            V += -integrate.quad(load_function, load['start'], x)[0]
        elif x > load['end']:
            V += -integrate.quad(load_function, load['start'], load['end'])[0]

    return V


# Pre: Accepts variables x, total_v_forces, and moments.
# Post: This calculates the vertical force's contribution to the moment at
#       all points along the beam at position "x".
#       This returns the moment at all point along the beam with variable "M".
def moment_at_point(x, total_v_forces, moments):
    M = 0
    for force in total_v_forces:
        if x > force['location']:
            M += force['magnitude'] * (x - force['location'])
    for moment in moments:
        if x > moment['location']:
            M -= moment['magnitude']
            # We subtract here because moments do the 'opposite' of what we expect
    return M


# Pre: Accepts inputtedLength, v_forces, initial_shear_force.
# Post: This plots the axial force diagram based on what the user inputted for horizontal forces.
#       It uses matplotlib for the graph.
def axial_diagram(ax, inputted_length, h_forces, total_h_forces, unit_system):
    length_unit = 'm' if unit_system == 'metric' else 'ft'
    force_unit = 'N' if unit_system == 'metric' else 'lb'

    x_values = np.linspace(-1e-10, inputted_length, 1000)
    # -1e-10 is here so that the initial jump is correctly displayed. If we started
    # at x = 0, there will be no space to plot the initial jump
    y_values = [axial_force_at_point(x, total_h_forces) for x in x_values]

    # This plots a vertical line for the horizontal point forces
    for force in h_forces:
        location = force['location']
        magnitude = force['magnitude']
        ax.axvline(x=location, linestyle='--',
                   label=f'Axial Force at {location} {length_unit}, {magnitude} {force_unit}')

    # This plots a vertical line for the pin reaction force
    pin_x = total_h_forces[-1]
    location = pin_x['location']
    magnitude = pin_x['magnitude']
    ax.axvline(x=location, linestyle='--', color='red',
               label=f'Horizontal Reaction Force at {location} m, {magnitude} N')

    # Finds the maximum absolute value and its x value
    max_index = np.argmax(np.abs(y_values))
    max_x = x_values[max_index]
    max_y = y_values[max_index]

    # Determine the vertical offset direction based on y position relative to the center
    # This finds whether to orient the annotation above or below the plotted line based on
    # which one is closest to the center
    y_range = np.max(y_values) - np.min(y_values)
    y_center = np.min(y_values) + y_range / 2

    # Calculate the distances for both potential annotation positions
    distance_above = abs((max_y * 1.5) - y_center)
    distance_below = abs((max_y / 1.5) - y_center)
    if distance_below < distance_above:
        # Place annotation below the point
        xytext = (max_x, max_y / 1.5)
    else:
        # Place annotation above the point
        xytext = (max_x, max_y * 1.5)

    # This makes the graph
    ax.axhline(y=0, color='k', linestyle='--')
    ax.plot(x_values, y_values, label="Axial Force Diagram", color='b')
    ax.annotate(f'Max |Force|: {abs(max_y):.2f} {force_unit}\nat x = {max_x:.2f} {length_unit}',
                xy=(max_x, max_y), xytext=xytext,
                arrowprops=dict(facecolor='r', shrink=0.05),
                fontsize=12, color='r', horizontalalignment='center')
    ax.set_title("Axial Force Diagram")
    ax.set_xlabel(f"Position ({length_unit})")
    ax.set_ylabel(f"Axial Force ({force_unit})")
    ax.legend(prop={'size': 8})
    ax.grid(True)


# Pre: Accepts inputtedLength, v_forces, initial_shear_force.
# Post: This plots the shear force diagram based on what the user inputted for vertical forces.
#       It uses matplotlib for the graph.
def shear_diagram(ax, inputted_length, v_forces, total_v_forces, dist_loads, unit_system):
    length_unit = 'm' if unit_system == 'metric' else 'ft'
    force_unit = 'N' if unit_system == 'metric' else 'lb'

    x_values = np.linspace(-1e-10, inputted_length, 1000)
    # -1e-10 is here so that the initial jump is correctly displayed. If we started
    # at x = 0, there will be no space to plot the initial jump
    y_values = [shear_force_at_point(x, total_v_forces, dist_loads) for x in x_values]

    # This plots a vertical line for the point shear forces
    for force in v_forces:
        location = force['location']
        magnitude = force['magnitude']
        ax.axvline(x=location, linestyle='--',
                   label=f'Shear Force at {location} {length_unit}, {magnitude} {force_unit}')

    # Plot the last two forces (roller and pin reactions)
    # The roller and pin reactions are appended to the end of the dictionary
    for force in total_v_forces[-2:]:
        location = force['location']
        magnitude = force['magnitude']
        ax.axvline(x=location, linestyle='--', color='blue',
                   label=f'Vertical Reaction Force at {location} m, {magnitude} N')

    # This plots a vertical line for the start and end of distributed loads
    for load in dist_loads:
        start = load['start']
        end = load['end']
        function = load['function']
        ax.axvline(x=start, linestyle='--', color='purple',
                   label=f'Distributed Load start at {start} {length_unit}, '
                         f'{function} {force_unit}/{length_unit}')
        ax.axvline(x=end, linestyle='--', color='purple',
                   label=f'Distributed Load end at {end} {length_unit}, '
                         f'{function} {force_unit}/{length_unit}')

    # Finds the maximum absolute value and its x value
    max_index = np.argmax(np.abs(y_values))
    max_x = x_values[max_index]
    max_y = y_values[max_index]

    # Determine the vertical offset direction based on y position relative to the center
    # This finds whether to orient the annotation above or below the plotted line based on
    # which one is closest to the center
    y_range = np.max(y_values) - np.min(y_values)
    y_center = np.min(y_values) + y_range / 2

    # Calculate the distances for both potential annotation positions
    distance_above = abs((max_y * 1.5) - y_center)
    distance_below = abs((max_y / 1.5) - y_center)
    if distance_below < distance_above:
        # Place annotation below the point
        xytext = (max_x, max_y / 1.5)
    else:
        # Place annotation above the point
        xytext = (max_x, max_y * 1.5)

    # This plots the graph
    ax.plot(x_values, y_values, label="Shear Force Diagram", color='r')
    ax.axhline(y=0, color='k', linestyle='--')
    ax.annotate(f'Max |Force|: {abs(max_y):.2f} {force_unit}\nat x = {max_x:.2f} {length_unit}',
                xy=(max_x, max_y), xytext=xytext,
                arrowprops=dict(facecolor='red', shrink=0.05),
                fontsize=12, color='red', horizontalalignment='center')
    ax.set_title("Shear Force Diagram")
    ax.set_xlabel(f"Position ({length_unit})")
    ax.set_ylabel(f"Shear Force ({force_unit})")
    ax.legend(prop={'size': 8})
    ax.grid(True)


# Pre: Accepts inputtedLength, total_v_forces, moments, and v_forces.
# Post: This plots the moment diagram based on what the user inputted for vertical forces and
#       moments. It uses matplotlib for the graph
def moment_diagram(ax, inputted_length, total_v_forces, moments,
                   v_forces, dist_loads, unit_system):
    length_unit = 'm' if unit_system == 'metric' else 'ft'
    force_unit = 'N' if unit_system == 'metric' else 'lb'
    moment_unit = 'N*m' if unit_system == 'metric' else 'ft*lb'

    x_values = np.linspace(-1e-10, inputted_length, 5000)
    # -1e-10 is here so that the initial jump is correctly displayed. If we started
    # at x = 0, there will be no space to plot the initial jump
    y_values = np.array([shear_force_at_point(x, total_v_forces, dist_loads) for x in x_values])

    # This gets the moment value at every point of x.
    # The moment diagram is the integral of the shear diagram
    moment_values = integrate.cumulative_trapezoid(y_values, x_values, initial=0)

    # Include applied moments
    for moment in moments:
        if moment['location'] <= inputted_length:
            idx = np.searchsorted(x_values, moment['location'])
            moment_values[idx:] -= moment['magnitude']

    # This plots a vertical line for the point vertical forces
    for force in v_forces:
        location = force['location']
        magnitude = force['magnitude']
        plt.axvline(x=location, linestyle='--',
                    label=f'Shear Force at {location} {length_unit}, '
                          f'{magnitude} {moment_unit}')

    # Plot the last two forces (roller and pin reactions)
    # The roller and pin reaction are appended to the end of the dictionary
    for force in total_v_forces[-2:]:
        location = force['location']
        magnitude = force['magnitude']
        ax.axvline(x=location, linestyle='--', color='blue',
                   label=f'Vertical Reaction Force at {location} m, {magnitude} N')

    # This plots a vertical line for the start and end of distributed loads
    for load in dist_loads:
        start = load['start']
        end = load['end']
        function = load['function']
        ax.axvline(x=start, linestyle='--', color='purple',
                   label=f'Distributed Load start at {start} {length_unit}, '
                         f'{function} {force_unit}/{length_unit}')
        ax.axvline(x=end, linestyle='--', color='purple',
                   label=f'Distributed Load end at {end} {length_unit}, '
                         f'{function} {force_unit}/{length_unit}')

    # This plots a vertical line for the point moments
    for moment in moments:
        location = moment['location']
        magnitude = moment['magnitude']
        plt.axvline(x=location, linestyle='--', color='red',
                    label=f'Moment at {location} {length_unit}, '
                          f'{magnitude} {moment_unit}')

    # Find the maximum absolute value and its corresponding x value
    max_index = np.argmax(np.abs(moment_values))
    max_x = x_values[max_index]
    max_y = moment_values[max_index]

    # Determine the vertical offset direction based on y position relative to the center
    # This finds whether to orient the annotation above or below the plotted line based on
    # which one is closest to the center
    y_range = np.max(moment_values) - np.min(moment_values)
    y_center = np.min(moment_values) + y_range / 2

    # Calculate the distances for both potential annotation positions
    distance_above = abs((max_y * 1.5) - y_center)
    distance_below = abs((max_y / 1.5) - y_center)
    if distance_below < distance_above:
        # Place annotation below the point
        xytext = (max_x, max_y / 1.5)
    else:
        # Place annotation above the point
        xytext = (max_x, max_y * 1.5)

    # Label the maximum absolute value
    ax.annotate(f'Max |Moment|: {abs(max_y):.2f} {moment_unit}\n'
                f'at x = {max_x:.2f} {length_unit}',
                xy=(max_x, max_y),
                xytext=xytext,
                arrowprops=dict(facecolor='red', shrink=0.05),
                fontsize=12, color='red',
                horizontalalignment='center')

    # Plot the moment function
    ax.axhline(y=0, color='k', linestyle='--')
    ax.plot(x_values, moment_values, label="Moment Diagram", color='g')
    ax.set_title("Moment Diagram")
    ax.set_xlabel(f"Position ({length_unit})")
    ax.set_ylabel(f"Moment ({moment_unit})")
    ax.legend(prop={'size': 8})
    ax.grid(True)


# Pre: Accepts dist_loads and a variable indicating our desired range for graphing the functions
#      We want the functions to be between [-2,2] in the y direction
# Post: Finds the max value that any function reaches and scales all the functions down accordingly
#       so that all the functions ranges are between [-2,2] while keeping relative heights
#       the same
def scale_functions(dist_loads, target_max=2):
    max_values = []

    if dist_loads == []:
        scaled_loads = []
        return scaled_loads

    # Calculate max value for each function
    for load in dist_loads:
        start = load['start']
        end = load['end']
        function = load['function']
        x = sp.Symbol('x')

        # If the function is constant, use the value directly
        if function.is_constant():
            max_value = float(function)
        else:
            # Calculate the maximum value within the given interval
            func = sp.lambdify(x, function, 'numpy')
            x_vals = np.linspace(start, end, 100)
            y_vals = func(x_vals)
            max_value = max(y_vals)

        max_values.append(max_value)

    global_max = max(max_values)
    scaling_factor = target_max / global_max

    # Create a new list with scaled functions
    scaled_loads = []
    for load in dist_loads:
        scaled_load = load.copy()
        scaled_load['function'] = load['function'] * scaling_factor
        scaled_loads.append(scaled_load)

    return scaled_loads


# Pre: Takes in h_forces, total_v_forces, moments, and inputtedLength
# Post: Plots a FBD of the beam otherwise known as the load diagram. This does not consider
#       loads yet. This is only a 1 dimensional representation
def load_diagram(ax, total_h_forces, total_v_forces, moments, inputted_length,
                 scaled_loads, unit_system, dist_loads):
    length_unit = 'm' if unit_system == 'metric' else 'ft'
    force_unit = 'N' if unit_system == 'metric' else 'lb'
    moment_unit = 'N*m' if unit_system == 'metric' else 'ft*lb'

    # Draw the beam
    ax.plot([0, inputted_length], [0, 0], 'k-', lw=5)

    for force in total_v_forces:
        location = force['location']
        magnitude = force['magnitude']

        if magnitude < 0:
            ax.arrow(location, 0, 0, -1, head_width=0.1, head_length=0.1, fc='b', ec='b', zorder=2)
            ax.text(location, -1.2, f"{abs(magnitude)} {force_unit}",
                    ha='center', va='top', color='b', zorder=2)
        elif magnitude > 0:
            ax.arrow(location, 0, 0, 1, head_width=0.1, head_length=0.1, fc='b', ec='b', zorder=2)
            ax.text(location, 1.2, f"{magnitude} {force_unit}",
                    ha='center', va='bottom', color='b', zorder=2)

    for force in total_h_forces:
        location = force['location']
        magnitude = force['magnitude']

        if magnitude < 0:
            ax.arrow(location, 0, -1, 0, head_width=0.1, head_length=0.1, fc='b', ec='b', zorder=2)
            ax.text(location - 0.5, -0.2, f"{abs(magnitude)} {force_unit}",
                    ha='center', color='b', zorder=2)
        elif magnitude > 0:
            ax.arrow(location, 0, 1, 0, head_width=0.1, head_length=0.1, fc='b', ec='b', zorder=2)
            ax.text(location + 0.5, -0.2, f"{magnitude} {force_unit}",
                    ha='center', color='b', zorder=2)

    # This make the moments
    for moment in moments:
        location = moment['location']
        magnitude = moment['magnitude']
        start = (location, -0.4)
        end = (location, 0.4)

        if magnitude > 0:
            arrow = FancyArrowPatch(start, end,
                                    connectionstyle=f"arc3,rad=0.4",  # Radius of the curve
                                    arrowstyle='->',
                                    mutation_scale=20,  # Size of the arrowhead
                                    lw=2,  # Line width
                                    color='blue',  # Arrow color
                                    zorder=2)
        elif magnitude < 0:
            arrow = FancyArrowPatch(start, end,
                                    connectionstyle=f"arc3,rad=-0.4",  # Radius of the curve
                                    arrowstyle='->',
                                    mutation_scale=20,  # Size of the arrowhead
                                    lw=2,  # Line width
                                    color='blue',  # Arrow color
                                    zorder=2)

        # Add the arrow to the plot
        ax.add_patch(arrow)
        ax.text(location, 0.5, f"{abs(magnitude)} {moment_unit}",
                ha='center', va='top', color='b')

    # This creates the dist load graph
    for load in scaled_loads:
        start = load['start']
        end = load['end']
        function = load['function']

        x_vals = np.linspace(start, end, 100)

        if function.is_constant():
            y_vals = np.full_like(x_vals, float(function))
        else:
            x = sp.Symbol('x')
            func = sp.lambdify(x, function, 'numpy')
            y_vals = func(x_vals)

        # Add arrows. The arrows start on the function line and end on the beam (x-axis)
        num_arrows = int((end - start) * 2)
        arrow_x_vals = np.linspace(start, end, num_arrows)
        if function.is_constant():
            arrow_y_vals = np.full_like(arrow_x_vals, float(function))
        else:
            arrow_y_vals = func(arrow_x_vals)

        for x_arrow, y_arrow in zip(arrow_x_vals, arrow_y_vals):
            ax.annotate('', xy=(x_arrow, 0), xytext=(x_arrow, y_arrow),
                        arrowprops=dict(arrowstyle='->', color='red', lw=1))

        ax.plot(x_vals, y_vals, color='red', label=f'{function}')

    # This labels the dist load function
    for load in dist_loads:
        start = load['start']
        end = load['end']
        function = load['function']

        # Distributed load annotations
        midpoint = (start + end) / 2
        function_text = f"Function: w(x) = {function.evalf(4)} {force_unit}/{length_unit}"
        ax.text(midpoint, 2.1, function_text, ha='center', va='bottom', color='red', fontsize=12)

    ax.set_xlim(-0.5, inputted_length + 0.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('auto')
    ax.set_xlabel(f'Length of Beam ({length_unit})')
    ax.set_title('Load Diagram')

    # Hide the y-axis
    ax.get_yaxis().set_visible(False)

    plt.grid(True)


def main():
    unit_system = unit_system_type()
    inputted_length = beam_length()  # This stores the return value for the length of the beam
    support_locations = support_locations_input(inputted_length)

    h_forces = point_horizontal_forces(inputted_length)  # This stores the return list for
    # the horizontal forces.
    
    v_forces = point_vertical_forces(inputted_length)  # This stores the return list for
    # the horizontal forces.
    
    moments = point_moments(inputted_length)
    # This stores the return list for the horizontal forces.

    dist_loads = distributed_load(inputted_length)
    # This stores the return list for the distributed loads

    rxn_RREF_array = solve_reaction_forces(h_forces, v_forces, moments, dist_loads,
                                           support_locations)
    # This stores the return list for the solved rxn forces

    roller_rxn = find_roller_rxn(rxn_RREF_array)
    pin_x = find_pin_x_rxn(rxn_RREF_array)
    pin_y = find_pin_y_rxn(rxn_RREF_array)

    total_v_forces = find_total_v_forces(v_forces, roller_rxn, support_locations, pin_y)
    # This stores the return list for the total vertical forces

    total_h_forces = find_total_h_forces(h_forces, pin_x, support_locations)
    # This stores the return list for the total h forces

    scaled_loads = scale_functions(dist_loads)
    # stores the scaled functions

    fig, ax = plt.subplots(figsize=(12, 16))
    load_diagram(ax, total_h_forces, total_v_forces, moments, inputted_length,
                 scaled_loads, unit_system, dist_loads)

    if h_forces == []:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
        shear_diagram(ax1, inputted_length, v_forces, total_v_forces, dist_loads, unit_system)
        moment_diagram(ax2, inputted_length, total_v_forces, moments,
                       v_forces, dist_loads, unit_system)
    # This only prints out the shear and moment graph if there are no axial forces.
    # If there are axial forces, all three graphs will be graphed
    else:
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16))
        axial_diagram(ax1, inputted_length, h_forces, total_h_forces, unit_system)
        shear_diagram(ax2, inputted_length, v_forces, total_v_forces, dist_loads, unit_system)
        moment_diagram(ax3, inputted_length, total_v_forces, moments,
                       v_forces, dist_loads, unit_system)

    # This avoids overlapping of text
    plt.tight_layout(pad=3.0)

    plt.show()


if __name__ == "__main__":
    main()
