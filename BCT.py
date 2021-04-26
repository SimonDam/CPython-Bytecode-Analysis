from utils.setup import setup
from measure import measure_programs
import baselines


def main():
    vanilla_path, bc_path, args, BCT_path = setup()
    measure_programs(args.source_dir,
                     vanilla_path,
                     bc_path,
                     BCT_path,
                     iterations=args.iterations,
                     time_limit=args.time_limit,
                     force = args.force,
                     verbose = args.verbose)
    if args.force:
        baselines.calculate_RDTSC()
        baselines.calculate_empty(vanilla_path)

if __name__ == "__main__":
    main()
