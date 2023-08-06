import apalib.config as config
import json
import apalib

pdb = apalib.PDB()

pdb.Fetch('5u59')

one = pdb.Contents().GetPeptideChains()['A'][1]
two = pdb.Contents().GetPeptideChains()['A'][2]

val = apalib.VectorPair(one, two)

print(apalib.GetCentAngle(one, two, rad=False))

data = apalib.Data()
pdb.Read(r"C:\Users\natem\OneDrive\Desktop\Research\ccSASA - Copy\1j1j\1j1j.mmol")


print("Stop")



# print("wow")
# #TODO Fix Mo
#
#
# class Element():
#     def __init__(self):
#         self.isotopes = []
#
#     def SetName(self, n):
#         self.name = n
#
#     def SetNumber(self, n):
#         self.number = n
#
#     def SetSymbol(self, s):
#         self.symbol = s
#
#     def SetIsotope(self, i, l):
#         self.isotopes.append([i, l[0], l[1]])
#         pass
#
# data = config.data.GetJson()
#
#
# with open("testjson.json","w") as fp:
#     json.dump(data, fp, indent=3)
#
# all = dict()
# # with open(r"C:\Users\natem\OneDrive\Desktop\final atoms.txt") as f:
# #     with open("output.txt", "w") as out:
# #         for line in f.read().splitlines():
# #             count = 0
# #             if line.find("Since") != -1:
# #                 out.write(line + "\n")
# #             else:
# #                 for i in range(len(line.split())):
# #                     if line.split()[i].find(''.join([i for i in line.split()[0] if not i.isdigit()])) != -1:
# #                         out.write('\n')
# #                     out.write(line.split()[i] + " ")
# #                 out.write('\n')
#
# with open(r'C:\Users\natem\PycharmProjects\apalib\output.txt') as f:
#     for line in f.read().splitlines():
#
#         if len(line.split()) == 0:
#             continue
#         if ''.join([i for i in line.split()[0] if not i.isdigit()]) not in all.keys():
#             all[''.join([i for i in line.split()[0] if not i.isdigit()])] = Element()
#         #New element
#         if line.find("Since") != -1:
#             number = ''.join([i for i in line.split()[0] if i.isdigit()])
#             symbol = ''.join([i for i in line.split()[0] if not i.isdigit()])
#             name = line.split()[1]
#             all[symbol].SetName(name)
#             all[symbol].SetSymbol(symbol)
#             all[symbol].SetNumber(number)
#         #Isotope of an element
#         else:
#             lst = line.split()
#             for i in range(len(lst)):
#                 lst[i] = lst[i].strip()
#             # print(lst)
#             symbol = ''.join([i for i in line.split()[0] if not i.isdigit()])
#             isotope = ''.join([i for i in line.split()[0] if i.isdigit()])
#             if lst[-1] == '1.0000':
#                 # print(line)
#                 pass
#             else:
#                 newlst = []
#                 flag = False
#                 for i in range(1, len(lst), 1):
#                     if flag:
#                         flag = False
#                         continue
#                     if lst[i].find(')') != -1:
#                         ln = lst[i - 1] + lst[i]
#                         newlst.append(ln)
#                         flag = True
#                 if len(newlst) == 1:
#                     newlst.append(lst[-1])
#                 for i in range(len(newlst)):
#                     newlst[i] = newlst[i][0:newlst[i].find('(')]
#
#                 try:
#                     all[symbol].SetIsotope(isotope, newlst)
#                 except IndexError:
#                     print(symbol, isotope, newlst)
#                 pass
#
#
# print("stop")
#
# for el in data['Atoms'].keys():
#     try:
#         # print(f"Comparing {data['Atoms'][el]['Symbol']}")
#         # print(data['Atoms'][el]['Symbol'], all[data['Atoms'][el]['Symbol']].symbol)
#         for iso in all[data['Atoms'][el]['Symbol']].isotopes:
#             flag = False
#             for iso2 in data['Atoms'][el]['Stable'].keys():
#                 print(iso[1], data['Atoms'][el]['Stable'][iso2]['Mass'])
#                 if iso[1] == str(data['Atoms'][el]['Stable'][iso2]['Mass']):
#                     flag = True
#             if not flag:
#                 print(data['Atoms'][el]['Symbol'], "Very bad")
#     except:
#         pass
# pass
# # for key in data['Atoms'].keys():
# #     print
# #     print(f"\"{key}\" : \"{key}\",")
# #     print(f"\"{data['Atoms'][key]['Symbol']}\" : \"{key}\",")
# #     # print("\"Isotopes\" : {}")
#
#
# # with open(r'C:\Users\natem\Downloads\IUPAC-atomic-masses.csv') as f:
# #     with open(r'C:\Users\natem\Downloads\IUPAC-2020.csv', 'w') as n:
# #         for line in f:
# #             if line.find(r'2020</a>') != -1:
# #                 n.write(line[:line.find('<')] + '\n')
# #
#
# # with open(r'C:\Users\natem\Downloads\IUPAC-2020.csv', 'r') as f:
# #     for line in f:
# #         line = line.replace(',',' ')
# #         spt = line.split()
# #         # print(spt[0])
# #         print(''.join([i for i in spt[0] if not i.isalpha()]), end=" ")
# #         print(config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()])), end=" ")
# #         print(''.join([i for i in spt[0] if not i.isdigit()]))
# #         if config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()])) not in info:
# #             info[config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))] = data['Atoms'][config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))]
# #         if ''.join([i for i in spt[0] if not i.isalpha()]) not in info[config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))]['Isotopes'].keys():
# #             info[config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))]['Isotopes'][''.join([i for i in spt[0] if not i.isalpha()])] = dict()
# #             info[config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))]['Isotopes'][
# #                 ''.join([i for i in spt[0] if not i.isalpha()])]['Mass'] = 0
# #             info[config.data.Map('Atoms', ''.join([i for i in spt[0] if not i.isdigit()]))]['Isotopes'][
# #                 ''.join([i for i in spt[0] if not i.isalpha()])]['Abundance'] = 0
#
#     # "Hydrogen":{
#     #   "Symbol": "H",
#     #   "Number": 1,
#     #   "Isotopes": {}
#     # },
#
# # print(info)
# # apalib.pdb.Fetch('5u59')
# # dic = config.Container.GetPeptideChains()
# # val = config.Container.AsList()
# #
# # val.sort()
# #
# # com = (dic['A'][9].GetRotamers(unique=True))
# #
# #

# ########################################################################################################################
# PrintSettings()
# Fetch('3mzw')
# Parse()
# print(GetProteinChains()['A'][1])
# print(getIEP(7.4))
# print(GetProteinChains()['A'][1].GetAtoms()[0].GetCoordinates(),
# #GetProteinChains()['A'][1].GetAtoms()[2].GetCoordinates())
# print(GetDistance(GetProteinChains()['A'][1].GetAtoms()[0].GetCoordinates(),
# #GetProteinChains()['A'][1].GetAtoms()[2].GetCoordinates()))