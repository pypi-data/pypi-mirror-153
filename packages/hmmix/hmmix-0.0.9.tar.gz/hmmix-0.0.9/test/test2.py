from dataclasses import dataclass, asdict
import json

@dataclass
class HMMParam:
    state_names: str
    starting_probabilities: float
    transitions: float
    emissions: float

def get_default_HMM_parameters():
    state_names = ['Human', 'Archaic']
    starting_probabilities = [0.98, 0.02]
    transitions = [[0.9999,0.0001],[0.02,0.98]]
    emissions = [0.04, 0.4]
    return HMMParam(state_names, starting_probabilities, transitions, emissions)

def read_HMM(infile):
    if infile is not None:
        with open(infile) as json_file:
            data = json.load(json_file)
            return HMMParam(**data)
    else:
        return get_default_HMM_parameters()

def write_HMM(hmmparam, outfile):
    json_string = json.dumps(asdict(hmmparam), indent = 2) 
    with open(outfile, 'w') as out:
        out.write(json_string)


myhmm = read_HMM('Initialguesses.json')
write_HMM(myhmm, 'miaw.json')
