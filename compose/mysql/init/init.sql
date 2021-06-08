create user 'hulk'@'%' IDENTIFIED by 'hulk';
grant all  on *.* to 'hulk'@'%' identified by 'hulk';
flush privileges;
