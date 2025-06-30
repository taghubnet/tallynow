class Pipe:
    def __init__(self, id, length, pup=False):
        self.id = id
        self.length = length
        self.num_pipes = 1
        self.pup = pup # Boolean for specifying whether the pipe is a pup
    
    def __repr__(self):
        return f"{self.id}"
    
    def __str__(self):
        return f"Pipe ID: {self.id}, l = {self.length}"
    
    def __lt__(self, other):
        return self.length < other.length
    
    def set_pup(self):
        self.pup = True


class AssemblyPipe:
    def __init__(self, 
                 id, 
                 length, 
                 lower_lim=None, 
                 upper_lim=None, 
                 sep_length=None, 
                 sep_ea=None, 
                 critical_point=None, 
                 is_top_assembly=False):
        
        self.id = id
        self.length = length # Length in meters

        # Top assembly constraint (used for tubing hanger)
        self.is_top_assembly = False    
        self.top_assembly_clear = True  # Flag describing whether the constraint is clear

        # General constraints
        self.lower_lim = None           # Depth in meters
        self.upper_lim = None           # Depth in meters
        self.sep_length = None          # Length in meters
        self.sep_ea = None              # Number of pipes
        self.ll_clear = True            # Flag describing whether the constraint is clear
        self.ul_clear = True            # ---||---
        self.sep_length_clear = True    # ---||---
        self.sep_ea_clear = True        # ---||---

        # Casing connection avoidance
        self.critical_point = None          # meters from bottom of assembly
        self.critical_point_clear = True    # Flag describing whether the constraint is clear
        self.critical_margin = 1.5          # meters margin above and below critical point

        # Update constraints if the AssemblyPipe is initialized with values for constraints.
        self.set_lower_limit(lower_lim)
        self.set_upper_limit(upper_lim)
        self.set_sep_length(sep_length)
        self.set_sep_ea(sep_ea)
        self.set_critical_point(critical_point)
        self.set_top_assembly(is_top_assembly)

    def __repr__(self):
        return str(self.id)
    
    def __str__(self):
        return f"\
{"ID":.<22}: {self.id}\n\
{"Length":.<22}: {self.length}\n\
{"Is top assembly":.<22}: {self.is_top_assembly}\n\
{"Lower limit depth":.<22}: {self.lower_lim}\n\
{"Upper limit depth":.<22}: {self.upper_lim}\n\
{"Length from last":.<22}: {self.sep_length}\n\
{"Pipe lengths from last":.<22}: {self.sep_ea}"
    
    def set_lower_limit(self, value):
        """Set limit value and update the constraint flag."""
        self.lower_lim = value
        if value == None:
            self.ll_clear = True
        else:
            self.ll_clear = False
    
    def set_upper_limit(self, value):
        """Set limit value and update the constraint flag."""
        self.upper_lim = value
        self.ul_clear = True # This parameter is True initially as the pipe is built bottom-up

    def set_sep_length(self, value):
        """Set limit value and update the constraint flag."""
        self.sep_length = value
        if value == None:
            self.sep_length_clear = True
        else:
            self.sep_length_clear = False

    def set_sep_ea(self, value):
        """Set limit value and update the constraint flag."""
        self.sep_ea = value
        if value == None:
            self.sep_ea_clear = True
        else:
            self.sep_ea_clear = False
    
    def set_critical_point(self, value):
        """Set limit value and update the constraint flag."""
        self.critical_point = value
        if value == None:
            self.critical_point_clear = True
        else:
            self.critical_point_clear = False
    
    def set_top_assembly(self, value):
        # Used only for tubing hanger.
        self.is_top_assembly = value

    def update_lower_limit_clear(self, completion) -> None:
        """ Boolean update to ll_clear.
        True if full pipe is above lower limit
        False otherwise
        """
        if self.lower_lim:
            if completion.length >= completion.goal - self.lower_lim:
                self.ll_clear = True
            else:
                self.ll_clear = False
        return

    def update_upper_limit_clear(self, completion) -> None:
        """Boolean update to ul_clear.
        True if full pipe is below upper limit
        False otherwise
        """
        if self.upper_lim:
            if (completion.length+self.length) >= completion.goal - self.upper_lim:
                self.ul_clear = False
            else:
                self.ul_clear = True
        return

    def update_sep_length_clear(self, completion) -> None:
        """Boolean update to sep_length_clear.
        True if the distance from the previous assembly is more than or equal to the sep_length
        False otherwise
        """
        if self.sep_length:
            if completion.length_since_prev >= self.sep_length:
                self.sep_length_clear = True
            else:
                self.sep_length_clear = False
        return

    def update_sep_ea_clear(self, completion) -> None:
        """Boolean update to sep_ea_clear.
        True if the number of pipes from the previous assembly is more than or equal to the sep_ea
        False otherwise

        Note: 'ea' abbreviation is used poorly here, sep_ea is just "pipes between". 
        """
        if self.sep_ea:
            if completion.ea_since_prev >= self.sep_ea:
                self.sep_ea_clear = True
            else:
                self.sep_ea_clear = False
        return
    
    def update_critical_point_clear(self, completion) -> None:
        """Boolean update to critical_point_clear.
        True if there are no casing joints within the margins of the critical point
        False otherwise
        """
        if self.critical_point:
            if completion.casing_joints == []:
                raise RuntimeError("No casing joints in completion.")
            
            # Find the depth of the critical point in the well
            critical_point_depth = completion.goal-(completion.length+self.critical_point)
            # Find the casing joint closest to the critical point depth
            closest_connection = min(completion.casing_joints, key=lambda x:abs(x-critical_point_depth))
            if abs(closest_connection-critical_point_depth) > self.critical_margin:
                self.critical_point_clear = True
            else:
                self.critical_point_clear = False
        return
    
    def update_top_assembly_clear(self, value) -> None:
        """This function works differently to the other update functions.
        It must be activated when checking for normal pipes."""
        self.top_assembly_clear = value

    def update_all_clears(self, completion):
        """Run all 'update_clear' functions, except for the one for top assembly."""
        self.update_lower_limit_clear(completion)
        self.update_upper_limit_clear(completion)
        self.update_sep_length_clear(completion)
        self.update_sep_ea_clear(completion)
        self.update_critical_point_clear(completion)

    def check_lower_limit_clear(self, completion, pipe):
        """Works the same way as the corresponding 'update' function, but it conciders an added pipe
        and checks whether the addition of this pipe will clear the constraint"""
        if self.lower_lim:
            if completion.length + pipe.length < completion.goal - self.lower_lim:
                return False
        return True

    def check_upper_limit_clear(self, completion, pipe):
        """Works the same way as the corresponding 'update' function, but it conciders an added pipe
        and checks whether the addition of this pipe will clear the constraint"""
        if self.upper_lim:
            if completion.length + pipe.length + self.length > self.upper_lim:
                return False
        return True

    def check_sep_length_clear(self, completion, pipe):
        """Works the same way as the corresponding 'update' function, but it conciders an added pipe
        and checks whether the addition of this pipe will clear the constraint"""
        if self.sep_length:
            if completion.length_since_prev + pipe.length < self.sep_length:
                return False
        return True

    def check_sep_ea_clear(self, completion, pipe):
        """Works the same way as the corresponding 'update' function, but it conciders an added pipe
        and checks whether the addition of this pipe will clear the constraint"""
        if self.sep_ea:
            if completion.ea_since_prev + pipe.num_pipes < self.sep_ea:
                return False
        return True

    def check_critical_point_clear(self, completion, pipe):
        """Works the same way as the corresponding 'update' function, but it conciders an added pipe
        and checks whether the addition of this pipe will clear the constraint"""
        if self.critical_point:
            if completion.casing_joints == []:
                raise RuntimeError("No casing joints in completion.")

            new_completion_length = completion.length + pipe.length
            critical_point_depth = completion.goal-(new_completion_length+self.critical_point)
            closest_connection = min(completion.casing_joints, key=lambda x:abs(x-critical_point_depth))
            if abs(closest_connection-critical_point_depth) < self.critical_margin:
                return False
        return True

    def check_all_clears_with_pipe(self, completion, pipe):
        """Run all 'check_clear' functions."""
        ll = self.check_lower_limit_clear(completion, pipe)
        ul = self.check_upper_limit_clear(completion, pipe)
        sl = self.check_sep_length_clear(completion, pipe)
        se = self.check_sep_ea_clear(completion, pipe)
        cp = self.check_critical_point_clear(completion, pipe)
        return ll and ul and sl and se and cp

    def is_available(self):
        """Checks status of all clear flags"""
        return self.ll_clear and self.ul_clear and self.sep_length_clear and self.sep_ea_clear and self.critical_point_clear


