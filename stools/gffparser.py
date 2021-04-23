from BCBio import GFF
import json
import os.path
from stools.utils import get_project_root

root = get_project_root()

def load_parse(in_file, query):
    odirectory=root+"/data/"
    #odirectory = "/data/"
    base=os.path.basename(in_file)
    ofilename = base + ".json"

    genes_to_locations = dict()

    if os.path.isfile(odirectory+ofilename):
        #load json into dictionary
        with open(odirectory+ofilename) as json_file:
            genes_to_locations = json.load(json_file)
    else:

        limit_info = dict(gff_type=["gene"])

        in_handle = open(in_file)
        for rec in GFF.parse(in_handle, limit_info=limit_info):
            for generec in rec.features:
                if generec.qualifiers['gene'][0] not in genes_to_locations:
                    genes_to_locations[generec.qualifiers['gene'][0]] = [str(generec.location)]
                else:
                    genes_to_locations[generec.qualifiers['gene'][0]].append(str(generec.location))
                
            
        in_handle.close()

        json_output = json.dumps(genes_to_locations)
        
        #output file to data directory
        f = open(odirectory+ofilename,"w")
        f.write(json_output)
        f.close()
    
    if query in genes_to_locations:
        print(genes_to_locations[query])
    elif query.upper() in genes_to_locations:
        print(genes_to_locations[query.upper()])
    elif query.lower() in genes_to_locations:
        print(genes_to_locations[query.lower()])
    else:
        print("No match found")

    
