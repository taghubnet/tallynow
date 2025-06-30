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
- **CSV Integration**: Fast data processing with standard CSV formats

## Input Files

The system uses CSV files (stored in the `data/` folder) for fast processing and better version control:

1. **assemblies.csv**: Assembly overview defining all assemblies that are part of the upper completion, including constraints like upper/lower limits, separation pipes, and critical points

2. **liner_tally.csv**: Liner tally data for the completion string

3. **tieback_tally.csv**: Tie-back tally of the liner system

4. **tubing_tally.csv**: Onshore tally of tubing pipes
5. **racked_tubing.csv**: Tally of pre-arranged tubing stands  
6. **pups.csv**: Overview of available pup joints (short pipe sections)

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

### Quick Start

1. **Clone and set up**:
   ```bash
   git clone <repository-url>
   cd TallyNow
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   make install
   ```

2. **Run completion calculation**:
   ```bash
   make well
   ```

3. **Run tests**:
   ```bash
   make tests
   ```

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your data**:
   - Place all CSV files in the `data/` folder
   - Ensure file names match the expected format (see Input Files section)
   - Verify data structure matches the expected CSV format

3. **Configure for your well**:
   - Update `well_depth` variable in main.py (line 39)
   - Adjust file paths if using different naming conventions
   - Modify constraints as needed for your specific well

### Available Make Targets

- `make well` - Run the completion tally calculation
- `make tests` - Run the test suite  
- `make install` - Install dependencies
- `make clean` - Clean temporary files
- `make help` - Show available commands

## Output

The system provides:
- Step-by-step completion calculations
- Required pipe counts and stand arrangements
- Final completion tally with specific equipment assignments
- Depth calculations and error margins
- Visual table showing pipe/stand assignments with top and bottom depths

## Testing

TallyNow includes a comprehensive test suite to ensure reliability:

```bash
# Run all tests
make tests

# Run specific test files
pytest tests/test_basic.py -v
pytest tests/test_utils.py -v
```

**Test Coverage:**
- ✅ CSV import and data processing
- ✅ Pipe, stand, and assembly operations  
- ✅ Calculation functions and utilities
- ✅ Error handling and edge cases
- 🔄 Integration tests and workflow validation

## Contributing

This project is open source and welcomes contributions! Areas for improvement include:

- Enhanced error handling and validation
- Support for additional file formats
- Web-based user interface
- Advanced optimization algorithms
- Integration with industry-standard software

### Development Setup

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Install dependencies: `make install`
4. Run tests to ensure everything works: `make tests`
5. Make your changes and add tests
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License allows you to use, modify, and distribute this software freely, including for commercial purposes.

## Disclaimer

This software is provided as-is for educational and research purposes. Always verify results with qualified engineering professionals before use in actual well operations.