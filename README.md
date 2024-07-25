# load_axial_shear_moment_diagrams
## Project Overview
Load, axial, shear, and moment diagrams are graphical representations of the internal forces as well as internal bending moments at every point along the length of a beam in response to external forces, moments, and distributed loads.
Here is an example of the load, shear, and moment diagrams of a **simply supported** beam courtesy of Dr. Erik Hurlen:
![image](https://github.com/user-attachments/assets/aa0e48a3-a604-4001-ab26-97f184a11f49)

This is a representation of the forces and moments occuring in the beam from this situation:
![image](https://github.com/user-attachments/assets/100f00f4-8a93-4602-a2a4-75504bd6eec0)
load_axial_shear_moment_diagrams aims to generate the load, axial, shear, and moment diagrams given the user input of where forces and moments are and their direction and magnitude. The program will also give information about the maximum absolute values the graphs achieve and their location.

## What are Load Diagrams, Axial forces, Shear forces, and Bending Moments?
Load Diagrams:
- Essentially a Free-Body Diagram of the beam
- It shows where the external forces and moments are applied

For a system to be in equilibrium, external forces must be balanced by an internal force as stated by Newton's 3rd law
- Axial forces, shear forces, and bending moments are 3rd law force pairs to external forces and moments


Axial Forces (*N* in diagrams):
- The internal compression or tension forces along the length of the beam
- External forces can cause the beam to stretch or compress 
- The axial force diagram shows the internal forces at all points such that stretching or compressing do not occur

Shear Forces (*V* in diagrams):
- The internal forces that act perpendicular to the beam
- External forces can cause the beam to slide or deform one part of the beam relative to the other part of the beam
- The shear force diagram shows the internal forces at all points such that the beam does not slide or shear in two

Bending Moments (*M* in diagrams):
- The internal bending moments along the beam 
- External forces can cause the beam to bend (this is a moment)
- The bending moment diagram shows the bending moment at all points such that the beam does not bend 

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
![image](https://github.com/user-attachments/assets/950ccb41-f801-490f-a7fb-ea9000449fa3)
### Output
![image](https://github.com/user-attachments/assets/6387d368-a310-443d-8bdd-b177ad6da391)
![image](https://github.com/user-attachments/assets/1101a178-20c7-4552-bdbc-c2f6c33e2272)