class Stand:
    def __init__(self, id, pipes=[]):
        self.id = id
        self.length = 0
        self.pipes = pipes
        self.num_pipes = 0
        self.__update_length() # Updates length if pipes are added on initialization

    def __repr__(self):
        return f"{self.id}"
    
    def __str__(self):
        return f"\
{"Stand ID":.<9}: {self.id}\n\
{"Length":.<9}: {self.length}\n\
{"Num pipes":.<9}: {self.num_pipes}\n\
{"Pipes":.<9}: {self.pipes}"
    
    def __lt__(self, other):
        return self.length < other.length
    
    def reset_pipes(self):
        self.pipes = []
        self.length = 0
        self.num_pipes = 0
    
    def set_pipes(self, pipe_list):
        for pipe in pipe_list:
            self.pipes.append(pipe)
            self.length += pipe.length
        self.length = round(self.length, 3) # Limit decimals to 3 points
        self.num_pipes = len(self.pipes)

    def change_pipe(self, old_pipe_id, new_pipe):
        for i, pipe in enumerate(self.pipes):
            if pipe.id == old_pipe_id:
                self.pipes[i] = new_pipe
        self.__update_length()

    def __update_length(self):
        self.length = 0
        for pipe in self.pipes:
            self.length += pipe.length
            self.num_pipes += 1 # Number of pipes is also updated when length is updated.
        self.length = round(self.length, 3)


