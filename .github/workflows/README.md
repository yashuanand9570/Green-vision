# 🚀 GitHub Actions Workflows Guide

This project includes GitHub Actions workflows that let you deploy and manage AWS infrastructure directly from the GitHub UI - no terminal or CLI needed!

## 📋 Available Workflows

### 1. Deploy Infrastructure 🏗️

**File**: `.github/workflows/deploy-infrastructure.yml`

**Purpose**: Deploy, update, or destroy your AWS infrastructure with a single click.

**How to Use**:
1. Navigate to the **Actions** tab in your GitHub repository
2. Select **Deploy Infrastructure** from the workflows list
3. Click the **Run workflow** dropdown button
4. Configure your deployment:
   - **Environment**: Choose `dev`, `staging`, or `production`
   - **Terraform action**: 
     - `plan` - Preview changes without applying
     - `apply` - Deploy/update infrastructure
     - `destroy` - Remove all infrastructure
5. Click **Run workflow** to start

**What It Does**:
- ✅ Checks out your code
- ✅ Configures AWS credentials securely
- ✅ Initializes Terraform
- ✅ Creates a Terraform plan
- ✅ Applies changes (if action is `apply`)
- ✅ Destroys infrastructure (if action is `destroy`)
- ✅ Outputs all resource details in a beautiful summary
- ✅ Saves outputs as downloadable artifacts

**Output Summary Includes**:
- 🖥️ **EC2 Instance**: Instance ID, Public IP, Public DNS
- 🐳 **ECR Repository**: Repository URL and Name
- 📦 **S3 Buckets**: Model and Prediction data bucket names
- 🌐 **Application URL**: Direct clickable link

**Artifacts Generated**:
- `terraform-outputs-{env}`: JSON file with all Terraform outputs
- `terraform-plan-{env}`: Terraform plan file for review

---

### 2. Infrastructure Status 🔍

**File**: `.github/workflows/infrastructure-status.yml`

**Purpose**: Check the current state of your infrastructure without making any changes.

**How to Use**:
1. Navigate to the **Actions** tab
2. Select **Infrastructure Status**
3. Click **Run workflow**
4. Optionally enable **detailed output** for more information
5. Click **Run workflow**

**What It Does**:
- ✅ Lists all resources in Terraform state
- ✅ Shows current infrastructure outputs
- ✅ Queries AWS for running resources
- ✅ Lists EC2 instances with their status
- ✅ Shows S3 buckets related to the project
- ✅ Lists ECR repositories
- ✅ Displays security groups (if detailed output enabled)
- ✅ Generates a comprehensive status report

**Output Summary Includes**:
- 📊 Terraform state resources
- 🔍 Connection details (IPs, URLs, bucket names)
- 🔎 AWS resource status
- 📝 Detailed resource information (optional)

**Artifacts Generated**:
- `infrastructure-status-report`: Text file with complete status
- `outputs.json`: Current Terraform outputs

---

### 3. Auto Deploy (Existing) ⚙️

**File**: `.github/workflows/terraform.yml`

**Purpose**: Automatically deploy infrastructure when code changes.

**Trigger**: Automatically runs when:
- Code is pushed to `main` branch
- Changes are made to files in `infrastructure/` directory
- Can also be manually triggered

---

## 🎯 Common Use Cases

### First Time Deployment
1. Run **Deploy Infrastructure** with:
   - Environment: `dev`
   - Action: `apply`
2. Wait for completion
3. View the job summary for connection details
4. Download artifacts if needed

### Checking What's Running
1. Run **Infrastructure Status**
2. View the summary for all current resources
3. Download the status report for detailed info

### Making Infrastructure Updates
1. Update Terraform files in `infrastructure/` directory
2. Run **Deploy Infrastructure** with:
   - Environment: `dev` (or your target environment)
   - Action: `plan` (to preview changes)
3. Review the plan output
4. Run again with Action: `apply` to apply changes

### Tearing Down Infrastructure
1. Run **Deploy Infrastructure** with:
   - Environment: `dev` (or your target environment)
   - Action: `destroy`
2. Confirm by clicking **Run workflow**
3. All resources will be removed

---

## 🔐 Required GitHub Secrets

These workflows require the following secrets to be configured in your repository:

| Secret Name | Description |
|-------------|-------------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key ID |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret access key |
| `AWS_DEFAULT_REGION` | AWS region (e.g., `us-east-1`) |

**To add secrets**:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each secret with its value

---

## 📊 Understanding the Outputs

### After Running Deploy Infrastructure

The workflow creates a beautiful job summary with all your infrastructure details:

```
### 🚀 Initializing Terraform for dev environment
✅ Terraform initialized successfully!

### 📋 Creating Terraform Plan
✅ Terraform plan created successfully!

#### Plan Output:
[Terraform plan details...]

### 🏗️ Applying Terraform Configuration
✅ Infrastructure deployed successfully!

### 📊 Infrastructure Details

#### 🖥️ EC2 Instance
- Instance ID: `i-0123456789abcdef0`
- Public IP: `54.123.45.67`
- Public DNS: `ec2-54-123-45-67.compute-1.amazonaws.com`

#### 🐳 ECR Repository
- Repository URL: `123456789012.dkr.ecr.us-east-1.amazonaws.com/sensor`
- Repository Name: `sensor`

#### 📦 S3 Buckets
- Model Bucket: `sensor-model-bucket`
- Prediction Data Bucket: `sensor-pred-data-bucket`

#### 🌐 Application Access
- Application URL: `http://54.123.45.67:8080`

---
✅ Deployment Complete for `dev` environment!
```

---

## 🎨 Features

### Visual Progress
- ✅ Step-by-step progress indicators
- ✅ Clear success/failure messages
- ✅ Emoji-enhanced readability

### Job Summaries
- ✅ Automatically generated after each run
- ✅ Formatted with Markdown for easy reading
- ✅ Includes all important details

### Artifacts
- ✅ Downloadable output files
- ✅ 30-day retention
- ✅ JSON and text formats

### Safety
- ✅ Manual trigger prevents accidental deployments
- ✅ Environment selection for multiple stages
- ✅ Plan before apply workflow

---

## 🛠️ Troubleshooting

### Workflow Fails on Init
- Check that AWS credentials are correctly configured
- Ensure the Terraform state bucket exists (`sensor-tf-state`)
- Verify AWS region in secrets matches your setup

### No Outputs Shown
- Run Infrastructure Status to check if resources exist
- Ensure apply step completed successfully
- Check Terraform state in the workflow logs

### Can't Access Application
- Verify security group allows inbound traffic on port 8080
- Check EC2 instance is running in AWS console
- Ensure public IP is correctly assigned

---

## 📚 Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)

---

## 🤝 Contributing

If you improve these workflows, please:
1. Test thoroughly in a dev environment
2. Update this documentation
3. Submit a pull request

---

**Happy Deploying! 🚀**
