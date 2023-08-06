# FRAST

The command line version of FRAST
Generates an output json file with data including MAFFT output, mutions for each sequence and related papers

# frast --help

Usage: frast [OPTIONS]

Options:
--m TEXT mode of archetype selection: automatic, reference, or
custom [default: automatic]
--a TEXT relative path to the custom archetype fasta file
--i TEXT relative path to the test sequences fasta file
[required]
--o TEXT output file prefix (extension will be .json automatically) [default:
output_file]
--help Show this message and exit.

# example commands

(automatically selecting archetype using input sequences)
frast --m automatic --i test_input.fasta --o output_file

(using one of the reference archetypes by name)
frast --m reference --a CytB --i test_input.fasta --o output_file

(using a custom archetype by fasta file)
frast --m custom --a test_archetype.fasta --i test_input.fasta --o output_file
