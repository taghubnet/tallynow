# TallyNow Test Suite

This directory contains tests for the TallyNow upper completion tally system.

## Running Tests

Make sure you have pytest installed:
```bash
pip install pytest
```

Run all tests:
```bash
pytest tests/ -v
```

Run specific test files:
```bash
pytest tests/test_basic.py -v
pytest tests/test_utils.py -v
```

## Test Files

- **test_basic.py**: Core functionality tests for pipes, stands, racks, and basic operations
- **test_utils.py**: Tests for utility functions including CSV import and calculations
- **fixtures/**: Sample CSV data files for testing

## Test Coverage

### Currently Tested:
✅ **CSV Import Functions**: Data extraction, type conversion, error handling  
✅ **Pipe Classes**: Pipe, Stand, Rack, Pile creation and operations  
✅ **Assembly Classes**: AssemblyPipe creation and basic properties  
✅ **Utility Functions**: Pipe calculations, ID mapping  
✅ **Error Handling**: Invalid data, out-of-bounds ranges, missing files  

### Future Test Areas:
- **Completion Algorithm**: Full optimization workflow testing
- **Integration Tests**: End-to-end workflow with real data
- **Constraint Validation**: Assembly limit checking
- **Performance Tests**: Large dataset processing

## Fixtures

Test fixtures in `fixtures/` provide sample data that mimics real CSV files:
- `sample_tubing.csv`: Pipe inventory data
- `sample_assemblies.csv`: Downhole equipment specifications  
- `sample_casing.csv`: Casing joint information
- `sample_racked.csv`: Pre-arranged pipe stands
- `sample_pups.csv`: Short pipe sections

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure all existing tests pass
3. Add fixture data if needed for integration tests
4. Update this README with new test coverage