# 🚀 Quick Start Guide - AWS Deployment

Deploy your pharmaceutical order management system to AWS in under 10 minutes!

## ⚡ Prerequisites (5 minutes)

1. **Install AWS CLI**:
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip && sudo ./aws/install
   aws configure  # Enter your AWS credentials
   ```

2. **Install Terraform**:
   ```bash
   # macOS
   brew install terraform
   
   # Ubuntu/Debian
   sudo apt-get update && sudo apt-get install terraform
   ```

3. **Install Docker**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install docker.io
   sudo systemctl start docker
   sudo usermod -aG docker $USER
   
   # macOS
   brew install docker
   ```

## 🚀 Deploy (3 minutes)

1. **Configure deployment**:
   ```bash
   cd terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars - change db_password at minimum!
   ```

2. **Deploy everything**:
   ```bash
   ./deploy.sh
   ```

3. **Wait for completion** (2-3 minutes)

## ✅ Validate (1 minute)

```bash
./validate-deployment.sh
```

## 🎉 Access Your Application

After successful deployment:
- **Application**: Use the URL displayed by the deployment script
- **Login**: Create a new user account or use existing credentials
- **API Docs**: Add `/docs` to your application URL

## 💰 Cost

Approximately **$55-80/month** for a small production deployment.

## 🧹 Cleanup

To remove everything:
```bash
cd terraform
terraform destroy
```

## 🆘 Need Help?

- Check `DEPLOYMENT.md` for detailed instructions
- Review CloudWatch logs for errors
- Ensure AWS credentials have proper permissions

---

**That's it! Your pharmaceutical order management system is now running on AWS! 🎉**