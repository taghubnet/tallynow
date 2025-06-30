# TallyNow
Prototype for a automated completion tally app

This code takes several excel sheets as input and creates a tally for an upper completion automatically. The Work flow is modeled to a dual derrick rig. The input files are:
1. Assembly overview: 
In this spreadsheet, all assemblies that are part of the upper completion are defined. For each assembly, multiple constraints can be defined: Upper limit, Lower limit, Seration pipes, Critical Point.   
3. 9 5/8'' liner tally: 
Tally from the liner in which the completion will be run.
5. 10 3/4'' tie-back tally: 
Tally of the tie-back of the liner.
7. tubing tallies: 
Onshore tally of tubing pipe.
Overview of all available pup joint.
Tally of racked tubing.

Main will solve the tally problem in three step:

# Step 1
Calculates the required number of pipes that need to be ordered for a given well length. Simply divides the well length by an avergae pipe length.

# Step 2
Creates a draft tally with an average pipe length and determines how many double and triple stands should be racked prior to running the completion. It takes the assembly overview, 9 5/8'' liner tally, the 10 3/4'' tie-back tally and the tubing tallies as input. The completion tally is created step wise, from bottom to top taking the boundaries set in the assembly overview into account and finding a solution that adheres to these boundaries.   

# Step 3
As a continuation of step 2, the racked tubing tally is now considered. A completion tally is created the same way as before but racked tubing is now used in a specific order, specified in the racked tubing tally. The solution adheres to the bounbdaries specified in the assembly overview and depicts the final tally.
