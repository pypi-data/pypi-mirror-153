from collections import defaultdict
import numpy as np
from numba import njit
import math

from helper_functions import Load_observations_weights_mutrates, Load_HMM_parameters, logoutput, Make_HMM_parameters, find_runs, Annotate_with_ref_genome, Make_folder_if_not_exists, Get_genome_coordinates, find_admixed_variants

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# HMM functions
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def Emission_probs_poisson(emissions, observations, weights, mutrates):
    n = len(observations)
    n_states = len(emissions)
    
    # observations values
    fractorials = np.zeros(n)
    for i, obs in enumerate(observations):
        fractorials[i] = math.factorial(obs)

    probabilities = np.zeros( (n, n_states) ) 
    for state in range(n_states): 
        probabilities[:,state] = (np.exp( - emissions[state] * weights * mutrates) *  ((emissions[state] * weights * mutrates )**observations )) / fractorials

    return probabilities

@njit
def fwd_step(alpha_prev, E, trans_mat):
    alpha_new = (alpha_prev @ trans_mat) * E
    n = np.sum(alpha_new)
    return alpha_new / n, n

@njit
def forward(probabilities, transitions, init_start):

    n = len(probabilities)
    forwards_in = np.zeros( (n, len(init_start)) ) 
    scale_param = np.ones(n)

    for t in range(n):
        if t == 0:
            forwards_in[t,:]=  init_start  * probabilities[t,:]
            scale_param[t] = np.sum( forwards_in[t,:])
            forwards_in[t,:] = forwards_in[t,:] / scale_param[t]
        else:
            forwards_in[t,:], scale_param[t] =  fwd_step(forwards_in[t-1,:], probabilities[t,:], transitions) 

    return forwards_in, scale_param
    

@njit
def bwd_step(beta_next, E, trans_mat, n):
    beta = (trans_mat * E) @ beta_next
    return beta / n

@njit
def backward(emissions, transitions, scales):
    n, n_states = emissions.shape
    beta = np.ones((n, n_states))
    for i in range(n - 1, 0, -1):
        beta[i - 1,:] = bwd_step(beta[i,:], emissions[i,:], transitions, scales[i])
    return beta


def GetProbability(starting_probabilities, transitions_matrix, emissions_matrix, weights, obs, mutrates):

    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions_matrix, starting_probabilities)
    forward_probility_of_obs = np.sum(np.log(scales))

    return forward_probility_of_obs


