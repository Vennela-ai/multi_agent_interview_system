**mysql-commands**

mysql>show databases;

+-----------------+

|  Database       |

+-----------------+

|information\_schema|

| aayurvedab       |

create database <database-name>

\#**create new database**

mysql> create database rcedb;

**query OK,1 row affected(0.00sec)**

**#enter to the database:**

mysql>use rcedb;

database changed

mysql>desc studentsdata;

+--------+-------------+------+-----+---------+-------+

| Field  | Type        | Null | Key | Default | Extra |

+--------+-------------+------+-----+---------+-------+

| id     | int         | YES  |     | NULL    |       |

| name   | varchar(50) | YES  |     | NULL    |       |

| age    | int         | YES  |     | NULL    |       |

| course | varchar(20) | YES  |     | NULL    |       |

+--------+-------------+------+-----+---------+-------+

insert into studentsdata values(101,'vennela',18,'MYSQL');

insert into studentsdata values(20,'RAJU',32,'java');

insert into studentsdata values(40,'kiran',25,'java'),(30,'mohan',25,'python'),(50,'bhanu',22,'reactjs');

Query OK, 3 rows affected (0.0157 sec)



Records: 3  Duplicates: 0  Warnings: 0

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select id,name,age,course from studentsdata;

+-----+---------+-----+---------+

| id  | name    | age | course  |

+-----+---------+-----+---------+

| 101 | vennela |  18 | MYSQL   |

|  20 | RAJU    |  32 | java    |

|  40 | kiran   |  25 | java    |

|  30 | mohan   |  25 | python  |

|  50 | bhanu   |  22 | reactjs |

+-----+---------+-----+---------+

