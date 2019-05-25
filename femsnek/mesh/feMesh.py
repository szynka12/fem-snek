"""
IGNORE: -----------------------------------------------------------
        ____                                            __
       / __/___   ____ ___          _____ ____   ___   / /__
      / /_ / _ \ / __ `__ \ ______ / ___// __ \ / _ \ / //_/
     / __//  __// / / / / //_____/(__  )/ / / //  __// ,<
    /_/   \___//_/ /_/ /_/       /____//_/ /_/ \___//_/|_|
    ~~~~~~~~~ Finite element method python package ~~~~~~~~~

------------------------------------------------------------ IGNORE

.. module:: feMesh
   :synopsis: Definition of finite element mesh along with boundaries and mesh regions
.. moduleauthor:: Wojciech Sadowski <github.com/szynka12>
"""

from numpy import unique, int64, empty, append, ndarray, array
from femsnek.fio.error import MeshError


class Mesh:
    """
    General mesh class, holds elements of one parametric dimension

    Attributes:

        - `_connectivityLists: list<femsnek.core.elements.connectivityList>` - list of connectivity lists
        - `_id` - mesh id
        - `_node_tags` - nodes that are mentioned in _connectivityLists
    """

    __slots__ = (
            '_connectivityLists',
            '_id',
            '_node_tags'
            )

    def __init__(self, lists: list, mesh_id: int):
        """
        Constructs instance of Mesh class.

        :param lists: list of elements connectivity lists
        :param mesh_id: physical id of the mesh
        """

        self._id = mesh_id
        self._node_tags = empty((1, 0), dtype=int64)
        for i in range(len(lists)):
            self._node_tags = append(self._node_tags, lists[i]._tags[:])

        self._node_tags = unique(self._node_tags)

        translator = dict()
        for i in range(self._node_tags.shape[0]):
            translator[self._node_tags[i]] = i

        for i in range(len(lists)):
            for j in range(lists[i].n_elements()):
                for k in range(lists[i].n_nodes()):
                    lists[i]._tags[k, j] = translator[lists[i]._tags[k, j]]

        self._connectivityLists = tuple(lists)

    def n_lists(self) -> int:
        """
        Get number of ConnectivityList objects

        :return: number of ConnectivityList objects
        """
        return len(self._connectivityLists)

    def n_nodes(self) -> int:
        """
        Get number of nodes in the mesh

        :return: Number of nodes in the mesh
        """
        return self._node_tags.shape[0]

    def lists(self):
        """
        Returns connectivity lists of the mesh

        :return: connectivity lists
        """

        return self._connectivityLists

    def id(self) -> str:
        """
        Get mesh id

        :return: Id (name) of the mesh
        """
        return self._id


