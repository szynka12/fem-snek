import numpy as np

import elements

def skip_section(file, section_name):
        
        while(file.readline() != ('$End' + section_name + '\n')):
            pass
         
        return 0
    
def entity_block_info(file):
        block = file.readline()
        block = [int(i) for i in block[:-1].split(' ')]
        
        return block[0], block[1] #number of entity blocks and number of objects in such block
    
def parse_entity(file):
        info = file.readline()
        info = [int(i) for i in info[:-1].split(' ')]
        
        objects = []
        
        phys_id = info[1]
        obj_type = info[2]
        n_object = info[3]
        
        #read objects as strings
        for i in range(n_object):
            objects.append( file.readline()[:-1] ) #append but delete <\n> 
        
        return objects, obj_type, phys_id

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
    
 
    
def read_Nodes(file):
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
                
        if (file.readline()=='$EndNodes\n'):
            return node_list, node_tags
        else:
            return -1
        
def read_Elements(file, ref_domain_list, ref_boundary_list, maxDim):
    n_entities = entity_block_info(file)[0]
    
    for i in range(n_entities):
        elements, el_type, phys_id = parse_entity(file)
        
        el_dim = gmshTypes[el_type]([], [])._d
        domain = 0
        if (el_dim == maxDim):
            domain = 1
            
        for el in elements:
            el = [int(i) for i in el[:-1].split(' ')]
            
            if (domain and el_dim):
                ref_domain_list.append(
                    gmshTypes[el_type](el[1:], phys_id)
                )
            elif (el_dim):
                ref_boundary_list.append(
                    gmshTypes[el_type](el[1:], phys_id)
                )
                
            

def read_Entities(file, mesh_info):
        entities = file.readline()
        entities = [int(i) for i in entities[:-1].split(' ')]
        mesh_info['#points'] = entities[0]
        mesh_info['#curves'] = entities[1]
        mesh_info['#surfaces'] = entities[2]
        mesh_info['#volumes'] = entities[3]
        
        while(file.readline() != '$EndEntities\n'):
            pass
         
        return 0
    
def read_MeshFormat(file, mesh_info):
        format = file.readline()
        format = format.split(' ')
        mesh_info['version'] = 'MSH ' + format[0] + ' ASCII'
        format = file.readline()
        return 0

def check_for_renumeration(node_tags, ref_skipped_nodes):
    for i in range(len(node_tags) - 1):
        if ((node_tags[i] + 1) != node_tags[i+1]):
            ref_skipped_nodes.append(node_tags[i] + 1)
    
    return len(ref_skipped_nodes)

def renumerate_elements(ref_elements, skipped_tags):
    for el in ref_elements:
        for j in range(len(el._connectivity)):
            el._connectivity[j] -= sum(
                [el._connectivity[j] > (i-1) for i in skipped_tags]
            )
    

gmshTypes = {
    1: elements.Line1,
    2: elements.Tri1,
    3: elements.Quad1,
    15: elements.Point
}