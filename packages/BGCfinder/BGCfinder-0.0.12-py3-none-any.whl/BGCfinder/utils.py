from torch_geometric.data import Data, Dataset, InMemoryDataset

def convert_molecule_into_graph(mol, label=None, name=None):
    try:
        # import RDKit
        import rdkit
        from rdkit import Chem, RDLogger
        from rdkit.Chem.rdchem import BondType as BT
        from rdkit.Chem.rdchem import HybridizationType
        RDLogger.DisableLog('rdApp.*')
        
        # import torch and torch_geometric
        import torch
        import torch.nn.functional as F
        from torch_scatter import scatter
        from tqdm import tqdm
        from torch_geometric.data import Data

    except ImportError:
        rdkit = None

    if rdkit is None:
        print(("Using a pre-processed version of the dataset. Please "
               "install 'rdkit' to alternatively process the raw data."),
              file=sys.stderr)

    types = {'H': 0, 'C': 1, 'N': 2, 'O': 3, 'F': 4, 'S':5}
    bonds = {BT.SINGLE: 0, BT.DOUBLE: 1, BT.TRIPLE: 2, BT.AROMATIC: 3}
    
    N = mol.GetNumAtoms()

    type_idx = []
    atomic_number = []
    aromatic = []
    sp = []
    sp2 = []
    sp3 = []
    num_hs = []
    for atom in mol.GetAtoms():
        type_idx.append(types[atom.GetSymbol()])
        atomic_number.append(atom.GetAtomicNum())
        aromatic.append(1 if atom.GetIsAromatic() else 0)
        hybridization = atom.GetHybridization()
        sp.append(1 if hybridization == HybridizationType.SP else 0)
        sp2.append(1 if hybridization == HybridizationType.SP2 else 0)
        sp3.append(1 if hybridization == HybridizationType.SP3 else 0)

    z = torch.tensor(atomic_number, dtype=torch.long)

    row, col, edge_type = [], [], []
    for bond in mol.GetBonds():
        start, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
        row += [start, end]
        col += [end, start]
        edge_type += 2 * [bonds[bond.GetBondType()]]

    edge_index = torch.tensor([row, col], dtype=torch.long)
    edge_type = torch.tensor(edge_type, dtype=torch.long)
    edge_attr = F.one_hot(edge_type,
                          num_classes=len(bonds)).to(torch.float)

    perm = (edge_index[0] * N + edge_index[1]).argsort()
    edSquidpyge_index = edge_index[:, perm]
    edge_type = edge_type[perm]
    edge_attr = edge_attr[perm]

    row, col = edge_index
    hs = (z == 1).to(torch.float)
    num_hs = scatter(hs[row], col, dim_size=N).tolist()

    x1 = F.one_hot(torch.tensor(type_idx), num_classes=len(types)) # 6-dimensional
    x2 = torch.tensor([atomic_number, aromatic, sp, sp2, sp3, num_hs],
                      dtype=torch.float).t().contiguous() # 6-dimensional
    x = torch.cat([x1.to(torch.float), x2], dim=-1) # 12-dimensional
    y=label
    
    data = Data(x=x, z=z, edge_index=edge_index, edge_attr=edge_attr, y=y, idx=None, name=name)
    return data
    
class graph_dataset(InMemoryDataset):
    def __init__(self, data_list):
        super(graph_dataset, self).__init__('/tmp/graph_dataset')
        self.data, self.slices = self.collate(data_list)