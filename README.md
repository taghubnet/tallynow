# TallyNow

**Automated Oil & Gas Upper Completion Tally System**

TallyNow is an automated upper completion tally application that optimizes the arrangement of tubing, pipes, and assemblies for oil and gas well upper completions. The system takes multiple Excel spreadsheets as input and generates an optimal upper completion tally that minimizes waste while meeting depth requirements and equipment constraints.

## Overview

This system automates the complex process of determining what equipment is needed and how to arrange it for **upper completion operations only**. It's designed for dual derrick rig workflows and solves what is essentially a sophisticated "bin packing" optimization problem for the upper portion of oil well completions.

## Features

- **Automated Pipe Calculation**: Determines optimal pipe arrangements for target well depths
- **Assembly Constraint Management**: Handles complex downhole equipment placement rules
- **Multi-Stand Optimization**: Efficiently arranges triple stands, double stands, and single pipes
- **Inventory Management**: Tracks available equipment and prevents double-use
- **Fine-Tuning with Pups**: Uses short pipe sections for precise depth matching
- **Excel Integration**: Seamlessly imports from standard industry tally formats

## Input Files

The system requires several Excel files (stored in the `sheets/` folder):

1. **assemblies_in_completion.xlsx**: Assembly overview defining all assemblies that are part of the upper completion, including constraints like upper/lower limits, separation pipes, and critical points

2. **9 5-8 Liner Tally Test Well As Run.xlsx**: Liner tally data for the completion string

3. **10 3-4 Tie-back Tally Test_Well_As Run.xlsx**: Tie-back tally of the liner system

4. **tubing tallies.xlsx**: Contains multiple sheets:
   - Onshore tally of tubing pipes
   - Overview of available pup joints
   - Tally of racked tubing arrangements

## How It Works

TallyNow solves the completion tally problem in three sequential steps:

### Step 1: Initial Pipe Estimation
- Calculates the required number of pipes for a given well depth
- Uses average pipe length (11.5m) for initial estimation
- Provides baseline requirements for procurement

### Step 2: Stand Calculation
- Creates a draft tally using average pipe lengths
- Determines optimal number of double and triple stands to rack
- Considers all input data: assemblies, liner tally, tie-back tally, and tubing inventory
- Builds completion from bottom to top while respecting assembly constraints
- Ensures solution adheres to specified boundaries

### Step 3: Final Completion Design
- Incorporates actual racked tubing inventory with specific pipe IDs and lengths
- Generates final completion tally using real equipment in optimal order
- Accounts for:
  - **Triple stands**: 3 pipes joined together for efficiency
  - **Double stands**: 2 pipes joined together
  - **Single pipes**: Individual pipes for flexibility
  - **Pups**: Short sections for precise depth adjustment
- Produces final upper completion tally ready for field operations

## Key Components

- **AssemblyPipe**: Specialized downhole equipment (packers, valves, etc.)
- **Casing Joints**: Protective steel tubing already installed in the well
- **Deck Tally**: Complete inventory of available pipes with IDs and lengths
- **Completion**: The final optimized arrangement that reaches target depth

## Installation & Usage

1. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pandas openpyxl
   ```

2. **Prepare your data**:
   - Place all Excel files in the `sheets/` folder
   - Ensure file names match the expected format
   - Verify sheet names within Excel files are correct

3. **Run the system**:
   ```bash
   python main.py
   ```

4. **Configure for your well**:
   - Update `well_depth` variable in main.py (line 39)
   - Adjust file paths if using different naming conventions
   - Modify constraints as needed for your specific well

## Output

The system provides:
- Step-by-step completion calculations
- Required pipe counts and stand arrangements
- Final completion tally with specific equipment assignments
- Depth calculations and error margins
- Visual table showing pipe/stand assignments with top and bottom depths

## Contributing

This project is open source and welcomes contributions! Areas for improvement include:

- Enhanced error handling and validation
- Support for additional file formats
- Web-based user interface
- Advanced optimization algorithms
- Integration with industry-standard software

## License

This project is released under an open source license. See LICENSE file for details.

## Disclaimer

This software is provided as-is for educational and research purposes. Always verify results with qualified engineering professionals before use in actual well operations.