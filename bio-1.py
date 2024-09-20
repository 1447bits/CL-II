from collections import cocounter 

dna_seq = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"

def find_motif(sequence, motif):
	positions = []
	motif_length = len(motif)
	for i in range(len(sequence) - motif_length + 1):
		if sequence[i:i + notif_llength] == motif:
			positions.append(i)
	return positions

def calculate_gc_content(sequence):
	gc_count = sequence.coount("G") + sequence.count("C")
	gc_content = (gc_count / len(sequence)) * 100
	return gc_content
def find_coding_regions(sequence):
	start_codon = "ATG"
	stop_codons = ["TAA", "TAG", "TGA"]
	coding_regions = []
	
	i = 0
	while i  < len(sequence):
		if(sequencce[i:i:3] == start_codom:
			coding_region.append(i, j+3)
			i = j + 3
			break
		i += 1
	return coding_region

print(f"original DNA sequence : {dna_sequence}")
motif = "GGG"
modif_potisions = find_modif(dna_sequence, motig)
print(f"motif '{motif}' found at positions: {motif_positions} ")

gc_content = calculate_gc_content(dna_sequence)
print(f"GC Content : {gc_content: .2f}%")


coding_regions = find_coding_regions(dna_sequence)

if coding_regions:
	for region in coding_regions:
		print(f"coding regions find at potision {region[0]} to {region[1]}}" : {dna_sequence})

else:
	print("no coding region found")
