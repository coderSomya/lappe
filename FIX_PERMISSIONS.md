# Fixing MariaDB Permission Issues

## 🔒 **Permission Denied Error - Solutions**

If you're getting "Permission denied" when accessing `/opt/homebrew/var/mysql/`, here are the solutions:

---

## ✅ **Solution 1: You Already Have Access (Recommended)**

You are the owner (`prom3`) of the directory, so you should be able to access it. Try:

```bash
# Navigate to the directory
cd /opt/homebrew/var/mysql/

# List contents
ls -la

# View your database
ls -la _af6374d4ed93f504/ | head -20
```

**If this still gives permission denied**, it might be because:
- You're using a different terminal/session
- The directory permissions changed
- macOS security restrictions

---

## ✅ **Solution 2: Use MySQL Commands (Safest Method)**

Instead of accessing files directly, use MySQL commands:

```bash
# Connect to database
mysql -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' _af6374d4ed93f504

# View all tables
mysql -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' -e "SHOW TABLES FROM _af6374d4ed93f504;"

# Get database size
mysql -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' -e "
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = '_af6374d4ed93f504'
GROUP BY table_schema;"
```

---

## ✅ **Solution 3: Fix Permissions (If Needed)**

If you need to fix permissions:

```bash
# Make sure you own the directory
sudo chown -R prom3:admin /opt/homebrew/var/mysql/

# Set proper permissions
sudo chmod 755 /opt/homebrew/var/mysql/
sudo chmod 700 /opt/homebrew/var/mysql/_af6374d4ed93f504/
```

**⚠️ Warning:** Only do this if you're sure. MariaDB sets these permissions for security.

---

## ✅ **Solution 4: Use the Helper Script**

I've created a helper script for you:

```bash
cd /Users/prom3/Desktop/regal/frappe-bench
./access_database.sh
```

This script will show you:
- Database information
- All tables
- File locations
- Backup commands
- Connection commands

---

## 🔍 **Why Permission Denied?**

MariaDB database directories have strict permissions:
- **Parent directory:** `drwxr-xr-x` (755) - readable by owner and group
- **Database directories:** `drwx------` (700) - only owner can access

This is **normal and secure**. Individual database folders are protected.

---

## 📋 **Current Permissions**

```
/opt/homebrew/var/mysql/          → drwxr-xr-x  prom3:admin
/opt/homebrew/var/mysql/_af6374d4ed93f504/ → drwx------  prom3:admin
```

You (`prom3`) are the owner, so you should have access.

---

## 🚀 **Recommended Approach**

**For viewing database info:**
```bash
# Use MySQL commands (no file access needed)
mysql -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' _af6374d4ed93f504
```

**For backups:**
```bash
# Use mysqldump (no file access needed)
mysqldump -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' \
  _af6374d4ed93f504 > backup.sql
```

**For AWS migration:**
```bash
# Export using mysqldump
mysqldump -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' \
  _af6374d4ed93f504 > frappe_lending_backup.sql
```

---

## ✅ **Quick Test**

Run this to verify access:

```bash
# Test 1: MySQL connection
mysql -u _af6374d4ed93f504 -p'zTmiKxBrhzpoetXi' -e "SELECT 1;" 2>&1 | grep -v "Warning"

# Test 2: File access (should work)
ls -ld /opt/homebrew/var/mysql/

# Test 3: Database directory (should work)
ls -ld /opt/homebrew/var/mysql/_af6374d4ed93f504/
```

---

## 💡 **Why Use MySQL Commands Instead of Direct File Access?**

1. **Safer** - No risk of corrupting database files
2. **More reliable** - Works regardless of file permissions
3. **Standard practice** - This is how databases should be accessed
4. **Better for backups** - `mysqldump` creates portable SQL files

---

**Last Updated:** $(date)

