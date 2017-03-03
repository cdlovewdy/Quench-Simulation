# Quench-Simulation
A numerical program used to simulate the quench process of superconducting magnet

Demo1
initial condition: uniform temperature 
boundary condition: two adiabat boundary, two fixed temperature boundary
material property:fixed

Demo2
initial condition: uniform temperature 
boundary condition: two adiabat boundary, two fixed temperature boundary
material property:change with temperature

Demo3
initial condition: uniform temperature
boundary condition: two adiabat boundary, two fixed temperature, imbalanced heat generating source
material property: change with temperature

material
Material properties for the quench simulation
Material type: Copper, NbTi, Nb3Sn, Kapton, G10
properties: electrical restivity, thermal conductivity, specificheat
Plot all the propertied of all these materials in the temperature range [4,300]K

MIITs
calculate the MIITs for different cable with different configuration

HeaterDelay
calculate the heater delay of the IHEP-Subscale step2 magnet
cable: Nb3Sn cu/sc=1 RRR=200
Heater: length 3139mm width 11mm thickness 100 micron Power 100w/cm^2
Insulation: kapton inner 100micron outer 50micron
boundary condition: three adibat boundary,the outer insulation fixed temperature 4.2K

Have a problem!!!
The calculation time is too long. It need sone optimization!!!
