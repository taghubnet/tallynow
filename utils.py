from completion import Completion
from pipes import AssemblyPipe, Pipe, Stand, Rack, Pile
from import_casing import extract_deck_tally, extract_ids, extract_excel_rows_to_list

def get_deck_tally(dt_path, dt_sheet, dt_column_ids, dt_column_lengths, dt_start, dt_end, are_pups=False):
    """Extract id and length of all pipes in deck tally from an excel file"""

    deck_tally_ids = extract_deck_tally(dt_path, dt_sheet, dt_column_ids, dt_start, dt_end)
    deck_tally_lengths = extract_deck_tally(dt_path, dt_sheet, dt_column_lengths, dt_start, dt_end)

    deck_tally = []
    for i, length in enumerate(deck_tally_lengths):
        pipe = Pipe(deck_tally_ids[i], length)
        
        # Define pups if the tally is a pup tally
        if are_pups == True:
            pipe.set_pup()

        deck_tally.append(pipe)
    return deck_tally

def get_triple_stands_from_file(path, sheet, column, start_row, stop_row, deck_tally):
    """Get pipes in triple stands from excel file and create the stands."""

    pipe_ids = extract_ids(path, sheet, column, start_row, stop_row)
    stands = []
    for i in range(len(pipe_ids)//3):
        stand_pipe_ids = pipe_ids[0:3]
        stand_pipes = ids_to_pipes(deck_tally, stand_pipe_ids)
        pipe_ids = pipe_ids[3:]
        stands.append(Stand(i+1, stand_pipes))
    return stands

def get_double_stands_from_file(path, sheet, column, start_row, stop_row, deck_tally):
    """Get pipes in double stands from excel file and create the stands."""

    pipe_ids = extract_ids(path, sheet, column, start_row, stop_row)
    stands = []
    for i in range(len(pipe_ids)//2):
        stand_pipe_ids = pipe_ids[0:2]
        stand_pipes = ids_to_pipes(deck_tally, stand_pipe_ids)
        pipe_ids = pipe_ids[2:]
        stands.append(Stand("Dbl"+str(i+1), stand_pipes))
    return stands

def get_assemblies_from_file(path):
    """Get assemblies from file.
    Warning: This function requires a strict structure on the assembly file."""

    assembly_list = extract_excel_rows_to_list(path)
    assemblies = []
    for row in assembly_list:
        new_assembly = AssemblyPipe(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        assemblies.append(new_assembly)
    return assemblies

def ids_to_pipes(tally, ids):
    """Gets the pipes that correspond to the ids from the tally"""
    pipes = []
    for id in ids:
        pipes += [pipe for pipe in tally if pipe.id == id]
    return pipes

def get_available_pipes(tally):
    """Returns the available stands, pipes and pups from the full deck tally"""
    available = []
    for rack in tally:
        available += rack.get_available()
    return available

def get_available_pipes_excluding_pups(tally):
    """Returns the available stands and pipes from the full deck tally"""
    available = []
    for rack in tally:
        if rack.type == "pups":
            continue
        available += rack.get_available()
    return available

def create_deck_tally(triples, doubles, singles, pups):
    triple_rack = Rack("triple stands")
    triple_rack.add_stands(triples)

    double_rack = Rack("double stands")
    double_rack.add_stands(doubles)

    single_pile = Pile("single pipes")
    single_pile.add_pipes(singles)

    pup_pile = Pile("pups")
    pup_pile.add_pipes(pups)

    return [triple_rack, double_rack, single_pile, pup_pile]

def remove_stand_pipes_from_tally(stands, tally):
    new_tally = []
    stand_pipes = []
    for stand in stands:
        stand_pipes += stand.pipes
    for pipe in tally:
        if pipe not in stand_pipes:
            new_tally.append(pipe)
    return new_tally

def remove_from_tally(tally, pipe):
    """Remove the input pipe from the tally in order to avoid re using the same pipe"""
    if pipe.num_pipes == 3:
        tally[0].remove_stand()
    elif pipe.num_pipes == 2:
        tally[1].remove_stand()
    elif (pipe.num_pipes == 1) and (pipe.pup == False):
        tally[2].remove_pipe(pipe.id)
    elif (pipe.num_pipes == 1) and (pipe.pup == True):
        tally[3].remove_pipe(pipe.id)
    return tally

# Step 1 Find number of normal pipes to order.
def get_num_pipes_required(goal, average_length=11.5) -> int:
    return int(goal // average_length)

# Step 2 Find number of triple- and double stands to be racked.
def get_num_stands_required(goal, ramco_tally, assembly_tally, casing_tally) -> Completion:
    # Setup
    dummy_completion = Completion(goal)
    max_iterations = len(ramco_tally)+len(assembly_tally)
    iteration = 0
    dummy_completion.add_casing_joints(casing_tally)
    assembly_tally_index = 0
    num_assemblies = len(assembly_tally)

    # Find average length of ramco pipes
    num_pipes = len(ramco_tally)
    sum_of_pipes = 0
    for i in range(num_pipes):
        sum_of_pipes += ramco_tally[i].length
    average_ramco_length = round(sum_of_pipes/num_pipes, 3)
    average_ramco_pipe = Pipe(average_ramco_length, average_ramco_length)
    
    # Create dummy completion solution
    while (dummy_completion.done == False) and (iteration < max_iterations):
        do_normal_pipe = True

        # Check for any assembly pipes, and if available, add to solution.
        if assembly_tally_index < num_assemblies:
            assembly = assembly_tally[assembly_tally_index] # Assemblies must be provided in correct order.
            assembly.update_all_clears(dummy_completion)
            if assembly.is_top_assembly:
                if round(dummy_completion.length + average_ramco_length + assembly.length, 3) > dummy_completion.goal:
                    dummy_completion.add_assembly_pipe(assembly)
                    dummy_completion.done = True
            elif assembly.is_available():
                dummy_completion.add_assembly_pipe(assembly)
                do_normal_pipe = False
                assembly_tally_index += 1
        
        # Check if normal pipe can be added or see if completion is done
        if do_normal_pipe:
            if dummy_completion.length + average_ramco_pipe.length <= dummy_completion.goal:
                dummy_completion.add_normal_pipe(average_ramco_pipe)
            else:
                dummy_completion.done = True
        
        iteration += 1
    
    dummy_completion.update_pipe_numbers()
    return dummy_completion

# Step 3 Find completion tally.
def generate_completion_tally(goal, deck_tally, assembly_tally, casing_tally) -> Completion:
    """
    arguments:
    - goal: float
    - deck_tally: [triple stand rack, double stand rack, singles, pups]
    - assembly_tally: [assy_1, ..., assy_n]
    """

    # Setup
    completion = Completion(goal)
    completion.add_casing_joints(casing_tally)
    max_iterations = goal//10 # Arbitrary number to avoid infinite loop
    iteration = 0
    num_assemblies = len(assembly_tally)
    assembly_index = 0
    assembly = None

    # Main loop
    while (completion.done == False) and (iteration < max_iterations):
        do_normal_pipe = True

        # Update active assembly if there are no active assemblies and not all assemblies are used
        if (assembly == None) and (assembly_index < num_assemblies):
            assembly = assembly_tally[assembly_index]
            assembly.update_all_clears(completion)
        
        
        if assembly.is_top_assembly:
            # Add length of assembly to total completion length before assessing which stand/pipe/pup to add next
            current_completion_length = completion.length + assembly.length

            # Get the available stands/pipes/pups and sort by length
            available_pipes = get_available_pipes(deck_tally)
            available_pipes = sorted(available_pipes)
            checked_available_pipes = []

            # Check each available pipe for overshooting goal length
            for pipe in available_pipes:
                if current_completion_length + pipe.length <= completion.goal:
                    checked_available_pipes.append(pipe) # Add stands/pipes/pups which do not overshoot

            if checked_available_pipes == []:
                completion.add_assembly_pipe(assembly)
                if completion.goal - completion.length < 5:     # Completion is done if error is less than 5 meters
                    completion.done = True
                    completion.add_leftover_tally(deck_tally)
                else:                                           # Error raised if completion does not reach within 5 meters of goal
                    raise RuntimeError("No available pipes!")   # Currently have no handling of this.
            
            # If there are any stands/pipes/pups which do not overshoot, add the longest one to the solution
            else:
                longest_pipe = checked_available_pipes[-1]
                completion.add_normal_pipe(longest_pipe)
                deck_tally = remove_from_tally(deck_tally, longest_pipe)
            iteration += 1
            continue # Since the assembly is the final assembly, we can skip the next part of the main loop

        # If the active assembly is available, add it to the solution
        if assembly.is_available():
            completion.add_assembly_pipe(assembly)
            do_normal_pipe = False
            assembly_index += 1
            assembly = None

        if do_normal_pipe:
            # Get and sort all available stands/pipes
            available_pipes = get_available_pipes_excluding_pups(deck_tally) # Excluding pups to avoid wasting the pups early on
            available_pipes = sorted(available_pipes)
            checked_available_pipes = []

            # Check if any of the stands/pipes allow the assembly to be placed after
            for pipe in available_pipes:
                if assembly.check_all_clears_with_pipe(completion, pipe):
                    checked_available_pipes.append(pipe)
            
            # If there are no stands/pipes which allow the assembly to be placed, add the longest available.
            if checked_available_pipes == []:
                longest_pipe = available_pipes[-1]
                if completion.length + longest_pipe.length <= completion.goal:
                    completion.add_normal_pipe(longest_pipe)
                    deck_tally = remove_from_tally(deck_tally, longest_pipe)
                else:
                    completion.done = True
            
            # If any stands/pipes allow the assembly to be placed, add the shortest available.
            else:
                shortest_pipe = checked_available_pipes[0]
                completion.add_normal_pipe(shortest_pipe)
                deck_tally = remove_from_tally(deck_tally, shortest_pipe)
                
            # Update the constraints for the assembly
            assembly.update_all_clears(completion)

        iteration += 1
    return completion
