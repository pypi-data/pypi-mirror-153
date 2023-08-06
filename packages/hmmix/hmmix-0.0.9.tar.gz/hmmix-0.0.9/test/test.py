import numpy as np
from collections import defaultdict

def Read_fasta(ancestral):
    ancestral_allele = ''
    with open(ancestral) as data:
        for line in data:
            if line.startswith('>'):
                pass
            else:
                ancestral_allele += line.strip().upper()

    return ancestral_allele





for CHROM in range(1,23):

    with open(f'fixed_human{CHROM}.txt', 'w') as out:

        print('chrom','pos','ref_allele_info','alt_allele_info','ancestral_base', sep = '\t', file = out)

        ancestral_allele = Read_fasta(f'/global/scratch2/pl1data/moorjani/DATASETS/resources/hg38/human_ancestor/homo_sapiens_ancestor_{CHROM}.fa')
        print('Loading ancestral', len(ancestral_allele))


        refgenome_allele = Read_fasta(f'/global/scratch2/pl1data/moorjani/DATASETS/resources/hg38/fasta/hg38_chr{CHROM}.fa')
        print('Loading ref genome', len(refgenome_allele))


        callability = np.zeros(300_000_000) 
        with open('../../callability/hg38.bed') as data:
            for line in data:
                chrom, start, end = line.strip().split()

                if chrom == f'chr{CHROM}':
                    callability[int(start):int(end)] = 1
        print('Loading callability file', np.sum(callability))


        outgroup_variants =np.zeros(300_000_000) 

        print('Loading 1000 genomes positions with variants')
        with open(f'../../outgroups/1000g_hg38/chr{CHROM}_variants.txt') as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos = line.split()[0:2]
                    outgroup_variants[int(pos)-1] = 1

        print('Loading HGDP positions with variants')
        with open(f'../../outgroups/HGDP_hg38/chr{CHROM}_variants.txt') as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos = line.split()[0:2]
                    outgroup_variants[int(pos)-1] = 1

        print('Loading outgroup file', np.sum(outgroup_variants))


        diff_bases = 0
        for index, (refbase, ancbase) in enumerate(zip(refgenome_allele, ancestral_allele)):

            if ancbase in 'ACGT' and refbase in 'ACGT':
                if refbase != ancbase and outgroup_variants[index] == 0: # and callability[index] == 1:
                    print(f'chr{CHROM}', index + 1, f'{refbase}:100', f'{ancbase}:0', ancbase, sep = '\t', file = out)
                    diff_bases += 1
                    
                    if 16161555 < index < 16161565:
                        print(f'chr{CHROM}', index + 1, f'{refbase}:100', f'{ancbase}:0', ancbase, sep = '\t')

        print()
        print('Potential differences', diff_bases)