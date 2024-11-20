# Load-Axial-Shear-Moment-Diagrams
## Project Overview
Load, axial, shear, and moment diagrams are graphical representations of the internal forces as well as internal bending moments at every point along the length of a beam in response to external forces, moments, and distributed loads.
Here is an example of the load, shear, and moment diagrams of a **simply supported** beam courtesy of Dr. Erik Hurlen:

![image](https://github.com/user-attachments/assets/aa0e48a3-a604-4001-ab26-97f184a11f49)

This is a representation of the forces and moments occuring in the beam from this situation:
![image](https://github.com/user-attachments/assets/100f00f4-8a93-4602-a2a4-75504bd6eec0)

load_axial_shear_moment_diagrams aims to generate the load, axial, shear, and moment diagrams for the three beam types given the user input of where forces and moments are and their direction and magnitude. The program will also give information about the maximum absolute values the graphs achieve and their location.

## What are Load Diagrams, Axial forces, Shear forces, and Bending Moments?
Load Diagrams:
- Essentially a Free-Body Diagram of the beam
- It shows where the external forces and moments are applied

For a system to be in equilibrium, there must be no net forces
- Axial forces, shear forces, and bending moments all sum to zero in equilibrium by Newton's Second Law 


Axial Forces (*N* in diagrams):
- Axial forces are internal compression or tension forces along the length of the beam
- External forces can cause the beam to stretch or compress 
- The axial force diagram shows the internal horizontal forces at all points 

Shear Forces (*V* in diagrams):
- Shear forces are the internal forces that act perpendicular to the beam
- External forces can cause the beam to slide or deform one part of the beam relative to the other part of the beam
- The shear force diagram shows the internal vertical forces at all points 

Bending Moments (*M* in diagrams):
- Bending moments are the internal bending moments along the beam 
- External forces can cause the beam to bend (this is a moment)
- The bending moment diagram shows the bending moment at all points 

## What are the Three Beam Types?
*Image from [SkyCiv.com](https://skyciv.com/docs/tutorials/beam-tutorials/types-of-beams/)*

![image](https://github.com/user-attachments/assets/93cf872d-168a-4ab7-9338-66c4f812395a)

### Simply Supported Beams
A simply supported beam is one where a pin support and a roller support are placed on opposite ends of the beam. This program will only deal with beams with a pin on the left side of the beam and a roller on the right side. If the roller needs to be on the left and the pin on the right, use overhanging_beam.py and place the supports in their necessary spots.

### Cantilever Beams
A cantilever beam is one that is attached to the wall using a fixed support. This support prevents horizontal forces, vertical, and rotational movements.

### Overhanging Beams
An overhanging beam is one supported with two supports, but one or more supports are not placed at the ends of the beam. This program only deals with statically determinate beams, so a roller support and a pin support are chosen.


## Installation
Clone the repository
```
git clone https://github.com/arthug-ME/load_axial_shear_moment_diagrams.git
```
Install dependencies
```
pip install -r requirements.txt
```

## Example 
### Input
![image](https://github.com/user-attachments/assets/61fae053-9da5-4349-90d2-f7f9a0136a61)
![image](https://github.com/user-attachments/assets/f2fe7239-9193-47fd-bbc0-1002488dc6ef)

### Output
![image](https://github.com/user-attachments/assets/54208d12-34ea-4b26-a29f-d60967583d81)
![image](https://github.com/user-attachments/assets/9ca97a53-4cc3-421c-ad94-82e4b3655bb3)

## Using Distributed Load Functions
This program was made to handle any type of function as long as it is inputted in a format that matplotlib can graph (i.e. *w(x) = 3x* is WRONG but *w(x) = 3 * x* is CORRECT). Here is an example where *w(x) = 120 * sqrt(x/2)* is used.
![image](https://github.com/user-attachments/assets/22538725-0da8-4fb2-9eb1-4f50b2ee2a95)
![image](https://github.com/user-attachments/assets/b74432ed-48a7-4ad0-aa86-2b4e2a122daa)

It is important to shift the function as needed. If we wanted a triangular distributed load that increases by 2 N / m on the interval from 3 to 6, we would input *w(x) = 2 * (x - 3)* and NOT *w(x) = 2 * x*. 
![image](https://github.com/user-attachments/assets/df4ef1de-a385-419b-b61d-6128ab9d08e7)




