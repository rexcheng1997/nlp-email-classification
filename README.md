# NLP Email Classification

Analyze the body messages of the emails and classify them based on purpose.


## Dataset Used

* [Enron Email Dataset](http://www.cs.cmu.edu/~enron/) hosted by CMU.

    May 7, 2015 Version of dataset (about 1.7GB). [Click Here to Download](http://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz).


## Quick Guide of Changing MySQL Data Directory

This tutorial is only for ubuntu users. For reference, [click this link](https://www.digitalocean.com/community/tutorials/how-to-move-a-mysql-data-directory-to-a-new-location-on-ubuntu-16-04).

### Check the current data directory

Run the following command to start mysql server.

`$ sudo service mysql start`

Then run `sudo mysql -u root -p` to login with root credential. Enter the password for root when prompted.

After entering the interactive mode, run the following query.

`mysql> SELECT @@datadir;`

You are supposed to see the following output:

| --- |
| @@datadir |
| --- |
| /var/lib/mysql/ |
| --- |
1 row in set (0.00 sec)

`/var/lib/mysql` is where your current data directory is. After confirm this, type `quit` to exit the interactive mode.

Run `sudo service mysql stop` to stop the server.

### Move the data directory to a new location

We use `rsync` command to copy the original data directory to a new specified location.

`$ sudo rsync -av /var/lib/mysql /path/to/new/location`

where `/path/to/new/location` is the absolute path to the new location you want your data directory to be.

Once `rsync` is completed, run the following command to back up your original data directory in case that the procedure fails.

`$ sudo mv /var/lib/mysql /var/lib/mysql.bak`

### Change path reference

Run the following command to edit the mysql configuration file.

`$ sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf`

Find the line that begins with `datadir = ` and change the path following `=` to the path to the new location you just specified.

```
...
datadir = /path/to/new/location
...
```

After this, we also need to edit the AppArmor Access Control Rules for the change to take effect. Run the following command:

`$ sudo vim /etc/apparmor.d/tunables/alias`

Add the following line at the bottom of the file.

```
...
alias /var/lib/mysql -> /path/to/new/location
...
```

Then run `sudo /etc/init.d/apparmor restart` to make changes take effect.

Also remember to run the following to circumvent the mysql server checking.

`$ sudo mkdir /var/lib/mysql/mysql -p`

### Restart MySQL

```
$ sudo service mysql start
$ sudo mysql -u root -p
mysql> SELECT @@datadir
```

If the output you see changes to the new location of the data directory, it means that you have succefully move the data directory to your specified place.

Now, you can remove your backup for the original data directory (optional).

`$ sudo rm -f -r /var/lib/mysql.bak`

If any error occurs during the above process, click the reference link above to see the post written by Melissa Anderson for error handling.
