/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

CREATE OR REPLACE PACKAGE bookkeepingoracledb AS

  TYPE udt_refcursor IS REF CURSOR;
  --TYPE ifileslist is VARRAY(30) of VARCHAR2(10);

  TYPE ifileslist IS TABLE OF varchar2(30)
    INDEX BY pls_integer;

  TYPE numberarray  IS TABLE OF NUMBER INDEX BY pls_integer;
  TYPE varchararray IS TABLE OF varchar2(256) INDEX BY pls_integer;
  TYPE bigvarchararray IS TABLE OF varchar2(2000) INDEX BY pls_integer;

PROCEDURE getavailablefiletypes(a_cursor OUT udt_refcursor );
FUNCTION insertfiletypes(v_name VARCHAR2, description VARCHAR2, filetype VARCHAR2) RETURN NUMBER;
PROCEDURE getavailableconfigurations(a_cursor OUT udt_refcursor);
FUNCTION getstepsforfiletypes(iftypes LISTS, oftypes LISTS, MATCH VARCHAR2) RETURN step_table pipelined;
FUNCTION getproductionprocessingpass(prod NUMBER) RETURN VARCHAR2;
FUNCTION getproductionporcpassname(v_procid NUMBER) RETURN VARCHAR2;
FUNCTION getproductionprocessingpassid(prod NUMBER) RETURN NUMBER;
FUNCTION getprocessingpassid(root VARCHAR2, fullpath VARCHAR2) RETURN NUMBER;
PROCEDURE getavailableeventtypes(a_cursor OUT udt_refcursor);
PROCEDURE getjobinfo(lfn VARCHAR2, a_cursor OUT udt_refcursor);
PROCEDURE inserttag(v_name VARCHAR2, v_tag VARCHAR2);
FUNCTION getdataqualityid(name VARCHAR2) RETURN NUMBER;
FUNCTION getqflagbyrunandprocid(rnumber NUMBER, procid NUMBER) RETURN VARCHAR2;
PROCEDURE getrunbyqflagandprocid(procid NUMBER, flag NUMBER, a_cursor OUT udt_refcursor);
FUNCTION getfileid(v_filename VARCHAR2) RETURN NUMBER;  -- FIXME: is it used?
PROCEDURE getfileandjobmetadata( v_jobid NUMBER, prod BOOLEAN, a_cursor OUT udt_refcursor);
PROCEDURE checkfile(name VARCHAR2, a_cursor OUT udt_refcursor);
FUNCTION checkfiletypeandversion (v_name  VARCHAR2,  v_version VARCHAR2) RETURN NUMBER;
PROCEDURE checkeventtype (v_eventtypeid NUMBER, a_cursor OUT udt_refcursor);
FUNCTION insertjobsrow (
     v_configname                  VARCHAR2,
     v_configversion               VARCHAR2,
     v_diracjobid                  NUMBER,
     v_diracversion                VARCHAR2,
     v_eventinputstat              NUMBER,
     v_exectime                    FLOAT,
     v_firsteventnumber            NUMBER,
     v_jobend                      TIMESTAMP,
     v_jobstart                    TIMESTAMP,
     v_location                    VARCHAR2,
     v_name                        VARCHAR2,
     v_numberofevents              NUMBER,
     v_production                  NUMBER,
     v_programname                 VARCHAR2,
     v_programversion              VARCHAR2,
     v_statisticsrequested         NUMBER,
     v_wncpupower                  VARCHAR2,
     v_cputime                   FLOAT,
     v_wncache                     VARCHAR2,
     v_wnmemory                    VARCHAR2,
     v_wnmodel                     VARCHAR2,
     v_workernode                  VARCHAR2,
     v_runnumber                   NUMBER,
     v_fillnumber                  NUMBER,
     v_wncpuhs06                   FLOAT,
     v_totalluminosity             NUMBER,
     v_tck                         VARCHAR2,
     v_stepid                      NUMBER,
     v_wnmjfhs06                   FLOAT,
     v_hlt2tck                     VARCHAR2,
     v_numproc                     NUMBER
) RETURN NUMBER;

FUNCTION insertfilesrow (
    v_adler32                         VARCHAR2,
    v_creationdate                    TIMESTAMP,
    v_eventstat                       NUMBER,
    v_eventtypeid                     NUMBER,
    v_filename                        VARCHAR2,
    v_filetypeid                      NUMBER,
    v_gotreplica                      VARCHAR2,
    v_guid                            VARCHAR2,
    v_jobid                           NUMBER,
    v_md5sum                          VARCHAR2,
    v_filesize                        NUMBER,
    v_fullstat                        NUMBER,
    v_utc                             TIMESTAMP,
    dqflag                            VARCHAR2,
    v_luminosity                      NUMBER,
    v_instluminosity                  NUMBER,
    v_visibilityflag                  VARCHAR2
) RETURN NUMBER;


PROCEDURE insertinputfilesrow (v_fileid NUMBER, v_jobid NUMBER);

PROCEDURE updatereplicarow(v_fileid NUMBER,v_replica VARCHAR2);
PROCEDURE deletejob(v_jobid NUMBER);
PROCEDURE deleteinputfiles(v_jobid NUMBER);
PROCEDURE deletefile(v_fileid NUMBER);
PROCEDURE deletesetpcontiner(v_prod NUMBER);  -- FIXME: to remove
PROCEDURE deletestepcontainer(v_prod NUMBER);

FUNCTION insertsimconditions (
    v_simdesc                VARCHAR2,
    v_beamcond               VARCHAR2,
    v_beamenergy             VARCHAR2,
    v_generator              VARCHAR2,
    v_magneticfield          VARCHAR2,
    v_detectorcond           VARCHAR2,
    v_luminosity             VARCHAR2,
    v_g4settings             VARCHAR2,
    v_visible                VARCHAR2
) RETURN NUMBER;

PROCEDURE getsimconditions(a_cursor OUT udt_refcursor);

FUNCTION insertdatatakingcond (
     v_description                                        VARCHAR2,
     v_beamcond                                           VARCHAR2,
     v_beamenergy                                         VARCHAR2,
     v_magneticfield                                      VARCHAR2,
     v_velo                                               VARCHAR2,
     v_it                                                 VARCHAR2,
     v_tt                                                 VARCHAR2,
     v_ot                                                 VARCHAR2,
     v_rich1                                              VARCHAR2,
     v_rich2                                              VARCHAR2,
     v_spd_prs                                            VARCHAR2,
     v_ecal                                               VARCHAR2,
     v_hcal                                               VARCHAR2,
     v_muon                                               VARCHAR2,
     v_l0                                                 VARCHAR2,
     v_hlt                                                VARCHAR2,
     v_veloposition                                       VARCHAR2
) RETURN NUMBER;

