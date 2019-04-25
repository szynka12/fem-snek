###################################################################             
#        ____                                            __       #
#       / __/___   ____ ___          _____ ____   ___   / /__     #
#      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/     #
#     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<        #
#    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|       #
#                                                                 #
###################################################################

#-------------------------------------------------------------------------------
## Imports 
#-------------------------------------------------------------------------------

import src.femCore.elements as elements
import numpy as np
from src.femMesh.feMesh import FeMesh
from src.io.error import MeshFormatError

#*******************************************************************************

#-------------------------------------------------------------------------------
## Data 
#-------------------------------------------------------------------------------

# Dictionary [gmsh element type] -> fem-snek element type
#   fem-snek element type is obtainable from connectivityList object

gmshTypes = {
        1: elements.ListLine1,
        2: elements.ListTri1,
        3: elements.ListQuad1
    }


#*******************************************************************************


#-------------------------------------------------------------------------------
## Functions
#-------------------------------------------------------------------------------

def read(filepath): #str filepath -> FeMesh mesh
    '''
        Importer of ascii .msh meshes.
        
        Imports meshes generated in Gmsh software. 
        Supported version: MSH 4.1 
        Supported elements:
            - Line (2 node)
            - Triangle (3 node)
            - Quadrangle (4 node)
    '''
    
    # dict that awill be passed to any reader
    data = {}
    
    
    with open(filepath) as file:
        while True:
            section_name = file.readline()
            if len(section_name) == 0: break
            
            reader = get_section_reader(file, section_name)
            reader(file, data)
        
    
    return FeMesh(data['version'],
                  np.array(data['nodes']),
                  data['element_lists'],
                  data['id_list'])       
       
       
#       Readers
#~~~~~~~~~~~~~~~~~~~~~~~

def skip_section(file, data):
    '''
    Skip section in .msh file
    '''
    while(file.readline()[0:4] != '$End'):
        pass
    
def read_MeshFormat(file, data):
    '''
    Read version of .msh file
    
    Input:
        file - opened file
        data - dictionary with all mesh data
    '''
    format = file.readline()
    format = format.split(' ')
    
    
    
    data['version'] = 'MSH ' + format[0] + ' ASCII'


def read_PhysicalNames(file, data):
    '''
    Read information about physical names of each entity
    
    Input:
        file - opened file
        data - dictionary with all mesh data
    '''
    n = int(file.readline()[:-1])
    data['phys_names']={}
    data['phys_names'][0]={}
    data['phys_names'][1]={}
    data['phys_names'][2]={}
    data['phys_names'][3]={}
    for i in range(n):
        entity_phys_info = file.readline()[:-1].split(' ')
        
        data['phys_names'][
            int(entity_phys_info[0])][
                int(entity_phys_info[1])] = entity_phys_info[2][1:-1]
    
    check_ending('$EndPhysicalNames\n', file.readline())


def read_Entities(file, data):
    '''
    Read information about entities
    
    Input:
        file - opened file
        data - dictionary with all mesh data
    '''
    
    entities = file.readline()
    entities = [int(i) for i in entities[:-1].split(' ')]
    data['#points'] = entities[0]
    data['#curves'] = entities[1]
    data['#surfaces'] = entities[2]
    data['#volumes'] = entities[3]
    
    data['entities'] = {}
    
    data['entities'][0] = {}
    
    if 'phys_names' in data:
        named = True
    else:
        named = False
        
    for i in range(data['#points']):
        file.readline()
    
    data['entities'][1] = {}
    for i in range(data['#curves']):
        curve = [int(float(i)) for i in file.readline()[:-2].split(' ')]
        if named and curve[8] in data['phys_names'][1]:
            data['entities'][1][i+1] = data['phys_names'][1][curve[8]]
        else:
            data['entities'][1][i+1] = curve[8]
    
    data['entities'][2] = {}
    for i in range(data['#surfaces']):
        surface = [int(float(i)) for i in file.readline()[:-2].split(' ')]
        if named and surface[8] in data['phys_names'][2]:
            data['entities'][2][i+1] = data['phys_names'][2][surface[8]]
        else:
            data['entities'][2][i+1] = surface[8]
    
    data['entities'][3] = {}
    for i in range(data['#volumes']):
        volume = [int(float(i)) for i in file.readline()[:-2].split(' ')]
        data['entities'][3][i+1] = volume[8]
    
    check_ending('$EndEntities\n', file.readline())    
    


