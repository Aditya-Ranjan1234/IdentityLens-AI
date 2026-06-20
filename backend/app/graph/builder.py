import networkx as nx
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')

group_permissions = {
    'Admins': ['Modify All Data', 'View All Data', 'Delete Records'],
    'DevOps': ['AdministratorAccess', 'AmazonEC2FullAccess', 'AmazonS3FullAccess'],
    'Engineering_Leads': ['Modify All Data', 'View All Data'],
    'AWS_Admins': ['AdministratorAccess', 'PowerUserAccess'],
    'Engineering': ['ReadOnlyAccess'],
    'Marketing': ['View All Data'],
    'Sales': ['View All Data'],
    'HR': ['View All Data'],
    'Finance': ['View All Data'],
    'All Users': ['View All Data']
}

def get_all_ancestor_groups(G, group_node):
    """Get all ancestor groups for nested group inheritance"""
    ancestors = set()
    for n in nx.ancestors(G, group_node):
        if G.nodes[n].get('type') == 'group':
            ancestors.add(n)
    return ancestors

def calculate_effective_privileges(G, user_id):
    """Calculate effective privileges for a user by traversing group/role hierarchy"""
    effective_perms = set()
    roles = set()
    groups = set()
    
    # Traverse all edges from user
    for platform_acc in G.successors(user_id):
        # Check roles and groups from platform account
        for role_or_group in G.successors(platform_acc):
            if G.nodes[role_or_group].get('type') == 'role':
                roles.add(G.nodes[role_or_group].get('label'))
                effective_perms.add(G.nodes[role_or_group].get('label'))
            elif G.nodes[role_or_group].get('type') == 'group':
                groups.add(G.nodes[role_or_group].get('label'))
                # Get all ancestor groups
                ancestors = get_all_ancestor_groups(G, role_or_group)
                for ancestor in ancestors:
                    ancestor_label = G.nodes[ancestor].get('label')
                    groups.add(ancestor_label)
                    if ancestor_label in group_permissions:
                        effective_perms.update(group_permissions[ancestor_label])
                if G.nodes[role_or_group].get('label') in group_permissions:
                    effective_perms.update(group_permissions[G.nodes[role_or_group].get('label')])
    
    return {
        'effective_permissions': list(effective_perms),
        'roles': list(roles),
        'groups': list(groups)
    }

def build_identity_graph_object():
    """Build and return a NetworkX graph object for internal processing"""
    users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    ad_df = pd.read_csv(os.path.join(DATA_DIR, 'ad_accounts.csv'))
    aws_df = pd.read_csv(os.path.join(DATA_DIR, 'aws_accounts.csv'))
    okta_df = pd.read_csv(os.path.join(DATA_DIR, 'okta_accounts.csv'))
    group_hierarchy_df = pd.read_csv(os.path.join(DATA_DIR, 'group_hierarchy.csv'))
    
    G = nx.DiGraph()
    
    # Add all users first!
    for _, user in users_df.iterrows():
        G.add_node(user['user_id'], type='user', label=user['name'], department=user['department'])
    
    # Add AD platform links
    for _, ad in ad_df.iterrows():
        ad_node = f"AD_{ad['ad_account']}"
        G.add_node(ad_node, type='platform_account', platform='AD', label=ad['ad_account'])
        G.add_edge(ad['user_id'], ad_node, type='has_account')
    
    # Add AWS roles
    for _, aws in aws_df.iterrows():
        aws_node = f"AWS_{aws['aws_user']}"
        G.add_node(aws_node, type='platform_account', platform='AWS', label=aws['aws_user'])
        G.add_edge(aws['user_id'], aws_node, type='has_account')
        for role in aws['roles'].split(','):
            role_node = f"AWS_ROLE_{role}"
            if role_node not in G:
                G.add_node(role_node, type='role', platform='AWS', label=role)
            G.add_edge(aws_node, role_node, type='has_role')
    
    # Add Okta groups first, then nested hierarchy
    for _, gh in group_hierarchy_df.iterrows():
        if pd.notna(gh['parent_group']) and gh['parent_group'] != '':
            child_node = f"Okta_GROUP_{gh['group_name']}"
            parent_node = f"Okta_GROUP_{gh['parent_group']}"
            if parent_node not in G:
                G.add_node(parent_node, type='group', platform=gh['platform'], label=gh['parent_group'])
            if child_node not in G:
                G.add_node(child_node, type='group', platform=gh['platform'], label=gh['group_name'])
            G.add_edge(child_node, parent_node, type='nested_in')  # Edge from child to parent for inheritance
    
    # Add Okta accounts to groups
    for _, okta in okta_df.iterrows():
        okta_node = f"Okta_{okta['okta_id']}"
        G.add_node(okta_node, type='platform_account', platform='Okta', label=okta['okta_id'])
        G.add_edge(okta['user_id'], okta_node, type='has_account')
        for group in okta['groups'].split(','):
            group_node = f"Okta_GROUP_{group}"
            if group_node not in G:
                G.add_node(group_node, type='group', platform='Okta', label=group)
            G.add_edge(okta_node, group_node, type='member_of')
    
    return G


def build_identity_graph():
    """Build graph and return JSON-serializable data for frontend"""
    G = build_identity_graph_object()
    
    # Convert to JSON format for frontend, order to include platform accounts first
    nodes = []
    edges = []
    
    # Order nodes to prioritize platform accounts first
    ordered_nodes = []
    for node, attrs in G.nodes(data=True):
        if attrs.get('type') == 'platform_account':
            ordered_nodes.append((node, attrs))
    for node, attrs in G.nodes(data=True):
        if attrs.get('type') == 'role' or attrs.get('type') == 'group':
            ordered_nodes.append((node, attrs))
    for node, attrs in G.nodes(data=True):
        if attrs.get('type') == 'user':
            ordered_nodes.append((node, attrs))
    
    for node, attrs in ordered_nodes:
        nodes.append({
            'id': node,
            'label': attrs.get('label', node),
            'type': attrs.get('type', 'unknown'),
            'platform': attrs.get('platform')
        })
    
    for u, v, attrs in G.edges(data=True):
        edges.append({
            'source': u,
            'target': v,
            'type': attrs.get('type', 'unknown')
        })
    
    return {'nodes': nodes, 'edges': edges}
