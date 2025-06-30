"""
Tests for pipe classes in pipes.py
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pipes import Pipe, Stand, Rack, Pile, AssemblyPipe


class TestPipe:
    """Test basic Pipe functionality"""
    
    def test_pipe_creation(self):
        """Test creating a basic pipe"""
        pipe = Pipe('P1', 11.5)
        assert pipe.id == 'P1'
        assert pipe.length == 11.5
        assert pipe.num_pipes == 1
        assert pipe.pup == False
    
    def test_pipe_set_pup(self):
        """Test setting pipe as pup"""
        pipe = Pipe('PUP1', 2.5)
        pipe.set_pup()
        assert pipe.pup == True
    
    def test_pipe_string_representation(self):
        """Test pipe string representation"""
        pipe = Pipe('P1', 11.5)
        assert str(pipe) == 'P1'
    
    def test_pipe_comparison(self):
        """Test pipe comparison (should be by length)"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        pipe3 = Pipe('P3', 11.5)
        
        assert pipe1 < pipe2
        assert pipe2 > pipe1
        assert pipe1 <= pipe3
        assert pipe1 >= pipe3


class TestStand:
    """Test Stand functionality"""
    
    def test_triple_stand_creation(self):
        """Test creating a triple stand"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        pipe3 = Pipe('P3', 11.8)
        
        stand = Stand('T1', [pipe1, pipe2, pipe3])
        
        assert stand.id == 'T1'
        assert stand.num_pipes == 3
        assert stand.length == 35.3  # 11.5 + 12.0 + 11.8
        assert len(stand.pipes) == 3
        assert stand.pup == False
    
    def test_double_stand_creation(self):
        """Test creating a double stand"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        stand = Stand('D1', [pipe1, pipe2])
        
        assert stand.id == 'D1'
        assert stand.num_pipes == 2
        assert stand.length == 23.5  # 11.5 + 12.0
        assert len(stand.pipes) == 2
    
    def test_stand_string_representation(self):
        """Test stand string representation"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        stand = Stand('T1', [pipe1, pipe2])
        
        assert str(stand) == 'T1'
    
    def test_stand_comparison(self):
        """Test stand comparison (should be by length)"""
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        pipe3 = Pipe('P3', 10.0)
        
        stand1 = Stand('S1', [pipe1, pipe2])  # 23.5
        stand2 = Stand('S2', [pipe1, pipe3])  # 21.5
        
        assert stand2 < stand1
        assert stand1 > stand2


class TestRack:
    """Test Rack functionality"""
    
    def test_rack_creation(self):
        """Test creating an empty rack"""
        rack = Rack("triple stands")
        
        assert rack.name == "triple stands"
        assert rack.type == "triple stands"
        assert len(rack.stands) == 0
        assert rack.number_of_stands == 0
    
    def test_add_stands_to_rack(self):
        """Test adding stands to rack"""
        rack = Rack("triple stands")
        
        # Create some stands
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        stand1 = Stand('T1', [pipe1, pipe2])
        stand2 = Stand('T2', [pipe1, pipe2])
        
        rack.add_stands([stand1, stand2])
        
        assert len(rack.stands) == 2
        assert rack.number_of_stands == 2
        assert rack.stands[0].id == 'T1'
        assert rack.stands[1].id == 'T2'
    
    def test_get_available_stands(self):
        """Test getting available stands from rack"""
        rack = Rack("triple stands")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        stand = Stand('T1', [pipe1, pipe2])
        
        rack.add_stands([stand])
        available = rack.get_available()
        
        assert len(available) == 1
        assert available[0].id == 'T1'
    
    def test_remove_stand_from_rack(self):
        """Test removing a stand from rack"""
        rack = Rack("triple stands")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        stand1 = Stand('T1', [pipe1, pipe2])
        stand2 = Stand('T2', [pipe1, pipe2])
        
        rack.add_stands([stand1, stand2])
        assert rack.number_of_stands == 2
        
        rack.remove_stand()
        assert rack.number_of_stands == 1
        assert len(rack.stands) == 1


class TestPile:
    """Test Pile functionality"""
    
    def test_pile_creation(self):
        """Test creating an empty pile"""
        pile = Pile("single pipes")
        
        assert pile.name == "single pipes"
        assert pile.type == "single pipes"
        assert len(pile.pipes) == 0
        assert pile.number_of_pipes == 0
    
    def test_add_pipes_to_pile(self):
        """Test adding pipes to pile"""
        pile = Pile("single pipes")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        pile.add_pipes([pipe1, pipe2])
        
        assert len(pile.pipes) == 2
        assert pile.number_of_pipes == 2
        assert pile.pipes[0].id == 'P1'
        assert pile.pipes[1].id == 'P2'
    
    def test_get_available_pipes(self):
        """Test getting available pipes from pile"""
        pile = Pile("single pipes")
        
        pipe = Pipe('P1', 11.5)
        pile.add_pipes([pipe])
        
        available = pile.get_available()
        assert len(available) == 1
        assert available[0].id == 'P1'
    
    def test_remove_pipe_from_pile(self):
        """Test removing a pipe from pile"""
        pile = Pile("single pipes")
        
        pipe1 = Pipe('P1', 11.5)
        pipe2 = Pipe('P2', 12.0)
        
        pile.add_pipes([pipe1, pipe2])
        assert pile.number_of_pipes == 2
        
        pile.remove_pipe('P1')
        assert pile.number_of_pipes == 1
        
        # Check that P1 was removed and P2 remains
        remaining_ids = [p.id for p in pile.pipes]
        assert 'P1' not in remaining_ids
        assert 'P2' in remaining_ids


class TestAssemblyPipe:
    """Test AssemblyPipe functionality"""
    
    def test_assembly_pipe_creation(self):
        """Test creating an assembly pipe"""
        assembly = AssemblyPipe(
            name='packer',
            length=12.5,
            upper_limit=100.0,
            lower_limit=200.0,
            is_top_assembly=False,
            upper_clear=50.0,
            lower_clear=50.0,
            seration_pipes=2
        )
        
        assert assembly.name == 'packer'
        assert assembly.length == 12.5
        assert assembly.upper_limit == 100.0
        assert assembly.lower_limit == 200.0
        assert assembly.is_top_assembly == False
        assert assembly.upper_clear == 50.0
        assert assembly.lower_clear == 50.0
        assert assembly.seration_pipes == 2
        assert assembly.num_pipes == 1
        assert assembly.pup == False
    
    def test_top_assembly_creation(self):
        """Test creating a top assembly"""
        assembly = AssemblyPipe(
            name='plug',
            length=15.0,
            upper_limit=0,
            lower_limit=0,
            is_top_assembly=True,
            upper_clear=0,
            lower_clear=0,
            seration_pipes=0
        )
        
        assert assembly.is_top_assembly == True
        assert assembly.name == 'plug'
        assert assembly.length == 15.0
    
    def test_assembly_string_representation(self):
        """Test assembly string representation"""
        assembly = AssemblyPipe('test_assembly', 10.0, 0, 0, False, 0, 0, 0)
        assert str(assembly) == 'test_assembly'
    
    def test_assembly_comparison(self):
        """Test assembly comparison (should be by length like other pipes)"""
        assembly1 = AssemblyPipe('assy1', 10.0, 0, 0, False, 0, 0, 0)
        assembly2 = AssemblyPipe('assy2', 15.0, 0, 0, False, 0, 0, 0)
        
        assert assembly1 < assembly2
        assert assembly2 > assembly1