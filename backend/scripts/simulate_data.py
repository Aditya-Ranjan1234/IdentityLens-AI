import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Constants
NUM_USERS = 500
NUM_AUDIT_LOGS = 10000
NUM_PRIVILEGE_CHANGES = 100
NUM_OFFBOARDING = 100

# Utility functions
def random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def random_datetime(start_date, end_date):
    time_between = end_date - start_date
    seconds_between = time_between.total_seconds()
    random_seconds = random.randrange(int(seconds_between))
    return start_date + timedelta(seconds=random_seconds)

today = datetime.now()
start_year_ago = today - timedelta(days=365)
end_year_from_now = today + timedelta(days=365)

# Departments and titles
departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'IT']
titles = ['SWE', 'Senior SWE', 'Staff SWE', 'Manager', 'Director', 'VP', 'Analyst', 'Designer']

# Platforms
platforms = ['AD', 'AWS', 'Okta', 'Salesforce']

# Generate users
users = []
for i in range(NUM_USERS):
    user_id = f"U{str(i+1).zfill(4)}"
    name = fake.name()
    email = fake.email()
    dept = random.choice(departments)
    title = random.choice(titles)
    manager = random.choice(users)['name'] if i > 10 else "CEO"
    emp_type = random.choice(['Full-Time', 'Contractor', 'Intern'])
    hire_date = random_date(start_year_ago, today)
    term_date = None
    if random.random() < 0.15:  # 15% terminated
        term_date = random_date(hire_date, today)
    status = 'ACTIVE' if term_date is None else 'INACTIVE'
    
    users.append({
        'user_id': user_id,
        'name': name,
        'email': email,
        'department': dept,
        'title': title,
        'manager': manager,
        'employment_type': emp_type,
        'hire_date': hire_date.strftime('%Y-%m-%d'),
        'termination_date': term_date.strftime('%Y-%m-%d') if term_date else '',
        'status': status
    })