PROCEDURE getfilemetadata(v_filename VARCHAR2, a_cursor OUT udt_refcursor);
PROCEDURE getfilemetadata3(iftypes varchararray, a_cursor OUT udt_refcursor);
FUNCTION fileexists(v_filename VARCHAR2)RETURN NUMBER;
PROCEDURE inserteventtypes (v_description VARCHAR2, v_eventtypeid NUMBER, v_primary VARCHAR2);
PROCEDURE updateeventtypes(v_description VARCHAR2, v_eventtypeid NUMBER, v_primary VARCHAR2);
PROCEDURE setfileinvisible(lfn VARCHAR2);
PROCEDURE setfilevisible(lfn VARCHAR2);
PROCEDURE getconfigsandevttype(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getjobsbysites(prodid NUMBER,a_cursor OUT udt_refcursor);
PROCEDURE getsteps(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getproductioninformation(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getnboffiles(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getsizeoffiles(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getnumberofevents(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE getjobsnb(prodid NUMBER, a_cursor OUT udt_refcursor);
PROCEDURE insertstepscontainer(v_prod NUMBER, v_stepid NUMBER, v_step NUMBER);
PROCEDURE insertproductionscontainer(v_prod NUMBER, v_processingid NUMBER, v_simid NUMBER, v_daqperiodid NUMBER, cname VARCHAR2, cversion VARCHAR2);
PROCEDURE geteventtypes(cname VARCHAR2, cversion VARCHAR2, a_cursor OUT udt_refcursor);
FUNCTION  getrunnumber(lfn VARCHAR2) RETURN NUMBER;
PROCEDURE insertrunquality(run NUMBER, qid NUMBER,procid NUMBER);
PROCEDURE getrunnbandtck(lfn VARCHAR2, a_cursor OUT udt_refcursor);
PROCEDURE deleteproductionscont(v_prod NUMBER);
PROCEDURE getruns(c_name VARCHAR2, c_version VARCHAR2,  a_cursor OUT udt_refcursor);
FUNCTION getrunprocpass(v_runnumber NUMBER) RETURN run_proc_table;
PROCEDURE getrunquality(runs numberarray , a_cursor OUT udt_refcursor);
PROCEDURE gettypevesrsion(lfn VARCHAR2, a_cursor OUT udt_refcursor);
PROCEDURE getrunfiles(v_runnumber NUMBER, a_cursor OUT udt_refcursor);
FUNCTION getprocessedevents(v_prodid NUMBER) RETURN NUMBER;
FUNCTION isvisible(v_stepid NUMBER) RETURN NUMBER;
PROCEDURE insertruntimeproject(pr_stepid NUMBER, run_pr_stepid NUMBER);
PROCEDURE updateruntimeproject(pr_stepid NUMBER, run_pr_stepid NUMBER);
PROCEDURE removeruntimeproject(pr_stepid NUMBER);
PROCEDURE getdirectorymetadata(f_name VARCHAR2, a_cursor OUT udt_refcursor);
FUNCTION getfilesforguid(v_guid VARCHAR2) RETURN VARCHAR2;
PROCEDURE updatedataqualityflag(v_qualityid NUMBER, lfns varchararray);
PROCEDURE bulkcheckfiles(lfns varchararray,  a_cursor OUT udt_refcursor);
PROCEDURE bulkupdatereplicarow(v_replica VARCHAR2, lfns varchararray);
PROCEDURE bulkgettypevesrsion(lfns varchararray, a_cursor OUT udt_refcursor);
PROCEDURE setobsolete;
PROCEDURE getdirectorymetadata_new(lfns varchararray, a_cursor OUT udt_refcursor);
PROCEDURE bulkjobinfo(lfns varchararray, a_cursor OUT udt_refcursor);
PROCEDURE bulkjobinfoforjobname(jobnames varchararray, a_cursor OUT udt_refcursor);
PROCEDURE bulkjobinfoforjobid(jobids numberarray, a_cursor OUT udt_refcursor);
PROCEDURE insertrunstatus(v_runnumber NUMBER, v_jobid NUMBER, v_finished VARCHAR2);
PROCEDURE setrunfinished(v_runnumber NUMBER, isfinished VARCHAR2);
PROCEDURE bulkupdatefilemetadata(files bigvarchararray);
PROCEDURE updateluminosity(v_runnumber NUMBER);
PROCEDURE updatedesluminosity(v_fileid NUMBER);
PROCEDURE getfiledesjobid(v_filename VARCHAR2, a_cursor OUT udt_refcursor);
FUNCTION getproducedevents(v_prodid NUMBER) RETURN NUMBER;
PROCEDURE bulkgetidsfromfiles(lfns varchararray, a_cursor OUT udt_refcursor);
PROCEDURE insertprodnoutputftypes(v_production NUMBER, v_stepid NUMBER, v_filetypeid NUMBER, v_visible char, v_eventtype NUMBER);
FUNCTION getjobidwithoutreplicacheck(v_filename VARCHAR2) RETURN NUMBER;
END;
 /


CREATE OR REPLACE PACKAGE BODY bookkeepingoracledb AS

-------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getavailablefiletypes(a_cursor OUT udt_refcursor )IS
BEGIN
OPEN a_cursor FOR
  SELECT DISTINCT filetypes.name,filetypes.description FROM filetypes ORDER BY filetypes.name;
END;

---------------------------------------------------------------------------------------------------------------------------------
FUNCTION insertfiletypes(
  v_name VARCHAR2,
  description VARCHAR2,
  filetype VARCHAR2
) RETURN NUMBER IS
id NUMBER;
FOUND NUMBER;
ecode varchar2(256);
thisproc constant varchar2(50) := 'trap_errmesg';
found_name EXCEPTION;
descr varchar2(256);
BEGIN
  FOUND := 0;
  id := -1;
  SELECT count(filetypeid) INTO FOUND
  FROM filetypes
  WHERE filetypes.name = upper(v_name)
    AND filetypes.version = filetype;
  IF FOUND > 0 THEN
    RAISE found_name;
  ELSE
    SELECT DISTINCT description INTO descr
    FROM filetypes
    WHERE name = upper(v_name);
    SELECT coalesce(max(filetypeid) + 1, 1) INTO id
    FROM filetypes;
    INSERT INTO filetypes(filetypeid,
                          name,
                          description,
                          VERSION)
    VALUES(id,
          upper(v_name),
          descr,
          filetype);
    COMMIT;
    RETURN id;
  END IF;
  EXCEPTION
    WHEN found_name THEN
      raise_application_error(-20001,'The ' || v_name || ' file type already exists!!!');
    WHEN no_data_found THEN
      SELECT coalesce(max(filetypeid) + 1, 1) INTO id FROM filetypes;
      INSERT INTO filetypes(filetypeid,
                           name,
                           description,
                           VERSION)
      VALUES(id,
            upper(v_name),
            description,
            filetype);
      COMMIT;
    RETURN id;
    WHEN others THEN
      ecode := sqlerrm; --SQLCODE;
dbms_output.put_line(thisproc || ' - ' || ecode);
      RETURN -1;
END;

-------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getavailableconfigurations (
    a_cursor                    OUT udt_refcursor
) IS
BEGIN
  OPEN a_cursor FOR
    SELECT configname,configversion FROM configurations;
END;

---------------------------------------------------------------------------------------------------------------------------
FUNCTION getstepsforfiletypes(iftypes LISTS, oftypes LISTS, MATCH VARCHAR2) RETURN step_table pipelined IS
INPUT BOOLEAN;
OUTPUT BOOLEAN;
BEGIN
IF iftypes.count = 0 AND oftypes.count = 0 THEN
  FOR cur IN (SELECT s.stepid, s.stepname, s.applicationname, s.applicationversion, s.optionfiles, s.dddb, s.conddb, s.extrapackages, s.visible, s.processingpass, s.usable, s.dqtag,s.optionsformat, s.ismulticore, s.systemconfig,s.mctck,
                     r.stepid AS rid, r.stepname AS rsname, r.applicationname AS rappname, r.applicationversion AS rappver, r.optionfiles AS roptsf, r.dddb AS rdddb, r.conddb AS rcondb, r.extrapackages AS rextra,
                     r.visible AS rvisi, r.processingpass AS rproc, r.usable AS rusab, r.dqtag AS rdq,r.optionsformat AS ropff, r.ismulticore AS rmulticore, r.systemconfig AS rsystemconfig, r.mctck AS rmctck
  FROM steps s, steps r, runtimeprojects rr  WHERE s.stepid = rr.stepid( + ) AND r.stepid( + ) = rr.runtimeprojectid AND s.inputfiletypes IS NULL AND s.usable != 'Obsolete') LOOP
  pipe row(stepobj(cur.stepid,cur.stepname,cur.applicationname, cur.applicationversion, cur.optionfiles, cur.dddb, cur.conddb, cur.extrapackages, cur.visible, cur.processingpass, cur.usable, cur.dqtag, cur.optionsformat, cur.ismulticore, cur.systemconfig, cur.mctck,
            cur.rid, cur.rsname, cur.rappname, cur.rappver, cur.roptsf, cur.rdddb, cur.rcondb, cur.rextra, cur.rvisi, cur.rproc, cur.rusab,cur.rdq,cur.ropff, cur.rmulticore, cur.rsystemconfig, cur.rmctck));
  END LOOP;
ELSE
IF iftypes.count > 0 THEN
  FOR c IN (SELECT s.stepid, s.inputfiletypes, s.outputfiletypes FROM steps s  WHERE s.inputfiletypes IS NOT NULL AND s.usable != 'Obsolete')
    LOOP
     --DBMS_OUTPUT.PUT_LINE('WHY!!? '||c.stepid);
     IF c.inputfiletypes IS NOT NULL THEN
       IF MATCH = 'YES' THEN
          IF c.inputfiletypes.count != iftypes.count THEN
             INPUT:=FALSE;
          ELSE
          FOR i IN c.inputfiletypes.first .. c.inputfiletypes.last LOOP
            IF i > iftypes.count THEN
              INPUT:= FALSE;
            ELSE
             INPUT:=iftypes(i) = c.inputfiletypes(i).name;
            END IF;
            exit WHEN NOT INPUT;
          END LOOP;
          END IF;
       ELSE
         INPUT:=FALSE;
         FOR i IN iftypes.first .. iftypes.last LOOP
           FOR j IN c.inputfiletypes.first .. c.inputfiletypes.last LOOP
             IF iftypes(i) = c.inputfiletypes(j).name THEN
               INPUT:=TRUE;
               exit;
             END IF;
           END LOOP;
         exit WHEN INPUT;
         END LOOP;
       END IF;
     END IF;
     IF INPUT THEN
       IF oftypes.count > 0 THEN
         OUTPUT:=FALSE;
         IF c.outputfiletypes IS NOT NULL THEN
           IF MATCH = 'YES' THEN
             IF c.outputfiletypes.count != oftypes.count THEN
                 OUTPUT:=FALSE;
             ELSE
             FOR i IN c.outputfiletypes.first .. c.outputfiletypes.last LOOP
               IF i > iftypes.count THEN
                  OUTPUT:=FALSE;
               ELSE
                 OUTPUT:=oftypes(i) = c.outputfiletypes(i).name;
               END IF;
               exit WHEN NOT OUTPUT;
             END LOOP;
             END IF;
           ELSE
             OUTPUT:=FALSE;
             FOR i IN oftypes.first .. oftypes.last LOOP
               FOR j IN c.outputfiletypes.first .. c.outputfiletypes.last LOOP
                 IF oftypes(i) = c.outputfiletypes(j).name THEN
             OUTPUT:=TRUE;
                   exit;
                 END IF;
               END LOOP;
               exit WHEN OUTPUT;
             END LOOP;
           END IF;
         END IF;
       ELSE
        OUTPUT := TRUE;
       END IF;
    IF INPUT AND OUTPUT THEN
      dbms_output.put_line('Insert1: ' || c.stepid);
      FOR cur IN (SELECT s.stepid, s.stepname, s.applicationname, s.applicationversion, s.optionfiles, s.dddb, s.conddb, s.extrapackages, s.visible, s.processingpass, s.usable, s.dqtag,s.optionsformat, s.ismulticore, s.systemconfig,s.mctck,
                  r.stepid AS rid, r.stepname AS rsname, r.applicationname AS rappname, r.applicationversion AS rappver, r.optionfiles AS roptsf, r.dddb AS rdddb, r.conddb AS rcondb, r.extrapackages AS rextra, r.visible AS rvisi,
                  r.processingpass AS rproc, r.usable AS rusab, r.dqtag AS rdq,r.optionsformat AS ropff, r.ismulticore AS rmulticore, r.systemconfig AS rsysconfig, r.mctck AS rmctck
        FROM steps s, steps r, runtimeprojects rr  WHERE s.stepid = rr.stepid( + ) AND r.stepid( + ) = rr.runtimeprojectid AND s.stepid = c.stepid AND s.usable != 'Obsolete' ) LOOP
      pipe row(stepobj(cur.stepid,cur.stepname,cur.applicationname, cur.applicationversion, cur.optionfiles, cur.dddb, cur.conddb, cur.extrapackages, cur.visible, cur.processingpass, cur.usable, cur.dqtag, cur.optionsformat, cur.ismulticore, cur.systemconfig, cur.mctck,
               cur.rid, cur.rsname, cur.rappname, cur.rappver, cur.roptsf, cur.rdddb, cur.rcondb, cur.rextra, cur.rvisi, cur.rproc, cur.rusab,cur.rdq,cur.ropff, cur.rmulticore, cur.rsysconfig, cur.mctck));
      END LOOP;
    END IF;
  END IF;
 END LOOP;
ELSE
  FOR c IN (SELECT s.stepid, s.inputfiletypes, s.outputfiletypes FROM steps s WHERE s.outputfiletypes IS NOT NULL AND s.usable != 'Obsolete')
    LOOP
     OUTPUT:=FALSE;
     IF c.outputfiletypes IS NOT NULL THEN
       IF MATCH = 'YES' THEN
         IF c.outputfiletypes.count != oftypes.count THEN
             OUTPUT:=FALSE;
         ELSE
         FOR i IN c.outputfiletypes.first .. c.outputfiletypes.last LOOP
           IF i > oftypes.count THEN
             OUTPUT:=FALSE;
           ELSE
             OUTPUT:=oftypes(i) = c.outputfiletypes(i).name;
           END IF;
           exit WHEN NOT OUTPUT;
         END LOOP;
         END IF;
       ELSE
        OUTPUT:=FALSE;
        FOR i IN oftypes.first .. oftypes.last LOOP
          FOR j IN c.outputfiletypes.first .. c.outputfiletypes.last LOOP
            IF oftypes(i) = c.outputfiletypes(j).name THEN
        OUTPUT:=TRUE;
              exit;
            END IF;
          END LOOP;
          exit WHEN OUTPUT;
        END LOOP;
       END IF;
     END IF;
     IF OUTPUT THEN
       IF iftypes.count > 0 THEN
         INPUT:=FALSE;
         IF MATCH = 'YES' THEN
           IF c.inputfiletypes.count != iftypes.count THEN
              INPUT:=FALSE;
           ELSE
           FOR j IN c.inputfiletypes.first .. c.inputfiletypes.last LOOP
             IF j > iftypes.count THEN
               INPUT:=FALSE;
             ELSE
               INPUT:=iftypes(j) = c.inputfiletypes(j).name;
             END IF;
             exit WHEN NOT OUTPUT;
           END LOOP;
           END IF;
         ELSE
           INPUT:=FALSE;
           FOR i IN iftypes.first .. iftypes.last LOOP
             FOR j IN c.inputfiletypes.first .. c.inputfiletypes.last LOOP
               IF iftypes(i) = c.inputfiletypes(j).name THEN
                 INPUT:=TRUE;
                 exit;
               END IF;
             END LOOP;
             exit WHEN INPUT;
           END LOOP;
         END IF;
       ELSE
        INPUT := TRUE;
       END IF;
    IF INPUT AND OUTPUT THEN
      dbms_output.put_line('Insert2: ' || c.stepid);
      FOR cur2 IN (SELECT s.stepid, s.stepname, s.applicationname, s.applicationversion, s.optionfiles, s.dddb, s.conddb, s.extrapackages, s.visible, s.processingpass, s.usable, s.dqtag,s.optionsformat, s.ismulticore, s.systemconfig,s.mctck,
                          r.stepid AS rid, r.stepname AS rsname, r.applicationname AS rappname, r.applicationversion AS rappver, r.optionfiles AS roptsf, r.dddb AS rdddb, r.conddb AS rcondb, r.extrapackages AS rextra, r.visible AS rvisi,
                          r.processingpass AS rproc, r.usable AS rusab, r.dqtag AS rdq,r.optionsformat AS ropff, r.ismulticore AS rmulticore, r.systemconfig AS rsysconfig, r.mctck AS rmctck
        FROM steps s, steps r, runtimeprojects rr  WHERE s.stepid = rr.stepid( + ) AND r.stepid( + ) = rr.runtimeprojectid AND s.stepid = c.stepid AND s.usable != 'Obsolete') LOOP
        pipe row(stepobj(cur2.stepid,cur2.stepname,cur2.applicationname, cur2.applicationversion, cur2.optionfiles, cur2.dddb, cur2.conddb, cur2.extrapackages, cur2.visible, cur2.processingpass, cur2.usable, cur2.dqtag, cur2.optionsformat, cur2.ismulticore, cur2.systemconfig,cur2.mctck,
                          cur2.rid, cur2.rsname, cur2.rappname, cur2.rappver, cur2.roptsf, cur2.rdddb, cur2.rcondb, cur2.rextra, cur2.rvisi, cur2.rproc, cur2.rusab,cur2.rdq,cur2.ropff, cur2.rmulticore, cur2.rsysconfig, cur2.rmctck));
      END LOOP;
    END IF;
  END IF;
 END LOOP;
END IF;
END IF;
END;

---------------------------------------------------------------------------------------------------------------------------

function getProductionProcessingPass(prod NUMBER) return varchar2 is
retval varchar2(256);
ecode NUMBER(38);
thisproc CONSTANT VARCHAR2(50) := 'trap_errmesg';
begin
 SELECT v.path into retval FROM (SELECT distinct  LEVEL-1 Pathlen, SYS_CONNECT_BY_PATH(name, '/') Path
   FROM processing
   WHERE LEVEL > 0 and id = (SELECT distinct processingid FROM productionscontainer WHERE productionscontainer.production=prod)
   CONNECT BY NOCYCLE PRIOR id=parentid order by Pathlen desc) v WHERE rownum<=1;
return retval;
EXCEPTION WHEN OTHERS THEN
raise_application_error(-20004, 'error found! The processing pass does not exists!');
--ecode := SQLERRM; --SQLCODE;
--dbms_output.put_line(thisproc || ' - ' || ecode);
return null;
end;

------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getproductionprocessingpassid (
    prod NUMBER
) RETURN NUMBER IS
    result   NUMBER;
    ecode    NUMBER(38);
    thisproc CONSTANT VARCHAR2(50) := 'trap_errmesg';
BEGIN
    SELECT DISTINCT
        processingid
    INTO result
    FROM
        productionscontainer prod
    WHERE
        prod.production = prod;

    RETURN result;
EXCEPTION
    WHEN OTHERS THEN
        ecode := sqlerrm;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getavailableeventtypes(a_cursor OUT udt_refcursor) IS
BEGIN
  OPEN a_cursor FOR
    SELECT DISTINCT eventtypeid, description
    FROM eventtypes;
END;

------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getjobinfo(
   lfn                             VARCHAR2,
   a_cursor                        OUT udt_refcursor
) IS
BEGIN
  OPEN a_cursor FOR
    SELECT jobs.diracjobid,
           jobs.diracversion,
           jobs.eventinputstat,
           jobs.exectime,
           jobs.firsteventnumber,
           jobs.location,
           jobs.name,
           jobs.numberofevents,
           jobs.statisticsrequested,
           jobs.wncpupower,
           jobs.cputime,
           jobs.wncache,
           jobs.wnmemory,
           jobs.wnmodel,
           jobs.workernode,
           jobs.wncpuhs06,
           jobs.jobid,
           jobs.totalluminosity,
           jobs.production,
           jobs.programname,
           jobs.programversion,
           jobs.wnmjfhs06,
           jobs.hlt2tck,
           jobs.numberofprocessors
    FROM jobs,files
    WHERE files.jobid = jobs.jobid
      AND files.filename = lfn;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE inserttag(
    v_name                            VARCHAR2,
    v_tag                             VARCHAR2
) IS
tid NUMBER;
BEGIN
  SELECT tags_index_seq.nextval INTO tid
  FROM dual;
  INSERT INTO tags(tagid,name, tag) VALUES(tid, v_name, v_tag);
  COMMIT;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getprocessingpassid(root VARCHAR2, fullpath VARCHAR2) RETURN NUMBER IS
RESULT NUMBER;
ecode number(38);
BEGIN
  RESULT:=-1;
  SELECT DISTINCT v.id INTO RESULT
  FROM (SELECT DISTINCT sys_connect_by_path(name, '/') path, id id
  FROM processing v START WITH id IN (
    SELECT DISTINCT id
    FROM processing
    WHERE name = root
    )
  CONNECT BY NOCYCLE PRIOR  id = parentid) v
  WHERE v.path = fullpath;
  RETURN  RESULT;
  EXCEPTION
    WHEN others THEN
      ecode := sqlerrm;
END;

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getdataqualityid(name VARCHAR2) RETURN NUMBER IS
RESULT NUMBER;
ecode number(38);
BEGIN
  RESULT:=1;
  SELECT DISTINCT qualityid INTO RESULT
  FROM dataquality
  WHERE dataqualityflag = name;
  RETURN RESULT;
  EXCEPTION WHEN others THEN
  ecode := sqlerrm;
END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getqflagbyrunandprocid (
    rnumber NUMBER,
    procid  NUMBER
) RETURN VARCHAR2 IS
    result VARCHAR2(256);
    ecode  NUMBER(38);
BEGIN
    result := -1;
    SELECT
        d.dataqualityflag
    INTO result
    FROM
        dataquality   d,
        newrunquality r
    WHERE
            r.runnumber = rnumber
        AND r.processingid = procid
        AND d.qualityid = r.qualityid;

    RETURN result;
EXCEPTION
    WHEN no_data_found THEN
        RETURN NULL;
    WHEN OTHERS THEN
        ecode := sqlerrm;
END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getrunbyqflagandprocid(
  procid NUMBER,
  flag NUMBER,
  a_cursor OUT udt_refcursor ) IS
BEGIN
  IF flag IS NOT NULL THEN
    OPEN a_cursor FOR
      SELECT runnumber
      FROM newrunquality
      WHERE processingid = procid
        AND qualityid = flag;
  ELSE
    OPEN a_cursor FOR SELECT runnumber FROM newrunquality WHERE processingid = procid;
  END IF;
END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getfileid(
  v_filename VARCHAR2
)
RETURN NUMBER IS fid NUMBER;
BEGIN
  fid := 0;
  SELECT files.fileid INTO fid
  FROM files
  WHERE files.filename = v_filename;
  RETURN fid;
  EXCEPTION WHEN others THEN
  RETURN NULL;
END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getfileandjobmetadata(
  v_jobid NUMBER,
  prod BOOLEAN,
  a_cursor OUT udt_refcursor
) IS
BEGIN
  IF NOT prod THEN
    OPEN a_cursor FOR
      SELECT files.filename,
             files.fileid,
             files.gotreplica,
             0,
             files.eventstat,
             files.eventtypeid,
             files.luminosity,
             files.instluminosity,
             filetypes.name
      FROM files, filetypes
      WHERE files.filetypeid = filetypes.filetypeid
        AND files.jobid = v_jobid;
  ELSE
    OPEN a_cursor FOR
      SELECT files.filename,
             files.fileid,
             files.gotreplica,
             jobs.production,
             files.eventstat,
             files.eventtypeid,
             files.luminosity,
             files.instluminosity,
             filetypes.name
      FROM files, jobs, filetypes
      WHERE files.filetypeid = filetypes.filetypeid
        AND jobs.jobid = files.jobid
        AND files.jobid = v_jobid;
  END IF;
END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE checkfile(
  name                            VARCHAR2,
  a_cursor                        OUT udt_refcursor
) IS
BEGIN
  OPEN a_cursor FOR
    SELECT fileid,
           jobid,
           filetypeid
    FROM files
    WHERE filename = name;
END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION checkfiletypeandversion (
       v_name                          VARCHAR2,
       v_version                       VARCHAR2
) RETURN NUMBER IS
  id NUMBER :=0;
  descr varchar2(256);
  BEGIN
    SELECT filetypeid INTO id
    FROM filetypes
    WHERE name = v_name
      AND VERSION = v_version;
    RETURN id;
    EXCEPTION
     WHEN too_many_rows THEN
      SELECT min(filetypeid) INTO id
      FROM filetypes
      WHERE name = v_name
        AND VERSION = v_version;RETURN id;
     WHEN others THEN
    SELECT count(*) INTO id
    FROM filetypes
    WHERE name = v_name;
    IF id > 0 THEN
    SELECT DISTINCT description INTO descr
    FROM filetypes
    WHERE name = v_name;
    SELECT coalesce(max(filetypeid) + 1, 1) INTO id FROM filetypes;
    INSERT INTO filetypes(filetypeid,name,description,VERSION) VALUES(id,v_name,descr,v_version);
    COMMIT;
    RETURN id;
    ELSE
      raise_application_error(-20013, 'File type does not exist!');
    END IF;
  END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE checkeventtype (
    v_eventtypeid                  NUMBER,
    a_cursor                       OUT udt_refcursor
 ) IS
 BEGIN
   OPEN a_cursor FOR
    SELECT description, PRIMARY
    FROM eventtypes
    WHERE eventtypeid = v_eventtypeid;
 END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION insertjobsrow (
     v_configname                  VARCHAR2,
     v_configversion               VARCHAR2,
     v_diracjobid                  NUMBER,
     v_diracversion                VARCHAR2,
     v_eventinputstat              NUMBER,
     v_exectime                    FLOAT,
     v_firsteventnumber            NUMBER,
     v_jobend                      TIMESTAMP,
     v_jobstart                    TIMESTAMP,
     v_location                    VARCHAR2,
     v_name                        VARCHAR2,
     v_numberofevents              NUMBER,
     v_production                  NUMBER,
     v_programname                 VARCHAR2,
     v_programversion              VARCHAR2,
     v_statisticsrequested         NUMBER,
     v_wncpupower                  VARCHAR2,
     v_cputime                     FLOAT,
     v_wncache                     VARCHAR2,
     v_wnmemory                    VARCHAR2,
     v_wnmodel                     VARCHAR2,
     v_workernode                  VARCHAR2,
     v_runnumber                   NUMBER,
     v_fillnumber                  NUMBER,
     v_wncpuhs06                   FLOAT,
     v_totalluminosity             NUMBER,
     v_tck                         VARCHAR2,
     v_stepid                      NUMBER,
     v_wnmjfhs06                   FLOAT,
     v_hlt2tck                     VARCHAR2,
     v_numproc                     NUMBER
  )RETURN NUMBER IS
  jid       NUMBER;
  configid  NUMBER;
  existindb  NUMBER;
  ecode    varchar2(256);
  BEGIN
    configid := 0;
    SELECT count(*) INTO existindb FROM configurations WHERE configname = v_configname AND configversion = v_configversion;
    IF existindb = 0 THEN
      SELECT configurationid_seq.nextval INTO configid FROM dual;
      INSERT INTO configurations(configurationid,configname,configversion)VALUES(configid, v_configname, v_configversion);
      COMMIT;
    ELSE
     SELECT configurationid INTO configid FROM configurations WHERE configname = v_configname AND configversion = v_configversion;
    END IF;

    SELECT jobid_seq.nextval INTO jid FROM dual;
     INSERT INTO jobs(
         jobid,
         configurationid,
         diracjobid,
         diracversion,
         eventinputstat,
         exectime,
         firsteventnumber,
         jobend,
         jobstart,
         LOCATION,
         name,
         numberofevents,
         production,
         programname,
         programversion,
         statisticsrequested,
         wncpupower,
         cputime,
         wncache,
         wnmemory,
         wnmodel,
         workernode,
         runnumber,
         fillnumber,
         wncpuhs06,
         totalluminosity,
         tck,
         stepid,
         wnmjfhs06,
         hlt2tck,
         numberofprocessors
         )
   VALUES(
          jid,
          configid,
          v_diracjobid,
          v_diracversion,
          v_eventinputstat,
          v_exectime,
          v_firsteventnumber,
          v_jobend,
          v_jobstart,
          v_location,
          v_name,
          v_numberofevents,
          v_production,
          v_programname,
          v_programversion,
          v_statisticsrequested,
          v_wncpupower,
          v_cputime,
          v_wncache,
          v_wnmemory,
          v_wnmodel,
          v_workernode,
          v_runnumber,
          v_fillnumber,
          v_wncpuhs06,
          v_totalluminosity,
          v_tck,
          v_stepid,
          v_wnmjfhs06,
          v_hlt2tck,
          v_numproc);

  COMMIT;
  RETURN jid;
  EXCEPTION
  WHEN dup_val_on_index THEN
    jid:=0;
    IF v_production < 0 THEN
      SELECT j.jobid INTO jid FROM jobs j WHERE j.runnumber = v_runnumber AND j.production < 0;
    ELSE
       SELECT j.jobid INTO jid FROM jobs j WHERE j.name = v_name AND j.production = v_production;
    END IF;

    IF jid = 0 THEN
      ecode:= sqlerrm;
      raise_application_error(ecode, 'It is not a run!');
    ELSE
       UPDATE jobs SET configurationid = configid,
         diracjobid = v_diracjobid,
         diracversion = v_diracversion,
         eventinputstat = v_eventinputstat,
         exectime = v_exectime,
         firsteventnumber = v_firsteventnumber,
         jobend = v_jobend,
         jobstart = v_jobstart,
         LOCATION = v_location,
         name = v_name,
         numberofevents = v_numberofevents,
         production = v_production,
         programname = v_programname,
         programversion = v_programversion,
         statisticsrequested = v_statisticsrequested,
         wncpupower = v_wncpupower,
         cputime = v_cputime,
         wncache = v_wncache,
         wnmemory = v_wnmemory,
         wnmodel = v_wnmodel,
         workernode = v_workernode,
         fillnumber = v_fillnumber,
         wncpuhs06 = v_wncpuhs06,
         totalluminosity = v_totalluminosity,
         stepid = v_stepid,
         tck = v_tck,
         wnmjfhs06 = v_wnmjfhs06,
         hlt2tck = v_hlt2tck,
         numberofprocessors = v_numproc WHERE jobid = jid;
      COMMIT;
    RETURN jid;
    END IF;
    RETURN -1;
  END;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION insertfilesrow(
  v_adler32                         VARCHAR2,
  v_creationdate                    TIMESTAMP,
  v_eventstat                       NUMBER,
  v_eventtypeid                     NUMBER,
  v_filename                        VARCHAR2,
  v_filetypeid                      NUMBER,
  v_gotreplica                      VARCHAR2,
  v_guid                            VARCHAR2,
  v_jobid                           NUMBER,
  v_md5sum                          VARCHAR2,
  v_filesize                        NUMBER,
  v_fullstat                      NUMBER,
  v_utc                             TIMESTAMP,
  dqflag                            VARCHAR2,
  v_luminosity                      NUMBER,
  v_instluminosity                   Number,
  v_visibilityflag                  VARCHAR2
) RETURN NUMBER IS
  fid NUMBER;
  dqid NUMBER;
  BEGIN
    dqid:=1;
    SELECT dataquality.qualityid INTO dqid FROM dataquality WHERE dataquality.dataqualityflag = dqflag;
    SELECT fileid_seq.nextval INTO fid FROM dual;
    INSERT INTO files (
                fileid,
                adler32,
                creationdate,
                eventstat,
                eventtypeid,
                filename,
                filetypeid,
                gotreplica,
                guid,
                jobid,
                md5sum,
                filesize,
                fullstat,
                qualityid,
                inserttimestamp,
                luminosity,
                instluminosity,
                visibilityflag
                )
           VALUES (
                fid,
                v_adler32,
                v_creationdate,
                v_eventstat,
                v_eventtypeid,
                v_filename,
                v_filetypeid,
                v_gotreplica,
                v_guid,
                v_jobid,
                v_md5sum,
                v_filesize,
                v_fullstat,
                dqid,
                v_utc,
                v_luminosity,
                v_instluminosity,
                v_visibilityflag
                );
  COMMIT;
  RETURN fid;
  EXCEPTION
  WHEN dup_val_on_index THEN
    SELECT fileid INTO fid FROM files WHERE filename = v_filename;
    UPDATE files SET adler32 = v_adler32,
                creationdate = v_creationdate,
                eventstat = v_eventstat,
                eventtypeid = v_eventtypeid,
                filetypeid = v_filetypeid,
                guid = v_guid,
                jobid = v_jobid,
                md5sum = v_md5sum,
                filesize = v_filesize,
                fullstat = v_fullstat,
                qualityid = dqid,
                inserttimestamp = v_utc,
                luminosity = v_luminosity,
                instluminosity = v_instluminosity,
                visibilityflag = v_visibilityflag WHERE fileid = fid;
    COMMIT;
    RETURN fid;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertinputfilesrow(
  v_fileid NUMBER,
  v_jobid NUMBER
)IS
  BEGIN
    INSERT INTO inputfiles(
         fileid,
         jobid
         ) VALUES(
                v_fileid,
                v_jobid);
  COMMIT;
  EXCEPTION
  WHEN dup_val_on_index THEN
    dbms_output.put_line('The input file of the job is added: ' || v_jobid);
  END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updatereplicarow(
  v_fileid NUMBER,
  v_replica VARCHAR2
)IS
  BEGIN
    UPDATE files
    SET inserttimestamp = sys_extract_utc(systimestamp),gotreplica = v_replica
    WHERE fileid = v_fileid;
    COMMIT;
  END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deletejob(
  v_jobid NUMBER
)IS
  BEGIN
    DELETE FROM jobs
    WHERE jobid = v_jobid;
    COMMIT;
  END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deleteinputfiles(
  v_jobid NUMBER
)IS
  BEGIN
    DELETE FROM inputfiles
    WHERE jobid = v_jobid;
    COMMIT;
  END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deletefile(
  v_fileid NUMBER
)IS
  BEGIN
    DELETE FROM files
    WHERE fileid = v_fileid;
    COMMIT;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deletesetpcontiner(
  v_prod NUMBER
)IS
  BEGIN
    DELETE FROM stepscontainer
    WHERE production = v_prod;
    COMMIT;
  END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deletestepcontainer(
  v_prod NUMBER
)IS
  BEGIN
    DELETE FROM stepscontainer
    WHERE production = v_prod;
    COMMIT;
  END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE deleteproductionscont(
  v_prod NUMBER
)IS
  BEGIN
    DELETE FROM productionscontainer
    WHERE production = v_prod;
    COMMIT;
  END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION insertsimconditions(
   v_simdesc                VARCHAR2,
   v_beamcond               VARCHAR2,
   v_beamenergy             VARCHAR2,
   v_generator              VARCHAR2,
   v_magneticfield          VARCHAR2,
   v_detectorcond           VARCHAR2,
   v_luminosity             VARCHAR2,
   v_g4settings             VARCHAR2,
   v_visible                VARCHAR2
)RETURN NUMBER
  IS
  simulid NUMBER;
  BEGIN
    SELECT simulationcondid_seq.nextval INTO simulid FROM dual;
    INSERT INTO simulationconditions(
                  simid,
                  simdescription,
                  beamcond,
                  beamenergy,
                  generator,
                  magneticfield,
                  detectorcond,
                  luminosity,
                  g4settings,
                  visible)
    VALUES(simulid,
           v_simdesc,
           v_beamcond,
           v_beamenergy,
           v_generator,
           v_magneticfield,
           v_detectorcond,
           v_luminosity,
           v_g4settings,
           v_visible);
  COMMIT;
  RETURN simulid;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getsimconditions(
  a_cursor OUT udt_refcursor
)IS
  BEGIN
    OPEN a_cursor FOR
    SELECT * FROM simulationconditions
    WHERE visible = 'Y'
    ORDER BY simid DESC;
  END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION insertdatatakingcond(
  v_description                                        VARCHAR2,
  v_beamcond                                           VARCHAR2,
  v_beamenergy                                         VARCHAR2,
  v_magneticfield                                      VARCHAR2,
  v_velo                                               VARCHAR2,
  v_it                                                 VARCHAR2,
  v_tt                                                 VARCHAR2,
  v_ot                                                 VARCHAR2,
  v_rich1                                              VARCHAR2,
  v_rich2                                              VARCHAR2,
  v_spd_prs                                            VARCHAR2,
  v_ecal                                               VARCHAR2,
  v_hcal                                               VARCHAR2,
  v_muon                                               VARCHAR2,
  v_l0                                                 VARCHAR2,
  v_hlt                                                VARCHAR2,
  v_veloposition                                       VARCHAR2
) RETURN NUMBER
IS
daq       NUMBER;
  BEGIN
      daq := 0;
      SELECT simulationcondid_seq.nextval INTO daq FROM dual;
      IF v_description IS NULL THEN
      INSERT /* APPEND */ INTO data_taking_conditions(daqperiodid, description, beamcond, beamenergy, magneticfield,
                                       velo, it, tt, ot, rich1, rich2, spd_prs, ecal, hcal, muon, l0, hlt,veloposition)
                                      VALUES(
                                         daq,
                                         'DataTaking' || daq,
                                         v_beamcond,
                                         v_beamenergy,
                                         v_magneticfield,
                                         v_velo,
                                         v_it,
                                         v_tt,
                                         v_ot,
                                         v_rich1,
                                         v_rich2,
                                         v_spd_prs,
                                         v_ecal,
                                         v_hcal,
                                         v_muon,
                                         v_l0,
                                         v_hlt,
                                         v_veloposition);
    COMMIT;
    ELSE
       INSERT /* APPEND */ INTO data_taking_conditions(daqperiodid, description, beamcond, beamenergy, magneticfield,
                                       velo, it, tt, ot, rich1, rich2, spd_prs, ecal, hcal, muon, l0, hlt,veloposition)
                                      VALUES(
                                         daq,
                                         v_description,
                                         v_beamcond,
                                         v_beamenergy,
                                         v_magneticfield,
                                         v_velo,
                                         v_it,
                                         v_tt,
                                         v_ot,
                                         v_rich1,
                                         v_rich2,
                                         v_spd_prs,
                                         v_ecal,
                                         v_hcal,
                                         v_muon,
                                         v_l0,
                                         v_hlt,
                                         v_veloposition);
    COMMIT;
    END IF;

    RETURN (daq);
    EXCEPTION WHEN others THEN
    RETURN 0;
  END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PROCEDURE getfilemetadata(
   v_filename VARCHAR2,
   a_cursor   OUT udt_refcursor
)IS
  BEGIN
   OPEN a_cursor FOR
     SELECT files.filename,files.adler32,files.creationdate,files.eventstat,files.eventtypeid,filetypes.name,files.gotreplica,files.guid,files.md5sum,files.filesize, files.fullstat, dataquality.dataqualityflag, files.jobid, jobs.runnumber, files.inserttimestamp,files.luminosity,files.instluminosity FROM files,filetypes,dataquality,jobs WHERE
         filename = v_filename AND
         jobs.jobid = files.jobid AND
         files.filetypeid = filetypes.filetypeid AND
         files.qualityid = dataquality.qualityid;
  END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getfilemetadata3(iftypes varchararray, a_cursor OUT udt_refcursor)
IS
lfnmeta metadata_table := metadata_table();
n integer := 0;
BEGIN
FOR j IN iftypes.first .. iftypes.last LOOP
  dbms_output.put_line('FileName: ' || iftypes(j));
  FOR cur IN (SELECT files.filename,files.adler32,files.creationdate,files.eventstat,files.eventtypeid,filetypes.name,files.gotreplica,files.guid,files.md5sum,files.filesize, files.fullstat, dataquality.dataqualityflag, files.jobid, jobs.runnumber, files.inserttimestamp,files.luminosity,files.instluminosity, files.visibilityflag FROM files,filetypes,dataquality,jobs WHERE
         filename = iftypes(j) AND
         jobs.jobid = files.jobid AND
         files.filetypeid = filetypes.filetypeid AND
         files.qualityid = dataquality.qualityid) LOOP
 lfnmeta.extend;
 n:=n + 1;
 lfnmeta (n):=metadata0bj(cur.filename, cur.adler32,cur.creationdate,cur.eventstat, cur.eventtypeid, cur.name, cur.gotreplica, cur.guid, cur.md5sum, cur.filesize, cur.fullstat, cur.dataqualityflag, cur.jobid, cur.runnumber, cur.inserttimestamp, cur.luminosity, cur.instluminosity, cur.visibilityflag, NULL, NULL);
  END LOOP;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(lfnmeta);
END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION fileexists (
    v_filename            VARCHAR2
)RETURN NUMBER IS
  fid NUMBER;
  BEGIN
    SELECT fileid INTO fid
    FROM files
    WHERE filename = v_filename;
  RETURN (fid);
    EXCEPTION WHEN others THEN
    RETURN 0;

END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE inserteventtypes(
  v_description           VARCHAR2,
  v_eventtypeid           NUMBER,
  v_primary               VARCHAR2
) IS
  BEGIN
    INSERT INTO eventtypes(description, eventtypeid, PRIMARY)
    VALUES (v_description, v_eventtypeid, v_primary);
    COMMIT;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE  updateeventtypes(
        v_description           VARCHAR2,
        v_eventtypeid           NUMBER,
        v_primary               VARCHAR2
) IS
  BEGIN
    UPDATE eventtypes
    SET description = v_description, PRIMARY = v_primary
    WHERE eventtypeid = v_eventtypeid;
    COMMIT;
  END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE setfileinvisible (
  lfn VARCHAR2
 )IS
 BEGIN
  UPDATE files
  SET visibilityflag = 'N',inserttimestamp = sys_extract_utc(systimestamp)
  WHERE files.filename = lfn;
  COMMIT;
 END;

PROCEDURE setfilevisible(
  lfn VARCHAR2
 )IS
 BEGIN
  UPDATE files
  SET visibilityflag = 'Y',inserttimestamp = sys_extract_utc(systimestamp)
  WHERE files.filename = lfn;
  COMMIT;
 END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getconfigsandevttype(
   prodid                  NUMBER,
   a_cursor                OUT udt_refcursor
)IS
  BEGIN
    OPEN a_cursor FOR
    SELECT c.configname,c.configversion,prod.eventtypeid
    FROM productionoutputfiles prod, configurations c, productionscontainer cont
    WHERE prod.production = prodid
      AND cont.production = prod.production
      AND cont.configurationid = c.configurationid
    GROUP BY c.configname,c.configversion,prod.eventtypeid;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getjobsbysites(
   prodid                  NUMBER,
   a_cursor                OUT udt_refcursor
)IS
  BEGIN
   OPEN a_cursor FOR
    SELECT count(*), jobs.location
    FROM jobs
    WHERE production = prodid
    GROUP BY LOCATION;
  END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getsteps(
   prodid                  NUMBER,
   a_cursor                OUT udt_refcursor
)IS
  BEGIN
   OPEN a_cursor FOR
    SELECT s.stepname, s.applicationname, s.applicationversion, s.optionfiles, s.dddb, s.conddb, s.extrapackages, s.stepid, s.visible
    FROM steps s, stepscontainer prod
    WHERE prod.stepid = s.stepid
      AND prod.production = prodid
    ORDER BY prod.step;
  EXCEPTION
  WHEN others THEN
    raise_application_error(-20003, 'error found the production does not exists  in the productionscontainer table!');
  END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getproductioninformation(
   prodid                  NUMBER,
   a_cursor                OUT udt_refcursor
  )IS
  pid NUMBER;
  BEGIN
   OPEN a_cursor FOR
     SELECT DISTINCT c.configname,c.configversion,f.eventtypeid,s.stepname, s.applicationname, s.applicationversion, s.optionfiles, s.dddb, s.conddb, s.extrapackages, prod.step
          FROM steps s, stepscontainer prod, jobs j, configurations c, files f WHERE
           j.jobid = f.jobid AND
           f.eventtypeid > 0 AND
           j.production = prodid AND
           c.configurationid = j.configurationid AND
           prod.stepid = s.stepid AND
           prod.production = j.production ORDER BY prod.step;
  END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getnboffiles( prodid                  NUMBER,
    a_cursor                OUT udt_refcursor
  )IS
  total NUMBER;
  BEGIN
   SELECT /*+ INDEX(files FILES_JOB_EVENT_FILETYPE) */ count(*) INTO total FROM files, jobs WHERE files.jobid = jobs.jobid AND jobs.production = prodid;
   OPEN a_cursor FOR
     SELECT /*+ INDEX(files FILES_JOB_EVENT_FILETYPE) */ count(*), filetypes.name,total AS totalfiles FROM files, jobs,filetypes WHERE
        files.jobid = jobs.jobid AND
        jobs.production = prodid AND
        filetypes.filetypeid = files.filetypeid GROUP BY filetypes.name;
  END;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getsizeoffiles(
    prodid                  NUMBER,
    a_cursor                OUT udt_refcursor
  )IS
  BEGIN
  OPEN a_cursor FOR
    SELECT /*+ INDEX(files FILES_JOB_EVENT_FILETYPE) */  sum(filesize) FROM files,jobs WHERE files.jobid = jobs.jobid AND jobs.production = prodid;
  END;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getnumberofevents(
    prodid                  NUMBER,
    a_cursor                OUT udt_refcursor
  )IS
  BEGIN
  OPEN a_cursor FOR
   SELECT /*+ INDEX(files FILES_JOB_EVENT_FILETYPE) */ filetypes.name,sum(files.eventstat), files.eventtypeid, sum(jobs.eventinputstat) FROM files,jobs,filetypes WHERE
            files.jobid = jobs.jobid AND
            files.gotreplica = 'Yes' AND
            jobs.production = prodid AND
            filetypes.filetypeid = files.filetypeid GROUP BY filetypes.name, files.eventtypeid;
  END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getjobsnb(
    prodid            NUMBER,
    a_cursor                OUT udt_refcursor
)IS
  BEGIN
  OPEN a_cursor FOR
    SELECT count(*)
    FROM jobs
    WHERE production = prodid;
END;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertstepscontainer(
    v_prod NUMBER,
    v_stepid NUMBER,
    v_step NUMBER
  )IS
  alreadyexists NUMBER;
  BEGIN
  INSERT INTO stepscontainer(production,stepid,step) VALUES(v_prod, v_stepid, v_step);
  COMMIT;
  EXCEPTION
    WHEN dup_val_on_index THEN
      dbms_output.put_line(v_prod || 'already in the steps container table');
      SELECT count(*) INTO alreadyexists
      FROM stepscontainer
      WHERE production = v_prod
        AND stepid = v_stepid
        AND step = v_step;
     IF alreadyexists > 0 THEN
       raise_application_error(-20005, 'The production already exists in the steps container table!');
     END IF;
END;
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertproductionscontainer(v_prod NUMBER, v_processingid NUMBER, v_simid NUMBER, v_daqperiodid NUMBER, cname VARCHAR2, cversion VARCHAR2) IS
configid NUMBER;
existindb NUMBER;
BEGIN
configid := 0;
SELECT count(*) INTO existindb FROM configurations WHERE configname = cname AND configversion = cversion;
IF existindb = 0 THEN
  SELECT configurationid_seq.nextval INTO configid FROM dual;
  INSERT INTO configurations(configurationid,configname,configversion)VALUES(configid, cname, cversion);
  COMMIT;
ELSE
 SELECT configurationid INTO configid FROM configurations WHERE configname = cname AND configversion = cversion;
END IF;
INSERT INTO productionscontainer(production,processingid,simid,daqperiodid, configurationid)VALUES(v_prod, v_processingid, v_simid, v_daqperiodid, configid);
COMMIT;
EXCEPTION
  WHEN dup_val_on_index THEN
   existindb := 0;
   dbms_output.put_line(v_prod || 'already in the steps container table');
   SELECT count(*) INTO existindb FROM productionscontainer WHERE production = v_prod AND processingid = v_processingid AND  simid = v_simid AND daqperiodid = v_daqperiodid AND configurationid = configid;
   IF existindb > 0 THEN
    raise_application_error(-20005, 'The production already exists in the productionscontainer table!');
   END IF;
END;
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 PROCEDURE geteventtypes(
    cname                 VARCHAR2,
    cversion              VARCHAR2,
    a_cursor              OUT udt_refcursor
   ) IS
BEGIN
  OPEN a_cursor FOR
    SELECT DISTINCT e.eventtypeid, e.description FROM productionoutputfiles prod, eventtypes e, productionscontainer cont,
    configurations c WHERE
    c.configname = cname AND c.configversion = cversion AND
    c.configurationid = cont.configurationid AND cont.production = prod.production AND
    prod.eventtypeid = e.eventtypeid
    ORDER BY e.eventtypeid DESC;
   END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION  getrunnumber(lfn VARCHAR2) RETURN NUMBER IS
id NUMBER;
BEGIN
SELECT jobs.runnumber INTO id FROM jobs,files WHERE files.jobid = jobs.jobid AND files.filename = lfn;
RETURN id;
EXCEPTION
  WHEN others THEN
  RETURN NULL;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertrunquality(run NUMBER, qid NUMBER, procid NUMBER) IS
BEGIN
INSERT INTO newrunquality(runnumber,qualityid, processingid) VALUES(run,qid,procid);
COMMIT;
EXCEPTION
  WHEN dup_val_on_index THEN
    UPDATE newrunquality SET qualityid = qid WHERE processingid = procid AND runnumber = run;
COMMIT;
END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getrunnbandtck(lfn VARCHAR2, a_cursor OUT udt_refcursor) IS
BEGIN
OPEN a_cursor FOR
  SELECT jobs.runnumber, jobs.tck FROM jobs,files WHERE files.jobid = jobs.jobid AND files.filename = lfn;
END;
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getruns(c_name VARCHAR2, c_version VARCHAR2,  a_cursor OUT udt_refcursor) IS
BEGIN
OPEN a_cursor FOR
  SELECT DISTINCT run.runnumber FROM productionoutputfiles prod, prodrunview run, configurations c, productionscontainer cont WHERE
  prod.production = run.production AND c.configname = c_name AND c.configversion = c_version AND
  cont.configurationid = c.configurationid AND cont.production = prod.production;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getrunprocpass(v_runnumber NUMBER) RETURN run_proc_table
IS
ret_tab run_proc_table := run_proc_table();
n integer := 0;
ret varchar2(256);
BEGIN
  FOR r IN (SELECT DISTINCT production FROM jobs WHERE runnumber = v_runnumber AND production > 0)
    LOOP
      ret_tab.extend;
      n := n + 1;
      ret:=getproductionprocessingpass(r.production);
      ret_tab(n) := runnb_proc(v_runnumber,ret);
      END LOOP;
RETURN ret_tab;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getrunquality(runs numberarray , a_cursor OUT udt_refcursor)
IS
ret_tab bulk_collect_run_quality_evt:= bulk_collect_run_quality_evt();
n integer := 0;
BEGIN
FOR i IN 1 .. runs.count LOOP
 FOR record IN (SELECT DISTINCT jobs.runnumber,dataquality.dataqualityflag,files. eventtypeid FROM files, jobs,dataquality WHERE files.jobid = jobs.jobid AND files.qualityid = dataquality.qualityid  AND jobs.production < 0 AND jobs.runnumber = runs(i)) LOOP
  ret_tab.extend;
  n := n + 1;
  ret_tab(n):= runnb_quality_eventtype(record.runnumber,record.dataqualityflag,record.eventtypeid);
  END LOOP;
  END LOOP;
OPEN a_cursor FOR SELECT * FROM table(ret_tab);
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE gettypevesrsion(lfn VARCHAR2, a_cursor OUT udt_refcursor)
IS
BEGIN
OPEN a_cursor FOR SELECT ftype.version FROM files f, filetypes ftype WHERE f.filetypeid = ftype.filetypeid AND f.filename = lfn;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getrunfiles(v_runnumber NUMBER, a_cursor OUT udt_refcursor)
IS
BEGIN
OPEN a_cursor FOR
SELECT f.filename, f.gotreplica, f.filesize,f.guid, f.luminosity, f.instluminosity, f.eventstat, f.fullstat
FROM jobs j ,files f, filetypes ft
WHERE j.jobid = f.jobid AND ft.filetypeid = f.filetypeid AND ft.name = 'RAW' AND  j.production < 0 AND j.runnumber = v_runnumber;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getprocessedevents(v_prodid NUMBER) RETURN NUMBER
IS
retval NUMBER := 0;
BEGIN
SELECT sum(j.numberofevents) INTO retval FROM jobs j, (SELECT scont.production, s.stepid
FROM stepscontainer scont, steps s
WHERE scont.stepid = s.stepid AND
scont.production = v_prodid AND
scont.step = (SELECT max(step) FROM stepscontainer WHERE stepscontainer.production = v_prodid)) firsts WHERE j.production = firsts.production AND j.stepid = firsts.stepid;
RETURN retval;
EXCEPTION
  WHEN others THEN
    raise_application_error(-20005, 'error found during the event NUMBER calculation');
END;
FUNCTION isvisible(v_stepid NUMBER) RETURN NUMBER
IS
vis char;
c NUMBER;
BEGIN
SELECT count(*) INTO c FROM table(SELECT s.outputfiletypes FROM steps s WHERE s.stepid = v_stepid);
IF c = 0 THEN
RETURN v_stepid;
ELSE
SELECT DISTINCT visible INTO vis FROM table(SELECT s.outputfiletypes FROM steps s WHERE s.stepid = v_stepid)
    WHERE visible = 'Y';
IF vis = 'Y' THEN
RETURN v_stepid;
ELSE
RETURN 0;
END IF;
END IF;
EXCEPTION
   WHEN no_data_found THEN
    RETURN -1;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertruntimeproject(pr_stepid NUMBER, run_pr_stepid NUMBER)
IS
BEGIN
INSERT INTO runtimeprojects(stepid, runtimeprojectid) VALUES (pr_stepid,run_pr_stepid);
COMMIT;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updateruntimeproject(pr_stepid NUMBER, run_pr_stepid NUMBER)
IS
counter Number;
BEGIN
 SELECT count(*) INTO counter FROM runtimeprojects WHERE stepid = pr_stepid;
 IF counter > 0 THEN
  UPDATE runtimeprojects SET runtimeprojectid = run_pr_stepid WHERE stepid = pr_stepid;
  ELSE
    insertruntimeproject (pr_stepid, run_pr_stepid);
  END IF;
COMMIT;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE removeruntimeproject(pr_stepid NUMBER)
IS
BEGIN
DELETE FROM runtimeprojects WHERE stepid = pr_stepid;
COMMIT;
END;

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getproductionporcpassname(v_procid NUMBER) RETURN VARCHAR2 IS
retval varchar2(256);
ecode    number(38);
thisproc constant varchar2(50) := 'trap_errmesg';
BEGIN
 SELECT v.path INTO retval FROM (SELECT DISTINCT  LEVEL-1 pathlen, sys_connect_by_path(name, '/') path
   FROM processing
   WHERE LEVEL > 0 AND id = v_procid
   CONNECT BY NOCYCLE PRIOR id = parentid ORDER BY pathlen DESC) v WHERE rownum <= 1;
RETURN retval;
EXCEPTION WHEN others THEN
raise_application_error(-20004, 'error found! The processing pass does not exists!');
--ecode := SQLERRM; --SQLCODE;
--dbms_output.put_line(thisproc || ' - ' || ecode);
RETURN NULL;
END;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getdirectorymetadata(f_name VARCHAR2, a_cursor OUT udt_refcursor)
IS
/*create or replace  type
directoryMetadata is object
(production NUMBER,
configname VARCHAR2(256),
configversion  VARCHAR2(256),
eventtypeid NUMBER,
filetype VARCHAR2(256),
processingpass VARCHAR2(256),
ConditionDescription VARCHAR2(256),
VISIBILITYFLAG CHAR(1));
create or replace
type bulk_collect_directoryMetadata is table of directoryMetadata;
*/
lfnmeta bulk_collect_directorymetadata := bulk_collect_directorymetadata();
n integer := 0;
procname varchar2(256);
simdesc varchar2(256);
daqdesc varchar2(256);
BEGIN
FOR c IN (SELECT /*+ INDEX(f FILES_FILENAME_UNIQUE) */ DISTINCT j.production, c.configname, c.configversion, ft.name, f.eventtypeid, f.visibilityflag FROM files f, jobs j, filetypes ft, configurations c WHERE
c.configurationid = j.configurationid AND ft.filetypeid = f.filetypeid AND j.jobid = f.jobid AND f.gotreplica = 'Yes' AND f.filename LIKE f_name)
LOOP
  SELECT getproductionporcpassname(prod.processingid),sim.simdescription, daq.description INTO procname, simdesc, daqdesc FROM productionscontainer prod, simulationconditions sim, data_taking_conditions daq WHERE
   production = c.production AND
   prod.simid = sim.simid( + ) AND
   prod.daqperiodid = daq.daqperiodid( + );
   lfnmeta.extend;
   n:=n + 1;
   IF simdesc IS NULL OR simdesc = '' THEN
     lfnmeta (n):= directorymetadata(c.production,c.configname, c.configversion, c.eventtypeid, c.name, procname,daqdesc,c.visibilityflag);
   ELSE
     lfnmeta (n):= directorymetadata(c.production,c.configname, c.configversion, c.eventtypeid, c.name, procname,simdesc,c.visibilityflag);
   END IF;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(lfnmeta);
EXCEPTION
   WHEN no_data_found THEN
    raise_application_error(-20088, 'The file ' || f_name || ' does not exists in the bookkeeping database!');
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getdirectorymetadata_new(lfns varchararray, a_cursor OUT udt_refcursor)
IS
/*create or replace  type
directoryMetadata_new is object
(lfn VARCHAR2(256),
production NUMBER,
configname VARCHAR2(256),
configversion  VARCHAR2(256),
eventtypeid NUMBER,
filetype VARCHAR2(256),
processingpass VARCHAR2(256),
ConditionDescription VARCHAR2(256),
VISIBILITYFLAG CHAR(1));
create or replace
type bulk_collect_directoryMet_new is table of directoryMetadata_new;
*/
lfnmeta bulk_collect_directorymet_new := bulk_collect_directorymet_new();
n integer := 0;
procname varchar2(256);
simdesc varchar2(256);
daqdesc varchar2(256);
allfiletypes varchar2(256);
FOUND NUMBER := 0;
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  FOR c IN (SELECT DISTINCT j.production, c.configname, c.configversion, ft.name, f.eventtypeid, f.visibilityflag FROM files f, jobs j, filetypes ft, configurations c WHERE
   c.configurationid = j.configurationid AND ft.filetypeid = f.filetypeid AND j.jobid = f.jobid AND f.gotreplica = 'Yes' AND f.filename LIKE lfns(i)) LOOP
   SELECT count(*) INTO FOUND FROM productionscontainer WHERE production = c.production;
   IF FOUND > 0 THEN
     SELECT getproductionporcpassname(prod.processingid),sim.simdescription, daq.description INTO procname, simdesc, daqdesc FROM productionscontainer prod, simulationconditions sim, data_taking_conditions daq WHERE
       production = c.production AND
       prod.simid = sim.simid( + ) AND
       prod.daqperiodid = daq.daqperiodid( + );
     lfnmeta.extend;
     n:=n + 1;
    allfiletypes := '';
    --we have to make the list of file types....
    FOR ff IN (SELECT DISTINCT ft.name FROM files f, jobs j, filetypes ft, configurations c WHERE
      c.configurationid = j.configurationid AND ft.filetypeid = f.filetypeid AND j.jobid = f.jobid AND f.gotreplica = 'Yes' AND f.filename LIKE lfns(i)) LOOP
       allfiletypes := concat(allfiletypes, concat(ff.name,','));
    END LOOP;
    --remove the coma
    allfiletypes := substr(allfiletypes, 0, length(allfiletypes)-1);
    IF simdesc IS NULL OR simdesc = '' THEN
      lfnmeta (n):= directorymetadata_new(lfns(i),c.production,c.configname, c.configversion, c.eventtypeid, allfiletypes, procname,daqdesc, c.visibilityflag);
    ELSE
      lfnmeta (n):= directorymetadata_new(lfns(i),c.production,c.configname, c.configversion, c.eventtypeid, allfiletypes, procname,simdesc, c.visibilityflag);
    END IF;
 END IF;
  END LOOP;
END LOOP;
--do not RETURN the duplicated rows.
OPEN a_cursor FOR SELECT DISTINCT lfn, production, configname, configversion,eventtypeid, filetype, processingpass,conditiondescription, visibilityflag FROM table(lfnmeta);
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getfilesforguid(v_guid VARCHAR2) RETURN VARCHAR2 IS
RESULT varchar2(256);
BEGIN
SELECT filename INTO RESULT FROM files WHERE guid = v_guid;
RETURN RESULT;
EXCEPTION
   WHEN no_data_found THEN
    raise_application_error(-20088, 'The file which corresponds to GUID: ' || v_guid || ' does not exists in the bookkeeping database!');
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updatedataqualityflag(v_qualityid NUMBER, lfns varchararray )
IS
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  UPDATE files SET inserttimestamp = sys_extract_utc(systimestamp), qualityid = v_qualityid WHERE filename = lfns(i);
END LOOP;
COMMIT;
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkcheckfiles(lfns varchararray,  a_cursor OUT udt_refcursor)
IS
lfnmeta metadata_table := metadata_table();
n integer := 0;
FOUND NUMBER := 0;
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  SELECT count(filename) INTO FOUND FROM files WHERE filename = lfns(i);
  IF FOUND = 0 THEN
    lfnmeta.extend;
    n:=n + 1;
    lfnmeta (n):=metadata0bj(lfns(i), NULL,NULL,NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
  END IF;
END LOOP;
OPEN a_cursor FOR SELECT filename FROM table(lfnmeta);
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkupdatereplicarow(v_replica VARCHAR2, lfns varchararray)
IS
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
 UPDATE files SET inserttimestamp = sys_extract_utc(systimestamp),gotreplica = v_replica WHERE filename = lfns(i);
 COMMIT;
END LOOP;
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkgettypevesrsion(lfns varchararray, a_cursor OUT udt_refcursor)
IS
lfnmeta metadata_table := metadata_table();
n integer := 0;
FOUND NUMBER := 0;
ftype varchar2(256);

BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  SELECT count(ftype.version) INTO FOUND FROM files f, filetypes ftype WHERE f.filetypeid = ftype.filetypeid AND f.filename = lfns(i);
  IF FOUND > 0 THEN
    SELECT ftype.version INTO ftype FROM files f, filetypes ftype WHERE f.filetypeid = ftype.filetypeid AND f.filename = lfns(i);
    lfnmeta.extend;
    n:=n + 1;
    lfnmeta (n):=metadata0bj(lfns(i), ftype ,NULL,NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL);
  END IF;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(lfnmeta);
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE setobsolete
IS
BEGIN
UPDATE steps SET usable = 'Obsolete' WHERE stepid IN (SELECT stepid FROM steps WHERE trunc(inserttimestamps) <= add_months(sysdate + 1,-12) AND usable != 'Obsolete');
COMMIT;
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkjobinfo(lfns varchararray, a_cursor OUT udt_refcursor)
IS
/*create or replace  type jobMetadata is object(lfn VARCHAR2(256),
  DiracJobId                  NUMBER,
  DiracVersion                VARCHAR2(256),
  EventInputStat              NUMBER,
  ExecTime                    FLOAT,
  FirstEventNumber            NUMBER,
  Location                    VARCHAR2(256),
  Name                        VARCHAR2(256),
  NumberOfEvents              NUMBER,
  StatisticsRequested         NUMBER,
  WNCPUPower                  VARCHAR2(256),
  CPUTime                     FLOAT,
  WNCache                     VARCHAR2(256),
  WNMemory                    VARCHAR2(256),
  WNModel                     VARCHAR2(256),
  WORKERNODE                  VARCHAR2(256),
  WNCPUHS06                   FLOAT,
  jobid                       NUMBER,
  totalLuminosity             NUMBER,
  production                  NUMBER,
  ProgramName                 VARCHAR2(256),
  ProgramVersion              VARCHAR2(256),
  WNMJFHS06                   FLOAT);
create or replace
type bulk_collect_jobMetadata is table of jobMetadata;
*/
n integer := 0;
jobmeta bulk_collect_jobmetadata := bulk_collect_jobmetadata();
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  FOR c IN (SELECT  jobs.diracjobid, jobs.diracversion, jobs.eventinputstat, jobs.exectime, jobs.firsteventnumber,jobs.location,  jobs.name, jobs.numberofevents,
                 jobs.statisticsrequested, jobs.wncpupower, jobs.cputime, jobs.wncache, jobs.wnmemory, jobs.wnmodel, jobs.workernode, jobs.wncpuhs06, jobs.jobid, jobs.totalluminosity, jobs.production, jobs.programname, jobs.programversion, jobs.wnmjfhs06
   FROM jobs,files WHERE files.jobid = jobs.jobid AND  files.filename = lfns(i)) LOOP
     jobmeta.extend;
     n:=n + 1;
    jobmeta (n):= jobmetadata(lfns(i), c.diracjobid, c.diracversion, c.eventinputstat, c.exectime, c.firsteventnumber,c.location,  c.name, c.numberofevents,
                 c.statisticsrequested, c.wncpupower, c.cputime, c.wncache, c.wnmemory, c.wnmodel, c.workernode, c.wncpuhs06, c.jobid, c.totalluminosity, c.production, c.programname, c.programversion, c.wnmjfhs06);
  END LOOP;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(jobmeta);
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkjobinfoforjobname(jobnames varchararray, a_cursor OUT udt_refcursor)
IS
n integer := 0;
jobmeta bulk_collect_jobmetadata := bulk_collect_jobmetadata();
BEGIN
FOR i IN jobnames.first .. jobnames.last LOOP
  FOR c IN (SELECT  jobs.diracjobid, jobs.diracversion, jobs.eventinputstat, jobs.exectime, jobs.firsteventnumber,jobs.location,  jobs.name, jobs.numberofevents,
                 jobs.statisticsrequested, jobs.wncpupower, jobs.cputime, jobs.wncache, jobs.wnmemory, jobs.wnmodel, jobs.workernode, jobs.wncpuhs06, jobs.jobid, jobs.totalluminosity, jobs.production, jobs.programname, jobs.programversion,wnmjfhs06
   FROM jobs,files WHERE files.jobid = jobs.jobid AND  jobs.name = jobnames(i)) LOOP
     jobmeta.extend;
     n:=n + 1;
    jobmeta (n):= jobmetadata(jobnames(i), c.diracjobid, c.diracversion, c.eventinputstat, c.exectime, c.firsteventnumber,c.location,  c.name, c.numberofevents,
                 c.statisticsrequested, c.wncpupower, c.cputime, c.wncache, c.wnmemory, c.wnmodel, c.workernode, c.wncpuhs06, c.jobid, c.totalluminosity, c.production, c.programname, c.programversion, c.wnmjfhs06);
  END LOOP;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(jobmeta);
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkjobinfoforjobid(jobids numberarray, a_cursor OUT udt_refcursor)
IS
n integer := 0;
jobmeta bulk_collect_jobmetadata := bulk_collect_jobmetadata();
BEGIN
FOR i IN jobids.first .. jobids.last LOOP
  FOR c IN (SELECT  DISTINCT jobs.diracjobid, jobs.diracversion, jobs.eventinputstat, jobs.exectime, jobs.firsteventnumber,jobs.location,  jobs.name, jobs.numberofevents,
                 jobs.statisticsrequested, jobs.wncpupower, jobs.cputime, jobs.wncache, jobs.wnmemory, jobs.wnmodel, jobs.workernode, jobs.wncpuhs06, jobs.jobid, jobs.totalluminosity, jobs.production, jobs.programname, jobs.programversion, wnmjfhs06
   FROM jobs,files WHERE files.jobid = jobs.jobid AND  jobs.diracjobid = jobids(i) ORDER BY jobs.name) LOOP
     jobmeta.extend;
     n:=n + 1;
    jobmeta (n):= jobmetadata(jobids(i), c.diracjobid, c.diracversion, c.eventinputstat, c.exectime, c.firsteventnumber,c.location,  c.name, c.numberofevents,
                 c.statisticsrequested, c.wncpupower, c.cputime, c.wncache, c.wnmemory, c.wnmodel, c.workernode, c.wncpuhs06, c.jobid, c.totalluminosity, c.production, c.programname, c.programversion, c.wnmjfhs06);
  END LOOP;
END LOOP;
OPEN a_cursor FOR SELECT * FROM table(jobmeta);
END;

PROCEDURE insertrunstatus(v_runnumber NUMBER, v_jobid NUMBER, v_finished VARCHAR2)IS
nbrows NUMBER;
BEGIN
    nbrows := 0;
    SELECT count(*) INTO nbrows FROM runstatus WHERE runnumber = v_runnumber;
    IF nbrows = 0 THEN
      INSERT INTO runstatus(
         runnumber,
         jobid,
         finished
         ) VALUES(
                v_runnumber,
                v_jobid,
                v_finished);
   COMMIT;
   END IF;
  EXCEPTION
  WHEN dup_val_on_index THEN
   UPDATE runstatus SET finished = v_finished WHERE runnumber = v_runnumber AND jobid = v_jobid;
   COMMIT;
  END;

PROCEDURE setrunfinished(
  v_runnumber NUMBER,
  isfinished VARCHAR2
 )IS
 BEGIN
  UPDATE runstatus SET finished = isfinished WHERE runnumber = v_runnumber;
 IF SQL % rowcount = 0 THEN
  raise_application_error(-20088, 'The ' || v_runnumber || ' does not exists in the bookkeeping database!');
 ELSE
   COMMIT;
 END IF;
END;

PROCEDURE bulkupdatefilemetadata(files bigvarchararray) IS
n NUMBER;
BEGIN
FOR i IN files.first .. files.last LOOP
   EXECUTE IMMEDIATE files(i);
END LOOP;
END;

PROCEDURE updateluminosity(v_runnumber NUMBER)IS
BEGIN
FOR c IN (SELECT f.filename, f.luminosity, f.fileid FROM jobs j, files f WHERE j.jobid = f.jobid AND j.runnumber = v_runnumber AND j.production < 0) LOOP
  updatedesluminosity(c.fileid);
END LOOP;
END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updatedesluminosity(v_fileid NUMBER)IS
lumi NUMBER;
BEGIN
IF v_fileid = 0 THEN
  RETURN;
END IF;
FOR c IN (
  SELECT
    f.filename,
    f.fileid,
    j.jobid
  FROM
    jobs j,
    files f,
    inputfiles i,
    filetypes ft
  WHERE
    ft.filetypeid = f.filetypeid AND
    ft.name != 'LOG' AND
    j.jobid = f.jobid AND
    j.jobid = i.jobid AND
    i.fileid = v_fileid
  ) LOOP
    SELECT sum(f.luminosity) INTO lumi
    FROM inputfiles i, files f
    WHERE
      f.fileid = i.fileid AND
      i.jobid = c.jobid;
  IF lumi > 0 THEN
    --dbms_output.put_line('update files set luminosity=' || lumi || ' WHERE filename='||c.filename);
    UPDATE files
    SET luminosity = lumi
    WHERE fileid = c.fileid;
    updatedesluminosity(c.fileid);
  END IF;
END LOOP;
END;

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE getfiledesjobid (
  v_filename VARCHAR2,
  a_cursor   OUT udt_refcursor
 ) IS
 BEGIN
    OPEN a_cursor FOR
      SELECT i.jobid FROM inputfiles i, files f WHERE i.fileid = f.fileid AND f.filename = v_filename;
 END;
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getproducedevents(v_prodid NUMBER) RETURN NUMBER
IS
retval NUMBER := 0;
BEGIN
SELECT sum(files.eventstat) INTO retval
  FROM files,
       jobs,
       ( SELECT
           stepscontainer.production,
           steps.stepid
         FROM
           stepscontainer,
           steps
         WHERE
            stepscontainer.stepid = steps.stepid AND
            stepscontainer.production = v_prodid AND
            stepscontainer.step = ( SELECT max(step)
                                    FROM stepscontainer
                                    WHERE stepscontainer.production = v_prodid
                                  )
      ) firsts
  WHERE jobs.jobid = files.jobid AND
        jobs.production = firsts.production AND
        jobs.stepid = firsts.stepid;
RETURN retval;
EXCEPTION
  WHEN others THEN
    raise_application_error(-20005, 'error found during the event NUMBER calculation');
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE bulkgetidsfromfiles(lfns varchararray,  a_cursor OUT udt_refcursor)
IS
lfnmeta metadata_table := metadata_table();
n integer := 0;
fileid NUMBER := 0;
filetypeid NUMBER := 0;
jobid NUMBER := 0;
BEGIN
FOR i IN lfns.first .. lfns.last LOOP
  BEGIN
    SELECT fileid, jobid, filetypeid INTO fileid, jobid, filetypeid FROM files WHERE filename = lfns(i);
    lfnmeta.extend;
    n:=n + 1;
    lfnmeta(n):=metadata0bj(lfns(i), NULL,NULL,NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, jobid,NULL, NULL, NULL, NULL, NULL, fileid,filetypeid);
  EXCEPTION WHEN no_data_found THEN
         NULL;
  END;
 END LOOP;
OPEN a_cursor FOR SELECT filename, jobid, fileid, filetypeid FROM table(lfnmeta);
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertprodnoutputftypes(
  v_production NUMBER,
  v_stepid NUMBER,
  v_filetypeid NUMBER,
  v_visible char,
  v_eventtype NUMBER
)IS
BEGIN
  INSERT INTO productionoutputfiles(production, stepid, filetypeid, visible, eventtypeid)
  VALUES(v_production,v_stepid, v_filetypeid, v_visible,v_eventtype);
  COMMIT;
EXCEPTION
  WHEN dup_val_on_index THEN
    dbms_output.put_line ('EXISTS:' || v_production || '->' || v_stepid || '->' || v_filetypeid || '->' || v_visible || '->' || v_eventtype);
    --NOT: If the production is already in the table, we only change the step!!!
    UPDATE productionoutputfiles SET stepid = v_stepid WHERE production = v_production AND filetypeid = v_filetypeid AND visible = v_visible AND eventtypeid = v_eventtype;
    COMMIT;
END;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
FUNCTION getjobidwithoutreplicacheck (
  v_filename varchar2
) RETURN number
  IS
  jid number;
  BEGIN
    SELECT jobs.jobid INTO jid
    FROM files, jobs
    WHERE
      files.jobid = jobs.jobid AND
      files.filename = v_filename;
    RETURN (jid);
    EXCEPTION WHEN others THEN
  RETURN 0;
  END;
END;
/
