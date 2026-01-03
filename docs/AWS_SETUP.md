# AWS Setup and Integration Guide

## Overview
This guide provides step-by-step instructions for setting up AWS services integration with the Bakhmach Business Hub repository.

## Prerequisites
- AWS Account with appropriate permissions
- AWS CLI installed locally
- GitHub account with repository access
- GitHub Personal Access Token

## 1. AWS S3 Setup

### 1.1 Create S3 Buckets

```bash
# Create bucket for documentation
aws s3 mb s3://bakhmach-business-hub-docs --region us-east-1

# Create bucket for source code backups
aws s3 mb s3://bakhmach-business-hub-src --region us-east-1

# Create bucket for artifacts
aws s3 mb s3://bakhmach-business-hub-artifacts --region us-east-1
```

### 1.2 Enable Versioning

```bash
aws s3api put-bucket-versioning \
  --bucket bakhmach-business-hub-docs \
  --versioning-configuration Status=Enabled
```

### 1.3 Configure Bucket Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::bakhmach-business-hub-docs/*"
    }
  ]
}
```

## 2. CloudFront Distribution Setup

### 2.1 Create Distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name bakhmach-business-hub-docs.s3.amazonaws.com \
  --default-root-object index.html
```

### 2.2 Configure Cache Behaviors

- **Cache Policy**: Managed-CachingOptimized
- **Origin Request Policy**: Managed-AllViewer
- **Viewer Protocol Policy**: Redirect HTTP to HTTPS

## 3. IAM User and Access Keys

### 3.1 Create IAM User

```bash
aws iam create-user --user-name bakhmach-github-actions
```

### 3.2 Create Access Keys

```bash
aws iam create-access-key --user-name bakhmach-github-actions
```

Save the Access Key ID and Secret Access Key securely.

### 3.3 Attach Policies

```bash
# S3 Policy
aws iam attach-user-policy \
  --user-name bakhmach-github-actions \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# CloudFront Policy
aws iam attach-user-policy \
  --user-name bakhmach-github-actions \
  --policy-arn arn:aws:iam::aws:policy/CloudFrontFullAccess
```

## 4. GitHub Secrets Configuration

Add the following secrets to your GitHub repository:

```
AWS_ACCESS_KEY_ID: <Your Access Key ID>
AWS_SECRET_ACCESS_KEY: <Your Secret Access Key>
AWS_DISTRIBUTION_ID: <Your CloudFront Distribution ID>
```

### Steps:
1. Go to Repository Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add each secret with the values above

## 5. Local Testing

### 5.1 Configure AWS CLI

```bash
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter region: us-east-1
# Enter output format: json
```

### 5.2 Test S3 Sync

```bash
aws s3 sync ./docs s3://bakhmach-business-hub-docs/ --dryrun
```

### 5.3 Perform Actual Sync

```bash
aws s3 sync ./docs s3://bakhmach-business-hub-docs/ --delete
```

## 6. CloudFront Invalidation

### 6.1 Manual Invalidation

```bash
aws cloudfront create-invalidation \
  --distribution-id E1234EXAMPLE \
  --paths "/*"
```

### 6.2 Invalidate Specific Paths

```bash
aws cloudfront create-invalidation \
  --distribution-id E1234EXAMPLE \
  --paths "/docs/*" "/api/*"
```

## 7. Monitoring and Logging

### 7.1 Enable CloudTrail

```bash
aws cloudtrail create-trail \
  --name bakhmach-business-hub-trail \
  --s3-bucket-name bakhmach-cloudtrail-logs
```

### 7.2 Enable S3 Access Logging

```bash
aws s3api put-bucket-logging \
  --bucket bakhmach-business-hub-docs \
  --bucket-logging-status file://logging.json
```

### logging.json
```json
{
  "LoggingEnabled": {
    "TargetBucket": "bakhmach-logs",
    "TargetPrefix": "s3-access-logs/"
  }
}
```

## 8. Cost Optimization

### 8.1 S3 Lifecycle Policies

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket bakhmach-business-hub-artifacts \
  --lifecycle-configuration file://lifecycle.json
```

### lifecycle.json
```json
{
  "Rules": [
    {
      "Id": "DeleteOldArtifacts",
      "Status": "Enabled",
      "ExpirationInDays": 90,
      "NoncurrentVersionExpirationInDays": 30
    }
  ]
}
```

## 9. Security Best Practices

- [ ] Enable S3 Block Public Access
- [ ] Enable versioning on all buckets
- [ ] Enable server-side encryption (SSE-S3 or SSE-KMS)
- [ ] Enable MFA Delete
- [ ] Use VPC endpoints for private access
- [ ] Enable CloudTrail for audit logging
- [ ] Rotate access keys regularly
- [ ] Use least privilege IAM policies

## 10. Troubleshooting

### Issue: Access Denied when syncing
**Solution**: Verify IAM user has S3FullAccess policy attached

### Issue: CloudFront not invalidating
**Solution**: Check that the distribution ID is correct and IAM user has CloudFrontFullAccess

### Issue: High AWS costs
**Solution**: Review CloudFront cache settings and implement S3 lifecycle policies

## Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS CloudFront Documentation](https://docs.aws.amazon.com/cloudfront/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)

---
*Last Updated: January 3, 2026*
*Maintained by: Bakhmach Business Hub Team*
