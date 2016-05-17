drop table if exists mail;
create table mail (
  id integer primary key autoincrement,
  mailAddress string not null,
  password string not null
);
