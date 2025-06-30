from pipes import AssemblyPipe, Rack, Pile
from utils import extract_casing_joints
from utils import *
from pprint import pprint
import os
import argparse

def print_step(step):
    print(f"\n##############################################\n\
###############     STEP {step}     ###############\n\
##############################################\n")
    
def prettier_print(dict):
    print(f"\n|{"Pipe/stand/assy":^24}|{"Top depth":^10}|{"Bot. depth":^10}|")
    print(f"|{"":=^24}|{"":=^10}|{"":=^10}|")
    for key in dict:
        print(f"|{key:^24}|{dict[key][0]:<10}|{dict[key][1]:<10}|")

if __name__ == "__main__":
    """
    TallyNow - Automated Upper Completion Tally System
    
    Usage:
        python main.py                    # Use default depth (2247m)
        python main.py --depth 1500      # Use custom depth
        make well                         # Use default depth
        make well -E depth=1500          # Use custom depth via Makefile
    """
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='TallyNow - Automated Upper Completion Tally System')
    parser.add_argument('--depth', type=float, default=2247, 
                        help='Well depth in meters (default: 2247)')
    args = parser.parse_args()
    
    step1 = True
    step2 = True
    step3 = True

    # Path to current directory where main.py is executed
    PATH = os.path.dirname(os.path.abspath(__file__)) + "/"

    print(f"TallyNow - Upper Completion Calculation")
    print(f"Well Depth: {args.depth} meters")
    print("=" * 50)
    
    ##############################################
    ###############     STEP 1     ###############
    ##############################################

    # Step 1 - Input
    if step1:
        well_depth = args.depth

    # Step 1 - Solving
    if step1:
        print_step(1)

        required_pipes = get_num_pipes_required(well_depth)
        print(f"Required pipes: {required_pipes}")



    ##############################################
    ###############     STEP 2     ###############
    ##############################################
    
    # Step 2 - Input
    # Assemblies
    if step2:
        """ 
        """
        
        assembly_path = PATH+"data/assemblies.csv"
        assembly_tally = get_assemblies_from_file(assembly_path)

    # Casing joints
    if step2:
        """Guide for importing casing joints:
        Important that the index of all "c_*" lists belong together.
        i.e. c_end_rows[0] is the ending row of c_columns[0] in the sheet c_sheets[0] in the file c_paths[0].
        
        The order is not important.
        
        Paths have to be absolute.
        """
        c_paths = [PATH+"data/tieback_tally.csv",\
                   PATH+"data/liner_tally.csv"]
        # c_sheets no longer needed for CSV files
        c_columns = ['I',\
                     'G']
        c_start_rows = [18,\
                        24]
        c_end_rows = [131,\
                      104]

        casing_tally = []
        for i in range(len(c_paths)):
            casing_tally += extract_casing_joints(c_paths[i], c_columns[i], c_start_rows[i], c_end_rows[i])
                                                  
    # Deck tally
    if step2:
        """
        Path has to be absolute
        """
        dt_path = PATH+"data/tubing_tally.csv"
        # dt_sheet no longer needed for CSV files
        dt_column_lengths = 'D'
        dt_column_ids = 'A'
        dt_start = 20
        dt_end = 200
        deck_tally = get_deck_tally(dt_path, None, dt_column_ids, dt_column_lengths, dt_start, dt_end)

    # Step 2 - Solving
    if step2:
        print_step(2)

        intermediate_completion = get_num_stands_required(well_depth, deck_tally, assembly_tally, casing_tally)
        completion_length = well_depth - intermediate_completion.get_length_error()

        step_2_completion_updated = get_num_stands_required(completion_length, deck_tally, assembly_tally, casing_tally)
        print(f"Required stands: {step_2_completion_updated.get_number_of_pipe_types()}")



    ##############################################
    ###############     STEP 3     ###############
    ##############################################

    # Step 3 - Input
    if step3:
        stands_pipes_path = PATH+"data/racked_tubing.csv"
        # pipes_sheet no longer needed for CSV files
        pups_path = PATH+"data/pups.csv"

    # Define triple stands
    if step3:
        t_column = 'F'
        t_start = 2
        t_end = 150
        triples = get_triple_stands_from_file(stands_pipes_path, None, t_column, t_start, t_end, deck_tally)

    # Define double stands
    if step3:
        d_column = 'O'
        d_start = 2
        d_end = 9
        doubles = get_double_stands_from_file(stands_pipes_path, None, d_column, d_start, d_end, deck_tally)

    # Define single pipes
    if step3:
        used_pipes = triples+doubles
        singles = remove_stand_pipes_from_tally(used_pipes, deck_tally)
    
    # Import pups
    if step3:
        p_column_lengths = 'E'
        p_column_ids = 'A'
        p_start = 25
        p_end = 33
        pups = get_deck_tally(pups_path, None, p_column_ids, p_column_lengths, p_start, p_end, are_pups=True)

    # Setup full deck tallys, one for itermediate step, one for final
    if step3:
        intermediate_deck_tally = create_deck_tally(triples, doubles, singles, pups)
        final_deck_tally = create_deck_tally(triples, doubles, singles, pups)

    # Step 3 - Solving
    if step3:
        print_step(3)

        intermediate_completion = generate_completion_tally(well_depth, intermediate_deck_tally, assembly_tally, casing_tally)
        completion_length = well_depth-intermediate_completion.get_length_error()

        final_completion = generate_completion_tally(completion_length, final_deck_tally, assembly_tally, casing_tally)
        print(f"Final solution:\n{final_completion}\n")
        # pprint(final_completion.get_solution_depths(), sort_dicts=False)
        prettier_print(final_completion.get_solution_depths())