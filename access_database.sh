#!/bin/bash
# MariaDB Database Access Helper Script
# This script provides safe ways to access your MariaDB database

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         MariaDB Database Access Helper                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

DB_USER="_af6374d4ed93f504"
DB_PASS="zTmiKxBrhzpoetXi"
DB_NAME="_af6374d4ed93f504"

echo "📊 Database Information:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mysql -u "$DB_USER" -p"$DB_PASS" -e "
SELECT 
    table_schema AS 'Database',
    COUNT(*) AS 'Tables',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = '$DB_NAME'
GROUP BY table_schema;
" 2>/dev/null | grep -v "Warning"

echo ""
echo "📋 All Tables in Database:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mysql -u "$DB_USER" -p"$DB_PASS" -e "SHOW TABLES FROM $DB_NAME;" 2>/dev/null | grep -v "Warning" | head -30

echo ""
echo "📁 Database File Location:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   /opt/homebrew/var/mysql/$DB_NAME/"
echo ""
echo "   To view files (you have access):"
echo "   ls -la /opt/homebrew/var/mysql/$DB_NAME/ | head -20"
echo ""

echo "💾 Backup Command:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   mysqldump -u $DB_USER -p'$DB_PASS' $DB_NAME > backup_\$(date +%Y%m%d).sql"
echo ""

echo "🔌 Connect to Database:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   mysql -u $DB_USER -p'$DB_PASS' $DB_NAME"
echo ""

echo "📂 View Database Files (Safe Method):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "/opt/homebrew/var/mysql/$DB_NAME" ]; then
    echo "   ✅ Database directory exists"
    echo "   File count: $(ls -1 /opt/homebrew/var/mysql/$DB_NAME/*.frm 2>/dev/null | wc -l | tr -d ' ') .frm files"
    echo "   Size: $(du -sh /opt/homebrew/var/mysql/$DB_NAME/ 2>/dev/null | cut -f1)"
else
    echo "   ❌ Database directory not found"
fi
echo ""

