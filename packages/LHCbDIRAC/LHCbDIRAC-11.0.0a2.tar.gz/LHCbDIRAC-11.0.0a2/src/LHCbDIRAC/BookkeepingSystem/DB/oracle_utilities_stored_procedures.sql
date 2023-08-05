/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges AND immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

CREATE OR REPLACE PACKAGE bkutilities AS
  TYPE numberarray IS TABLE OF NUMBER INDEX BY pls_integer;

  PROCEDURE updatenbevt(v_production NUMBER);
  PROCEDURE updatejobnbofevt(v_jobid NUMBER);
  PROCEDURE updateeventinputstat(v_production NUMBER, fixstripping BOOLEAN);
  PROCEDURE updatejobevtinpstat(v_jobid NUMBER, fixstripping BOOLEAN);
  PROCEDURE destroydatasets;
  PROCEDURE insertprotopordoutput(v_production NUMBER);
  PROCEDURE updateprotopordoutput(v_production NUMBER);
  PROCEDURE updateprodoutputfiles;
  PROCEDURE updateprodrunview;
END;
 /

 CREATE OR REPLACE PACKAGE BODY bkutilities AS
PROCEDURE updatenbevt(
  v_production NUMBER
) IS
BEGIN
/* It updates the NUMBER of events for a given production*/
  FOR c IN (SELECT j.jobid
            FROM jobs j
            WHERE j.production = v_production)
   LOOP
    updatejobnbofevt(c.jobid);
   END LOOP;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updatejobnbofevt(v_jobid NUMBER)IS
sumevt NUMBER;
BEGIN
/* UPDATE the NUMBER of event for a given job.
The NUMBER of events is the sum of the eventstat of the input files */
SELECT sum(f.eventstat) INTO sumevt
  FROM jobs j,
       files f,
       inputfiles i
   WHERE
      i.jobid = v_jobid AND
      i.fileid = f.fileid AND
      f.jobid = j.jobid  AND
      f.eventstat IS NOT NULL AND
      f.filetypeid NOT IN (SELECT filetypeid
                           FROM filetypes
                           WHERE name = 'RAW');
  IF sumevt > 0 THEN
    UPDATE jobs SET numberofevents = sumevt WHERE jobid = v_jobid;
  --for c in (SELECT j.jobid
  --            FROM jobs j, files f, inputfiles i
  --              WHERE
  --                i.jobid=v_jobid AND
  --                i.fileid=f.fileid AND
  --                f.jobid=j.jobid AND
  --                f.eventstat IS NOT NULL AND f.filetypeid not in (SELECT filetypeid FROM filetypes WHERE name='RAW'))
  --LOOP
 --   updateJobNbofevt(c.jobid);
  --END LOOP;
  END IF;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updateeventinputstat(
  v_production NUMBER,
  fixstripping BOOLEAN
) IS
BEGIN
/* It updates the eventinputstat for a given production.
If the fixstripping is true, the value of the eventinputstat is calculated using the
eventinputstat for the input jobs, othetwise we use the eventstat for the input files.
for example: If we want to fix the eventinputstat of reconstructed files (FULL.DST), fixstripping equal False*/
  IF fixstripping = TRUE THEN
    FOR c IN (SELECT j.jobid
              FROM jobs j,
                   files f
              WHERE j.jobid = f.jobid
                AND j.production = v_production
              )
      LOOP
        updatejobevtinpstat(c.jobid, fixstripping);
      END LOOP;
  ELSE
    FOR c IN (SELECT j.jobid
              FROM jobs j,
                   files f
              WHERE j.jobid = f.jobid AND
                    j.production = v_production AND
                    f.gotreplica = 'Yes' AND
                    f.visibilityflag = 'Y')
      LOOP
        updatejobevtinpstat(c.jobid, fixstripping);
      END LOOP;
  END IF;
END;

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updatejobevtinpstat(
  v_jobid NUMBER,
  fixstripping BOOLEAN
) IS
/*It updates the eventinputstat for a given job */
sumevtinp NUMBER;
BEGIN
  IF fixstripping = TRUE THEN
    SELECT sum(j.eventinputstat) INTO sumevtinp
    FROM jobs j,
         files f,
         inputfiles i
    WHERE i.jobid = v_jobid AND
          i.fileid = f.fileid AND
          f.jobid = j.jobid;
  ELSE
    SELECT sum(f.eventstat) INTO sumevtinp
    FROM jobs j,
         files f,
         inputfiles i
    WHERE i.jobid = v_jobid AND
          i.fileid = f.fileid AND
          f.jobid = j.jobid;
  END IF;
  IF sumevtinp > 0 THEN
    UPDATE jobs SET eventinputstat = sumevtinp WHERE jobid = v_jobid;
  END IF;