5 rows in set (0.0012 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL >

insert into studentsdata values(102,'venny',21,'C');

Query OK, 1 row affected (0.0120 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into studentsdata values(12,'ponny',23,'D');

Query OK, 1 row affected (0.0129 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from studentsdata;

+-----+---------+-----+---------+

| id  | name    | age | course  |

+-----+---------+-----+---------+

| 101 | vennela |  18 | MYSQL   |

|  20 | RAJU    |  32 | java    |

|  40 | kiran   |  25 | java    |

|  30 | mohan   |  25 | python  |

|  50 | bhanu   |  22 | reactjs |

| 102 | venny   |  21 | C       |

|  12 | ponny   |  23 | D       |

+-----+---------+-----+---------+

7 rows in set (0.0009 sec)



&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > create table employee(empno int,ename varchar(20),sal decimal(8,2));

Query OK, 0 rows affected (0.0500 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc employee;

+-------+--------------+------+-----+---------+-------+

| Field | Type         | Null | Key | Default | Extra |

+-------+--------------+------+-----+---------+-------+

| empno | int          | YES  |     | NULL    |       |

| ename | varchar(20)  | YES  |     | NULL    |       |

| sal   | decimal(8,2) | YES  |     | NULL    |       |

+-------+--------------+------+-----+---------+-------+

3 rows in set (0.0038 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(101,'vennela',18,'MYSQL');

ERROR: 1136: Column count doesn't match value count at row 1

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(101,'vennela',5000);

Query OK, 1 row affected (0.0141 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(200,'mohan',7000);

Query OK, 1 row affected (0.0093 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(300,'kiran',3000);

Query OK, 1 row affected (0.0157 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(400,'raj',50000);

Query OK, 1 row affected (0.0134 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into employee values(500,'rajesh',10000);

Query OK, 1 row affected (0.0129 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee;

+-------+---------+----------+

| empno | ename   | sal      |

+-------+---------+----------+

|   101 | vennela |  5000.00 |

|   200 | mohan   |  7000.00 |

|   300 | kiran   |  3000.00 |

|   400 | raj     | 50000.00 |

|   500 | rajesh  | 10000.00 |

+-------+---------+----------+

5 rows in set (0.0011 sec)



&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where empno=101;

+-------+---------+---------+

| empno | ename   | sal     |

+-------+---------+---------+

|   101 | vennela | 5000.00 |

+-------+---------+---------+

1 row in set (0.0010 sec)

select \* from employee where ename='raj';

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   400 | raj   | 50000.00 |

+-------+-------+----------+

1 row in set (0.0014 sec)

select \* from employee where sal>5000;

+-------+--------+----------+

| empno | ename  | sal      |

+-------+--------+----------+

|   200 | mohan  |  7000.00 |

|   400 | raj    | 50000.00 |

|   500 | rajesh | 10000.00 |

+-------+--------+----------+

3 rows in set (0.0015 sec)

select \* from employee where sal<10000;

+-------+---------+---------+

| empno | ename   | sal     |

+-------+---------+---------+

|   101 | vennela | 5000.00 |

|   200 | mohan   | 7000.00 |

|   300 | kiran   | 3000.00 |

+-------+---------+---------+

3 rows in set (0.0011 sec)

&#x20;select \* from employee where ename!='raj';

+-------+---------+----------+

| empno | ename   | sal      |

+-------+---------+----------+

|   101 | vennela |  5000.00 |

|   200 | mohan   |  7000.00 |

|   300 | kiran   |  3000.00 |

|   500 | rajesh  | 10000.00 |

+-------+---------+----------+

4 rows in set (0.0015 sec)

&#x20;select \* from employee where sal>=5000 and sal<10000;

+-------+---------+---------+

| empno | ename   | sal     |

+-------+---------+---------+

|   101 | vennela | 5000.00 |

|   200 | mohan   | 7000.00 |

+-------+---------+---------+

2 rows in set (0.0014 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where ename='raj' or ename='mohan';

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   200 | mohan |  7000.00 |

|   400 | raj   | 50000.00 |

+-------+-------+----------+

2 rows in set (0.0014 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where not ename='raj';

+-------+---------+----------+

| empno | ename   | sal      |

+-------+---------+----------+

|   101 | vennela |  5000.00 |

|   200 | mohan   |  7000.00 |

|   300 | kiran   |  3000.00 |

|   500 | rajesh  | 10000.00 |

+-------+---------+----------+

4 rows in set (0.0011 sec)



&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where sal between 5000 and 10000;

+-------+---------+----------+

| empno | ename   | sal      |

+-------+---------+----------+

|   101 | vennela |  5000.00 |

|   200 | mohan   |  7000.00 |

|   500 | rajesh  | 10000.00 |

+-------+---------+----------+

3 rows in set (0.0017 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where empno between 200 and 400;

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   200 | mohan |  7000.00 |

|   300 | kiran |  3000.00 |

|   400 | raj   | 50000.00 |

+-------+-------+----------+

3 rows in set (0.0010 sec)

&#x20;select \* from employee where empno between 200 and 400;

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   200 | mohan |  7000.00 |

|   300 | kiran |  3000.00 |

|   400 | raj   | 50000.00 |

+-------+-------+----------+

3 rows in set (0.0010 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where sal in(7000,50000);

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   200 | mohan |  7000.00 |

|   400 | raj   | 50000.00 |

+-------+-------+----------+

2 rows in set (0.0018 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where ename like 'r%';

+-------+--------+----------+

| empno | ename  | sal      |

+-------+--------+----------+

|   400 | raj    | 50000.00 |

|   500 | rajesh | 10000.00 |

+-------+--------+----------+

2 rows in set (0.0015 sec)

select \* from employee where ename like '%j';

+-------+-------+----------+

| empno | ename | sal      |

+-------+-------+----------+

|   400 | raj   | 50000.00 |

+-------+-------+----------+

1 row in set (0.0010 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where ename like '%an';

+-------+-------+---------+

| empno | ename | sal     |

+-------+-------+---------+

|   200 | mohan | 7000.00 |

|   300 | kiran | 3000.00 |

+-------+-------+---------+

2 rows in set (0.0012 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where ename not like '%an';

+-------+---------+----------+

| empno | ename   | sal      |

+-------+---------+----------+

|   101 | vennela |  5000.00 |

|   400 | raj     | 50000.00 |

|   500 | rajesh  | 10000.00 |

+-------+---------+----------+

3 rows in set (0.0010 sec)

select \* from employee where sal>5000 order by sal asc;

+-------+--------+----------+

| empno | ename  | sal      |

+-------+--------+----------+

|   200 | mohan  |  7000.00 |

|   500 | rajesh | 10000.00 |

|   400 | raj    | 50000.00 |

+-------+--------+----------+

3 rows in set (0.0016 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from employee where sal<10000 order by sal asc;

+-------+---------+---------+

| empno | ename   | sal     |

+-------+---------+---------+

|   300 | kiran   | 3000.00 |

|   101 | vennela | 5000.00 |

|   200 | mohan   | 7000.00 |

+-------+---------+---------+

3 rows in set (0.0015 sec)

&#x20;drop table studentsdata;

Query OK, 0 rows affected (0.0488 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc studentsdata;

ERROR: 1146: Table 'rcedb.studentsdata' doesn't exist

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > create table persons(personid int,lastname varchar(10),firstname varchar(10),address varchar(10),city varchar(10));

Query OK, 0 rows affected (0.0525 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc persons;

+-----------+-------------+------+-----+---------+-------+

| Field     | Type        | Null | Key | Default | Extra |

+-----------+-------------+------+-----+---------+-------+

| personid  | int         | YES  |     | NULL    |       |

| lastname  | varchar(10) | YES  |     | NULL    |       |

| firstname | varchar(10) | YES  |     | NULL    |       |

| address   | varchar(10) | YES  |     | NULL    |       |

| city      | varchar(10) | YES  |     | NULL    |       |

+-----------+-------------+------+-----+---------+-------+

5 rows in set (0.0053 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > alter table persons;

Query OK, 0 rows affected (0.0095 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > add dob date;

ERROR: 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'add dob date' at line 1

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > add dob ,date;

ERROR: 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'add dob ,date' at line 1

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL >

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > ADD dateofbirth,date;

ERROR: 1064: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'ADD dateofbirth,date' at line 1

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > alter table persons ADD DateofBirth date;

Query OK, 0 rows affected (0.0843 sec)



Records: 0  Duplicates: 0  Warnings: 0

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc persons;

+-------------+-------------+------+-----+---------+-------+

| Field       | Type        | Null | Key | Default | Extra |

+-------------+-------------+------+-----+---------+-------+

| personid    | int         | YES  |     | NULL    |       |

| lastname    | varchar(10) | YES  |     | NULL    |       |

| firstname   | varchar(10) | YES  |     | NULL    |       |

| address     | varchar(10) | YES  |     | NULL    |       |

| city        | varchar(10) | YES  |     | NULL    |       |

| DateofBirth | date        | YES  |     | NULL    |       |

+-------------+-------------+------+-----+---------+-------+

6 rows in set (0.0026 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into persons values(200,'raj','mohan','bang','city','2017-10-20');

Query OK, 1 row affected (0.0139 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into persons values(300,'ABC','ABC123','bang','city','2017-10-21');

Query OK, 1 row affected (0.0128 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into persons values(200,'ravi','kumar','bang','city','2017-10-17');

Query OK, 1 row affected (0.0133 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into persons values(200,'kiran','kumar','bang','city','2017-10-11');

Query OK, 1 row affected (0.0139 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc persons;

+-------------+-------------+------+-----+---------+-------+

| Field       | Type        | Null | Key | Default | Extra |

+-------------+-------------+------+-----+---------+-------+

| personid    | int         | YES  |     | NULL    |       |

| lastname    | varchar(10) | YES  |     | NULL    |       |

| firstname   | varchar(10) | YES  |     | NULL    |       |

| address     | varchar(10) | YES  |     | NULL    |       |

| city        | varchar(10) | YES  |     | NULL    |       |

| DateofBirth | date        | YES  |     | NULL    |       |

+-------------+-------------+------+-----+---------+-------+

6 rows in set (0.0032 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from persons;

+----------+----------+-----------+---------+------+-------------+

| personid | lastname | firstname | address | city | DateofBirth |

+----------+----------+-----------+---------+------+-------------+

|      200 | raj      | mohan     | bang    | city | 2017-10-20  |

|      300 | ABC      | ABC123    | bang    | city | 2017-10-21  |

|      200 | ravi     | kumar     | bang    | city | 2017-10-17  |

|      200 | kiran    | kumar     | bang    | city | 2017-10-11  |

+----------+----------+-----------+---------+------+-------------+

4 rows in set (0.0011 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > insert into persons values(200,null,null,'bang','city','2017-10-11');

Query OK, 1 row affected (0.0129 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > select \* from persons;

+----------+----------+-----------+---------+------+-------------+

| personid | lastname | firstname | address | city | DateofBirth |

+----------+----------+-----------+---------+------+-------------+

|      200 | raj      | mohan     | bang    | city | 2017-10-20  |

|      300 | ABC      | ABC123    | bang    | city | 2017-10-21  |

|      200 | ravi     | kumar     | bang    | city | 2017-10-17  |

|      200 | kiran    | kumar     | bang    | city | 2017-10-11  |

|      200 | NULL     | NULL      | bang    | city | 2017-10-11  |

+----------+----------+-----------+---------+------+-------------+

5 rows in set (0.0011 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > delete from persons where firstname='mohan';

Query OK, 1 row affected (0.0140 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > delete from persons where personid=200;

Query OK, 3 rows affected (0.0123 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > drop table persons;

Query OK, 0 rows affected (0.0337 sec)

&#x20;MySQL  localhost:33060+ ssl  rcedb  SQL > desc persons;

ERROR: 1146: Table 'rcedb.persons' doesn't exist

