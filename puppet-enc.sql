CREATE TABLE environments (
    envid integer primary key,
    name text unique not null,
    desc text
);
CREATE TABLE sites (
    siteid integer primary key,
    name text unique not null,
    desc text
);
CREATE TABLE roles (
    roleid integer primary key,
    name text unique not null,
    desc text
);
CREATE TABLE systems (
    systemid integer primary key,
    name text unique not null,
    desc text
);
CREATE TABLE hosts (
    hostid integer primary key,
    name text unique not null,
    desc text,
    envid integer not null,
    siteid integer not null,
    systemid integer not null,
    roleid integer not null,
    foreign key (envid) references environments(envid)
    foreign key (siteid) references sites(siteid)
    foreign key (systemid) references systems(systemid)
    foreign key (roleid) references roles(roleid)
);
CREATE INDEX hostnames on hosts(name);
CREATE INDEX sitenames on sites(name);
CREATE INDEX rolenames on roles(name);
CREATE INDEX systemnames on systems(name);
CREATE VIEW hostoverview AS
    SELECT hosts.name as host_name,
           environments.name as env_name,
           sites.name as site_name,
           systems.name as system_name,
           roles.name as role_name
    FROM hosts
    INNER JOIN environments ON hosts.envid=environments.envid
    INNER JOIN sites ON hosts.siteid=sites.siteid
    INNER JOIN systems ON hosts.systemid=systems.systemid
    INNER JOIN roles ON hosts.roleid=roles.roleid;

