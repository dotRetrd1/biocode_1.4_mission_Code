import random
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(base, "results")
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Changed the output file name to match the requirements in the image
output_file_path = os.path.join(results_dir, "Out_RandProtSeq.txt")

AminoAcids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
nonPolarAminoAcids = ['A', 'V', 'L', 'I', 'P', 'F', 'M', 'W', 'G', 'C']
PolarAminoAcids = ['N', 'Q', 'S', 'T', 'Y']
NegativelyChargedAminoAcids = ['D', 'E']
PositivelyChargedAminoAcids = ['H', 'K', 'R']
length = 150


def generateSequence(number, file_handle):
    #total 150. 'M' takes 1 non-polar spot.
    np_pool = [random.choice(nonPolarAminoAcids) for _ in range(int(0.5 * length) - 1)]
    p_pool = [random.choice(PolarAminoAcids) for _ in range(int(0.3 * length))]
    pc_pool = [random.choice(PositivelyChargedAminoAcids) for _ in range(int(0.1 * length))]
    nc_pool = [random.choice(NegativelyChargedAminoAcids) for _ in range(int(0.1 * length))]
    
    pool = np_pool + p_pool + pc_pool + nc_pool
    random.shuffle(pool)
    
    sequence = 'M' + ''.join(pool)
    
    file_handle.write(f">Rand_Prot{number}\n{sequence}\n")
    return sequence


#I made this before I read the assignment to check myself, its not really related or needed.
def checkSeq(sequence):
    counts = {'non_polar': 0, 'polar': 0, 'positive': 0, 'negative': 0, 'unknown': 0}

    if sequence[0] != 'M':
            print(f"Invalid: Sequence starts with '{sequence[0]}', expected 'M'.")
            return False

    if len(sequence) != length:
        print(f"Invalid: Sequence length is {len(sequence)}, expected {length}.")
        return False

    for aa in sequence:
        if aa in nonPolarAminoAcids:
            counts['non_polar'] += 1
        elif aa in PolarAminoAcids:
            counts['polar'] += 1
        elif aa in PositivelyChargedAminoAcids:
            counts['positive'] += 1
        elif aa in NegativelyChargedAminoAcids:
            counts['negative'] += 1
        else:
            counts['unknown'] += 1
            print(f"Invalid: Unrecognized amino acid '{aa}' found.")

    target_counts = {
        'non_polar': 75, # 50%
        'polar': 45,     # 30%
        'positive': 15,  # 10%
        'negative': 15   # 10%
    }
    
    is_valid = True
    
    if counts['unknown'] > 0:
        print(f"Invalid: Contains {counts['unknown']} unrecognized characters.")
        is_valid = False
        
    for group, target in target_counts.items():
        if counts[group] != target:
            print(f"Invalid: '{group}' count is {counts[group]}, expected {target}.")
            is_valid = False
            
    if is_valid:
        pass 
        
    return is_valid

def main():
    while True:
        try:
            amount = int(input("Please indicate how many random protein sequences you need (1-1000)? "))
            if 1 <= amount <= 1000:
                break
            else:
                print("Error: Please enter a number between 1 and 1000.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")
            
    with open(output_file_path, "w") as output_file:
        for i in range(amount):
            sequence = generateSequence(i + 1, output_file)
            checkSeq(sequence)
            
    print(f"Generated {amount} sequences in {output_file_path}")

if __name__ == "__main__":
    main()