class FeMesh:
    """
    Class containing information about finite element mesh.

    This class contains information about finite element mesh.
    Attributes:

        - `_info: string` - contains information about the mesh, input format etc
        - `_nodes: np_array` - table with node coordinates, its shape is equal to (3,nNodes)
        - `_internalMesh: touple<femsnek.feMesh.mesh>` - internal mesh objects
        - `_boundar mesh: touple<femsnek.feMesh.mesh>` - boundary mesh objects

    Each mesh partition can be described by region double: `('i'/'b', N)`:
    - `'i'` means internal and 'b' boundary
    - `N` number of the mesh
    """

    __slots__ = (
            '_info',
            '_nodes',
            '_internalMesh',
            '_boundaryMesh'
            )

    def __init__(self, info: str, nodes: ndarray, element_lists: list, physical_ids: list):
        """
        Constructs instance of feMesh class.

        :param info: information about mesh version or original format
        :param nodes: table with node coordinates, its shape is equal to (3,nNodes)
        :param element_lists: list of femsnek.core.element.conectivityList
        :param physical_ids: physical id of each element in element_lists
        """
        self._info = info
        self._nodes = nodes
        self._internalMesh = []
        self._boundaryMesh = []

        # get max dimension of the mesh
        max_dim = max([i.dim() for i in element_lists])

        # extract indices in element lists that correspond to internal mesh
        internal_index = [i for (i, elist) in enumerate(element_lists) if elist.dim() == max_dim]

        # extract indices in element lists that correspond to boundary mesh
        boundary_index = [i for (i, elist) in enumerate(element_lists) if elist.dim() < max_dim]

        # extract boundary data
        b_ids = [physical_ids[i] for i in boundary_index]
        b_lists = [element_lists[i] for i in boundary_index]

        # sort boundary data
        while b_ids:
            same_ids = [i for (i, id) in enumerate(b_ids) if id == b_ids[0]]

            self._boundaryMesh.append(
                    Mesh(
                            [b_lists[i] for i in same_ids],
                            b_ids[0]
                            )
                    )

            b_lists = [b_lists[i] for i in range(len(b_lists))
                       if i not in same_ids]

            b_ids = list(filter(lambda a: a != b_ids[0], b_ids))

        # extract internal data
        i_ids = [physical_ids[i] for i in internal_index]
        i_lists = [element_lists[i] for i in internal_index]

        # sort internal data
        while i_ids:
            same_ids = [i for (i, id) in enumerate(i_ids) if id == i_ids[0]]
            self._internalMesh.append(
                    Mesh(
                            [i_lists[i] for i in same_ids],
                            i_ids[0]
                            )
                    )

            i_ids = list(filter(lambda a: a != i_ids[0], i_ids))

        # convert to tuple
        self._internalMesh = tuple(self._internalMesh)
        self._boundaryMesh = tuple(self._boundaryMesh)

    # Importers ----------------------------------------------------------------------------
    @classmethod
    def from_gmsh(cls, path_to_file: str):
        """
                Importer of ascii .msh meshes.

                Imports meshes generated in Gmsh software.
                Supported version: MSH 4.1
                Supported elements:
                    - Line (2 node)
                    - Triangle (3 node)
                    - Quadrangle (4 node)
            """
        import femsnek.fio.gmsh as gmsh

        # dict that will be passed to any reader
        data = {}

        with open(path_to_file) as file:
            while True:
                section_name = file.readline()
                if len(section_name) == 0:
                    break

                reader = gmsh.get_section_reader(section_name)
                reader(file, data)

        return cls(data['version'], array(data['nodes']), data['element_lists'], data['id_list'])

    # Getters --------------------------------------------------------------------
    def nodes(self):
        """
        Get array of node coordinates

        :return:
        """
        return self._nodes

    def n_nodes(self, region: (str, int) = ('', -1)) -> int:
        """
        Get number of nodes in the mesh

        :return: Number of nodes in the mesh
        """
        if region != ('', -1):
            if region[0] is 'i':
                return self._internalMesh[region[1]].n_nodes()
            else:
                return self._boundaryMesh[region[1]].n_nodes()
        return self._nodes.shape[1]

    def name2region(self, name: str) -> (str, int):
        """
        Returns region touple of mesh, given its name.

        :param name: name of the boundary mesh e.g. 'wall'
        :return: region touple of chosen mesh
        """
        for i in range(len(self._boundaryMesh)):
            if name == self._boundaryMesh[i].id():
                return 'b', i
        else:
            for i in range(len(self._internalMesh)):
                if name == self._internalMesh[i].id():
                    return 'i', i
            else:
                raise MeshError('No boundary named <' + name + '> found!')

    def mesh_by_region(self, region: (str, int)) -> Mesh:
        """
        Returns internal or boundary mesh based on region tuple.

        :param region: region tuple
        :return: internal or boundary mesh
        """
        if region[0] == "i":
            try:
                return self._internalMesh[region[1]]
            except IndexError:
                raise MeshError('Mesh index in tuple region out of range.')
        elif region[0] == "b":
            try:
                return self._boundaryMesh[region[1]]
            except IndexError:
                raise MeshError('Mesh index in tuple region out of range.')
        else:
            raise MeshError('First element of region tuple must be \'b\' or \'i\'!')

    def info(self):
        import femsnek.fio.stream as os
        info_stream = os.OStream()
        info_stream << "******* Mesh Info: *******" << os.endl
        info_stream << "Version: " << self._info << os.endl
        info_stream << "Nodes:   " << self.n_nodes() << os.endl
        info_stream << "Mesh regions:" << os.endl
        info_stream << "  Internal:" << os.endl
        for i in range(len(self._internalMesh)):
            info_stream << "    #: " << i \
                        << ", Physical name: " << self._internalMesh[i].id() \
                        << os.endl
        info_stream << "  Boundary:" << os.endl
        for i in range(len(self._boundaryMesh)):
            info_stream << "    #: " << i \
                        << ", Physical name: " << self._boundaryMesh[i].id() \
                        << os.endl
        info_stream << "**************************" << os.endl

    # Operators --------------------------------------------------------------------

    def __getitem__(self, region: (str, int)):
        return self.mesh_by_region(region)

    def __call__(self, name: str):
        return self.name2region(name)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
