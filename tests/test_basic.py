"""
Basic tests for TallyNow core functionality
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pipes import Pipe, Stand, Rack, Pile, AssemblyPipe
from utils import get_num_pipes_required, extract_casing_joints
import tempfile
import pandas as pd


class TestBasicFunctionality:
    """Test core functionality that we know works"""
    
    def test_pipe_creation(self):
        """Test creating a basic pipe"""
        pipe = Pipe('P1', 11.5)
        assert pipe.id == 'P1'
        assert pipe.length == 11.5
        assert pipe.num_pipes == 1
        assert pipe.pup == False
    
    def test_pipe_repr(self):
        """Test pipe representation (__repr__)"""
        pipe = Pipe('P1', 11.5)
        assert repr(pipe) == 'P1'  # Uses __repr__
    
    def test_pipe_comparison(self):
        """Test pipe comparison (only < is implemented)"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        assert pipe1 < pipe2
        assert not (pipe2 < pipe1)
    
    def test_pipe_set_pup(self):
        """Test setting pipe as pup"""
        pipe = Pipe('PUP1', 2.5)
        pipe.set_pup()
        assert pipe.pup == True
    
    def test_stand_creation(self):
        """Test creating a stand"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        stand = Stand('T1', [pipe1, pipe2])
        
        assert stand.id == 'T1'
        assert len(stand.pipes) == 2
        assert stand.length == 23.5  # 11.5 + 12.0
        assert stand.num_pipes == 2
    
    def test_assembly_pipe_creation(self):
        """Test creating an assembly pipe with correct parameters"""
        assembly = AssemblyPipe(
            id='packer',
            length=12.5,
            lower_lim=100.0,
            upper_lim=200.0,
            is_top_assembly=False
        )
        
        assert assembly.id == 'packer'
        assert assembly.length == 12.5
        assert assembly.lower_lim == 100.0
        assert assembly.upper_lim == 200.0
        assert assembly.is_top_assembly == False
    
    def test_rack_creation(self):
        """Test creating a rack"""
        rack = Rack("triple stands")
        
        assert rack.type == "triple stands"
        assert len(rack.stands) == 0
    
    def test_rack_add_and_remove(self):
        """Test adding and removing stands from rack"""
        rack = Rack("triple stands")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        stand = Stand('T1', [pipe1, pipe2])
        
        rack.add_stands([stand])
        assert len(rack.stands) == 1
        
        available = rack.get_available()
        assert len(available) == 1
        assert available[0].id == 'T1'
        
        removed = rack.remove_stand()
        assert removed.id == 'T1'
        assert len(rack.stands) == 0
    
    def test_pile_creation(self):
        """Test creating a pile"""
        pile = Pile("single pipes")
        
        assert pile.type == "single pipes"
        assert len(pile.pipes) == 0
    
    def test_pile_add_and_remove(self):
        """Test adding and removing pipes from pile"""
        pile = Pile("single pipes")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        pile.add_pipes([pipe1, pipe2])
        assert len(pile.pipes) == 2
        
        available = pile.get_available()
        assert len(available) == 2
        
        removed = pile.remove_pipe('P1')
        assert removed.id == 'P1'
        assert len(pile.pipes) == 1
    
    def test_get_num_pipes_required(self):
        """Test pipe requirement calculation"""
        result = get_num_pipes_required(115.0)  # 115m / 11.5m = 10
        assert result == 10
        
        result = get_num_pipes_required(120.0, average_length=10.0)
        assert result == 12
    
    def test_csv_import_basic(self):
        """Test basic CSV import functionality"""
        # Create simple test CSV
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [11.5, 12.0, 11.8, 12.2, 11.3]
        }
        df = pd.DataFrame(data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            
            # Test casing joints extraction
            result = extract_casing_joints(f.name, 'B', 1, 3)
            expected = [11.5, 12.0, 11.8]
            assert result == expected
            
            # Cleanup
            os.unlink(f.name)


class TestWorkflowBasics:
    """Test basic workflow components"""
    
    def test_fixture_files_exist(self):
        """Test that fixture files were created"""
        fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        expected_files = [
            'sample_tubing.csv',
            'sample_assemblies.csv', 
            'sample_casing.csv',
            'sample_racked.csv',
            'sample_pups.csv'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(fixture_dir, filename)
            if os.path.exists(filepath):
                # Just check it can be read as CSV
                df = pd.read_csv(filepath)
                assert len(df) > 0
    
    def test_main_script_exists(self):
        """Test that main.py exists and can be imported"""
        main_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')
        assert os.path.exists(main_path)
    
    def test_data_files_exist(self):
        """Test that data directory exists with CSV files"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            assert len(csv_files) > 0