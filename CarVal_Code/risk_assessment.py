import re
import pydot
import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph(nx.nx_pydot.read_dot('AttackGraph.dot'))


def parse_vulExists(label_string):
    split_string = label_string.split('\'')
    fea = int(split_string[1][3:])/10
    imp = int(split_string[3][3:])/10
    return fea, imp

def parse_attackerCanAccess(label_string):
    split_string = label_string.split('\'')
    fea = int(split_string[1][3:])/10
    return fea

def parse_attackRuleNode(label_string):
    split_string = re.split('\: | |\"|\n|\)', label_string)
    fea = int(split_string[-4][3:])/10
    imp = int(split_string[-3][3:])/10
    return fea, imp


def compute_TARA_attackNode(keys_prim_nodes):
    fea = 1
    imp = 1
    for key in keys_prim_nodes:
        if('fea' in G.nodes[key]):
            fea = fea * G.nodes[key]['fea']
        if('imp' in G.nodes[key]):
            imp = imp * G.nodes[key]['imp']
    return fea, imp


# Parse TARA scores
for key in G.nodes:
    if ( 'shape' in G.nodes[key]) and ( 'label' in G.nodes[key])  and (G.nodes[key]['shape'] == 'box') and ( 'vulExists' in G.nodes[key]['label']) :
        fea, imp = parse_vulExists(G.nodes[key]['label'])
        G.nodes[key]['fea'] = fea
        G.nodes[key]['imp'] = imp
    if ( 'shape' in G.nodes[key]) and ( 'label' in G.nodes[key])  and (G.nodes[key]['shape'] == 'box') and ( 'attackerCanAccess' in G.nodes[key]['label']) :
        fea = parse_attackerCanAccess(G.nodes[key]['label'])
        G.nodes[key]['fea'] = fea
    if ( 'shape' in G.nodes[key]) and (G.nodes[key]['shape'] == 'ellipse'):
        fea, imp = parse_attackRuleNode(G.nodes[key]['label'])
        G.nodes[key]['fea'] = fea
        G.nodes[key]['imp'] = imp


attackNode_keys = []
for key in G.nodes:
    if ( 'shape' in G.nodes[key]) and (G.nodes[key]['shape'] == 'ellipse'):
        attackNode_keys.append(key)
        #print(key)
        #print(G.nodes[key])


for key in reversed(attackNode_keys):
    print(key)
    print(G.nodes[key])
    keys_prim_nodes = [n for n in G.predecessors(key)]
    key_derived_attackNode = [n for n in G.successors(key)]
    fea_pre, imp_pre = compute_TARA_attackNode(keys_prim_nodes)
    fea_current = fea_pre * G.nodes[key]['fea']
    imp_current = imp_pre * G.nodes[key]['imp']
    #print(fea_current, imp_current)
    key_suc_attackNode = key_derived_attackNode[0]
    G.nodes[key_suc_attackNode]['fea'] = round(fea_current, 3)
    G.nodes[key_suc_attackNode]['imp'] = round(imp_current, 3)
    G.nodes[key_suc_attackNode]['risk'] = round(0.001 + fea_current * imp_current, 3)
    #print(keys_prim_nodes)
    #print(key_derived_attackNode)
    print('**********')



for key in G.nodes:
    if ('shape' in G.nodes[key] and (G.nodes[key]['shape'] == 'diamond')):
        print(key)
        #print(G.nodes[key])
        #G.nodes[key]['label'] = G.nodes[key]['label'] + ' fea-' + str(G.nodes[key]['fea']) + ' imp-' + str(G.nodes[key]['imp']) + ' risk-' + str(G.nodes[key]['risk'])
        G.nodes[key]['label'] = G.nodes[key]['label'].replace(':', '-') + ' fea-' + str(G.nodes[key]['fea']) + ' imp-' + str(G.nodes[key]['imp']) + ' risk-' + str(G.nodes[key]['risk'])
        print(G.nodes[key]['label'])


print("***************")
print(G.nodes)
print("***************")

nx.drawing.nx_pydot.write_dot(G, 'risk_assess_output.dot')
PG = nx.nx_pydot.to_pydot(G)


PG.write_pdf("risk_assess_output.pdf")
PG.write_png("risk_assess_output.png")




