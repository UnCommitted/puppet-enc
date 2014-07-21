PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE environments (
    envid integer primary key,
    name text unique not null,
    desc text
);
INSERT INTO "environments" VALUES(1,'production','Default Production Environment');
INSERT INTO "environments" VALUES(2,'dev','Development Environment for testing changes');
CREATE TABLE sites (
    siteid integer primary key,
    name text unique not null,
    desc text
);
INSERT INTO "sites" VALUES(1,'city-west','Located as City West Data Centre');
INSERT INTO "sites" VALUES(2,'plaza','Located as Plaza Data Centre');
CREATE TABLE hosts (
    hostid integer primary key,
    name text unique not null,
    desc text,
    envid integer not null default 1,
    siteid integer not null default 1,
    foreign key (envid) references environments(envid)
    foreign key (siteid) references sites(siteid)
);
INSERT INTO "hosts" VALUES(1,'host1','Main Puppet Master Host',1,1);
INSERT INTO "hosts" VALUES(2,'host2','Ubuntu APT Repository Host',2,1);
CREATE TABLE tags (
    tagid integer primary key,
    name text unique not null,
    desc text
);
INSERT INTO "tags" VALUES(1,'puppetmaster','Host is a Puppet Master');
INSERT INTO "tags" VALUES(2,'apt-repo-host','Host serves out APT Repositories');
CREATE TABLE hosttags (
    hosttagid integer primary key,
    hostid integer not null,
    tagid integer not null,
    foreign key(hostid) references hosts(hostid),
    foreign key(tagid) references tags(tagid)
);
INSERT INTO "hosttags" VALUES(1,1,1);
INSERT INTO "hosttags" VALUES(2,1,2);
INSERT INTO "hosttags" VALUES(3,2,2);
CREATE INDEX hostnames on hosts(name);
CREATE INDEX tagnames on tags(name);
CREATE INDEX sitenames on sites(name);
CREATE VIEW host_location as select hosts.name as host_name,sites.name as site_name,sites.desc as site_description from hosts inner join sites on hosts.siteid=sites.siteid;
CREATE VIEW host_environments as select hosts.name as host_name,environments.name as env_name,environments.desc as env_description from hosts inner join environments on hosts.envid=environments.envid;
CREATE VIEW hosttag_mappings as select hosttags.hosttagid, hosts.name as host_name, tags.name as tag_name, tags.desc as tag_description from hosttags inner join tags on hosttags.tagid=tags.tagid inner join hosts on hosttags.hostid=hosts.hostid;
COMMIT;