with open(os.path.join(os.path.dirname(__file__), '../data/users.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'name', 'email', 'department', 'title', 'manager', 'employment_type', 'hire_date', 'termination_date', 'status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for user in users:
        writer.writerow(user)

# Generate AD accounts
ad_accounts = []
for user in users:
    ad_account = user['name'].lower().replace(' ', '.')
    status = 'ACTIVE' if user['status'] == 'ACTIVE' else 'DISABLED'
    last_login = random_date(start_year_ago, today).strftime('%Y-%m-%d') if status == 'ACTIVE' else ''
    ad_accounts.append({
        'user_id': user['user_id'],
        'ad_account': ad_account,
        'status': status,
        'last_login': last_login
    })

with open(os.path.join(os.path.dirname(__file__), '../data/ad_accounts.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'ad_account', 'status', 'last_login']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for acc in ad_accounts:
        writer.writerow(acc)

# Generate AWS accounts
aws_accounts = []
aws_roles = ['ReadOnlyAccess', 'AdministratorAccess', 'AmazonS3FullAccess', 'AmazonEC2FullAccess', 'PowerUserAccess']
for user in users:
    aws_user = user['name'].lower().replace(' ', '-')
    roles = random.sample(aws_roles, k=random.randint(1, 3))
    last_login = random_date(start_year_ago, today).strftime('%Y-%m-%d') if user['status'] == 'ACTIVE' else ''
    aws_accounts.append({
        'user_id': user['user_id'],
        'aws_user': aws_user,
        'roles': ','.join(roles),
        'last_login': last_login
    })

with open(os.path.join(os.path.dirname(__file__), '../data/aws_accounts.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'aws_user', 'roles', 'last_login']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for acc in aws_accounts:
        writer.writerow(acc)

# Generate nested groups structure
okta_groups = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Admins', 'All Users', 'SRE', 'DevOps', 'AWS_Admins', 'Engineering_Leads']
group_nesting = {
    'DevOps': ['Engineering', 'Admins'],
    'AWS_Admins': ['Admins', 'DevOps'],
    'Engineering_Leads': ['Engineering', 'Admins'],
    'SRE': ['Engineering', 'DevOps']
}
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

# Generate group hierarchy CSV
group_hierarchy = []
for group, parents in group_nesting.items():
    for parent in parents:
        group_hierarchy.append({
            'group_name': group,
            'parent_group': parent,
            'platform': 'Okta'
        })
    group_hierarchy.append({
        'group_name': 'Admins',
        'parent_group': '',
        'platform': 'Okta'
    })
    group_hierarchy.append({
        'group_name': 'Engineering',
        'parent_group': 'All Users',
        'platform': 'Okta'
    })

with open(os.path.join(os.path.dirname(__file__), '../data/group_hierarchy.csv'), 'w', newline='') as csvfile:
    fieldnames = ['group_name', 'parent_group', 'platform']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for gh in group_hierarchy:
        writer.writerow(gh)

# Generate Okta accounts with nested group permissions
okta_accounts = []
for user in users:
    okta_id = user['email']
    groups = random.sample(okta_groups, k=random.randint(1, 2))
    mfa = random.choice([True, False])
    okta_accounts.append({
        'user_id': user['user_id'],
        'okta_id': okta_id,
        'groups': ','.join(groups),
        'mfa_enabled': mfa
    })

with open(os.path.join(os.path.dirname(__file__), '../data/okta_accounts.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'okta_id', 'groups', 'mfa_enabled']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for acc in okta_accounts:
        writer.writerow(acc)

# Generate Salesforce accounts
salesforce_accounts = []
sf_profiles = ['Standard User', 'System Administrator', 'Marketing User', 'Sales User']
sf_perms = ['View All Data', 'Modify All Data', 'Delete Records', 'Export Reports']
for user in users:
    profile = random.choice(sf_profiles)
    perms = random.sample(sf_perms, k=random.randint(1, 2))
    salesforce_accounts.append({
        'user_id': user['user_id'],
        'profile': profile,
        'permissions': ','.join(perms)
    })

with open(os.path.join(os.path.dirname(__file__), '../data/salesforce_accounts.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'profile', 'permissions']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for acc in salesforce_accounts:
        writer.writerow(acc)

# Generate audit logs
actions = ['LOGIN', 'LOGOUT', 'S3_ACCESS', 'EC2_ACCESS', 'PRIVILEGE_CHANGE', 'API_CALL']
resources = ['customer_bucket', 'prod_ec2', 'dev_s3', 'user_data', 'salesforce_leads']
countries = ['USA', 'Canada', 'UK', 'Germany', 'India', 'Russia', 'China', 'Brazil']

audit_logs = []
for i in range(NUM_AUDIT_LOGS):
    user = random.choice(users)
    timestamp = random_datetime(start_year_ago, today).isoformat() + 'Z'
    platform = random.choice(platforms)
    action = random.choice(actions)
    resource = random.choice(resources)
    ip = fake.ipv4()
    country = random.choice(countries)
    success = random.random() > 0.1  # 90% success rate
    audit_logs.append({
        'timestamp': timestamp,
        'user_id': user['user_id'],
        'platform': platform,
        'action': action,
        'resource': resource,
        'ip': ip,
        'country': country,
        'success': 'TRUE' if success else 'FALSE'
    })

with open(os.path.join(os.path.dirname(__file__), '../data/audit_logs.csv'), 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'user_id', 'platform', 'action', 'resource', 'ip', 'country', 'success']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for log in audit_logs:
        writer.writerow(log)

# Generate privilege changes
privilege_changes = []
for i in range(NUM_PRIVILEGE_CHANGES):
    user = random.choice(users)
    old_role = random.choice(aws_roles)
    new_role = random.choice(aws_roles)
    platform = random.choice(platforms)
    timestamp = random_datetime(start_year_ago, today).isoformat() + 'Z'
    privilege_changes.append({
        'user_id': user['user_id'],
        'old_role': old_role,
        'new_role': new_role,
        'platform': platform,
        'timestamp': timestamp
    })

with open(os.path.join(os.path.dirname(__file__), '../data/privilege_changes.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'old_role', 'new_role', 'platform', 'timestamp']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for change in privilege_changes:
        writer.writerow(change)

# Generate offboarding records
offboarding = []
for user in users:
    if user['termination_date']:
        # Create some gaps!
        ad_disabled = random.random() > 0.1  # 10% chance AD still enabled
        aws_disabled = random.random() > 0.2  # 20% chance AWS still enabled
        okta_disabled = random.random() > 0.15  # 15% chance Okta still enabled
        offboarding.append({
            'user_id': user['user_id'],
            'termination_date': user['termination_date'],
            'ad_disabled': 'TRUE' if ad_disabled else 'FALSE',
            'aws_disabled': 'TRUE' if aws_disabled else 'FALSE',
            'okta_disabled': 'TRUE' if okta_disabled else 'FALSE'
        })

with open(os.path.join(os.path.dirname(__file__), '../data/offboarding.csv'), 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'termination_date', 'ad_disabled', 'aws_disabled', 'okta_disabled']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for record in offboarding:
        writer.writerow(record)

print("Data simulation complete!")