END;
PROCEDURE destroydatasets IS
runsteps numberarray;
productionsteps numberarray;
i NUMBER;
v_production NUMBER;
BEGIN
    v_production:=2; /*this must be same as in the integration test: LHCbDIRAC/tests/Integration/BookkeepingSystem/Test_Bookkeeping.py*/
    /*DELETE run data*/
    DELETE productionscontainer WHERE production = 3;
    DELETE stepscontainer WHERE production = 3;
    DELETE productionscontainer WHERE production = -1122;
    i:=1;/*before we DELETE the steps FROM the stepcontainer table, the steps must be saved*/
    FOR step IN (SELECT stepid
                 FROM stepscontainer
                 WHERE production = -1122) LOOP
      runsteps(i):=step.stepid;
      i:=i + 1;
      dbms_output.put_line('run Step:' || step.stepid);
    END LOOP;
    DELETE stepscontainer WHERE production = -1122;
    DELETE runstatus WHERE runnumber = 1122;
    DELETE files WHERE jobid IN (SELECT jobid FROM jobs WHERE runnumber = 1122);
    DELETE jobs WHERE runnumber = 1122;
    FOR i IN 1 .. runsteps.count LOOP
      dbms_output.put_line('run step DELETE:' || runsteps(i));
      DELETE steps WHERE stepid = runsteps(i);
    END LOOP;
    /* DELETE production data */
    i:=1;
    /*before we DELETE the steps FROM the stepcontainer table, the steps must be saved*/
    FOR step IN (SELECT stepid FROM stepscontainer WHERE production = v_production) LOOP
      productionsteps(i):=step.stepid;
      i:=i + 1;
      dbms_output.put_line('production step:' || step.stepid);
    END LOOP;
    DELETE productionscontainer WHERE production = v_production;
    DELETE stepscontainer WHERE production = v_production;
    DELETE files WHERE jobid IN (SELECT jobid FROM jobs WHERE production = v_production);
    DELETE jobs WHERE production = v_production;
    FOR i IN 1 .. productionsteps.count LOOP
      dbms_output.put_line('production step DELETE:' || productionsteps(i));
      DELETE steps WHERE stepid = productionsteps(i);
    END LOOP;
    COMMIT;
END;


---------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE insertprotopordoutput(
  v_production NUMBER
) IS
BEGIN
  FOR prod IN(SELECT j.production,
                     j.stepid,
                     f.eventtypeid,
                     f.filetypeid,
                     f.gotreplica,
                     f.visibilityflag
              FROM jobs j,
                   files f
              WHERE j.jobid = f.jobid AND
                    j.production = v_production AND
                    f.gotreplica IS NOT NULL AND
                    f.filetypeid NOT IN(9,17)
              GROUP BY j.production,
                       j.stepid,
                       f.eventtypeid,
                       f.filetypeid,
                       f.gotreplica,
                       f.visibilityflag
              ORDER BY f.gotreplica,
                       f.visibilityflag
              ASC) LOOP
    dbms_output.put_line('Inserting -> Production:' || prod.production || '->step:' || prod.stepid || '->file type:' || prod.filetypeid || '->visible:' || prod.visibilityflag || '->event type:' || prod.eventtypeid || '->replica flag:' || prod.gotreplica);
    INSERT INTO productionoutputfiles(production,
                                      stepid,
                                      filetypeid,
                                      visible,
                                      eventtypeid,
                                      gotreplica)
           VALUES(prod.production,
                  prod.stepid,
                  prod.filetypeid,
                  prod.visibilityflag,
                  prod.eventtypeid,
                  prod.gotreplica);
  END LOOP;
