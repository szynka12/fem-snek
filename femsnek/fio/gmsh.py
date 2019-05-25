"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: gmsh
   :synopsis: Provides IO functionality for gmsh mesh generator
.. moduleauthor:: Wojciech Sadowski <wojciech1sadowski@gmail.com>
"""

import femsnek.core.elements as elements
import numpy as np
from femsnek.fio.error import MeshFormatError
from _io import TextIOWrapper


# Dictionary [gmsh element type] -> fem-snek element type
# fem-snek element type is obtainable from connectivityList object
gmshTypes = {
        1: elements.ListLine1,
        2: elements.ListTri1,
        3: elements.ListQuad1
        }


#       Readers
# ~~~~~~~~~~~~~~~~~~~~~~~

def skip_section(file: TextIOWrapper, data: dict):
    """
    Skip section in .msh file

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """

    while file.readline()[0:4] != '$End':
        pass


def read_MeshFormat(file: TextIOWrapper, data: dict):
    """
    Read version of .msh file

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """

    mesh_format = file.readline()
    mesh_format = mesh_format.split(' ')

    data['version'] = 'MSH ' + mesh_format[0] + ' ASCII'

    check_ending('$EndMeshFormat\n', file.readline())


def read_PhysicalNames(file: TextIOWrapper, data: dict):
    """
    Read information about physical names of each entity

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """
    n = int(file.readline()[:-1])
    data['phys_names'] = {}
    data['phys_names'][0] = {}
    data['phys_names'][1] = {}
    data['phys_names'][2] = {}
    data['phys_names'][3] = {}
    for i in range(n):
        entity_phys_info = file.readline()[:-1].split(' ')

        data['phys_names'][
            int(entity_phys_info[0])][
            int(entity_phys_info[1])] = entity_phys_info[2][1:-1]

    check_ending('$EndPhysicalNames\n', file.readline())


def read_Entities(file: TextIOWrapper, data: dict):
    """
    Read information about entities

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """

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
            data['entities'][1][i + 1] = data['phys_names'][1][curve[8]]
        else:
            data['entities'][1][i + 1] = curve[8]

    data['entities'][2] = {}
    for i in range(data['#surfaces']):
        surface = [int(float(i)) for i in file.readline()[:-2].split(' ')]
        if named and surface[8] in data['phys_names'][2]:
            data['entities'][2][i + 1] = data['phys_names'][2][surface[8]]
        else:
            data['entities'][2][i + 1] = surface[8]

    data['entities'][3] = {}
    for i in range(data['#volumes']):
        volume = [int(float(i)) for i in file.readline()[:-2].split(' ')]
        data['entities'][3][i + 1] = volume[8]

    check_ending('$EndEntities\n', file.readline())


def read_Nodes(file: TextIOWrapper, data: dict):
    """
    Read Nodes section from .msh file

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """
    n_entities, n_nodes = entity_block_info(file)
    node_list = np.empty((3, n_nodes))
    node_tags = []
    j = 0
    for i in range(n_entities):

        nodes = parse_nodes(file, node_tags)

        for node in nodes:
            node = node.split(' ')
            node_list[:, j] = [float(node[0]), float(node[1]), float(node[2])]
            j += 1

    check_ending('$EndNodes\n', file.readline())

    data['nodes'] = node_list
    data['node_tags'] = node_tags


def read_Elements(file: TextIOWrapper, data: dict):
    """
    Read Elements section from .msh file

    :param file: opened .msh file
    :param data: dictionary with data describing mesh
    """
    n_entities = entity_block_info(file)[0]

    data['element_lists'] = []
    data['id_list'] = []

    for i in range(n_entities):
        n_elements, elements_str_list, el_type, tag, dim = parse_entity(file)
        if dim != 0:
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
# ~~~~~~~~~~~~~~~~~~~~~~~

def entity_block_info(file: TextIOWrapper) -> (int, int):
    """
    Read information about current entity block

    :param file: opened .msh file
    :return: number of entity blocks, number of objects
    """
    block = file.readline()
    block = [int(i) for i in block[:-1].split(' ')]

    # number of entity blocks and number of objects in such block
    return block[0], block[1]


def parse_nodes(file: TextIOWrapper, ref_node_tags: list) -> list:
    """
    Parse one $Nodes entity block in .msh format

    :param file: opened .msh file
    :param ref_node_tags: mutable node tags list
    :return: nodal coordinates as string
    """
    info = file.readline()
    info = [int(i) for i in info[:-1].split(' ')]

    nodes = []

    n_nodes = info[3]

    # read node tags in order to check if eny nodes have been skiped
    for i in range(n_nodes):
        ref_node_tags.append(int(file.readline()[:-1]))

    # read nodal coordinates as strings
    for i in range(n_nodes):
        nodes.append(file.readline()[:-1])  # append but delete <\n>

    return nodes


def parse_entity(file: TextIOWrapper) -> (int, list, int, int, int):
    """
    Parse one entity block in .msh format

    :param file: opened .msh file
    :return: number of objects, objects, objects type, entity tag, entity dimension
    """
    info = file.readline()
    info = [int(i) for i in info[:-1].split(' ')]

    objects = []
    entity_dimension = info[0]
    entity_tag = info[1]
    obj_type = info[2]
    n_object = info[3]

    # read objects as strings
    for i in range(n_object):
        objects.append(file.readline()[:-2])  # append but delete <\n>

    return n_object, objects, obj_type, entity_tag, entity_dimension


def get_section_reader(section_name: str):
    """
    Get appropriate reader for each gmsh section

    :param section_name: name of the current section
    :return: section reader
    """

    section_name = section_name[1:-1]

    # Dictionary [gmsh section name] -> section reader
    #   readers defined below

    gmsh_sections = {'MeshFormat':    read_MeshFormat,
                     'Nodes':         read_Nodes,
                     'Elements':      read_Elements,
                     'Entities':      read_Entities,
                     'PhysicalNames': read_PhysicalNames}

    return gmsh_sections.get(section_name, skip_section)


def check_ending(expected_name: str, string: str):
    """
    Check section ending

    :param string: string from opened .msh file
    :param expected_name: expected name of the current section ending
    """
    if not string == expected_name:
        raise MeshFormatError('Expected <' + expected_name.rstrip('\n') + '>, got: <' +
                              string.rstrip('\n') + '>')
