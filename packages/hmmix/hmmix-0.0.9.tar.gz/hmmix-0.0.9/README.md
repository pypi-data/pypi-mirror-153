
# Introgression detection

These are the scripts needed to infere archaic introgression in modern populations using an unadmixed outgroup.

1. [Installation](#installation)
2. [Usage](#usage)
3. [Quick tutorial](#quick-tutorial)
4. [1000 genomes tutorial](#example-with-1000-genomes-data)
      - [Get data](#getting-data)
      - [Find derived variants in outgroup](#finding-snps-which-are-derived-in-the-outgroup)
      - [Estimate local mutation rate](#estimating-mutation-rate-across-genome)
      - [Find variants in ingroup](#find-a-set-of-variants-which-are-not-derived-in-the-outgroup)
      - [Train the HMM](#training)
      - [Decoding](#decoding)
      - [Phased data](#training-and-decoding-with-phased-data)
      - [Annotate](#annotate-with-known-admixing-population)
---
## Installation

Run the following to install:

```python
pip install hmmix 
```

If you want to work with bcf/vcf files I would also install vcftools and bcftools. You can either use conda or visit their websites.

```python
conda install -c bioconda vcftools bcftools
```

![Overview of model](https://user-images.githubusercontent.com/30321818/43464826-4d11d46c-94dc-11e8-8f1a-6851aa5d9125.jpg)

The way the model works is by removing variation found in an outgroup population and then using the remaining variants to group the genome into regions of different variant density. If the model works well we would expect that introgressed regions have higher variant density than non-introgressed - because they have spend more time accumulation variation that is not found in the outgroup.

An example on simulated data is provided below:

![het_vs_archaic](https://user-images.githubusercontent.com/30321818/46877046-217eff80-ce40-11e8-9010-edb544e3e1ee.png)

In this example we zoom in on 1 Mb of simulated data for a haploid genome. The top panel shows the coalescence times with the outgroup across the region and the green segment is an archaic introgressed segment. Notice how much more deeper the coalescence time with the outgroup is. The second panel shows that probability of being in the archaic state. We can see that the probability is much higher in the archaic segment, demonstrating that in this toy example the model is working like we would hope. The next panel is the snp density if you dont remove all snps found in the outgroup. By looking at this one cant tell where the archaic segments begins and ends, or even if there is one. The bottom panel is the snp density when all variation in the outgroup is removed. Notice that now it is much clearer where the archaic segment begins and ends!

The method is now published in PlosGenetics and can be found here: [Detecting archaic introgression using an unadmixed outgroup](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1007641) This paper is describing and evaluating the method. 

---
## Usage

```
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

Different modes:
    make_test_data      Create test data
    create_outgroup     Create outgroup information
    mutation_rate       Estimate mutation rate
    create_ingroup      Create ingroup data
    train               Train HMM
    decode              Decode HMM
```
---
## Quick tutorial

Lets make some test data and start using the program.

```
> hmmix make_test_data
making test data...
creating 2 chromosomes with 50 Mb of test data (100K bins) with the following parameters..

State names: ['Human' 'Archaic']
Starting_probabilities: [0.98 0.02]
Transition matrix: 
[[9.999e-01 1.000e-04]
 [2.000e-02 9.800e-01]]
Emission values: [0.04 0.4 ]
```

This will generate 4 files, obs.txt, weights.bed, mutrates.bed and Initialguesses.json. obs.txt. These are the mutation that are left after removing variants which are found in the outgroup.

```
chrom  pos     ancestral_base  genotype
chr1   5212    A               AG
chr1   32198   A               AG
chr1   65251   C               CG
chr1   117853  A               AG
chr1   122518  T               TC
chr1   142322  T               TC
chr1   144695  C               CG
chr1   206370  T               TG
chr1   218969  A               AT
```

weights.bed. This is the parts of the genome that we can accurately map to - in this case we have simulated the data and can accurately access the entire genome.

```
chr1	1	50000000
chr2	1	50000000
```

mutrates.bed. This is the normalized mutation rate across the genome (in bins of 1 Mb).

```notes
chr1  0        1000000   1
chr1  1000000  2000000   1
chr1  2000000  3000000   1
chr1  3000000  4000000   1
chr1  4000000  5000000   1
chr1  5000000  6000000   1
chr1  6000000  7000000   1
chr1  7000000  8000000   1
chr1  8000000  9000000   1
chr1  9000000  10000000  1
```

Initialguesses.json. This is our initial guesses when training the model - note these are different from those we simulated from.

```json
{
  "state_names": ["Human","Archaic"],
  "starting_probabilities": [0.5,0.5],
  "transitions": [[0.99,0.01],[0.02,0.98]],
  "emissions": [0.03,0.3]
}
```

We can find the best fitting parameters using BaumWelsch training - note you can try to ommit the weights and mutrates arguments. Since this is simulated data the mutation is constant across the genome and we can asses the entire genome. Also notice how the parameters approach the parameters the data was generated from (jubii).

```bash
> hmmix train  -obs=obs.txt -weights=weights.bed -mutrates=mutrates.bed -param=Initialguesses.json -out=trained.json

iteration    loglikelihood  start1  start2  emis1   emis2   trans1_1  trans2_2
0            -18123.4475    0.5     0.5     0.03    0.3     0.99      0.98
1            -17506.0219    0.96    0.04    0.035   0.2202  0.9969    0.9242
2            -17487.797     0.971   0.029   0.0369  0.2235  0.9974    0.9141
...
17           -17401.3835    0.994   0.006   0.0398  0.4586  0.9999    0.9807
18           -17401.3832    0.994   0.006   0.0398  0.4587  0.9999    0.9808
19           -17401.3832    0.994   0.006   0.0398  0.4588  0.9999    0.9808


# run without mutrate and weights (only do this for simulated data)
> hmmix train  -obs=obs.txt -param=Initialguesses.json -out=trained.json
```

We can now decode the data with the best parameters that maximize the likelihood and find the archaic segments:

```bash
> hmmix decode -obs=obs.txt -weights=weights.bed -mutrates=mutrates.bed -param=trained.json

chrom  start     end       length    state    mean_prob  snps
chr1   0         7232000   7233000   Human    0.99946    287
chr1   7233000   7246000   14000     Archaic  0.88736    9
chr1   7247000   21618000  14372000  Human    0.99912    610
chr1   21619000  21674000  56000     Archaic  0.96543    22
chr1   21675000  26857000  5183000   Human    0.99864    204
chr1   26858000  26941000  84000     Archaic  0.96681    36
chr1   26942000  49989000  23048000  Human    0.99979    863
chr2   0         6792000   6793000   Human    0.99974    237
chr2   6793000   6822000   30000     Archaic  0.94435    14
chr2   6823000   12643000  5821000   Human    0.99936    243
chr2   12644000  12746000  103000    Archaic  0.96152    56
chr2   12747000  15461000  2715000   Human    0.99857    125
chr2   15462000  15548000  87000     Archaic  0.9441     39
chr2   15549000  32626000  17078000  Human    0.99951    708
chr2   32627000  32695000  69000     Archaic  0.98447    31
chr2   32696000  41086000  8391000   Human    0.99944    360
chr2   41087000  41181000  95000     Archaic  0.95239    43
chr2   41182000  49952000  8771000   Human    0.99771    328
chr2   49953000  49977000  25000     Archaic  0.98677    13

# Again here you could ommit weights and mutationrates. Actually one could also ommit trained.json because then the model defaults to using the parameters we used the generated the data
> hmmix decode -obs=obs.txt
```
---
## Example with 1000 genomes data
---
### Getting data
I thought it would be nice to have an entire reproduceble example of how to use this model. From a common starting point such as a VCF file (well a BCF file in this case) to the final output.  The reason for using BCF files is because it is MUCH faster to extract data for each individual. You can convert a vcf file to a bcf file like this:

```bash
bcftools view file.vcf -l 1 -O b > file.bcf
bcftools index file.bcf
```

In this example I will analyse an individual (HG00096) from the 1000 genomes project phase 3.


First we will need to know which 1) bases can be called in the genome and 2) which variants are found in the outgroup. So let's start out by downloading the files from the following directories.
To download callability regions, ancestral alleles information, ingroup outgroup information call this command:

```bash
# bcffiles (hg19)
ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/bcf_files/

# callability (remember to remove chr in the beginning of each line to make it compatible with hg19 e.g. chr1 > 1)
ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/accessible_genome_masks/20141020.strict_mask.whole_genome.bed
sed 's/^chr\|%$//g' 20141020.strict_mask.whole_genome.bed | awk '{print $1"\t"$2"\t"$3}' > strickmask.bed

# outgroup information
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/integrated_call_samples_v3.20130502.ALL.panel

# Ancestral information
ftp://ftp.ensembl.org/pub/release-74/fasta/ancestral_alleles/homo_sapiens_ancestor_GRCh37_e71.tar.bz2

# Reference genome
wget 'ftp://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/chromFa.tar.gz' -O chromFa.tar.gz
```

For this example we will use all individuals from 'YRI','MSL' and 'ESN' as outgroup individuals. While we will only be decoding hG00096 in this example you can add as many individuals as you want to the ingroup.  

```json
{
  "ingroup": [
    "HG00096",
    "HG00097"
  ],
  "outgroup": [
    "HG02922",
    "HG02923",
    ...
    "HG02944",
    "HG02946"]
}
```
---
### Finding snps which are derived in the outgroup
First we need to find a set of variants found in the outgroup. We can use the wildcard character to loop through all bcf files. If you dont have ancestral information you can skip the ancestral argument.
```bash
(took an hour) > hmmix create_outgroup -ind=individuals.json -vcf=*.bcf -weights=strickmask.bed -out=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa

# Alternative usage (if you only have a few individual in the outgroup you can also provide a comma separated list)
> hmmix create_outgroup -ind=HG02922,HG02923,HG02938 -vcf=*.bcf -weights=strickmask.bed -out=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa

# Alternative usage (if you have no ancestral information)
> hmmix create_outgroup -ind=individuals.json -vcf=*.bcf -weights=strickmask.bed -out=outgroup.txt 

# Alternative usage (if you only want to run the model on a subset of chromosomes, with or without ancestral information)
> hmmix create_outgroup -ind=individuals.json -vcf=chr1.bcf,chr2.bcf -weights=strickmask.bed -out=outgroup.txt

> hmmix create_outgroup -ind=individuals.json -vcf=chr1.bcf,chr2.bcf -weights=strickmask.bed -out=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_1.fa,homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_2.fa
```

Something to note is that if you use an outgroup vcffile (like 1000 genomes) and an ingroup vcf file from a different dataset (like SGDP) there is an edge case which could occur. There could be recurrent mutations where every individual in 1000 genome has the derived variant. This means that this position will not be present in the outgroup file. However if a recurrent mutation occurs it will look like multiple individuals in the ingroup file have the mutation. This does not happen often but just in case you can create the outgroup file and adding the sites which are fixed derived in all individuals using the reference genome:

```bash
# Alternative usage (if you want to remove sites which are fixed derived in your outgroup/ingroup)
> hmmix create_outgroup -ind=HG02922,HG02923,HG02938 -vcf=*.bcf -weights=strickmask.bed -out=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa -refgenome=*fa
```

---
### Estimating mutation rate across genome
We can use the number of variants in the outgroup to estimate the substitution rate as a proxy for mutation rate.
```bash
(took 30 sec) > hmmix mutation_rate -outgroup=outgroup.txt  -weights=strickmask.bed -window_size=1000000 -out mutationrate.bed
```
---
### Find a set of variants which are not derived in the outgroup
Keep variants that are not found to be derived in the outgroup for each individual in ingroup. You can also speficy a single individual or a comma separated list of individuals.
```bash
# Different way to define which individuals are in the ingroup
(took 20 min) > hmmix create_ingroup  -ind=individuals.json -vcf=*.bcf -weights=strickmask.bed -out=obs -outgroup=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa

(took 20 min) > hmmix create_ingroup  -ind=HG00096,HG00097 -vcf=*.bcf -weights=strickmask.bed -out=obs -outgroup=outgroup.txt -ancestral=homo_sapiens_ancestor_GRCh37_e71/homo_sapiens_ancestor_*.fa
```
---
### Training
Now for training the HMM parameters and decoding
```bash
(took 3 min) > hmmix train  -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -out=trained.HG00096.json 

iteration  loglikelihood  start1  start2  emis1   emis2   trans1_1  trans2_2
0          -510843.77     0.98    0.02    0.04    0.4     0.9999    0.98
1          -506415.4794   0.957   0.043   0.0502  0.3855  0.9994    0.9864
2          -506275.0461   0.953   0.047   0.05    0.3852  0.9992    0.9842
...
23         -506165.0257   0.949   0.051   0.0489  0.3815  0.9988    0.9782
24         -506165.0256   0.949   0.051   0.0489  0.3815  0.9988    0.9782
25         -506165.0255   0.949   0.051   0.0489  0.3815  0.9988    0.9782
```

---
### Decoding


```bash
(took 30 sec) > hmmix decode -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -param=trained.HG00096.json 

chrom      start          end       length   state    snps    mean_prob
1          0              2987000   2988000  Human    98      0.98211
1          2988000        2996000   9000     Archaic  6       0.70696
1          2997000        3424000   428000   Human    30      0.99001
1          3425000        3451000   27000    Archaic  22      0.95557
1          3452000        4301000   850000   Human    38      0.98272
1          4302000        4359000   58000    Archaic  20      0.83793
1          4360000        4499000   140000   Human    5       0.96475
1          4500000        4510000   11000    Archaic  9       0.92193
```

---
### Training and decoding with phased data
It is also possible to tell the model that the data is phased with the -haploid parameter. For that we first need to train the parameters for haploid data and then decode. Training the model on phased data is done like this - and we also remember to change the name of the parameter file to include phased so future versions of ourselves don't forget.

```bash
(took 4 min) > hmmix train  -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -out=trained.HG00096.phased.json -haploid

iteration  loglikelihood  start1  start2  emis1   emis2   trans1_1  trans2_2
0          -619830.0716   0.98    0.02    0.04    0.4     0.9999    0.98
1          -608904.5334   0.982   0.018   0.0273  0.396   0.9997    0.9856
2          -608285.6314   0.976   0.024   0.0263  0.3666  0.9996    0.9832
...
19         -607957.9519   0.969   0.031   0.0252  0.3317  0.9993    0.9769
20         -607957.9505   0.969   0.031   0.0252  0.3317  0.9993    0.9769
21         -607957.9498   0.969   0.031   0.0252  0.3317  0.9993    0.9769
```

Below I am only showing the first archaic segments. The seem to fall more or less in the same places as when we used diploid data.

```bash
(took 30 sec) > hmmix decode -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -param=trained.HG00096.phased.json -haploid

chrom      start          end       length   state    mean_prob    snps
1_hap1     2158000        2184000   27000    Archaic  0.63635      6
1_hap1     3425000        3451000   27000    Archaic  0.96534      22
...
1_hap2     2780000        2802000   23000    Archaic  0.65649      7
1_hap2     4302000        4336000   35000    Archaic  0.93799      13
1_hap2     4500000        4510000   11000    Archaic  0.87386      7
```
---

### Annotate with known admixing population

Even though this method does not use archaic reference genomes for finding segments you can still use them to annotate your segments. If you have a vcf from the population that admixed in VCF/BCF format you can write this:

```
> hmmix decode -obs=obs.HG00096.txt -weights=strickmask.bed -mutrates=mutationrate.bed -param=trained.HG00096.json -admixpop=archaicvar/*bcf

chrom  start    end      length  state    mean_prob  snps  admixpopvariants  AltaiNeandertal  Vindija33.19  Denisova  Chagyrskaya-Phalanx
1      2988000  2996000  9000    Archaic  0.70672    6     4                 4                4             1         4
1      3425000  3451000  27000   Archaic  0.95557    22    17                17               15            3         17
1      4302000  4359000  58000   Archaic  0.83794    20    12                11               12            11        11
1      4500000  4510000  11000   Archaic  0.92193    9     5                 4                5             4         5
1      5340000  5343000  4000    Archaic  0.52736    4     3                 2                3             0         3
1      6144000  6151000  8000    Archaic  0.82457    6     0                 0                0             0         0
1      8003000  8023000  21000   Archaic  0.56249    4     0                 0                0             0         0
1      9319000  9358000  40000   Archaic  0.86669    11    0                 0                0             0         0
```

For the first segment there are 6 derived snps. Of these snps 4 are shared with Altai,Vindija, Denisova and Chagyrskaya.

And that is it! Now you have run the model and gotten a set of parameters that you can interpret biologically (see my paper) and you have a list of segments that belong to the human and Archaic state.

If you have any questions about the use of the scripts, if you find errors or if you have feedback you can contact my here (make an issue) or write to:

---
Contact:

lauritsskov2@gmail.com
