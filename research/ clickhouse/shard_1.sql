CREATE DATABASE shard;
// Ok.
// 0 rows in set. Elapsed: 0.009 sec.

CREATE DATABASE replica;
// Ok.
// 0 rows in set. Elapsed: 0.009 sec.

CREATE TABLE shard.test (`id` UInt64,
    `user_id` UInt64,
    `film_id` UInt64,
    `view_time` UInt64,
    `event_time` DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_1') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;
// Ok.
// 0 rows in set. Elapsed: 0.112 sec.

CREATE TABLE replica.test (`id` UInt64,
    `user_id` UInt64,
    `film_id` UInt64,
    `view_time` UInt64,
    `event_time` DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_2') PARTITION BY toYYYYMMDD(event_time) ORDER BY id;
// Ok.
// 0 rows in set. Elapsed: 0.112 sec.

CREATE TABLE default.test (`id` UInt64,
    `user_id` UInt64,
    `film_id` UInt64,
    `view_time` UInt64,
    `event_time` DateTime) ENGINE = Distributed('company_cluster', '', test, rand());
// Ok.
// 0 rows in set. Elapsed: 0.112 sec.