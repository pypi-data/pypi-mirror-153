#!/usr/bin/env python3
#
# GlobalChem - Montmorillonite Adsorption
#
# ---------------------------------------

class MontmorilloniteAdsorption(object):

    def __init__(self):

        self.name = 'montmorillonite_adsorption'

    @staticmethod
    def get_smiles():

        smiles = {
            '3,3′,4,4′,5-pentachlorobiphenyl': 'C1=CC(=C(C=C1C2=CC(=C(C(=C2)Cl)Cl)Cl)Cl)Cl',
            '3,4,3′,4′-tetrachlorobiphenyl': 'C1=CC(=C(C=C1C2=CC(=C(C=C2)Cl)Cl)Cl)Cl',
            '2,2′,4,4′,5,5′-hexachlorobiphenyl': 'C1=C(C(=CC(=C1Cl)Cl)Cl)C2=CC(=C(C=C2Cl)Cl)Cl',
            'bisphenol A': 'CC(C)(C1=CC=C(C=C1)O)C2=CC=C(C=C2)O',
            '2,3,3′,4,4′,5′-hexachlorobiphenyl': 'C1=CC(=C(C=C1C2=CC(=C(C(=C2Cl)Cl)Cl)Cl)Cl)Cl',
            '2,2′,4,4′,6,6′-hexachlorobiphenyl': 'C1=C(C=C(C(=C1Cl)C2=CC(=C(C=C2Cl)Cl)Cl)Cl)Cl',
            '2,2′,4,4′,5,6′-hexachlorobiphenyl': 'C1=CC=C(C(=C1)C2=C(C(=C(C(=C2Cl)Cl)Cl)Cl)Cl)Cl',
            'lindane': 'C1(C(C(C(C(C1Cl)Cl)Cl)Cl)Cl)Cl',
            'naphthalene': 'C1=CC=C2C=CC=CC2=C1',
            'benz[e]acephenanthrylene': 'C1=CC=C2C3=C4C(=CC=C3)C5=CC=CC=C5C4=CC2=C1',
            'dieldrin': 'C1C2C3C(C1C4C2O4)C5(C(=C(C3(C5(Cl)Cl)Cl)Cl)Cl)Cl',
            'linuron': 'CN(C(=O)NC1=CC(=C(C=C1)Cl)Cl)OC',
            'trifluralin': 'CCCN(CCC)C1=C(C=C(C=C1[N+](=O)[O-])C(F)(F)F)[N+](=O)[O-]',
            'toluene': 'CC1=CC=CC=C1',
            'benzene': 'C1=CC=CC=C1',
            'bisphenol S': 'C1=CC(=CC=C1O)S(=O)(=O)C2=CC=C(C=C2)O',
            'bisphenol F': 'c1cc(ccc1Cc2ccc(cc2)O)O',
            'benzo[a]pyrene': 'C1=CC=C2C3=C4C(=CC2=C1)C=CC5=C4C(=CC=C5)C=C3',
            '2,4-dichlorophenoxyacetic acid': 'C1=CC(=C(C=C1Cl)Cl)OCC(=O)O',
            'clofenotane (DDT)': 'C1=CC(=CC=C1C(C2=CC=C(C=C2)Cl)C(Cl)(Cl)Cl)Cl',
            'pyrene': 'C1=CC2=C3C(=C1)C=CC4=CC=CC(=C43)C=C2',
            'deoxynivalenol (vomitoxin)': 'CC1=CC2C(C(C1=O)O)(C3(CC(C(C34CO4)O2)O)C)CO',
            'glyphosate': 'C(C(=O)O)NCP(=O)(O)O',
            'fumonisin-B1': 'CCCCC(C)C(C(CC(C)CC(CCCCC(CC(C(C)N)O)O)O)OC(=O)CC(CC(=O)O)C(=O)O)OC(=O)CC(CC(=O)O)C(=O)O',
            'aflatoxin-B1': 'COC1=C2C3=C(C(=O)CC3)C(=O)OC2=C4C5C=COC5OC4=C1',
            '2,4,6-trichlorophenol': 'C1=C(C=C(C(=C1Cl)O)Cl)Cl',
            'diazinon': 'CCOP(=S)(OCC)OC1=NC(=NC(=C1)C)C(C)C',
            'paraquat': 'C[N+]1=CC=C(C=C1)C2=CC=[N+](C=C2)C',
            'phenol': 'C1=CC=C(C=C1)O',
            'aminomethylphosphonic acid': 'C(N)P(=O)(O)O',
            'chlorpyriphos': 'CCOP(=S)(OCC)OC1=NC(=C(C=C1Cl)Cl)Cl',
            'xearalenone': 'CC1CCCC(=O)CCCC=CC2=C(C(=CC(=C2)O)O)C(=O)O1',
            'aldicarb': 'CC(C)(C=NOC(=O)NC)SC'
        }
        return smiles

    @staticmethod
    def get_smarts():

        smarts = {
            '3,3′,4,4′,5-pentachlorobiphenyl': '[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#6]1:[#6]:[#6](:[#6](:[#6](:[#6]:1)-[#17])-[#17])-[#17])-[#17])-[#17]',
            '3,4,3′,4′-tetrachlorobiphenyl': '[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1)-[#17])-[#17])-[#17])-[#17]',
            '2,2′,4,4′,5,5′-hexachlorobiphenyl': '[#6]1:[#6](:[#6](:[#6]:[#6](:[#6]:1-[#17])-[#17])-[#17])-[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#17])-[#17])-[#17]',
            'bisphenol A': '[#6]-[#6](-[#6])(-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#8])-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#8]',
            '2,3,3′,4,4′,5′-hexachlorobiphenyl': '[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#6]1:[#6]:[#6](:[#6](:[#6](:[#6]:1-[#17])-[#17])-[#17])-[#17])-[#17])-[#17]',
            '2,2′,4,4′,6,6′-hexachlorobiphenyl': '[#6]1:[#6](:[#6]:[#6](:[#6](:[#6]:1-[#17])-[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#17])-[#17])-[#17])-[#17])-[#17]',
            '2,2′,4,4′,5,6′-hexachlorobiphenyl': '[#6]1:[#6]:[#6]:[#6](:[#6](:[#6]:1)-[#6]1:[#6](:[#6](:[#6](:[#6](:[#6]:1-[#17])-[#17])-[#17])-[#17])-[#17])-[#17]',
            'lindane': '[#6]1(-[#6](-[#6](-[#6](-[#6](-[#6]-1-[#17])-[#17])-[#17])-[#17])-[#17])-[#17]',
            'naphthalene': '[#6]1:[#6]:[#6]:[#6]2:[#6]:[#6]:[#6]:[#6]:[#6]:2:[#6]:1',
            'benz[e]acephenanthrylene': '[#6]1:[#6]:[#6]:[#6]2:[#6]3:[#6]4:[#6](:[#6]:[#6]:[#6]:3)-[#6]3:[#6]:[#6]:[#6]:[#6]:[#6]:3-[#6]:4:[#6]:[#6]:2:[#6]:1',
            'dieldrin': '[#6]1-[#6]2-[#6]3-[#6](-[#6]-1-[#6]1-[#6]-2-[#8]-1)-[#6]1(-[#6](=[#6](-[#6]-3(-[#6]-1(-[#17])-[#17])-[#17])-[#17])-[#17])-[#17]',
            'linuron': '[#6]-[#7](-[#6](=[#8])-[#7]-[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1)-[#17])-[#17])-[#8]-[#6]',
            'trifluralin': '[#6]-[#6]-[#6]-[#7](-[#6]-[#6]-[#6])-[#6]1:[#6](:[#6]:[#6](:[#6]:[#6]:1-[#7+](=[#8])-[#8-])-[#6](-[#9])(-[#9])-[#9])-[#7+](=[#8])-[#8-]',
            'toluene': '[#6]-[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1',
            'benzene': '[#6]1:[#6]:[#6]:[#6]:[#6]:[#6]:1',
            'bisphenol S': '[#6]1:[#6]:[#6](:[#6]:[#6]:[#6]:1-[#8])-[#16](=[#8])(=[#8])-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#8]',
            'bisphenol F': '[#6]1:[#6]:[#6](:[#6]:[#6]:[#6]:1-[#6]-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#8])-[#8]',
            'benzo[a]pyrene': '[#6]1:[#6]:[#6]:[#6]2:[#6]3:[#6]4:[#6](:[#6]:[#6]:2:[#6]:1):[#6]:[#6]:[#6]1:[#6]:4:[#6](:[#6]:[#6]:[#6]:1):[#6]:[#6]:3',
            '2,4-dichlorophenoxyacetic acid': '[#6]1:[#6]:[#6](:[#6](:[#6]:[#6]:1-[#17])-[#17])-[#8]-[#6]-[#6](=[#8])-[#8]',
            'clofenotane (DDT)': '[#6]1:[#6]:[#6](:[#6]:[#6]:[#6]:1-[#6](-[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#17])-[#6](-[#17])(-[#17])-[#17])-[#17]',
            'pyrene': '[#6]1:[#6]:[#6]2:[#6]3:[#6](:[#6]:1):[#6]:[#6]:[#6]1:[#6]:[#6]:[#6]:[#6](:[#6]:3:1):[#6]:[#6]:2',
            'deoxynivalenol (vomitoxin)': '[#6]-[#6]1=[#6]-[#6]2-[#6](-[#6](-[#6]-1=[#8])-[#8])(-[#6]1(-[#6]-[#6](-[#6](-[#6]-13-[#6]-[#8]-3)-[#8]-2)-[#8])-[#6])-[#6]-[#8]',
            'glyphosate': '[#6](-[#6](=[#8])-[#8])-[#7]-[#6]-[#15](=[#8])(-[#8])-[#8]',
            'fumonisin-B1': '[#6]-[#6]-[#6]-[#6]-[#6](-[#6])-[#6](-[#6](-[#6]-[#6](-[#6])-[#6]-[#6](-[#6]-[#6]-[#6]-[#6]-[#6](-[#6]-[#6](-[#6](-[#6])-[#7])-[#8])-[#8])-[#8])-[#8]-[#6](=[#8])-[#6]-[#6](-[#6]-[#6](=[#8])-[#8])-[#6](=[#8])-[#8])-[#8]-[#6](=[#8])-[#6]-[#6](-[#6]-[#6](=[#8])-[#8])-[#6](=[#8])-[#8]',
            'aflatoxin-B1': '[#6]-[#8]-[#6]1:[#6]2:[#6]3:[#6](-[#6](=[#8])-[#6]-[#6]-3):[#6](=[#8]):[#8]:[#6]:2:[#6]2-[#6]3-[#6]=[#6]-[#8]-[#6]-3-[#8]-[#6]:2:[#6]:1',
            '2,4,6-trichlorophenol': '[#6]1:[#6](:[#6]:[#6](:[#6](:[#6]:1-[#17])-[#8])-[#17])-[#17]',
            'diazinon': '[#6]-[#6]-[#8]-[#15](=[#16])(-[#8]-[#6]-[#6])-[#8]-[#6]1:[#7]:[#6](:[#7]:[#6](:[#6]:1)-[#6])-[#6](-[#6])-[#6]',
            'paraquat': '[#6]-[#7+]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#6]1:[#6]:[#6]:[#7+](:[#6]:[#6]:1)-[#6]',
            'phenol': '[#6]1:[#6]:[#6]:[#6](:[#6]:[#6]:1)-[#8]',
            'aminomethylphosphonic acid': '[#6](-[#7])-[#15](=[#8])(-[#8])-[#8]',
            'chlorpyriphos': '[#6]-[#6]-[#8]-[#15](=[#16])(-[#8]-[#6]-[#6])-[#8]-[#6]1:[#7]:[#6](:[#6](:[#6]:[#6]:1-[#17])-[#17])-[#17]',
            'xearalenone': '[#6]-[#6]1-[#6]-[#6]-[#6]-[#6](=[#8])-[#6]-[#6]-[#6]-[#6]=[#6]-[#6]2:[#6](:[#6](:[#6]:[#6](:[#6]:2)-[#8])-[#8])-[#6](=[#8])-[#8]-1',
            'aldicarb': '[#6]-[#6](-[#6])(-[#6]=[#7]-[#8]-[#6](=[#8])-[#7]-[#6])-[#16]-[#6]',
        }

        return smarts