def TrainBaumWelsch(starting_probabilities, transitions_matrix, emissions_matrix, weights, obs, mutrates):
    """
    Trains the model once, using the forward-backward algorithm. 
    """

    n_states = len(starting_probabilities)

    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions_matrix, starting_probabilities)
    backward_probs = backward(emissions, transitions_matrix, scales)

    # Update emission
    new_emissions_matrix = np.zeros((n_states))
    for state in range(n_states):
        top = np.sum(forward_probs[:, state] * backward_probs[:, state] * obs)
        bottom = np.sum(forward_probs[:, state] * backward_probs[:, state] * (weights * mutrates) )
        new_emissions_matrix[state] = top/bottom


    # Update starting probs
    posterior_probs = forward_probs * backward_probs
    normalize = np.sum(posterior_probs)
    new_starting_probabilities = np.sum(posterior_probs, axis=0)/normalize 


    # Update Transition probs 
    new_transitions_matrix =  np.zeros((n_states, n_states))
    for state1 in range(n_states):
        for state2 in range(n_states):
            new_transitions_matrix[state1,state2] = np.sum( forward_probs[:-1,state1]  * transitions_matrix[state1, state2] * emissions[1:,state2] * backward_probs[1:,state2] / scales[1:] )

    new_transitions_matrix /=  new_transitions_matrix.sum(axis=1)[:,np.newaxis]


    return (new_starting_probabilities, new_transitions_matrix, new_emissions_matrix) 


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Train
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def TrainModel(obs_file, weights_file, mutation_rates_file, parameters_file, outfile, window_size, haploid):

    obs, mutrates, weights = Load_observations_weights_mutrates(obs_file, mutation_rates_file, weights_file, window_size, haploid)
    state_names, transitions, emissions_matrix, starting_probabilities = Load_HMM_parameters(parameters_file)
    epsilon = 1e-3

    # Print parameters to screen
    print('-' * 40)
    print('Selected parameters')
    print('> State names:', state_names)
    print('> Starting_probabilities:', starting_probabilities)
    print('> Transition matrix:')
    print(transitions)
    print('> Emission values:',emissions_matrix)   
    print()
    print('> number of windows:', len(obs), '. Number of snps = ', sum(obs))
    print('> total callability:', round(np.sum(weights) / len(obs),2) )
    print('> average mutation rate per bin:', round(np.sum(mutrates * weights) / np.sum(weights), 2) )
    print('> Output is',outfile) 
    print('-' * 40)

    # Get probability of sequece with start parameters
    previous_loglikelihood = GetProbability(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
    logoutput(emissions_matrix, previous_loglikelihood, transitions, starting_probabilities, 0)
    
    # Train parameters using Baum Welch algorithm
    for i in range(1,1000):
        starting_probabilities, transitions, emissions_matrix = TrainBaumWelsch(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
        new_loglikelihood = GetProbability(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
        logoutput(emissions_matrix, new_loglikelihood, transitions, starting_probabilities, i)

        if new_loglikelihood - previous_loglikelihood < epsilon:       
            break 

        previous_loglikelihood = new_loglikelihood

    # Write the optimal parameters
    Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions_matrix, outfile)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Decode
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def DecodeModel(obs_file, weights_file, mutation_rates_file, parameters_file, output, window_size, haploid, decode_per_bin, admixpop):
    
    obs, mutrates, weights = Load_observations_weights_mutrates(obs_file, mutation_rates_file, weights_file, window_size, haploid)
    state_names, transitions, emissions_matrix, starting_probabilities = Load_HMM_parameters(parameters_file)
    chroms, starts, variants = Get_genome_coordinates(obs_file, window_size, haploid)

    # Print parameters to screen
    print('-' * 40)
    print('Selected parameters')
    print('> State names:', state_names)
    print('> Starting_probabilities:', starting_probabilities)
    print('> Transition matrix:')
    print(transitions)
    print('> Emission values:',emissions_matrix)   
    print()
    print('> number of windows:', len(obs), '. Number of snps = ', sum(obs))
    print('> total callability:', round(np.sum(weights) / len(obs),2) )
    print('> average mutation rate per bin:', round(np.sum(mutrates * weights) / np.sum(weights), 2) )
    print('> Output is',output) 
    print('-' * 40)

    # Posterior decode the file
    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions, starting_probabilities)
    backward_probs = backward(emissions, transitions, scales)
    post_seq = (forward_probs * backward_probs).T

    # write summary file 
    Make_folder_if_not_exists(output)

    if not decode_per_bin:
        
       
        with open(output,'w') as out: 

            if admixpop is not None:
                admix_pop_variants, admixpop_names = Annotate_with_ref_genome(admixpop, obs_file)
                header = 'chrom\tstart\tend\tlength\tstate\tmean_prob\tsnps\tadmixpopvariants\t{}\n'.format('\t'.join(admixpop_names))
            else:
                header = 'chrom\tstart\tend\tlength\tstate\tmean_prob\tsnps\n'

            out.write(header)

            for (chrom, chrom_start_index, chrom_length_index) in find_runs(chroms):

                state_with_highest_prob = np.argmax(post_seq[:,chrom_start_index:chrom_start_index + chrom_length_index-1], axis = 0)

                for (state, start_index, length_index) in find_runs(state_with_highest_prob):

                    start_index = start_index + chrom_start_index
                    end_index = start_index + length_index

                    genome_start = starts[start_index]
                    genome_end = starts[start_index + length_index - 1]
                    genome_length =  length_index * window_size

                    snp_counter = np.sum(obs[start_index:end_index])
                    mean_prob = np.mean(post_seq[state, start_index:end_index])


                    if admixpop is not None:
                        mylist = find_admixed_variants(variants[start_index:end_index])
                        archiac_variants_dict = defaultdict(int)
                        for snp_position in mylist:
                            variant = admix_pop_variants[f'{chrom}_{snp_position}']
                            if variant != '':
                                if '|' in variant:
                                    for ind in variant.split('|'):
                                        archiac_variants_dict[ind] += 1
                                else:
                                    archiac_variants_dict[variant] += 1

                                archiac_variants_dict['total'] += 1

                        archaic_variants = '\t'.join([str(archiac_variants_dict[x]) for x in ['total'] + admixpop_names])
                        print(chrom, genome_start, genome_end, genome_length, state_names[state], round(mean_prob, 5), snp_counter, archaic_variants, sep = '\t', file = out)
                    else:
                        print(chrom, genome_start, genome_end, genome_length, state_names[state], round(mean_prob, 5), snp_counter, sep = '\t', file = out)



    # write posterios prob for each bin (if specified)    
    if decode_per_bin:

        if admixpop is not None:
            header = 'chrom\tstart\tobservations\tMostlikely\t{}\tvariants\tadmixpopvariants\n'.format('\t'.join(state_names))
            admix_pop_variants, admixpop_names = Annotate_with_ref_genome(admixpop, obs_file)
        else:
            header = 'chrom\tstart\tobservations\tMostlikely\t{}\tvariants\n'.format('\t'.join(state_names))

        with open(output,'w') as out:
            out.write(header)
            state_with_highest_prob = np.argmax(post_seq, axis = 0)
            for index, (chrom, variant_in_bin, obs_in_bin) in enumerate(zip(chroms, variants, obs)):

                state = state_names[state_with_highest_prob[index]]
                probability_of_states = '\t'.join([str(round(val,4)) for val in post_seq[:, index]])

                if admixpop is not None:
                    admix_pop_variants_window = '|'.join([admix_pop_variants[f'{chrom}_{x}'] for x in variant_in_bin.split(',')])
                    print(chrom, index * window_size, obs_in_bin, state, probability_of_states, variant_in_bin, admix_pop_variants_window, sep = '\t', file =  out)
                else:
                    print(chrom, index * window_size, obs_in_bin, state, probability_of_states, variant_in_bin, sep = '\t', file =  out)


