from utils.setup import setup
from measure import measure_programs, Measurement

def main():
    vanilla_path, bc_path, args, BCT_path = setup()
    measurement_lst = measure_programs(args.source_dir, vanilla_path, bc_path, BCT_path, force = args.force, verbose = args.verbose)

if __name__ == "__main__":
    main()
