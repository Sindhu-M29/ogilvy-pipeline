import subprocess

def deploy_from_blob_to_app_service(blob_url, app_service_name, resource_group_name):
    # Construct the command to deploy files from Azure Blob Storage to Azure App Service
    command = [
        'az', 'webapp', 'deployment', 'source', 'config',
        'sind-pipeline', resource_group_name,
        'Ogilvy-pipeline', app_service_name,
        'https://ogilvypipesa.blob.core.windows.net/attachments?sp=racwdl&st=2024-03-19T06:49:41Z&se=2024-03-19T14:49:41Z&spr=https&sv=2022-11-02&sr=c&sig=GbUXGfcTgcKBLcqxEqcLMgL3zwCIYSxL07lOiLOQ8rM%3D', blob_url
        
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print("Files deployed successfully from Azure Blob Storage to the Azure App Service.")
    except subprocess.CalledProcessError as e:
        print("Error deploying files from Azure Blob Storage to the Azure App Service:", e)

# Example usage:
blob_url = 'https://ogilvypipesa.blob.core.windows.net/attachments?sp=racwdl&st=2024-03-19T06:49:41Z&se=2024-03-19T14:49:41Z&spr=https&sv=2022-11-02&sr=c&sig=GbUXGfcTgcKBLcqxEqcLMgL3zwCIYSxL07lOiLOQ8rM%3D'
app_service_name = 'Ogilvy-pipeline'
resource_group_name = 'sind-pipeline'

deploy_from_blob_to_app_service(blob_url, app_service_name, resource_group_name)
