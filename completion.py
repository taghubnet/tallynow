from lib.pipes import AssemblyPipe

class Completion:
    def __init__(self, goal: float):
        self.goal = goal                # Know where to go
        self.solution = []              # Know how it got there
        self.assy_depth = {}            # Know depth of each assembly
        self.length = 0                 # Know how long the solution is
        self.done = False               # Know if solution is finished
        self.ea_since_prev = 0          # Number of pipes placed since previous assembly
        self.length_since_prev = 0      # Distance since previous assembly
        self.num_pipes = 0              # Total number of pipes used
        self.num_assemblies = 0         # Total number of assemblies used
        self.casing_joints = []         # Overview of casing joint depths
        self.ea_between_assemblies = [] # Number of pipes between each assembly, used for step 2
        self.num_pipe_types = {"triples": 0,\
                               "doubles": 0,\
                               "singles": 0,\
                               "pups": 0,\
                               "assemblies": 0} # Overview of number of each type of pipe
        self.leftover_tally = None      # Tally of unused stands and pipes

    def __repr__(self):
        return f"Completion goal: {self.goal}, done: {self.done}"

    def __str__(self):
        return f"\
{"Goal":.<20}: {self.goal}\n\
{"Length":.<20}: {self.length}\n\
{"Done":.<20}: {self.done}\n\
{"Number of pipes":.<20}: {self.num_pipes}\n\
{"Number of pipe types":.<20}: {self.num_pipe_types}\n\
{"Number of assemblies":.<20}: {self.num_assemblies}\n\
{"Solution":.<20}: {self.solution}."

    def add_assembly_pipe(self, assembly) -> None:
        self.solution.append(assembly)
        self.num_pipe_types["assemblies"] += 1
        self.length += assembly.length
        self.length = round(self.length, 3) # Keep length at 3 decimals.
        self.num_assemblies += 1

        # Store and update ea and length since previous assembly in order to find number of triples and doubles necessary.
        if self.ea_since_prev != 0:
            self.ea_between_assemblies.append(self.ea_since_prev)

        # Update ea and length since previous assembly
        self.ea_since_prev = 0
        self.length_since_prev = 0

    def add_normal_pipe(self, pipe) -> None:
        self.solution.append(pipe)
        self.length += pipe.length
        self.length = round(self.length, 3) # Keep length at 3 decimals.
        self.num_pipes += pipe.num_pipes

        # Update length and ea since previous assembly
        self.length_since_prev += pipe.length
        self.length_since_prev = round(self.length_since_prev, 3)
        self.ea_since_prev += pipe.num_pipes

        # Update overview of pipe types
        if pipe.num_pipes == 3:
            self.num_pipe_types["triples"] += 1
        elif pipe.num_pipes == 2:
            self.num_pipe_types["doubles"] += 1
        elif (pipe.num_pipes == 1) and (pipe.pup == False):
            self.num_pipe_types["singles"] += 1
        elif (pipe.num_pipes == 1) and (pipe.pup == True):
            self.num_pipe_types["pups"] += 1

    def update_pipe_numbers(self):
        """Finds the required number of stands, used in step 2"""
        self.num_pipe_types = {"triples": 0, "doubles": 0, "singles": 0}
        if self.ea_since_prev:
            self.ea_between_assemblies.append(self.ea_since_prev)
            self.ea_since_prev = 0
        for ea in self.ea_between_assemblies:
            total = ea
            self.num_pipe_types["triples"] += total // 3
            total = total % 3
            self.num_pipe_types["doubles"] += total // 2
            total = total % 2
            self.num_pipe_types["singles"] += total
        return
    
    def add_casing_joints(self, joints) -> None:
        self.casing_joints = joints

    def get_number_of_pipe_types(self):
        return self.num_pipe_types
    
    def get_solution_depths(self):
        """Solution is stored as the completion length, that is bottom->top.
        This function reverses this in order to get the depths"""
        reversed_solution = list(reversed(self.solution))
        depth = 0
        solution_depths = {}
        for pipe in reversed_solution:
            solution_depths[pipe.id] = [round(depth, 3), round(depth+pipe.length, 3)]
            depth += pipe.length
            if (type(pipe) == AssemblyPipe) and (pipe.critical_point != None):
                solution_depths[pipe.id].append(round(depth-pipe.critical_point, 3))
        return solution_depths
    
    def get_length_error(self):
        return self.goal - self.length
    
    def add_leftover_tally(self, tally):
        self.leftover_tally = tally
    
    def print_leftover_tally(self):
        for tally in self.leftover_tally:
            if tally.type == "triple stands" or tally.type == "double stands":
                print(tally.stands)
            else:
                print(tally.pipes)
