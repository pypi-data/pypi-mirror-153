/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

-- Bookkeeping DB schema cleaner (Oracle)

SET serveroutput ON

--- DROP package BOOKKEEPINGORACLEDB
BEGIN
  EXECUTE IMMEDIATE 'DROP PACKAGE BOOKKEEPINGORACLEDB';
EXCEPTION
  WHEN others THEN
    IF SQLCODE != -4043 THEN
      RAISE;
    END IF;
END;
 /

 --- DROP package BKUTILITIES
BEGIN
  EXECUTE IMMEDIATE 'DROP PACKAGE BKUTILITIES';
EXCEPTION
  WHEN others THEN
    IF SQLCODE != -4043 THEN
      RAISE;
    END IF;
END;
 /

 --- DROP DBMS_SCHEDULER.JOB
BEGIN
  dbms_scheduler.drop_job(job_name => 'produpdatejob');
EXCEPTION
  WHEN others THEN
    IF SQLCODE != -27475 THEN
      RAISE;
    END IF;
END;
 /

 --- DROP DBMS_SCHEDULER.JOB
BEGIN
  dbms_scheduler.drop_job(job_name => 'prodrunupdatejob');
EXCEPTION
  WHEN others THEN
    IF SQLCODE != -27475 THEN
      RAISE;
    END IF;
END;
 /


 --- DROP TABLEs
DECLARE table_names sys.dbms_debug_vc2coll
  := sys.dbms_debug_vc2coll(
                            'applications',
                            'inputfiles',
                            'files',
                            'tags',
                            'stepscontainer',
                            'newrunquality',
                            'productionoutputfiles',
                            'filetypes',
                            'dataquality',
                            'eventtypes',
                            'runtimeprojects',
                            'runstatus',
                            'stepstmp',
                            'jobs',
                            'steps',
                            'productionscontainer',
                            'processing',
                            'configurations',
                            'simulationconditions',
                            'data_taking_conditions',
                            'prodrunview'
                            );
BEGIN
  FOR tn IN table_names.first..table_names.last
  LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE ' || table_names(tn);
    EXCEPTION
      WHEN others THEN
        IF SQLCODE != -942 THEN
          RAISE;
        END IF;
    END;
  END LOOP;
END;
 /


 --- DROP SEQUENCEs
DECLARE type_names sys.dbms_debug_vc2coll
  := sys.dbms_debug_vc2coll('applications_index_seq',
                            'configurationid_seq',
                            'fileid_seq',
                            'groupid_seq',
                            'jobid_seq',
                            'pass_index_seq',
                            'production_seq',
                            'simulationcondid_seq',
                            'tags_index_seq');
BEGIN
  FOR tn IN type_names.first..type_names.last
  LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP SEQUENCE ' || type_names(tn);
    EXCEPTION
      WHEN others THEN
        IF SQLCODE != -2289 THEN
          RAISE;
        END IF;
    END;
  END LOOP;
END;
 /


 --- DROP TYPEs
DECLARE type_names sys.dbms_debug_vc2coll
  := sys.dbms_debug_vc2coll('bulk_collect_directoryMetadata',
                            'bulk_collect_directoryMet_new',
                            'bulk_collect_jobMetadata',
                            'bulk_collect_run_quality_evt',
                            'directoryMetadata_new',
                            'directoryMetadata',
                            'filetypesARRAY',
                            'ftype',
                            'jobMetadata',
                            'lists',
                            'metadata_table',
                            'metadata0bj',
                            'run_proc_table',
                            'runnb_proc',
                            'runnb_quality_eventtype',
                            'step_table',
                            'stepobj'
);
BEGIN
  FOR tn IN type_names.first..type_names.last
  LOOP
    BEGIN
      EXECUTE IMMEDIATE 'DROP TYPE ' || type_names(tn);
    EXCEPTION
      WHEN others THEN
        IF SQLCODE != -4043 THEN
          RAISE;
        END IF;
    END;
  END LOOP;
END;
 /