def read_Nodes(file, data):
    '''
    Read Nodes section from .msh file
    
    Input:
            file - opened file
            data - dictionary
    '''
    n_entities, n_nodes = entity_block_info(file)
    node_list = np.empty((3, n_nodes))
    node_tags = []
    j= 0
    for i in range(n_entities):
        
        nodes = parse_nodes(file, node_tags)
        
        for node in nodes:
            node = node.split(' ')
            node_list[:,j] =  [float(node[0]), float(node[1]), float(node[2])]
            j += 1
    
    check_ending('$EndNodes\n', file.readline()) 
   
            
    data['nodes'] = node_list
    data['node_tags'] = node_tags
    
    
def read_Elements(file, data):
    '''
    Read Elements section from .msh file
    
    Input:
            file - opened file
            data - dictionary
    '''
    n_entities = entity_block_info(file)[0]
    
    data['element_lists'] = []
    data['id_list'] = []
    
    for i in range(n_entities):
        n_elements, elements_str_list, el_type, tag, dim  = parse_entity(file)
        
        data['id_list'].append(
            data['entities'][dim][tag]
        )
        element_list = gmshTypes[el_type](n_elements)
        for j in range(n_elements):
            el = elements_str_list[j]
            connectivity = [(int(i) - 1) for i in el.split(' ')]
            element_list[j] = connectivity[1:]
            
        data['element_lists'].append(element_list)
    
    check_ending('$EndElements\n', file.readline()) 
   
        
        
#       Helpers
#~~~~~~~~~~~~~~~~~~~~~~~ 

def entity_block_info(file):
    '''
    Read information about current entity block
    
    Input:
        file - opened file
    Output:
        number of entity blocks, 
        number of objects
    '''
    block = file.readline()
    block = [int(i) for i in block[:-1].split(' ')]
    
    #number of entity blocks and number of objects in such block
    return block[0], block[1]
    

def parse_nodes(file, ref_node_tags):
    info = file.readline()
    info = [int(i) for i in info[:-1].split(' ')]
    
    nodes = []

    n_nodes = info[3]
    
    # read node tags in order to check if eny nodes have been skiped
    for i in range(n_nodes):
        ref_node_tags.append(int(file.readline()[:-1]) )

    #read nodal coordinates as strings
    for i in range(n_nodes):
        nodes.append( file.readline()[:-1] ) #append but delete <\n> 
    
    return nodes

def parse_entity(file):
        info = file.readline()
        info = [int(i) for i in info[:-1].split(' ')]
        
        objects = []
        entity_dimension = info[0]
        entity_tag = info[1]
        obj_type = info[2]
        n_object = info[3]
        
        #read objects as strings
        for i in range(n_object):
            objects.append( file.readline()[:-2] ) #append but delete <\n> 
        
        return n_object, objects, obj_type, entity_tag, entity_dimension

def get_section_reader(file, section_name):
    '''
    Get appropiate reader for each gmsh section
    
    Input:
        file - opened file
    Output:
        reader - function object  
    '''
    section_name = section_name[1:-1]
    
    # Dictionary [gmsh section name] -> section reader
    #   readers defined below

    gmshSections = {
            'MeshFormat'    : read_MeshFormat,
            'Nodes'         : read_Nodes,
            'Elements'      : read_Elements,
            'Entities'      : read_Entities,
            'PhysicalNames' : read_PhysicalNames
        }

    
    return gmshSections.get(section_name, skip_section)

def check_ending(name, string):
    if not string == name:
        raise MeshFormatError('Expected <'+ name.rstrip('\n') +'>, got: <' + 
                              string.rstrip('\n') + '>')