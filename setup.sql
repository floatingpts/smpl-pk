create database cs4501 character set utf8;
create user 'www'@'%' identified by '$3cureUS';
grant all on cs4501.* to 'www'@'%';
