## VCF\_to\_MAP-AB
Script to convert a VCF file to Map-AB format that is used in Genotype Corrector (Miao et al., 2018, https://github.com/freemao/Genotype-corrector)



### Python version notes ###

The Genotype Corrector pipeline I mentioned before was written with python version 2 (at the time I developed this script). This tool was written using python version 3, so please be aware when you are using this.


## Walkthrough example

### Input parameters
This script was designed to work from the command line.

	python3 VCF_to_AB.py -i Progeny_File.vcf -p Parent_File.vcf -a PHW30 -c S -o Progeny_File_Format


### Input explanation
- -i VCF file of the progeny data.

- -p VCF file of parent data (2 parents). There should only be two genotypes in this file. ParentA and ParentB for your population

- -a Specifies the parent that will be labelled parent A, needs to match the name of the two parents given in the parent VCF file

- -c Specify what the prefix is for your chromosome in the SNP ID, for example if the SNPID is S1_1000 put S the script will replace S with chr, default is no prefix

- -o Pefix for the output file of AB file, stored as .map


  
###Output file
The script will output a file that is properly formatted for use with genotype corrector (.map).