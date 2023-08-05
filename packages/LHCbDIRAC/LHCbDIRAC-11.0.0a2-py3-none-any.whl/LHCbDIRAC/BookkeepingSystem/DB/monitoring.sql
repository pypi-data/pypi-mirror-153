/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

-- you can check the blockin queries using the following commands:
select distinct final_blocking_session, final_blocking_instance from v$session;

-- List the queries, which are taking very long for a given session
select * from V$SESSION_LONGOPS where  SQL_ID=xxxxx;

select * from V$SESSION_LONGOPS where sid in (select sid from v$session where username='LHCB_DIRACBOOKKEEPING' and status='ACTIVE') and sofar!=totalwork;

-- The queries which are belonging to the system:
select S.USERNAME, s.sid, s.osuser, t.sql_id, sql_text
from v$sqltext_with_newlines t,V$SESSION s
where t.address =s.sql_address
and t.hash_value = s.sql_hash_value
and s.status = 'ACTIVE'
and s.username <> 'SYSTEM'
order by s.sid,t.piece;

-- which database object is being locked (can be index, table, etc.)
select
  object_name,
  object_type,
  session_id,
  type,         -- Type or system/user lock
  lmode,        -- lock mode in which session holds lock
  request,
  block,
  ctime         -- Time since current mode was granted
from
  v$locked_object, all_objects, v$lock
where
  v$locked_object.object_id = all_objects.object_id AND
  v$lock.id1 = all_objects.object_id AND
  v$lock.sid = v$locked_object.session_id
order by
  session_id, ctime desc, object_name;

-- queries which are taking very long (which are still running):
SELECT sid, to_char(start_time,'hh24:mi:ss') stime,
message,( sofar/totalwork)* 100 percent
FROM v$session_longops
WHERE sofar/totalwork < 1;

-- active query running in the backround.
select s.username,s.sid,s.serial#,s.last_call_et/60 mins_running,q.sql_text from v$session s
join v$sqltext_with_newlines q
on s.sql_address = q.address
 where status='ACTIVE'
and type <>'BACKGROUND'
and last_call_et> 60
order by sid,serial#,q.piece;

-- When an index is analyzed
SELECT index_name, last_analyzed, status
   FROM user_indexes
   WHERE index_name = 'PROD_CONFIG';

-- you can see which database objects are in the database memory.
set pages 999
set lines 80

drop table t1;
create table t1 as select
   o.object_name    object_name,
   o.object_type    object_type,

   count(1)         num_blocks
from
   dba_objects  o,
   v$bh         bh
where
   o.object_id  = bh.objd
and
   o.owner not in ('SYS','SYSTEM')
group by
   o.object_name,
   o.object_type
order by
   count(1) desc;

column c1 heading "Object|Name"                 format a30
column c2 heading "Object|Type"                 format a12
column c3 heading "Number of|Blocks"            format 999,999,999,999
column c4 heading "Percentage|of object|data blocks|in Buffer" format 999

select
   object_name       c1,
   object_type       c2,
   num_blocks        c3,
   (num_blocks/decode(sum(blocks), 0, .001, sum(blocks)))*100 c4
from
   t1,
   dba_segments s
where
   s.segment_name = t1.object_name
and
   num_blocks > 10
group by
   object_name,
   object_type,
   num_blocks
order by
   num_blocks desc;

----start-- It is same as the previous one, but this does not take into account the
--- database objects which are belonging to the system
--******************************************************************
--   Contents of Data Buffers
--******************************************************************
set pages 999
set lines 92

ttitle 'Contents of Data Buffers'

drop table t1;

