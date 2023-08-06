import typer
from os.path import exists
import requests
import json

app = typer.Typer()

def parse_fasta_string(fasta_string):
    sequences_list = []
    for sequence_data in (fasta_string.split(">"))[1:]:
        split_sequence_data = sequence_data.partition("\n")
        sequence_tuple = (split_sequence_data[0].replace("\n", ""), split_sequence_data[2].replace("\n", ""))
        sequences_list.append({"name": sequence_tuple[0], "sequence": sequence_tuple[1]})
    
    return sequences_list


@app.command()
def main(
    m: str = typer.Option("automatic", help="mode of archetype selection: automatic, reference, or custom"),
    a: str = typer.Option(None, help="relative path to the custom archetype fasta file"),
    i: str = typer.Option(..., help="relative path to the test sequences fasta file"),
    o: str = typer.Option("output", help="output file prefix (extension will be .json automatically)"),
): 
    if(m != "automatic" and m != "reference" and m != "custom"):
        print("mode (--m) must be either: automatic, reference, or custom")
    else:
        input_exists = False
        input_exists = exists(i)
        if(input_exists != True):
            print("invalid path to input file (--i): path must be relative and include file extension")
        else:
            sequences_fasta_string = ""
            sequences_reading_error = False
            
            try:
                with open(i, 'r') as file:
                    sequences_fasta_string = file.read().rstrip()
            except:
                sequences_reading_error = True
            
            if(sequences_reading_error == True):
                print("error reading input file (--i): check the file path, and if the file is valid")
            else:
                archetype = None
                archetype_selecting_error = False

                if(m == "automatic"):
                    #get first sequence in the file
                    #send request to do blast search
                    #get top result and set it as archetype
                    #if there's an error reading or no results then set error

                    try:
                        temp_test_sequence = parse_fasta_string(sequences_fasta_string)[0]
                        
                        response = requests.post('https://www.frast.com.au/api/v1/post_blast_search', data=f">{temp_test_sequence['name']}\n{temp_test_sequence['sequence']}")
                        
                        if(response.status_code != 200):
                            archetype_selecting_error = True
                        else:
                            blast_sequences_json = response.json()

                            
                            archetype = {"name": blast_sequences_json["blast_sequences"][0]["name"], "sequence": blast_sequences_json["blast_sequences"][0]["sequence"]}
                    except:
                        archetype_selecting_error = True



                    
                
                elif(m == "custom"):
                    #get archetype from file
                    #check if a is not None
                    #check if the file exist
                    #set archetype variable ("name" and "sequence") to the input file data
                    manual_archetype_string = ""

                    input_exists = False
                    input_exists = exists(a)
                    if(input_exists != True):
                        print("invalid path to input file (--i): path must be relative and include file extension")
                    else:
                        try:
                            with open(a, 'r') as file:
                                manual_archetype_string = file.read().rstrip()
                            
                            archetype = parse_fasta_string(manual_archetype_string)[0]
                        except:
                            archetype_selecting_error = True


                elif(m == "reference"):
                    #get archetypes from database
                    #check if a is one of the ones from database
                    #if so set archetype ("name" and "sequence") else set error
                    if(a == None):
                        print("error finding archetype (--a) from database: make sure to use one of the archetype from database (www.frast.com.au)")
                        archetype_selecting_error = True
                    else:
                        try:
                            response = requests.get('https://www.frast.com.au/api/v1/get_archetypes_database')
                            
                            if(response.status_code != 200):
                                archetype_selecting_error = True
                            else:
                                database_sequences_json = response.json()

                                found = False
                                for database_sequence in database_sequences_json["archetypes"]:
                                    if(a.lower() == database_sequence["name"].lower()):
                                        archetype = database_sequence
                                        found = True
                                
                                if(found != True):
                                    print("error finding archetype (--a) from database: make sure to use one of the archetype from database (www.frast.com.au)")
                        except:
                            archetype_selecting_error = True

                
                if(archetype_selecting_error or archetype == None):
                    print("error setting the archetype: make sure files are valid or try a different mode")
                else:
                    alignment_error = False
                    alignment_json = None

                    #send sequences_fasta_string and archetype to the server and get result
                    #fastaString: ""
                    #archetype: {}
                    try:
                        response = requests.post('https://www.frast.com.au/api/v1/post_parse_sequences', data=json.dumps({'fastaString': sequences_fasta_string, 'archetype': archetype}))
                        
                        if(response.status_code != 200):
                            alignment_error = True
                        else:
                            alignment_json = response.json()
                    except:
                        alignment_error = True

                    if(alignment_error == True or alignment_json == None):
                        print("error aligning sequences using mafft: check input files or try setting the archetype manually")
                    else:
                        #save the output file
                        try:
                            with open(f"{o}.json", 'w') as file:
                                file.writelines(json.dumps(alignment_json))
                        except:
                            print("error writing to output file (--o): check path, extension, and write permissions")

                



            

if __name__ == "__main__":
    app()