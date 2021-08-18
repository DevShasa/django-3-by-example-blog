# Setup postgresql 
After installing type
```
$ sudo su - postgres
```
if teh above fails try 
```
sudo -i -u postgres
```

first login to psql using the default prompt should be reading 
```
postgres@slikboi:~$
```

type psql kwa prompt, new terminal should read 
```
postgres=#
```

Create a new user with the command   
**note**   
Substitute blog with whatever database you want to create, make sure the database matches the project(website) you want to create and the password is similar to the databasename
```
postgres=# CREATE ROLE blog WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD 'blog';
```
check that the user exists 
```
postgres=# \du
```

Now that the user exists create a database matching the name of the user   
Exit psql using the command 
```
postgres=# \q
```
terminal will now read 
```
postgres@slikboi:~$ 
```
enter the command  
**note**  
The name of the database matches the user mkay
```
postgres@slikboi:~$ createdb blog
```
now login back to psql
```
postgres@slikboi:~$ psql
```
check that the database you create exists 
```
postgres=# \l
```
it will list database and owners  
Now change the owner of database blog to user blog, substitute blog with whatever project you are on 
```
postgres=# ALTER DATABASE blog OWNER to blog;
```

I think you should be good to connect to django now, fingers crossed

Incase you need to change password for default user  you can do it with command 
```
try the command below first 
postgres=# ALTER USER postgres PASSWORD 'admin';

if it fails try the one below
ALTER USER postgres WITH PASSWORD 'postgres';
```
