#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Generates arithmetic expressions using a simple genetic algorithm.

Based on the tutorial at http://www.ai-junkie.com/ga/intro/gat1.html

The generated expressions are assumed to be left-associative, with equal
precedence of all operators.

Usage:
    ./arithmetic_expr.py <target-number>

Example:
    $ ./arithmetic_expr.py 10
    $ 10 = 2 * 4 + 2
'''

__author__ = 'Oscar Söderlund'
__license__ = 'MIT'


import random
import sys


NUMBER_GENES = {
    '0000': 0,
    '0001': 1,
    '0010': 2,
    '0011': 3,
    '0100': 4,
    '0101': 5,
    '0110': 6,
    '0111': 7,
    '1000': 8,
    '1001': 9,
}


OPERATOR_GENES = {
    '1010': '+',
    '1011': '-',
    '1100': '*',
    '1101': '/',
}


GENE_SIZE = 4
CHROMOSOME_SIZE = 20
POPULATION_SIZE = 500
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.7
MAX_GENERATION = 100000


def apply_operator(lhs, operator, rhs):
    if operator == '+':
        return lhs + rhs
    elif operator == '-':
        return lhs - rhs
    elif operator == '*':
        return lhs * rhs
    elif operator == '/':
        return lhs / float(rhs)


def decode_next_gene(chromosome, gene_dict):
    next_gene = chromosome[:GENE_SIZE]
    remaining_chromosome = chromosome[GENE_SIZE:]
    if next_gene in gene_dict:
        return gene_dict[next_gene], remaining_chromosome
    elif remaining_chromosome:
        return decode_next_gene(remaining_chromosome, gene_dict)
    else:
        return None, None


def decode_chromosome(chromosome, accumulator):
    acc, remainder = decode_next_gene(chromosome, NUMBER_GENES)
    while remainder:
        operator, remainder = decode_next_gene(remainder, OPERATOR_GENES)
        if operator and remainder:
            number, remainder = decode_next_gene(remainder, NUMBER_GENES)
            if number:
                acc = accumulator(acc, operator, number)
    return acc


def fitness(target_value, chromosome_value):
    return 1 / abs(target_value - chromosome_value)


def weighted_random_selection(items, weights):
    rand = random.uniform(0, sum(weights))
    curr_sum = 0
    for item, weight in zip(items, weights):
        curr_sum += weight
        if rand < curr_sum:
            return item
    return item


def crossover(c1, c2, position):
    return c1[:position] + c2[position:], c2[:position] + c1[position:]


def mutate_bit(bit):
    should_mutate = random.random() < MUTATION_RATE
    if should_mutate:
        return '0' if bit == '1' else '1'
    else:
        return bit


def mutate_chromosome(chromosome):
    return ''.join([mutate_bit(bit) for bit in list(chromosome)])


def select_two_crossover_and_mutate(population, fitnesses):
    c1 = weighted_random_selection(population, fitnesses)
    c2 = weighted_random_selection(population, fitnesses)
    should_do_crossover = random.random() < CROSSOVER_RATE
    if should_do_crossover:
        c1, c2 = crossover(c1, c2, random.randint(0, len(c1)))
    return mutate_chromosome(c1), mutate_chromosome(c2)


def decode_to_str(chromosome):
    def to_str(acc, operator, number):
        return '%s %s %s' % (str(acc), operator, str(number))
    return decode_chromosome(chromosome, to_str)


def decode_to_value(chromosome):
    return decode_chromosome(chromosome, apply_operator)


def random_bit():
    return str(random.randint(0, 1))


def random_gene():
    return ''.join([random_bit() for i in range(GENE_SIZE)])


def random_chromosome():
    return ''.join(random_gene() for i in range(CHROMOSOME_SIZE))


def find_arithmetic_expression(target_value):
    population = [random_chromosome() for i in range(POPULATION_SIZE)]
    generation = 0
    while generation < MAX_GENERATION:
        generation += 1
        print('Generation %d...' % generation)
        fitnesses = []
        for chromosome in population:
            chromosome_value = decode_to_value(chromosome)
            if chromosome_value == target_value:
                return chromosome, generation
            else:
                fitnesses.append(fitness(target_value, chromosome_value))
        population = [chromosome for chromosome in
                      select_two_crossover_and_mutate(population, fitnesses)
                      for i in range(POPULATION_SIZE / 2)]
    return None, generation


if __name__ == "__main__":
    target_value = float(sys.argv[1])
    chromosome, generation = find_arithmetic_expression(target_value)
    if chromosome is not None:
        print('Found an expression after %d generations:\n' % generation)
        print('  %.1f = %s' % (target_value, decode_to_str(chromosome)))
    else:
        print('Failed to find an expression after %d generations' % generation)
