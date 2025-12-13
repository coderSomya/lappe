#!/bin/bash
# AWS Deployment Helper Script
# This script helps you deploy your Frappe + API server to AWS

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         AWS Deployment Helper Script                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="./backups"
DB_USER="_af6374d4ed93f504"
DB_PASS="zTmiKxBrhzpoetXi"
DB_NAME="_af6374d4ed93f504"

echo "📋 This script will help you:"
echo "   1. Backup your local database"
echo "   2. Prepare files for AWS deployment"
echo "   3. Generate deployment commands"
echo ""

# Step 1: Backup Database
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Creating Database Backup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

mkdir -p "$BACKUP_DIR"

BACKUP_FILE="$BACKUP_DIR/frappe_lending_backup_$(date +%Y%m%d_%H%M%S).sql"

echo "Creating backup: $BACKUP_FILE"
mysqldump -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE" 2>&1

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✅ Backup created successfully!${NC}"
    echo "   Size: $BACKUP_SIZE"
    echo "   File: $BACKUP_FILE"
else
    echo -e "${RED}❌ Backup failed!${NC}"
    exit 1
fi

echo ""

# Step 2: Create deployment package
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Creating Deployment Package"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DEPLOY_DIR="./deploy_package"
mkdir -p "$DEPLOY_DIR"

# Copy server folder
echo "Copying server folder..."
cp -r server "$DEPLOY_DIR/"

# Copy backup
echo "Copying database backup..."
cp "$BACKUP_FILE" "$DEPLOY_DIR/"

# Create deployment info
cat > "$DEPLOY_DIR/DEPLOYMENT_INFO.txt" << EOF
╔════════════════════════════════════════════════════════════════╗
║              DEPLOYMENT INFORMATION                            ║
╚════════════════════════════════════════════════════════════════╝

Database Backup: $(basename $BACKUP_FILE)
Backup Size: $BACKUP_SIZE

Local Database Details:
  Database: $DB_NAME
  User: $DB_USER
  Host: 127.0.0.1
  Port: 3306

Next Steps:
1. Upload deploy_package/ to your EC2 instance
2. Import database to RDS
3. Deploy server code
4. Configure services

See AWS_HOSTING_COMPLETE_GUIDE.md for detailed instructions.
EOF

echo -e "${GREEN}✅ Deployment package created!${NC}"
echo "   Location: $DEPLOY_DIR"
echo ""

# Step 3: Generate upload commands
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Upload Commands"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cat > "$DEPLOY_DIR/UPLOAD_COMMANDS.sh" << 'EOFSCRIPT'
#!/bin/bash
# Commands to upload files to EC2
# Replace [EC2-IP] and [KEY-FILE] with your values

EC2_IP="[YOUR-EC2-IP]"
KEY_FILE="[YOUR-KEY-FILE.pem]"

echo "Uploading server folder..."
scp -i "$KEY_FILE" -r server/ ubuntu@$EC2_IP:~/frappe-bench/

echo "Uploading database backup..."
scp -i "$KEY_FILE" frappe_lending_backup_*.sql ubuntu@$EC2_IP:~/backups/

echo "✅ Upload complete!"
EOFSCRIPT

chmod +x "$DEPLOY_DIR/UPLOAD_COMMANDS.sh"

echo -e "${GREEN}✅ Upload script created!${NC}"
echo "   Edit: $DEPLOY_DIR/UPLOAD_COMMANDS.sh"
echo ""

# Step 4: Generate import commands
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Database Import Commands"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cat > "$DEPLOY_DIR/IMPORT_DATABASE.sh" << 'EOFIMPORT'
#!/bin/bash
# Commands to import database to RDS
# Replace [RDS-ENDPOINT] and [PASSWORD] with your values

RDS_ENDPOINT="[YOUR-RDS-ENDPOINT]"
RDS_USER="frappe_admin"
RDS_PASS="[YOUR-RDS-PASSWORD]"
DB_NAME="frappe_lending"
BACKUP_FILE="frappe_lending_backup_*.sql"

echo "Creating database on RDS..."
mysql -h "$RDS_ENDPOINT" -u "$RDS_USER" -p"$RDS_PASS" \
  -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "Importing database..."
mysql -h "$RDS_ENDPOINT" -u "$RDS_USER" -p"$RDS_PASS" \
  "$DB_NAME" < "$BACKUP_FILE"

echo "✅ Database imported!"
EOFIMPORT

chmod +x "$DEPLOY_DIR/IMPORT_DATABASE.sh"

echo -e "${GREEN}✅ Import script created!${NC}"
echo "   Edit: $DEPLOY_DIR/IMPORT_DATABASE.sh"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Deployment Package Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Package Location: $DEPLOY_DIR"
echo ""
echo "Contents:"
echo "  ✅ server/ - Your API server code"
echo "  ✅ $(basename $BACKUP_FILE) - Database backup"
echo "  ✅ DEPLOYMENT_INFO.txt - Deployment information"
echo "  ✅ UPLOAD_COMMANDS.sh - Upload script"
echo "  ✅ IMPORT_DATABASE.sh - Database import script"
echo ""
echo "Next Steps:"
echo "  1. Read: AWS_HOSTING_COMPLETE_GUIDE.md"
echo "  2. Create AWS RDS and EC2 instances"
echo "  3. Edit and run: $DEPLOY_DIR/UPLOAD_COMMANDS.sh"
echo "  4. Edit and run: $DEPLOY_DIR/IMPORT_DATABASE.sh"
echo "  5. Follow the complete guide for remaining steps"
echo ""
echo -e "${GREEN}✅ Ready for deployment!${NC}"
echo ""