create table t1 as
select
   o.owner          owner,
   o.object_name    object_name,
   o.subobject_name subobject_name,
   o.object_type    object_type,
   count(distinct file# || block#)         num_blocks
from
   dba_objects  o,
   v$bh         bh
where
   o.data_object_id  = bh.objd
and
   o.owner not in ('SYS','SYSTEM')
and
   bh.status != 'free'
and
  owner='LHCB_DIRACBOOKKEEPING'
group by
   o.owner,
   o.object_name,
   o.subobject_name,
   o.object_type
order by
   count(distinct file# || block#) desc
;

column c0 heading "Owner"                                    format a12
column c1 heading "Object|Name"                              format a30
column c2 heading "Object|Type"                              format a8
column c3 heading "Number of|Blocks in|Buffer|Cache"         format 99,999,999
column c4 heading "Percentage|of object|blocks in|Buffer"    format 999
column c5 heading "Buffer|Pool"                              format a7
column c6 heading "Block|Size"                               format 99,999
\
select
   t1.owner                                          c0,
   object_name                                       c1,
   case when object_type = 'TABLE PARTITION' then 'TAB PART'
        when object_type = 'INDEX PARTITION' then 'IDX PART'
        else object_type end c2,
   sum(num_blocks)                                     c3,
   (sum(num_blocks)/greatest(sum(blocks), .001))*100 c4,
   buffer_pool                                       c5,
   sum(bytes)/sum(blocks)                            c6
from
   t1,
   dba_segments s
where
   s.segment_name = t1.object_name
and
   s.owner = t1.owner
and
   s.segment_type = t1.object_type
and
   nvl(s.partition_name,'-') = nvl(t1.subobject_name,'-')
group by
   t1.owner,
   object_name,
   object_type,
   buffer_pool
having
   sum(num_blocks) > 10
order by
   sum(num_blocks) desc;
---end--

--- database blocks read from differebt cache
 SELECT name, value
FROM V$SYSSTAT
WHERE name IN ('db block gets from cache', 'consistent gets from cache',
'physical reads cache');

--- How much do we read from cache
SELECT name, physical_reads, db_block_gets, consistent_gets,
       1 - (physical_reads / (db_block_gets + consistent_gets)) "Hit Ratio"
  FROM V$BUFFER_POOL_STATISTICS;

---How much we read from buffer (similar to the prevoius one)
SELECT TRUNC((1-(sum(decode(name,'physical reads',value,0))/
                (sum(decode(name,'db block gets',value,0))+
                (sum(decode(name,'consistent gets',value,0)))))
             )* 100) "Buffer Hit Ratio"
FROM v$SYSSTAT;

--- This includes also the writing
SELECT A.value + B.value  "logical_reads",
       C.value            "phys_reads",
       D.value            "phy_writes",
       ROUND(100 * ((A.value+B.value)-C.value) / (A.value+B.value))
         "BUFFER HIT RATIO"
FROM V$SYSSTAT A, V$SYSSTAT B, V$SYSSTAT C, V$SYSSTAT D
WHERE
   A.statistic# = 37
AND
   B.statistic# = 38
AND
   C.statistic# = 39
AND
   D.statistic# = 40;

--- V$DB_CACHE_ADVICE contains rows that predict the number of physical reads for the cache size corresponding to each row.

column c1   heading 'Cache Size (meg)'   format 999,999,999,999
 select
   size_for_estimate          c1,
   buffers_for_estimate       c2,
   estd_physical_read_factor  c3,
   estd_physical_reads        c4
from
   v$db_cache_advice
where
   name = 'DEFAULT'
and
   block_size  = (SELECT value FROM V$PARAMETER
                   WHERE name = 'db_block_size')
and
   advice_status = 'ON';

--size of the database

select sum(bytes)/1024/1024/1024/1024 size_in_TB from dba_data_files WHERE TABLESPACE_NAME like 'LHCB_DIRAC%';
select FILE_NAME, TABLESPACE_NAME, BLOCKS, ONLINE_STATUS, bytes/1024/1024/1024 size_in_GB from dba_data_files WHERE TABLESPACE_NAME like 'LHCB_DIRAC%';

-- all database jobs
select * from all_jobs;

--- it dispalys the execution plan
select * from table(dbms_xplan.display_cursor(format=>'allstats last +cost'));

--- When the statistics are created
select DBMS_STATS.GET_STATS_HISTORY_AVAILABILITY  from dual;

----- when the statistics are created for a given table
select TABLE_NAME, Partition_name, subpartition_name, STATS_UPDATE_TIME from dba_tab_stats_history where table_name='FILES'; and owner='SYSTEM';

-- check current statistics
select table_name,partition_name,num_rows,cast(last_analyzed as timestamp),dbms_stats.get_prefs('PUBLISH',owner,table_name)
from dba_tab_statistics where owner='LHCB_DIRACBOOKKEEPING' and table_name in ('PRODUCTIONSCONTAINER','JOBS', 'FILES')
order by object_type desc,table_name,partition_name nulls first,partition_position;

-- gather stats (then in pending mode) NOTE: degree=>16 will be faster, becuase the aggregation will be done in parallel
exec dbms_stats.gather_table_stats('LHCB_DIRACBOOKKEEPING','PRODUCTIONSCONTAINER', cascade=>True);
exec dbms_stats.gather_table_stats('LHCB_DIRACBOOKKEEPING','JOBS',cascade=>True, degree=>16);
exec dbms_stats.gather_table_stats('LHCB_DIRACBOOKKEEPING','FILES',cascade=>True,degree=>16);
exec dbms_stats.GATHER_INDEX_STATS('LHCB_DIRACBOOKKEEPING','JOBS_PROD_CONFIG_JOBID',degree=>16);
exec dbms_stats.GATHER_INDEX_STATS('LHCB_DIRACBOOKKEEPING','F_GOTREPLICA',degree=>16);
exec dbms_stats.GATHER_INDEX_STATS('LHCB_DIRACBOOKKEEPING','FILES_JOB_EVENT_FILETYPE',degree=>16);

--- START !!!NOTE: Make sure that you know what yoy are doing. It not recommended to execute the following commands.
exec dbms_stats.set_table_prefs('LHCB_DIRACBOOKKEEPING','PRODUCTIONSCONTAINER','publish','false');
exec dbms_stats.set_table_prefs('LHCB_DIRACBOOKKEEPING','JOBS','publish','false');

-- test with pending stats in my session
alter session set optimizer_use_pending_statistics=true;
--query to test
select /*+ gather_plan_statistics */ distinct jobs.Production, eventTypes.EventTypeId, eventTypes.Description,
configurations.Configname, configurations.Configversion,
productionscontainer. simid,productionscontainer.daqperiodid, files.filetypeid, jobs.programname, jobs.programversion
from eventTypes, files, jobs,configurations,productionscontainer
where eventTypes.eventTypeid=files.eventTypeid and
files.gotreplica='Yes' and files.visibilityflag ='Y' and jobs.jobid=files.jobid and jobs.configurationid=configurations.configurationId and jobs.production=productionscontainer.production
/
-- check execution plan
select * from table(dbms_xplan.display_cursor(format=>'allstats last +cost'));
-- end testing with pending statistics
alter session set optimizer_use_pending_statistics=false;

-- if not ok just delete the pending stats
exec dbms_stats.delete_pending_stats('LHCB_DIRACBOOKKEEPING_I','PRODUCTIONSCONTAINER');
exec dbms_stats.delete_pending_stats('LHCB_DIRACBOOKKEEPING_I','JOBS');
-- else if ok, publish them (invalidate all cursors immediately so that they use new statistics - if any regression better to see them immediately)
exec dbms_stats.publish_pending_stats('LHCB_DIRACBOOKKEEPING','PRODUCTIONSCONTAINER',no_invalidate=>false);
exec dbms_stats.publish_pending_stats('LHCB_DIRACBOOKKEEPING','JOBS',no_invalidate=>false);
-- at the end put back in publish mode
exec dbms_stats.set_table_prefs('LHCB_DIRACBOOKKEEPING','PRODUCTIONSCONTAINER','publish','true');
exec dbms_stats.set_table_prefs('LHCB_DIRACBOOKKEEPING','JOBS','publish','true');
-- check new statistics
select table_name,partition_name,num_rows,cast(last_analyzed as timestamp),dbms_stats.get_prefs('PUBLISH',owner,table_name)
from dba_tab_statistics where owner='LHCB_DIRACBOOKKEEPING' and table_name in ('PRODUCTIONSCONTAINER','JOBS', 'FILES')
order by object_type desc,table_name,partition_name nulls first,partition_position;
-- optionally check the difference (here from 1 day ago)
select report from table(dbms_stats.diff_table_stats_in_history('LHCB_DIRACBOOKKEEPING','PRODUCTIONSCONTAINER',sysdate-1,sysdate,0));
select report from table(dbms_stats.diff_table_stats_in_history('LHCB_DIRACBOOKKEEPING','JOBS',sysdate-1,sysdate));
-- in case of regression encountered later, restore the old stats:
exec dbms_stats.restore_table_stats('LHCB_DIRACBOOKKEEPING_','PRODUCTIONSCONTAINER',sysdate-1,no_invalidate=>false);
exec dbms_stats.restore_table_stats('LHCB_DIRACBOOKKEEPING_INT','JOBS',sysdate-1,no_invalidate=>false);
-- show the history of operations
select end_time,end_time-start_time,operation,target,notes,status
from DBA_OPTSTAT_OPERATIONS where target in ('LHCB_DIRACBOOKKEEPING.PRODUCTIONSCONTAINER','LHCB_DIRACBOOKKEEPING_INT.JOBS') and end_time>sysdate-1;
----- END !!!!!!

--- database name
select name from v$database;
select * from v$locked_object join dba_objects using (object_id);

---all tables
select * from user_tables;
