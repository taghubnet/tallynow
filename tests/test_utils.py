"""
Tests for utility functions in utils.py
"""

import pytest
import os
import tempfile
import pandas as pd
from utils import (
    extract_casing_joints, 
    extract_deck_tally, 
    extract_ids, 
    extract_csv_rows_to_list,
    get_num_pipes_required,
    ids_to_pipes
)
from pipes import Pipe


class TestCSVImportFunctions:
    """Test CSV import functionality"""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file for testing"""
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [11.5, 12.0, 11.8, 'invalid', 12.3],
            'C': ['text1', 'text2', 'text3', 'text4', 'text5']
        }
        df = pd.DataFrame(data)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            return f.name
    
    def test_extract_casing_joints_valid_data(self, sample_csv_file):
        """Test extracting casing joints with valid numeric data"""
        result = extract_casing_joints(sample_csv_file, 'A', 1, 3)
        expected = [1.0, 2.0, 3.0]
        assert result == expected
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_extract_casing_joints_with_invalid_data(self, sample_csv_file):
        """Test extracting from column with mixed data types"""
        result = extract_casing_joints(sample_csv_file, 'B', 1, 5)
        expected = [11.5, 12.0, 11.8, 12.3]  # Should skip 'invalid'
        assert result == expected
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_extract_deck_tally_valid_data(self, sample_csv_file):
        """Test extracting deck tally data"""
        result = extract_deck_tally(sample_csv_file, 'B', 1, 3)
        expected = [11.5, 12.0, 11.8]
        assert result == expected
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_extract_ids_valid_data(self, sample_csv_file):
        """Test extracting IDs (rounded integers)"""
        result = extract_ids(sample_csv_file, 'A', 2, 4)
        expected = [2, 3, 4]
        assert result == expected
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_invalid_column_letter(self, sample_csv_file):
        """Test error handling for invalid column"""
        with pytest.raises(ValueError, match="Column Z not found"):
            extract_casing_joints(sample_csv_file, 'Z', 1, 3)
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_out_of_bounds_rows(self, sample_csv_file):
        """Test error handling for out of bounds row range"""
        with pytest.raises(ValueError, match="Row range .* is out of bounds"):
            extract_casing_joints(sample_csv_file, 'A', 1, 100)
        
        # Cleanup
        os.unlink(sample_csv_file)
    
    def test_extract_csv_rows_to_list(self):
        """Test extracting all rows to list format"""
        # Create test CSV with known data
        test_data = [
            [1, 'A', 11.5, True, None, 2.5, 'X', 'Y'],
            [2, 'B', 12.0, False, 3.0, 1.8, 'Z', 'W']
        ]
        df = pd.DataFrame(test_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            
            result = extract_csv_rows_to_list(f.name)
            
            # Check structure (should have 2 rows, 8 columns each)
            assert len(result) == 2
            assert len(result[0]) == 8
            assert len(result[1]) == 8
            
            # Check some values
            assert result[0][0] == 1
            assert result[0][1] == 'A'
            assert result[0][2] == 11.5
            
            # Cleanup
            os.unlink(f.name)


class TestUtilityFunctions:
    """Test utility calculation functions"""
    
    def test_get_num_pipes_required_default_length(self):
        """Test pipe requirement calculation with default average length"""
        result = get_num_pipes_required(115.0)  # 115m / 11.5m = 10
        assert result == 10
    
    def test_get_num_pipes_required_custom_length(self):
        """Test pipe requirement calculation with custom average length"""
        result = get_num_pipes_required(120.0, average_length=10.0)
        assert result == 12
    
    def test_get_num_pipes_required_fractional_result(self):
        """Test that result is properly rounded down"""
        result = get_num_pipes_required(118.0)  # 118 / 11.5 = 10.26... -> 10
        assert result == 10
    
    def test_ids_to_pipes(self):
        """Test finding pipes by ID from tally"""
        # Create test pipes
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        pipe3 = Pipe('P3', 11.8)
        
        tally = [pipe1, pipe2, pipe3]
        
        # Test finding existing pipes
        result = ids_to_pipes(tally, ['P1', 'P3'])
        assert len(result) == 2
        assert result[0].id == 'P1'
        assert result[1].id == 'P3'
        assert result[0].length == 11.5
        assert result[1].length == 11.8
    
    def test_ids_to_pipes_nonexistent_id(self):
        """Test behavior with non-existent pipe ID"""
        pipe1 = Pipe('P1', 11.5)
        tally = [pipe1]
        
        result = ids_to_pipes(tally, ['P1', 'P999'])  # P999 doesn't exist
        assert len(result) == 1  # Should only find P1
        assert result[0].id == 'P1'
    
    def test_ids_to_pipes_empty_tally(self):
        """Test with empty tally"""
        result = ids_to_pipes([], ['P1'])
        assert result == []
    
    def test_ids_to_pipes_empty_ids(self):
        """Test with empty ID list"""
        pipe1 = Pipe('P1', 11.5)
        tally = [pipe1]
        
        result = ids_to_pipes(tally, [])
        assert result == []


class TestFixtureData:
    """Test that our fixture files are valid"""
    
    def test_sample_tubing_fixture(self):
        """Test that sample tubing fixture can be loaded"""
        fixture_path = os.path.join('tests', 'fixtures', 'sample_tubing.csv')
        if os.path.exists(fixture_path):
            df = pd.read_csv(fixture_path)
            assert len(df) > 0
            assert 'ID' in df.columns
            assert 'Length' in df.columns
    
    def test_sample_assemblies_fixture(self):
        """Test that sample assemblies fixture can be loaded"""
        fixture_path = os.path.join('tests', 'fixtures', 'sample_assemblies.csv')
        if os.path.exists(fixture_path):
            df = pd.read_csv(fixture_path)
            assert len(df) > 0
            assert 'name' in df.columns
            assert 'length' in df.columns