class Rack:
    """This is to hold double and triple stands in order. The order is 'first in, last out'. """
    def __init__(self, type):
        self.type = type # Define the type of rack: triples, doubles, singles etc.
        self.stands = []

    def __repr__(self):
        return f"Rack: {self.type}"
    
    def __str__(self):
        return f"{"Rack":.<6}: {self.type}\n{"Stands":.<6}: {self.stands}"

    def add_stands(self, stand_list):
        if type(stand_list) == Stand:
            self.stands.append(stand_list)  # Singular stands can be appended.
        else:
            self.stands += stand_list       # List of stands must be added to not create sublists.

    def get_available(self):
        """Peek the outmost stand/pipe in rack"""
        if self.stands == []:
            return []
        return [self.stands[-1]] # Return the last added element, i.e. the outmost stand/pipe
        
    def remove_stand(self):
        """Remove outmost stand/pipe from rack"""
        if self.stands == []:
            return None
        return self.stands.pop()


class Pile:
    """This is to keep singles and pups in one place, but order is not important. In piles, all elements are always available."""
    def __init__(self, type):
        self.type = type # Define the type of rack: triples, doubles, singles etc.
        self.pipes = []

    def __repr__(self):
        return f"Pile: {self.type}"
    
    def __str__(self):
        return f"{"Pile":.<5}: {self.type}\n{"Pipes":.<5}: {self.pipes}"

    def add_pipes(self, pipe_list):
        if type(pipe_list) == Pipe:
            self.pipes.append(pipe_list)    # Singular pipes can be appended
        else:
            self.pipes += pipe_list         # List of pipes must be added to not create sublists.

    def get_available(self):
        return self.pipes
        
    def remove_pipe(self, id):
        for i, pipe in enumerate(self.pipes):
            if pipe.id == id:
                return self.pipes.pop(i) # Remove the specific pipe.
        return None