END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updateprotopordoutput(
  v_production NUMBER
) IS
nb NUMBER;
BEGIN
  FOR prod IN(SELECT j.production,
                     j.stepid,
                     f.eventtypeid,
                     f.filetypeid,
                     f.gotreplica,
                     f.visibilityflag
              FROM jobs j,
                   files f
              WHERE j.jobid = f.jobid AND
                    j.production = v_production AND
                    f.gotreplica IS NOT NULL AND
                    f.filetypeid NOT IN(9,17)
              GROUP BY j.production,
                       j.stepid,
                       f.eventtypeid,
                       f.filetypeid,
                       f.gotreplica,
                       f.visibilityflag
              ORDER BY f.gotreplica,
                       f.visibilityflag
              ASC) LOOP
    SELECT count(*) INTO nb FROM productionoutputfiles WHERE production = prod.production AND eventtypeid = prod.eventtypeid AND filetypeid = prod.filetypeid AND stepid = prod.stepid AND visible = prod.visibilityflag AND gotreplica = prod.gotreplica;
    dbms_output.put_line('Try UPDATE -> Production:' || prod.production || '->step:' || prod.stepid || '->file type:' || prod.filetypeid || '->visible:' || prod.visibilityflag || '->event type:' || prod.eventtypeid || '->replica flag:' || prod.gotreplica);
    IF nb = 0 THEN -- we want to UPDATE only the row, which has modified...
      -- we have to see which rows can be updated
      FOR toupdate IN (SELECT * FROM (SELECT production,
                                             stepid,
                                             eventtypeid,
                                             filetypeid,
                                             gotreplica,
                                             visible AS visibilityflag
                                      FROM productionoutputfiles
                                      WHERE production = v_production)
                         MINUS
                       SELECT j.production,
                              j.stepid,
                              f.eventtypeid,
                              f.filetypeid,
                              f.gotreplica,
                              f.visibilityflag
                       FROM jobs j,
                            files f
                       WHERE j.jobid = f.jobid AND
                             j.production = v_production AND
                             f.gotreplica IS NOT NULL AND
                             f.filetypeid NOT IN(9,17)
                       GROUP BY j.production,
                                j.stepid,
                                f.eventtypeid,
                                f.filetypeid,
                                f.gotreplica,
                                f.visibilityflag) LOOP
        dbms_output.put_line('Update -> Production:' || prod.production || '->step:' || prod.stepid || '->file type:' || prod.filetypeid || '->visible:' || prod.visibilityflag || '->event type:' || prod.eventtypeid || '->replica flag:' || prod.gotreplica);
        UPDATE productionoutputfiles SET visible = prod.visibilityflag, gotreplica = prod.gotreplica WHERE production = prod.production AND eventtypeid = prod.eventtypeid AND filetypeid = prod.filetypeid AND stepid = prod.stepid AND visible = toupdate.visibilityflag AND gotreplica = toupdate.gotreplica;
      END LOOP;
    END IF;
  END LOOP;
END;


---------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updateprodoutputfiles IS
nbrows NUMBER;
nbrowstobeprocessed NUMBER;
nb NUMBER;
err_num NUMBER;
err_msg varchar2(1000);
BEGIN
--FOR toprod in (SELECT distinct j.production FROM jobs j, files f WHERE f.jobid=j.jobid AND j.production>0 AND f.gotreplica='Yes') LOOP
  FOR c IN (SELECT j.production
            FROM jobs j,
                 files f
            WHERE f.inserttimestamp >= systimestamp - 1 AND
                  j.jobid = f.jobid AND
                  --j.production=toprod.production AND
                  f.gotreplica IS NOT NULL AND
                  f.filetypeid NOT IN(9,17) GROUP BY j.production) LOOP
    SELECT count(*) INTO nbrows
    FROM  productionoutputfiles
    WHERE production = c.production;
    SELECT count(*) INTO nbrowstobeprocessed
    FROM (SELECT j.production,
                 j.stepid,
                 f.eventtypeid,
                 f.filetypeid,
                 f.gotreplica,
                 f.visibilityflag
          FROM jobs j, files f
          WHERE j.jobid = f.jobid AND
                j.production = c.production AND
                f.gotreplica IS NOT NULL AND
                f.filetypeid NOT IN(9,17)
          GROUP BY j.production,
                   j.stepid,
                   f.eventtypeid,
                   f.filetypeid,
                   f.gotreplica,
                   f.visibilityflag
          ORDER BY f.gotreplica,
                   f.visibilityflag
         );
    IF nbrows > 0 THEN
      IF nbrows = nbrowstobeprocessed THEN
        updateprotopordoutput(c.production);
      elsif nbrows > nbrowstobeprocessed THEN
        updateprotopordoutput(c.production);
        FOR todelete IN (SELECT * FROM (SELECT production,
                                               stepid,
                                               eventtypeid,
                                               filetypeid,
                                               gotreplica,
                                               visible AS visibilityflag
                                        FROM productionoutputfiles
                                        WHERE production = c.production)
                           MINUS
                         SELECT j.production,
                                j.stepid,
                                f.eventtypeid,
                                f.filetypeid,
                                f.gotreplica,
                                f.visibilityflag
                         FROM jobs j,
                              files f
                         WHERE j.jobid = f.jobid AND
                               j.production = c.production AND
                               f.gotreplica IS NOT NULL AND
                               f.filetypeid NOT IN(9,17)
                         GROUP BY j.production,
                                  j.stepid,
                                  f.eventtypeid,
                                  f.filetypeid,
                                  f.gotreplica,
                                  f.visibilityflag) LOOP
          dbms_output.put_line('Delete -> Production:' || todelete.production || '->step:' || todelete.stepid || '->file type:' || todelete.filetypeid || '->visible:' || todelete.visibilityflag || '->event type:' || todelete.eventtypeid || '->replica flag:' || todelete.gotreplica);
          DELETE productionoutputfiles WHERE production = todelete.production AND eventtypeid = todelete.eventtypeid AND filetypeid = todelete.filetypeid AND stepid = todelete.stepid AND visible = todelete.visibilityflag AND gotreplica = todelete.gotreplica;
      END LOOP;
      elsif nbrows < nbrowstobeprocessed THEN
        updateprotopordoutput(c.production);
        FOR toinsert IN(SELECT * FROM (SELECT j.production,j.stepid, f.eventtypeid, f.filetypeid, f.gotreplica, f.visibilityflag FROM jobs j, files f WHERE
            j.jobid = f.jobid AND
            j.production = c.production AND
            f.gotreplica IS NOT NULL AND
            f.filetypeid NOT IN(9,17) GROUP BY j.production, j.stepid, f.eventtypeid, f.filetypeid, f.gotreplica, f.visibilityflag ORDER BY f.gotreplica,f.visibilityflag)  MINUS
                   SELECT production, stepid, eventtypeid, filetypeid, gotreplica, visible AS visibilityflag FROM productionoutputfiles WHERE production = c.production) LOOP
                dbms_output.put_line('Inserting -> Production:' || toinsert.production || '->step:' || toinsert.stepid || '->file type:' || toinsert.filetypeid || '->visible:' || toinsert.visibilityflag || '->event type:' || toinsert.eventtypeid || '->replica flag:' || toinsert.gotreplica);
                INSERT INTO productionoutputfiles(production, stepid, filetypeid, visible, eventtypeid,gotreplica)VALUES(toinsert.production,toinsert.stepid, toinsert.filetypeid, toinsert.visibilityflag,toinsert.eventtypeid, toinsert.gotreplica);
        END LOOP;
      END IF;
    ELSE
        insertprotopordoutput(c.production);
    END IF;
    COMMIT;
  END LOOP;
