import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy import integrate


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


# Pre: Accepts variable x, h_forces, initial_axial_force
# Post: This calculates the axial force at all points of x so that it can be plotted
def axial_force_at_point(x, total_h_forces):
    h = 0
    for force in total_h_forces:
        if x >= force["location"]:
            h += force["magnitude"]

    return h


def piecewise_v_function(x, total_v_forces, dist_loads):
    """
    Shear force at point x on the beam.
    """
    V = 0
    for force in total_v_forces:
        if x >= force['location']:
            V += force['magnitude']

    # for load in dist_loads:
    #     if load['start'] <= x <= load['end']:
    #         V += -load['function'] * (x - load['start'])
    #     elif x > load['end']:
    #         V += -load['function'] * (load['end'] - load['start'])
    for load in dist_loads:
        load_function = sp.lambdify(sp.symbols('x'), load['function'], modules='numpy')
        if load['start'] <= x <= load['end']:
            V += -integrate.quad(load_function, load['start'], x)[0]
        elif x > load['end']:
            V += -integrate.quad(load_function, load['start'], load['end'])[0]

    return V


def shear_diagram(ax, inputted_length, total_v_forces, dist_loads):
    x_values = np.linspace(0, inputted_length, 1000)
    y_values = [piecewise_v_function(x, total_v_forces, dist_loads) for x in x_values]

    ax.plot(x_values, y_values, label="Shear Force Diagram", color='r')

    ax.axhline(y=0, color='k', linestyle='--')

    ax.set_title("Shear Force Diagram")
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Shear Force (kN)")
    ax.grid(True)


def moment_diagram(ax, inputted_length, total_v_forces, moments, dist_loads):
    x_values = np.linspace(0, inputted_length, 1000)
    v_values = np.array([piecewise_v_function(x, total_v_forces, dist_loads) for x in x_values])

    # Compute the cumulative integral (moment diagram) using the trapezoidal rule
    moment_values = integrate.cumulative_trapezoid(v_values, x_values, initial=0)

    # Include applied moments
    for moment in moments:
        if moment['location'] <= inputted_length:
            idx = np.searchsorted(x_values, moment['location'])
            moment_values[idx:] -= moment['magnitude']

    # Mark the x axis
    ax.axhline(y=0, color='k', linestyle='--')

    # Plot the moment function
    ax.plot(x_values, moment_values, 'g-', linewidth=2)
    ax.set_title("Moment Diagram")
    ax.set_xlabel("Position (m)")
    ax.set_ylabel("Moment (kNm)")
    ax.grid(True)


def solve_reaction_forces(h_forces, v_forces, moments, dist_loads, support_locations):
    rxn = np.empty(shape=(3, 4))
    # The following rows are hardcoded as that is always the form this system of equations
    # will be in. What is missing is the 4th column which will be solved for.
    row1_h = [1, 0, 0, 0]
    row2_v = [0, 1, 1, 0]
    row3_m = [0, support_locations[0], support_locations[1], 0]
    # support_location[0] is where the ROLLER support is located
    # support_location[1] is where teh PIN support is locoated

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


def main():
    x = sp.symbols('x')
    # Input data
    inputted_length = 30
    h_forces = []
    total_v_forces = [{'location': 0, 'magnitude': -1000}, {'location': 30, 'magnitude': 1000}, {'location': 10, 'magnitude': 2000}]  # {'location': 0, 'magnitude': 2000}, {'location': 12, 'magnitude': 2000}
    v_forces = [{'location': 0, 'magnitude': -1000}]
    moments = []
    dist_loads = [{'start': 20, 'end': 30, 'function': 200}]

    support_locations = support_locations_input(inputted_length)
    print(support_locations)

    rxn_RREF_array = solve_reaction_forces(h_forces, v_forces, moments, dist_loads, support_locations)
    # This stores the return list for the solved rxn forces

    print(rxn_RREF_array)


    # Plot the moment diagram
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    shear_diagram(ax1, inputted_length, total_v_forces, dist_loads)
    moment_diagram(ax2, inputted_length, total_v_forces, moments, dist_loads)

    # This avoids overlapping of text
    plt.tight_layout(pad=3.0)

    plt.show()


if __name__ == "__main__":
    main()