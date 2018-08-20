import argparse

parser = argparse.ArgumentParser(description='Uses a parent file (Parent A Parent B) \
to convert a progeny file to A/B/X/- file format. It assumes parents are polymorphic and are \
the SNPs to subset from the progeny')

parser.add_argument('--input_progeny', '-i', dest = 'input_file',
                    help='VCF file of the progeny data')
parser.add_argument('--output_file', '-o', dest = 'output_file',
                    help='Pefix for the output file of AB file, stored as .map')
parser.add_argument('--parent_file', '-p', dest = 'parent_file',
                    help='VCF file of parent data (2 parents)')
parser.add_argument('--parentA', '-a', dest = 'parentA',
                    help='Specifies the parent that will be labelled parent A, needs to match the parent file')
parser.add_argument('--chromPrefix', '-c', dest = 'chromPrefix', default = argparse.SUPPRESS,
                    help='Specify what the prefix is for your chromosome, for example S1_1000, default is no prefix')                
args = parser.parse_args()

##Reads in the parent file and then removes the last line if it is a blank
with open(args.parent_file, 'r') as lines:
    par = [x.strip('\n') for x in lines.readlines()]

##Creates a dictionary that contains the SNP_ID
par_snpID = []
par_key = {}
for i in range(len(par)):
    current = par[i].strip().split('\t')
    if(len(current) > 1):
        if(current[0] == "#CHROM"):
            par_header = current
        else:
            par_snpID.append(current[2])
            par_key[current[2]] = i

##Set the parent A, so this one is always called the A allele
##Then assign parent positions so we know which one to grab from the parent file to compare
parentA = args.parentA
for i in range(len(par_header)):
    if par_header[i] == parentA:
        parentA_pos = i
        
if parentA_pos == 10:
    parentB_pos = 9
else:
    parentB_pos = 10


##Import progeny data and then removes the last line if it is a blank
with open(args.input_file, 'r') as lines:
    prog = [x.strip('\n') for x in lines.readlines()]

prog_snpID = []
prog_key = {}
for i in range(len(prog)):
    current = prog[i].strip().split('\t')
    if(len(current) > 1):
        if(current[0] == "#CHROM"):
            prog_header = current
        else:
            prog_snpID.append(current[2])
            prog_key[current[2]] = i

fileName = args.output_file + '.map'
outputFile = open(fileName,'w')
out = ["locus_name"] + prog_header[9:len(prog_header)]
outputFile.write('\t'.join(out) + '\n')

##Want to ignore all lines starting with ##.
##Want to look up the SNP in the parent file, find the allele and determine if it is A or B
##B allele to then output to the matrix type.

for snp in par_snpID:
    parA = par[par_key.get(snp)].strip().split('\t')[parentA_pos]
    parB = par[par_key.get(snp)].strip().split('\t')[parentB_pos]
    
    line = prog[prog_key.get(snp)].strip().split('\t')
    if(format("chromPrefix" in args)):
        out=["chr"+snp.replace(args.chromPrefix,"").replace("_","-")]
    else:
        out=["chr"+snp.replace("S","").replace("_","-")]
    
    for gen in range(9,len(line)):
        if (line[gen] == './.'):
            out.append('-')
        elif (line[gen] == parA):
            out.append('A')
        elif (line[gen] == parB):
            out.append('B')
        else:
            out.append('X')
    
    outputFile.write('\t'.join(out) + '\n')
    outputFile.flush()    

outputFile.close()
