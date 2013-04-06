CREATE TABLE gameinfo_openttd_company
(
id serial not null,
name text not null,
clients integer not null,
inaunguarated_year integer not null,
value integer not null,
money integer not null,
income integer not null,
performance integer not null,
password_protected boolean not null default false,
added timestamptz default current_timestamp
);

CREATE TABLE gameinfo_openttd_game
(
id serial not null,
server text not null,
clients integer not null,
spectators integer not null,
companies integer not null,
alive boolean default true,
game_date timestamp not null,
start_date timestamp not null,
added timestamptz default current_timestamp
);
