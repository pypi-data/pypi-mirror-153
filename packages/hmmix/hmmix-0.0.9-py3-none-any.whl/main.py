import argparse

from hmm_functions import TrainModel, DecodeModel
from bcf_vcf import make_out_group, make_ingroup_obs
from Maketestdata import Maketestdata
from make_mutationrate import make_mutation_rate


def print_script_usage():
    toprint = '''
    Script for identifying introgressed archaic segments

    Turorial:
    hmmix make_test_data 
    hmmix train  -obs=obs.txt -weights=weights.bed -mutrates=mutrates.bed -param=Initialguesses.json -out=trained.json 
    hmmix decode -obs=obs.txt -weights=weights.bed -mutrates=mutrates.bed -param=trained.json


    Turorial with 1000 genomes data:
    hmmix create_outgroup -ind=individuals.json -vcf=*.bcf -weights=strickmask.bed -out=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa
    hmmix mutation_rate -outgroup=outgroup.txt  -weights=strickmask.bed -window_size=1000000 -out mutationrate.bed
    hmmix create_ingroup  -ind=individuals.json -vcf=*.bcf -weights=strickmask.bed -out=obs -outgroup=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa
    
    hmmix train  -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -out=trained.HG00096.json 
    hmmix decode -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -param=trained.HG00096.json 

    '''

    return toprint

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():

    parser = argparse.ArgumentParser(description=print_script_usage(), formatter_class=argparse.RawTextHelpFormatter)

    subparser = parser.add_subparsers(dest = 'mode')

    # Run test
    test_subparser = subparser.add_parser('make_test_data', help='Create test data')

    # Make outgroup
    outgroup_subparser = subparser.add_parser('create_outgroup', help='Create outgroup information')
    outgroup_subparser.add_argument("-ind",help="[required] ingroup/outgrop list (json file) or commaseparated list e.g. ind1,ind2", type=str, required = True)
    outgroup_subparser.add_argument("-vcf",help="[required] path to list of commaseparated vcf/bcf file(s) or wildcard characters e.g. chr*.bcf", type=str, required = True)
    outgroup_subparser.add_argument("-weights", metavar='',help="file with callability (defaults to all positions being called)")
    outgroup_subparser.add_argument("-out", metavar='',help="outputfile (defaults to stdout)", default = '/dev/stdout')
    outgroup_subparser.add_argument("-ancestral", metavar='',help="fasta file with ancestral information (default none)", default='')
    outgroup_subparser.add_argument("-refgenome", metavar='',help="fasta file with reference genome (default none)", default='')

    # Make mutation rates
    mutation_rate = subparser.add_parser('mutation_rate', help='Estimate mutation rate')
    mutation_rate.add_argument("-outgroup", help="[required] path to variants found in outgroup", type=str, required = True)
    mutation_rate.add_argument("-out", metavar='',help="outputfile (defaults to mutationrate.bed)", default = 'mutationrate.bed')
    mutation_rate.add_argument("-weights", metavar='',help="file with callability (defaults to all positions being called)")
    mutation_rate.add_argument("-window_size", metavar='',help="size of bins (defaults to 1 Mb)", type=int, default = 1000000)

    # Make ingroup observations
    create_obs_subparser = subparser.add_parser('create_ingroup', help='Create ingroup data')
    create_obs_subparser.add_argument("-ind", help="[required] ingroup/outgrop list (json file) or commaseparated list e.g. ind1,ind2", type=str, required = True)
    create_obs_subparser.add_argument("-vcf", help="[required] path to list of commaseparated vcf/bcf file(s) or wildcard characters e.g. chr*.bcf", type=str, required = True)
    create_obs_subparser.add_argument("-outgroup", help="[required] path to variant found in outgroup", type=str, required = True)
    create_obs_subparser.add_argument("-weights", metavar='',help="file with callability (defaults to all positions being called)")
    create_obs_subparser.add_argument("-out", metavar='',help="outputfile prefix (default is a file named obs.<ind>.txt where ind is the name of individual in ingroup/outgrop list)", default = 'obs')
    create_obs_subparser.add_argument("-ancestral", metavar='',help="fasta file with ancestral information (default none)", default='')

    # Train model
    train_subparser = subparser.add_parser('train', help='Train HMM')
    train_subparser.add_argument("-obs",help="[required] file with observation data", type=str, required = True)
    train_subparser.add_argument("-weights", metavar='',help="file with callability (defaults to all positions being called)")
    train_subparser.add_argument("-mutrates", metavar='',help="file with mutation rates (default is mutation rate is uniform)")
    train_subparser.add_argument("-param", metavar='',help="markov parameters file (default is human/neanderthal like parameters)", type=str)
    train_subparser.add_argument("-out", metavar='',help="outputfile prefix (default is a file named trained.json)", default = 'trained.json')
    train_subparser.add_argument("-window_size", metavar='',help="size of bins (default is 1000 bp)", default = 1000)
    train_subparser.add_argument("-haploid",help="Change from using dipliod data to haploid data", action='store_true', default = False)

    # Decode model
    decode_subparser = subparser.add_parser('decode', help='Decode HMM')
    decode_subparser.add_argument("-obs",help="[required] file with observation data", type=str, required = True)
    decode_subparser.add_argument("-weights", metavar='',help="file with callability (defaults to all positions being called)")
    decode_subparser.add_argument("-mutrates", metavar='',help="file with mutation rates (default is mutation rate is uniform)")
    decode_subparser.add_argument("-param", metavar='',help="markov parameters file (default is human/neanderthal like parameters)", type=str)
    decode_subparser.add_argument("-out", metavar='',help="outputfile prefix (default is stdout)", default = '/dev/stdout')
    decode_subparser.add_argument("-window_size", metavar='',help="size of bins (default is 1000 bp)", default = 1000)
    decode_subparser.add_argument("-decode_per_bin",help="get the posterior probability for each window", action='store_true', default = False)
    decode_subparser.add_argument("-haploid",help="Change from using dipliod data to haploid data", action='store_true', default = False)
    decode_subparser.add_argument("-admixpop",help="Annotate using vcffile with admixing population")


    args = parser.parse_args()

    if args.mode == 'make_test_data':
        Maketestdata(data_set_length = 50000)

    elif args.mode == 'train':
        TrainModel(args.obs, args.weights, args.mutrates, args.param, args.out, args.window_size, args.haploid)

    elif args.mode == 'decode':
        DecodeModel(args.obs, args.weights, args.mutrates, args.param, args.out, args.window_size, args.haploid, args.decode_per_bin, args.admixpop)

    elif args.mode == 'create_outgroup':
        make_out_group(args.ind, args.weights, args.vcf, args.out, args.ancestral, args.refgenome)

    elif args.mode == 'create_ingroup':
        make_ingroup_obs(args.ind, args.weights, args.vcf, args.out, args.outgroup, args.ancestral)

    elif args.mode == 'mutation_rate':
        make_mutation_rate(args.outgroup, args.out, args.weights, args.window_size)
    else:
        print(print_script_usage())


if __name__ == "__main__":
    main()

