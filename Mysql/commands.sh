# MySQL commands
zcat railmitra_app_20231018_171009.sql.gz | mysql -u railmitra-app -p railmitra-app


# Allow Specific IP Address to Access MySQL Port
sudo ufw allow from 192.168.1.100 to any port 3306 proto tcp
sudo ufw allow from 2001:0db8:85a3:0000:0000:8a2e:0370:7334 to any port 3306 proto tcp













#Set Auto AUTO_INCREMENT Start Number
ALTER TABLE `tbl` AUTO_INCREMENT = 100;



mysqldump -u root -p -Av | gzip > backup_all.sql.gz
mysqldump railrest_app -u root -p -v | gzip > railrest_app.sql.gz
gunzip railrest_app.sql.gz | mysql -u root -p railrest_app < railrest_app.sql

Export & Import
    mysqldump -u root -p database_name | mysql -h remote_host -u root -p remote_database_name
    > Before running the command, make sure the database already exists on the remote server.


Export:
    mysqldump -u root -p --all-databases > alldb.sql
    Look up the documentation for mysqldump. You may want to use some of the options mentioned in comments

    mysqldump -u root -p --opt --all-databases > alldb.sql
    mysqldump -u root -p --all-databases --skip-lock-tables > alldb.sql

Import:
    mysql -u root -p < alldb.sql
    
    mysql --one-database database_name < all_databases.sql

    mysql -u root -p -e "create database database_name";
    mysql -u root -p database_name < database_name.sql

    mysql -h 127.0.0.1 -uroot -p databasename < database-backup.sql.gz
    mysql --binary-mode=1 -h 127.0.0.1 -uroot -p databasename < database-backup.sql.gz

    # Using Mysql
    mysql> use db_name;
    mysql> SET autocommit=0 ; source the_sql_file.sql ; COMMIT ;
    



Automate Backups with Cron
    
1. Create a file named .my.cnf in your user home directory:
    
    sudo nano ~/.my.cnf

    Copy and paste the following text into the .my.cnf file.
        [client]
        user = dbuser
        password = dbpasswd

    * Do not forget to replace dbuser and dbpasswdwith the database user and user’s password.

2. Restrict permissions of the credentials file so that only your user has access to it:
    chmod 600 ~/.my.cnf

3. Create a directory to store the backups:
    mkdir ~/db_backups

4. Open your user crontab file:
    crontab -e

5. Add the following cron job that will create a backup of a database name mydb every day at 3am:
    0 3 * * * /usr/bin/mysqldump -u dbuser mydb > /home/username/db_backups/mydb-$(date +\%Y\%m\%d).sql

    * Do not forget to replace username with your actual user name. We’re also escaping the percent-signs (%), because they have special meaning in crontab.

6. You can also create another cronjob to delete any backups older than 30 days:
    find /path/to/backups -type f -name "*.sql" -mtime +30 -delete
    
    * Of course, you need to adjust the command according to your backup location and file names. To learn more about the find command check our How to Find Files in Linux Using the Command Line guide.