--END LOOP;
  EXCEPTION
  WHEN others THEN
    err_num := SQLCODE;
    err_msg := substr(sqlerrm, 1, 1000);
    utl_mail.send(sender => 'lhcb-geoc@cern.ch',
            recipients => 'lhcb-bookkeeping@cern.ch',
            subject    => 'Failed to UPDATE productionoutputfiles',
            message    => 'ERROR NUMBER:' || err_num || ' error message:' || err_msg || ' More info: https://lhcb-dirac.readthedocs.io/en/latest/AdministratorGuide/Bookkeeping/administrate_oracle.html#automatic-updating-of-the-productionoutputfiles');
END;

---------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROCEDURE updateprodrunview IS
err_num NUMBER;
err_msg varchar2(1000);
BEGIN
-- get the modified production list
 FOR prod IN (SELECT j.production FROM jobs j, files f WHERE
                f.inserttimestamp >= systimestamp - 1 AND
                j.jobid = f.jobid AND
                f.gotreplica IS NOT NULL AND
                f.filetypeid NOT IN(9,17) GROUP BY j.production)
  LOOP
    DELETE prodrunview WHERE production = prod.production;
    FOR insertprod IN (SELECT j.production, j.runnumber FROM jobs j, files f WHERE j.jobid = f.jobid AND j.production = prod.production AND f.gotreplica = 'Yes'
                                 AND f.visibilityflag = 'Y' AND j.runnumber IS NOT NULL GROUP BY j.production,j.runnumber)
    LOOP
      INSERT INTO prodrunview(production,runnumber)VALUES(insertprod.production,insertprod.runnumber);
    END LOOP;
    COMMIT;
  END LOOP;
  EXCEPTION
    WHEN others THEN
        err_num := SQLCODE;
        err_msg := substr(sqlerrm, 1, 1000);
        utl_mail.send(sender => 'lhcb-geoc@cern.ch',
                recipients => 'lhcb-bookkeeping@cern.ch',
                subject    => 'Failed to update prodrunview',
                message    => 'ERROR number:' || err_num || ' error message:' || err_msg || ' More info: https://lhcb-dirac.readthedocs.io/en/latest/AdministratorGuide/Bookkeeping/administrate_oracle.html#automatic-updating-of-the-prodrunview');
END;
END;
 /
