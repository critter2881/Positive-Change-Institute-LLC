import yaml
import requests

# Load the Ultimate Manifest YAML file
manifest_file = 'path/to/ultimate_manifest.yaml'  # Update with the actual path

# Function to create a GitHub Project Board task

def create_github_task(title, description, labels, status):
    # Set the GitHub API URL for the project board tasks
    url = 'https://api.github.com/projects/columns/{column_id}/cards'  # Replace with the correct column ID
    # Prepare the data for the task
    task_data = {
        'note': f'Description: {description}\nStatus: {status}',
        'labels': labels,  # Labels should be in a list format
    }
    headers = {
        'Authorization': 'token YOUR_GITHUB_TOKEN',  # Use your GitHub token
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.post(url, json=task_data, headers=headers)
    if response.status_code == 201:
        print(f'Task created: {title}')
    else:
        print(f'Failed to create task: {response.status_code} - {response.text}') 

# Main logic to parse the manifest and create tasks
with open(manifest_file, 'r') as file:
    manifest = yaml.safe_load(file)

for task in manifest['tasks']:
    title = task['title']
    description = task.get('description', 'No description provided')
    labels = task.get('labels', [])  # List of labels
    status = task.get('status', 'To Do')  # Default status
    create_github_task(title, description, labels, status)