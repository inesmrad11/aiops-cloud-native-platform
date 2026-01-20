# CI secrets setup

This file explains how to provide credentials for the GitHub Actions pipeline. Preferred: add `AZURE_CREDENTIALS` (service principal JSON). Fallback: add `ACR_USERNAME` and `ACR_PASSWORD`.

1) Create an Azure service principal (preferred)

Replace the subscription id if different. This command creates a service principal with Contributor role scoped to the resource group and outputs the `--sdk-auth` JSON suitable for `AZURE_CREDENTIALS`.

```bash
az ad sp create-for-rbac \
  --name "aiops-ci-sp" \
  --role Contributor \
  --scopes /subscriptions/aeeb39f5-51cc-4571-9c8a-883fa5a53867/resourceGroups/rg-aiops-dev \
  --sdk-auth
```

Save the JSON output. It looks like:

```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  ...
}
```

2) Add `AZURE_CREDENTIALS` to GitHub repository secrets (recommended)

- UI: Repository → Settings → Secrets and variables → Actions → New repository secret
  - Name: `AZURE_CREDENTIALS`
  - Value: paste the full JSON from the previous command

- CLI (requires repo admin permissions):

```bash
# assuming $AZ_JSON holds the JSON
gh secret set AZURE_CREDENTIALS --body "$AZ_JSON"
```

3) Fallback: ACR username/password (less secure)

Get the ACR admin credentials (if admin user is enabled) or create a service principal with pull/push permissions to ACR. To read admin creds:

```bash
ACR_NAME=acraioopsdev395
ACR_USERNAME=$(az acr credential show -n $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show -n $ACR_NAME --query "passwords[0].value" -o tsv)
echo "$ACR_USERNAME" "$ACR_PASSWORD"
```

Add them to GitHub secrets:

```bash
gh secret set ACR_USERNAME --body "$ACR_USERNAME"
gh secret set ACR_PASSWORD --body "$ACR_PASSWORD"
```

Or use the UI: Repository → Settings → Secrets and variables → Actions → New repository secret

4) Trigger the workflow

- Manually: GitHub → Actions → select the workflow `AIOps CI/CD Pipeline` → Run workflow → choose `main` → Run
- CLI: `gh workflow run ci-cd-pipeline.yaml --ref main`

Notes
- `gh secret set` requires repo admin permissions and a valid `GITHUB_TOKEN` scope; if it fails, use the UI.
- Creating a service principal requires Azure privileges; if your account lacks permission, ask a tenant admin to run the `az ad sp create-for-rbac ... --sdk-auth` command and add the secret.

After secrets are added, re-run the workflow and inspect logs. If you want, I can trigger the workflow and stream logs once you confirm secrets are present.
