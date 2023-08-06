
# from molecular.analysis.peptide import compute_secondary_structure
from molecular.io import read_pdb


trj1 = read_pdb('trajectory_short.pdb')
# trj1.add_structure(read_pdb('x'))
# assert len(trj1) == 2

# secondary_structure = compute_secondary_structure(trj1, executable='C:/Users/Chris/Downloads/stride/stride.exe')
# ss = SecondaryStructure(secondary_structure.T)
# print(ss.mean(axis=None))
# print(ss.mean(axis=0))
# print(ss.mean(axis=1))


# str1 = trj1[0]
# assert pd.testing.assert_frame_equal(str1._data, trj1._data), (str1._data, trj1._data)
# str1.to_pdb('test.pdb')

# sel = trj1.query('structure_id == 0 & atom_id == 0')
# print(sel)
# trj1._data.loc[sel.index, 'record'] = ['FISH']
# sel = trj1.query('structure_id == 0 & atom_id == 0')
# print(sel)
# sel = trj1[0].query('structure_id == 0 & atom_id == 0')
# print(sel)

# sel = str1.query('structure_id == 0 & atom_id == 0')
# print(sel)
# str1._data.loc[sel.index, 'record'] = ['FISH']
# sel = str1.query('structure_id == 0 & atom_id == 0')
# print(sel)
# sel = trj1.query('structure_id == 0 & atom_id == 0')
# print(sel)


# for i in range(10):
#     str2 = read_pdb('test.pdb') + i
#     print(i, str1.rmsd(str2))

# ss = str1.get_secondary_structure(executable='C:/Users/Chris/Downloads/stride/stride.exe')
# print(ss)

