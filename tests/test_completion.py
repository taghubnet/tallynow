"""
Tests for completion functionality in completion.py
"""

import pytest
from completion import Completion
from pipes import Pipe, AssemblyPipe


class TestCompletion:
    """Test Completion class functionality"""
    
    def test_completion_creation(self):
        """Test creating a new completion"""
        completion = Completion(1000.0)
        
        assert completion.goal == 1000.0
        assert completion.length == 0.0
        assert completion.done == False
        assert len(completion.solution) == 0
        assert len(completion.casing_joints) == 0
        assert completion.num_normal_pipes == 0
        assert completion.num_assemblies == 0
    
    def test_add_normal_pipe(self):
        """Test adding a normal pipe to completion"""
        completion = Completion(100.0)
        pipe = Pipe('P1', 11.5)
        
        completion.add_normal_pipe(pipe)
        
        assert completion.length == 11.5
        assert completion.num_normal_pipes == 1
        assert len(completion.solution) == 1
        assert completion.solution[0] == pipe
    
    def test_add_assembly_pipe(self):
        """Test adding an assembly pipe to completion"""
        completion = Completion(100.0)
        assembly = AssemblyPipe('packer', 12.5, 0, 0, False, 0, 0, 0)
        
        completion.add_assembly_pipe(assembly)
        
        assert completion.length == 12.5
        assert completion.num_assemblies == 1
        assert len(completion.solution) == 1
        assert completion.solution[0] == assembly
    
    def test_add_casing_joints(self):
        """Test adding casing joints to completion"""
        completion = Completion(100.0)
        casing_lengths = [10.5, 12.0, 11.8]
        
        completion.add_casing_joints(casing_lengths)
        
        assert len(completion.casing_joints) == 3
        assert completion.casing_joints == casing_lengths
    
    def test_get_length_error(self):
        """Test calculating length error"""
        completion = Completion(100.0)
        pipe = Pipe('P1', 95.0)
        
        completion.add_normal_pipe(pipe)
        
        error = completion.get_length_error()
        assert error == 5.0  # 100.0 - 95.0
    
    def test_get_length_error_overshoot(self):
        """Test length error when overshooting goal"""
        completion = Completion(100.0)
        pipe = Pipe('P1', 105.0)
        
        completion.add_normal_pipe(pipe)
        
        error = completion.get_length_error()
        assert error == -5.0  # 100.0 - 105.0 (negative means overshoot)
    
    def test_update_pipe_numbers(self):
        """Test updating pipe type counts"""
        completion = Completion(200.0)
        
        # Add various pipe types
        triple_stand = Pipe('T1', 35.0)
        triple_stand.num_pipes = 3
        
        double_stand = Pipe('D1', 24.0)
        double_stand.num_pipes = 2
        
        single_pipe = Pipe('S1', 12.0)
        single_pipe.num_pipes = 1
        
        pup = Pipe('PUP1', 2.5)
        pup.num_pipes = 1
        pup.set_pup()
        
        assembly = AssemblyPipe('assy1', 10.0, 0, 0, False, 0, 0, 0)
        
        completion.add_normal_pipe(triple_stand)
        completion.add_normal_pipe(double_stand)
        completion.add_normal_pipe(single_pipe)
        completion.add_normal_pipe(pup)
        completion.add_assembly_pipe(assembly)
        
        completion.update_pipe_numbers()
        
        pipe_counts = completion.get_number_of_pipe_types()
        assert pipe_counts['triples'] == 1
        assert pipe_counts['doubles'] == 1
        assert pipe_counts['singles'] == 1
        assert pipe_counts['pups'] == 1
        assert pipe_counts['assemblies'] == 1
    
    def test_get_solution_depths(self):
        """Test getting solution with depth calculations"""
        completion = Completion(50.0)
        
        pipe1 = Pipe('P1', 20.0)
        pipe2 = Pipe('P2', 15.0)
        assembly = AssemblyPipe('assy1', 10.0, 0, 0, False, 0, 0, 0)
        
        completion.add_normal_pipe(pipe1)
        completion.add_assembly_pipe(assembly)
        completion.add_normal_pipe(pipe2)
        
        depths = completion.get_solution_depths()
        
        # Should have entries for each component
        assert 'P1' in depths
        assert 'assy1' in depths
        assert 'P2' in depths
        
        # Check depth calculations
        # P1: 0 to 20
        assert depths['P1'][0] == 0
        assert depths['P1'][1] == 20.0
        
        # assy1: 20 to 30
        assert depths['assy1'][0] == 20.0
        assert depths['assy1'][1] == 30.0
        
        # P2: 30 to 45
        assert depths['P2'][0] == 30.0
        assert depths['P2'][1] == 45.0
    
    def test_string_representation(self):
        """Test completion string representation"""
        completion = Completion(100.0)
        pipe = Pipe('P1', 50.0)
        completion.add_normal_pipe(pipe)
        
        str_repr = str(completion)
        
        # Should contain key information
        assert 'Goal' in str_repr
        assert 'Length' in str_repr
        assert 'Done' in str_repr
        assert '100' in str_repr
        assert '50' in str_repr
    
    def test_completion_done_status(self):
        """Test completion done status"""
        completion = Completion(100.0)
        
        # Initially not done
        assert completion.done == False
        
        # Add pipe that reaches goal
        pipe = Pipe('P1', 100.0)
        completion.add_normal_pipe(pipe)
        
        # Should still not be automatically done (needs to be set manually)
        assert completion.done == False
        
        # Set done manually
        completion.done = True
        assert completion.done == True
    
    def test_mixed_solution_order(self):
        """Test that solution maintains order of addition"""
        completion = Completion(100.0)
        
        pipe1 = Pipe('P1', 20.0)
        assembly = AssemblyPipe('assy1', 15.0, 0, 0, False, 0, 0, 0)
        pipe2 = Pipe('P2', 25.0)
        
        completion.add_normal_pipe(pipe1)
        completion.add_assembly_pipe(assembly)
        completion.add_normal_pipe(pipe2)
        
        solution = completion.solution
        
        assert len(solution) == 3
        assert solution[0].id == 'P1'
        assert solution[1].name == 'assy1'
        assert solution[2].id == 'P2'


class TestCompletionEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_zero_goal_completion(self):
        """Test completion with zero goal"""
        completion = Completion(0.0)
        
        assert completion.goal == 0.0
        assert completion.get_length_error() == 0.0
    
    def test_negative_goal_completion(self):
        """Test completion with negative goal (unusual but should work)"""
        completion = Completion(-10.0)
        
        pipe = Pipe('P1', 5.0)
        completion.add_normal_pipe(pipe)
        
        # Error should be negative goal minus positive length
        error = completion.get_length_error()
        assert error == -15.0  # -10.0 - 5.0
    
    def test_empty_solution_depths(self):
        """Test getting depths from empty solution"""
        completion = Completion(100.0)
        
        depths = completion.get_solution_depths()
        assert isinstance(depths, dict)
        assert len(depths) == 0
    
    def test_very_large_completion(self):
        """Test completion with very large goal"""
        completion = Completion(10000.0)
        
        # Add many pipes
        for i in range(100):
            pipe = Pipe(f'P{i}', 50.0)
            completion.add_normal_pipe(pipe)
        
        assert completion.length == 5000.0  # 100 * 50
        assert len(completion.solution) == 100
        assert completion.get_length_error() == 5000.0  # 10000 - 5000