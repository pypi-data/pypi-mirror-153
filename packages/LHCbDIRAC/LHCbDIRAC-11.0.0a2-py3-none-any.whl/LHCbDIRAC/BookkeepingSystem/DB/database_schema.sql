/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

-- Bookkeeping DB schema (Oracle)


CREATE OR REPLACE TYPE stepobj IS object(
    stepid              NUMBER,
    stepname            varchar2(256),
    applicationname     varchar2(128),
    applicationversion  varchar2(128),
    optionfiles         varchar2(1000),
    dddb                varchar2(256),
    conddb              varchar2(256),
    extrapackages       varchar2(256),
    visible             char(1),
    processingpass      varchar2(256),
    usable              varchar2(10),
    dqtag               varchar2(256),
    optionsformat       varchar2(30),
    ismulticore         char(1),
    systemconfig        varchar2(256),
    mctck               varchar2(256),
    rstepid             NUMBER,
    rstepname           varchar2(256),
    rapplicationname    varchar2(128),
    rapplicationversion varchar2(128),
    roptionfiles        varchar2(1000),
    rdddb               varchar2(256),
    rconddb             varchar2(256),
    rextrapackages      varchar2(256),
    rvisible            char(1),
    rprocessingpass     varchar2(256),
    rusable             varchar2(10),
    rdqtag              varchar2(256),
    roptionsformat      varchar2(30),
    rismulticore        char(1),
    rsystemconfig       varchar2(256),
    rmctck              varchar2(256)
);
 /

CREATE OR REPLACE TYPE step_table IS TABLE OF stepobj;
 /

CREATE OR REPLACE TYPE runnb_quality_eventtype IS object(
    runnumber NUMBER,
    dataqualityflag varchar2(256),
    eventtypeid NUMBER
);
 /

CREATE OR REPLACE TYPE runnb_proc IS object(
    runnumber NUMBER,
    processingpass varchar2(256)
);
 /

CREATE OR REPLACE TYPE run_proc_table IS TABLE OF runnb_proc;
 /


CREATE OR REPLACE TYPE metadata0bj IS object(
    filename        varchar2(256),
    adler32         varchar2(256),
    creationdate    timestamp(6),
    eventstat       NUMBER,
    eventtypeid     NUMBER,
    name            varchar2(256),
    gotreplica      varchar2(3),
    guid            varchar2(256),
    md5sum          varchar2(256),
    filesize        NUMBER,
    fullstat        NUMBER,
    dataqualityflag varchar2(256),
    jobid           number(38,0),
    runnumber       NUMBER,
    inserttimestamp timestamp(6),
    luminosity      NUMBER,
    instluminosity  NUMBER,
    visibilityflag  char(1),
    fileid          NUMBER,
    filetypeid      NUMBER
);
 /

CREATE OR REPLACE TYPE metadata_table IS TABLE OF metadata0bj;
 /

CREATE OR REPLACE TYPE LISTS IS TABLE OF varchar2(256);
 /

CREATE OR REPLACE TYPE jobmetadata IS object(
    lfn                         varchar2(256),
    diracjobid                  NUMBER,
    diracversion                varchar2(256),
    eventinputstat              NUMBER,
    exectime                    FLOAT,
    firsteventnumber            NUMBER,
    LOCATION                    varchar2(256),
    name                        varchar2(256),
    numberofevents              NUMBER,
    statisticsrequested         NUMBER,
    wncpupower                  varchar2(256),
    cputime                     FLOAT,
    wncache                     varchar2(256),
    wnmemory                    varchar2(256),
    wnmodel                     varchar2(256),
    workernode                  varchar2(256),
    wncpuhs06                   FLOAT,
    jobid                       number,
    totalluminosity             NUMBER,
    production                  NUMBER,
    programname                 varchar2(256),
    programversion              varchar2(256),
    wnmjfhs06                   FLOAT
);
 /

CREATE OR REPLACE TYPE ftype AS object(
    name varchar2(256),
    visible char(1)
);
 /

CREATE OR REPLACE TYPE filetypesarray IS varray(30) OF ftype;
 /

CREATE OR REPLACE TYPE directorymetadata_new IS object(
    lfn                   varchar2(256),
    production            NUMBER,
    configname            varchar2(256),
    configversion         varchar2(256),
    eventtypeid           NUMBER,
    filetype              varchar2(256),
    processingpass        varchar2(256),
    conditiondescription  varchar2(256),
    visibilityflag        char(1)
);
 /

CREATE OR REPLACE TYPE directorymetadata IS object(
    production            NUMBER,
    configname            varchar2(256),
    configversion         varchar2(256),
    eventtypeid           NUMBER,
    filetype              varchar2(256),
    processingpass        varchar2(256),
    conditiondescription  varchar2(256),
    visibilityflag        char(1)
);
 /

CREATE OR REPLACE TYPE bulk_collect_run_quality_evt IS TABLE OF runnb_quality_eventtype;
 /

CREATE OR REPLACE TYPE bulk_collect_jobmetadata IS TABLE OF jobmetadata;
 /

CREATE OR REPLACE TYPE bulk_collect_directorymetadata IS TABLE OF directorymetadata;
 /

CREATE OR REPLACE TYPE bulk_collect_directorymet_new IS TABLE OF directorymetadata_new;
 /

 CREATE SEQUENCE applications_index_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE configurationid_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE fileid_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE groupid_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE jobid_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE pass_index_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE production_seq MINVALUE -99999999999999999999999999 MAXVALUE -1 INCREMENT BY -1 START WITH -1;

CREATE SEQUENCE simulationcondid_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE SEQUENCE tags_index_seq MINVALUE 1 MAXVALUE 999999999999999999999999999 INCREMENT BY 1 START WITH 1;

CREATE GLOBAL TEMPORARY TABLE stepstmp(
    stepid              NUMBER,
    stepname            varchar2(256),
    applicationname     varchar2(128),
    applicationversion  varchar2(128),
    optionfiles         varchar2(1000),
    dddb                varchar2(256),
    conddb              varchar2(256),
    extrapackages       varchar2(256),
    visible             char(1) DEFAULT 'Y',
    processingpass      varchar2(256),
    usable              varchar2(10) DEFAULT 'Not ready',
    dqtag               varchar2(256),
    optionsformat       varchar2(30),
    ismulticore         char(1) DEFAULT 'N',
    systemconfig        varchar2(256),
    mctck               varchar2(256),
    rstepid             NUMBER,
    rstepname           varchar2(256),
    rapplicationname    varchar2(128),
    rapplicationversion varchar2(128),
    roptionfiles        varchar2(1000),
    rdddb               varchar2(256),
    rconddb             varchar2(256),
    rextrapackages      varchar2(256),
    rvisible            char(1),
    rprocessingpass     varchar2(256),
    rusable             varchar2(10),
    rdqtag              varchar2(256),
    roptionsformat      varchar2(30),
    rismulticore        char(1) DEFAULT 'N',
    rsystemconfig       varchar2(256),
    rmctck              varchar2(256)
) ON COMMIT DELETE ROWS;

---------------------------------------------------------------------------------------
CREATE TABLE tags(
    tagid           NUMBER,
    name            varchar2(256),
    tag             varchar2(256),
    inserttimestamp TIMESTAMP (6) DEFAULT systimestamp
);

---------------------------------------------------------------------------------------
CREATE TABLE processing(
    id       NUMBER,
    parentid NUMBER,
    name     varchar2(256),
    CONSTRAINT processing_pk PRIMARY KEY (id)
);

CREATE INDEX processing_pid ON processing (parentid);
CREATE INDEX processing_pid_name ON processing (parentid, name);

CREATE OR REPLACE editionable TRIGGER processing_before_insert
BEFORE INSERT
  ON processing
    FOR EACH ROW
  DECLARE
  BEGIN
  IF instr(:new.name,'/') > 0 THEN
    raise_application_error(-20001,'The processing pass name can not contain / characther!!!');
  END IF;
END;
 /
 ---------------------------------------------------------------------------------------
CREATE TABLE filetypes(
    filetypeid  NUMBER,
    description varchar2(256),
    name        varchar2(64),
    VERSION     varchar2(256),
    PRIMARY KEY (filetypeid),
    CONSTRAINT filetypes_name_version UNIQUE (name, VERSION),
    CONSTRAINT filetypes_id_name_uk UNIQUE (filetypeid, name)
);

---------------------------------------------------------------------------------------
CREATE TABLE applications(
    applicationid      NUMBER,
    applicationname    varchar2(128) NOT NULL,
    applicationversion varchar2(128) NOT NULL,
    optionfiles        varchar2(1000),
    dddb               varchar2(256),
    conddb             varchar2(256),
    extrapackages      varchar2(256),
    PRIMARY KEY (applicationid)
);

---------------------------------------------------------------------------------------
CREATE TABLE configurations(
    configurationid NUMBER,
    configname      varchar2(128) NOT NULL,
    configversion   varchar2(128) NOT NULL,
    PRIMARY KEY (configurationid),
    CONSTRAINT configuration_uk UNIQUE (configname, configversion)
);

---------------------------------------------------------------------------------------
CREATE TABLE data_taking_conditions(
    daqperiodid   NUMBER,
    description   varchar2(256),
    beamcond      varchar2(256),
    beamenergy    varchar2(256),
    magneticfield varchar2(256),
    velo          varchar2(256),
    it            varchar2(256),
    tt            varchar2(256),
    ot            varchar2(256),
    rich1         varchar2(256),
    rich2         varchar2(256),
    spd_prs       varchar2(256),
    ecal          varchar2(256),
    hcal          varchar2(256),
    muon          varchar2(256),
    l0            varchar2(256),
    hlt           varchar2(256),
    veloposition  varchar2(255),
    PRIMARY KEY (daqperiodid)
);

CREATE INDEX data_taking_condition_id_desc ON data_taking_conditions (daqperiodid, description);

---------------------------------------------------------------------------------------
CREATE TABLE dataquality(
    qualityid       NUMBER,
    dataqualityflag varchar2(256),
    PRIMARY KEY (qualityid)
);

INSERT INTO dataquality (qualityid,dataqualityflag) SELECT 1,'UNCHECKED' FROM dual WHERE NOT EXISTS (SELECT * FROM dataquality WHERE (qualityid = 1 AND dataqualityflag = 'UNCHECKED'));
INSERT INTO dataquality (qualityid,dataqualityflag) SELECT 2,'OK' FROM dual WHERE NOT EXISTS (SELECT * FROM dataquality WHERE (qualityid = 2 AND dataqualityflag = 'OK'));
INSERT INTO dataquality (qualityid,dataqualityflag) SELECT 3,'BAD' FROM dual WHERE NOT EXISTS (SELECT * FROM dataquality WHERE (qualityid = 3 AND dataqualityflag = 'BAD'));
COMMIT;

---------------------------------------------------------------------------------------
CREATE TABLE eventtypes(
    description   varchar2(256),
    eventtypeid   NUMBER,
    PRIMARY       varchar2(256),
    PRIMARY KEY (eventtypeid)
);

---------------------------------------------------------------------------------------
CREATE TABLE simulationconditions(
    simid NUMBER,
    simdescription varchar2(256),
    beamcond varchar2(256),
    beamenergy varchar2(256),
    generator varchar2(256),
    magneticfield varchar2(256),
    detectorcond varchar2(256),
    luminosity varchar2(256),
    g4settings varchar2(256) DEFAULT ' ',
    visible char(1) DEFAULT 'Y',
    inserttimestamps TIMESTAMP (6) DEFAULT sys_extract_utc(systimestamp),
    CONSTRAINT simcond_pk PRIMARY KEY (simid),
    CONSTRAINT simdesc UNIQUE (simdescription),
    CHECK (visible IN ('N','Y'))
);

---------------------------------------------------------------------------------------
CREATE TABLE productionscontainer(
    production NUMBER,
    processingid NUMBER,
    simid NUMBER,
    daqperiodid NUMBER,
    totalprocessing varchar2(256),
    configurationid NUMBER,
    CONSTRAINT pk_productionscontainer PRIMARY KEY (production),
    CONSTRAINT fk1_productionscontainer FOREIGN KEY (simid) REFERENCES simulationconditions (simid),
    CONSTRAINT fk2_productionscontainer FOREIGN KEY (daqperiodid) REFERENCES data_taking_conditions (daqperiodid),
    CONSTRAINT fk_productionscontainer_proc FOREIGN KEY (processingid) REFERENCES processing (id),
    FOREIGN KEY (configurationid) REFERENCES configurations (configurationid)
);

CREATE INDEX prodcontdaq ON productionscontainer (daqperiodid, production);
CREATE INDEX prodcontpsim ON productionscontainer (simid, production);
CREATE INDEX prodcont_proc ON productionscontainer (processingid);
CREATE INDEX prodcont_proc_prod ON productionscontainer (processingid, production);

---------------------------------------------------------------------------------------
CREATE TABLE steps(
     stepid             NUMBER,
     stepname           varchar2(256),
     applicationname    varchar2(128) NOT NULL DISABLE,
     applicationversion varchar2(128) NOT NULL DISABLE,
     optionfiles        varchar2(1000),
     dddb               varchar2(256),
     conddb             varchar2(256),
     extrapackages      varchar2(256),
     inserttimestamps   TIMESTAMP (6) DEFAULT sys_extract_utc(systimestamp),
     visible            char(1) DEFAULT 'Y',
     inputfiletypes     filetypesarray,
     outputfiletypes    filetypesarray,
     processingpass     varchar2(256),
     usable             varchar2(10) DEFAULT 'Not ready',
     dqtag              varchar2(256),
     optionsformat      varchar2(30),
     ismulticore        char(1) DEFAULT 'N',
     systemconfig       varchar2(256),
     mctck              varchar2(256),
     CHECK (visible IN ('N', 'Y')),
     PRIMARY KEY (stepid),
     CONSTRAINT s_processingpass CHECK (processingpass IS NOT NULL),
     CHECK (usable = 'Yes' OR usable = 'Not ready' OR usable = 'Obsolete'),
     CHECK (ismulticore IN ('N', 'Y'))
);

---------------------------------------------------------------------------------------
CREATE TABLE stepscontainer(
     production  NUMBER,
     stepid      NUMBER,
     step        NUMBER,
     eventtypeid NUMBER,
     CONSTRAINT pk_stepcontainer PRIMARY KEY (production, stepid),
     CONSTRAINT fk_stepcontainer FOREIGN KEY (stepid) REFERENCES steps (stepid),
     CONSTRAINT fk_stepscontainer_eventtypeid FOREIGN KEY (eventtypeid) REFERENCES eventtypes (eventtypeid)
);

CREATE INDEX steps_id ON stepscontainer (stepid);


CREATE OR REPLACE editionable TRIGGER step_insert
BEFORE INSERT ON steps
REFERENCING NEW AS NEW OLD AS OLD
FOR EACH ROW
DECLARE
BEGIN
  IF :new.dddb = 'NULL' OR :new.dddb = 'None' OR :new.dddb = '' THEN
     :new.dddb:=NULL;
  END IF;
  IF :new.conddb = 'NULL' OR :new.conddb = 'None' OR :new.conddb = '' THEN
    :new.conddb := NULL;
  END IF;
END;
 /

CREATE OR REPLACE editionable TRIGGER steps_before_insert
BEFORE INSERT ON steps
FOR EACH ROW
DECLARE
BEGIN
  IF instr(:new.processingpass,'/') > 0 THEN
    raise_application_error(-20001,'The processing pass name can not contain / characther!!!');
  END IF;
END;
 /

CREATE OR REPLACE editionable TRIGGER step_update
BEFORE UPDATE ON steps
REFERENCING NEW AS NEW OLD AS OLD
FOR EACH ROW DECLARE rowcnt NUMBER;
BEGIN
  SELECT count(*) INTO rowcnt FROM stepscontainer s WHERE s.stepid = :new.stepid;
    IF rowcnt > 0 THEN
       dbms_output.put_line('      Tag: ' || :new.visible || :old.stepname);
       :new.stepname:=:old.stepname;
       :new.applicationname:=:old.applicationname;
       :new.applicationversion:=:old.applicationversion;
       :new.optionfiles:=:old.optionfiles;
       :new.dddb:=:old.dddb;
       :new.conddb:=:old.conddb;
       :new.extrapackages:=:old.extrapackages;
       :new.visible:=:old.visible;
       :new.inputfiletypes:=:old.inputfiletypes;
       :new.outputfiletypes:=:old.outputfiletypes;
       :new.processingpass:=:old.processingpass;
       --raise_application_error (-20999,'You are not allowed to modify already used steps!');
    END IF;
END;
 /

 ---------------------------------------------------------------------------------------
CREATE TABLE jobs(
    jobid               NUMBER,
    configurationid     NUMBER,
    diracjobid          NUMBER,
    diracversion        varchar2(256),
    eventinputstat      NUMBER,
    exectime            float(126),
    firsteventnumber    NUMBER,
    geometryversion     varchar2(256),
    gridjobid           varchar2(256),
    jobend              TIMESTAMP (6),
    jobstart            TIMESTAMP (6),
    localjobid          varchar2(256),
    LOCATION            varchar2(256),
    name                varchar2(256),
    numberofevents      NUMBER,
    production          NUMBER,
    programname         varchar2(256),
    programversion      varchar2(256),
    statisticsrequested NUMBER,
    wncpupower          varchar2(256),
    cputime             float(126),
    wncache             varchar2(256),
    wnmemory            varchar2(256),
    wnmodel             varchar2(256),
    workernode          varchar2(256),
    generator           varchar2(256),
    runnumber           NUMBER,
    fillnumber          NUMBER,
    wncpuhs06           float(126) DEFAULT 0.0,
    totalluminosity     NUMBER DEFAULT 0,
    tck                 varchar2(20) DEFAULT 'None',
    stepid              NUMBER,
    wnmjfhs06           float(126),
    hlt2tck             varchar2(20),
    numberofprocessors  NUMBER DEFAULT 1,
    PRIMARY KEY (jobid),
    CONSTRAINT job_name_unique UNIQUE (name),
    CONSTRAINT fk_prodcont_prod FOREIGN KEY (production) REFERENCES productionscontainer (production),
    CONSTRAINT jobs_fk1 FOREIGN KEY (configurationid) REFERENCES configurations (configurationid),
    CONSTRAINT fk_jobs_stepid FOREIGN KEY (stepid) REFERENCES steps (stepid)
) PARTITION BY range (production)
  subpartition BY hash (configurationid)
  subpartition TEMPLATE (
    subpartition config1,
    subpartition config2,
    subpartition config3,
    subpartition config4,
    subpartition config5,
    subpartition config6,
    subpartition config7,
    subpartition config8
  ) (
    PARTITION runlast  VALUES LESS THAN (-187450),
    PARTITION run2     VALUES LESS THAN (-90000),
    PARTITION run1     VALUES LESS THAN (0),
    PARTITION prod1    VALUES LESS THAN (33612),
    PARTITION prod2    VALUES LESS THAN (42466),
    PARTITION prod3    VALUES LESS THAN (49181),
    PARTITION prodlast VALUES LESS THAN (MAXVALUE));

CREATE INDEX conf_job_run ON jobs (configurationid, jobid, runnumber);
CREATE INDEX jobsprognameandversion ON jobs (programname, programversion);
CREATE INDEX jobs_diracjobid_jobid ON jobs (diracjobid, jobid) LOCAL;
CREATE INDEX jobs_fill_runnumber ON jobs (fillnumber, runnumber);
CREATE INDEX jobs_productionid ON jobs (production);
CREATE INDEX jobs_prod_config_jobid ON jobs (production, configurationid, jobid) LOCAL;
CREATE INDEX prod_start_end ON jobs (production, jobstart, jobend);
CREATE INDEX runnumber ON jobs (runnumber);


---------------------------------------------------------------------------------------
CREATE TABLE files(
    fileid          NUMBER,
    adler32         varchar2(256),
    creationdate    TIMESTAMP (6),
    eventstat       NUMBER,
    eventtypeid     NUMBER,
    filename        varchar2(256) NOT NULL,
    filetypeid      NUMBER,
    gotreplica      varchar2(3) DEFAULT 'No',
    guid            varchar2(256) NOT NULL,
    jobid           number(38, 0),
    md5sum          varchar2(256) NOT NULL,
    filesize        NUMBER DEFAULT 0,
    qualityid       NUMBER DEFAULT 1,
    inserttimestamp TIMESTAMP (6) DEFAULT CURRENT_TIMESTAMP NOT NULL,
    fullstat        NUMBER,
    physicstat      NUMBER,
    luminosity      NUMBER DEFAULT 0,
    visibilityflag  char(1) DEFAULT 'Y',
    instluminosity  NUMBER DEFAULT 0,
    CONSTRAINT files_pk11 PRIMARY KEY (fileid),
    CONSTRAINT files_filename_unique UNIQUE (filename),
    CONSTRAINT check_physicstat CHECK (physicstat < 0),
    CHECK (visibilityflag IN ('N', 'Y')),
    CONSTRAINT files_fk11 FOREIGN KEY (eventtypeid) REFERENCES eventtypes (eventtypeid),
    CONSTRAINT files_fk21 FOREIGN KEY (filetypeid) REFERENCES filetypes (filetypeid),
    CONSTRAINT fk_qualityid FOREIGN KEY (qualityid) REFERENCES dataquality (qualityid),
    CONSTRAINT files_fk31 FOREIGN KEY (jobid) REFERENCES jobs (jobid) ON DELETE CASCADE
)
PARTITION BY RANGE (jobid)
INTERVAL (20000000) (
  PARTITION sect_0020m VALUES LESS THAN (20000000)
) nologging;

CREATE INDEX files_filetypeid ON files (filetypeid);
ALTER INDEX files_filetypeid unusable;
CREATE INDEX files_guid ON files (guid);
CREATE INDEX files_job_event_filetype ON files (jobid, eventtypeid, filetypeid) LOCAL;
CREATE INDEX files_time_gotreplica ON files (inserttimestamp, gotreplica);
ALTER INDEX files_time_gotreplica invisible;
CREATE INDEX f_gotreplica ON files (gotreplica, visibilityflag, jobid) LOCAL;


---------------------------------------------------------------------------------------
CREATE TABLE inputfiles(
    fileid NUMBER,
    jobid  NUMBER,
    CONSTRAINT pk_inputfiles_ PRIMARY KEY (fileid, jobid),
    CONSTRAINT files_fk1 FOREIGN KEY (fileid) REFERENCES files (fileid),
    CONSTRAINT inputfiles_fk31 FOREIGN KEY (jobid) REFERENCES jobs (jobid) ON
    DELETE CASCADE
);

CREATE INDEX inputfiles_jobid_test ON inputfiles (jobid, fileid)
  GLOBAL PARTITION BY range(jobid) (
    PARTITION sect_0020m  VALUES LESS THAN (20000000),
    PARTITION sect_0040m  VALUES LESS THAN (40000000),
    PARTITION sect_0060m  VALUES LESS THAN (60000000),
    PARTITION sect_0080m  VALUES LESS THAN (80000000),
    PARTITION sect_0100m  VALUES LESS THAN (100000000),
    PARTITION sect_0120m  VALUES LESS THAN (120000000),
    PARTITION sect_0140m  VALUES LESS THAN (140000000),
    PARTITION sect_0160m  VALUES LESS THAN (160000000),
    PARTITION sect_0180m  VALUES LESS THAN (180000000),
    PARTITION sect_0200m  VALUES LESS THAN (200000000),
    PARTITION sect_0220m  VALUES LESS THAN (220000000),
    PARTITION sect_0240m  VALUES LESS THAN (240000000),
    PARTITION sect_0260m  VALUES LESS THAN (260000000),
    PARTITION sect_0280m  VALUES LESS THAN (280000000),
    PARTITION sect_0300m  VALUES LESS THAN (300000000),
    PARTITION sect_0320m  VALUES LESS THAN (320000000),
    PARTITION sect_0340m  VALUES LESS THAN (340000000),
    PARTITION sect_0360m  VALUES LESS THAN (360000000),
    PARTITION sect_0380m  VALUES LESS THAN (380000000),
    PARTITION sect_0400m  VALUES LESS THAN (400000000),
    PARTITION sect_0420m  VALUES LESS THAN (420000000),
    PARTITION sect_0440m  VALUES LESS THAN (440000000),
    PARTITION sect_0460m  VALUES LESS THAN (460000000),
    PARTITION sect_0480m  VALUES LESS THAN (480000000),
    PARTITION sect_0500m  VALUES LESS THAN (500000000),
    PARTITION sect_0520m  VALUES LESS THAN (520000000),
    PARTITION p_greater_than_520000000 VALUES LESS THAN (MAXVALUE));


---------------------------------------------------------------------------------------
CREATE TABLE newrunquality(
    runnumber    NUMBER,
    qualityid    NUMBER,
    processingid NUMBER,
    CONSTRAINT pk_run_quality PRIMARY KEY (runnumber, processingid),
    CONSTRAINT fk_qualityid_run FOREIGN KEY (qualityid) REFERENCES dataquality (qualityid),
    CONSTRAINT processing_id FOREIGN KEY (processingid) REFERENCES processing (id)
  );

CREATE INDEX newrunquality_proc ON newrunquality (processingid);

CREATE OR REPLACE editionable TRIGGER runquality
BEFORE UPDATE OR INSERT ON newrunquality REFERENCING NEW AS NEW OLD AS OLD
FOR EACH ROW
  BEGIN
    UPDATE
      files
    SET
      inserttimestamp = sys_extract_utc(systimestamp + INTERVAL '5' MINUTE), files.qualityid = :NEW.qualityid
    WHERE
      jobid IN
      (
        SELECT
          j.jobid
        FROM
          jobs j
        WHERE
          j.runnumber = :NEW.runnumber
          AND j.production < 0
      );
    UPDATE
      files
    SET
      inserttimestamp = sys_extract_utc(systimestamp + INTERVAL '5' MINUTE),
      files.qualityid = :NEW.qualityid
    WHERE
      files.fileid IN
      (
        SELECT
          f.fileid
        FROM
          files f,
          jobs j
        WHERE
          j.jobid = f.jobid
          AND j.runnumber = :NEW.runnumber
          AND f.gotreplica = 'Yes'
          AND j.production IN
          (
            SELECT
              prod.production
            FROM
              productionscontainer prod
            WHERE
              prod.processingid = :NEW.processingid
          )
      );
  END;
 /

 ---------------------------------------------------------------------------------------
CREATE TABLE productionoutputfiles(
    production  NUMBER,
    stepid      NUMBER,
    eventtypeid NUMBER,
    filetypeid  NUMBER,
    visible     char(1) DEFAULT 'Y',
    gotreplica  varchar2(3) DEFAULT 'No',
    CONSTRAINT pk_productionoutputfiles_p PRIMARY KEY (production, stepid, filetypeid, eventtypeid, visible),
    CONSTRAINT fk_productionoutputfiles_steps FOREIGN KEY (stepid) REFERENCES steps (stepid),
    CONSTRAINT fk_productionoutputfiles_evt FOREIGN KEY (eventtypeid) REFERENCES eventtypes (eventtypeid),
    CONSTRAINT fk_productionoutputfiles_ft FOREIGN KEY (filetypeid) REFERENCES filetypes (filetypeid),
    CONSTRAINT fk_productionoutputfiles_prod FOREIGN KEY (production)
    REFERENCES productionscontainer (production) ON DELETE CASCADE
);


---------------------------------------------------------------------------------------
CREATE TABLE runstatus(
    runnumber NUMBER,
    jobid NUMBER,
    finished char(1) DEFAULT 'N',
    CONSTRAINT pk_runstatus PRIMARY KEY (runnumber, jobid),
    CONSTRAINT fk_runstatus FOREIGN KEY (jobid)
    REFERENCES jobs (jobid)
);

CREATE OR REPLACE editionable TRIGGER runstatus
BEFORE UPDATE ON runstatus
REFERENCING NEW AS NEW OLD AS OLD
FOR EACH ROW
  BEGIN
     bookkeepingoracledb.updateluminosity(:new.runnumber);
  END;
 /
---------------------------------------------------------------------------------------
CREATE TABLE runtimeprojects(
    stepid           NUMBER,
    runtimeprojectid NUMBER,
    CONSTRAINT runtimeproject_pk PRIMARY KEY (runtimeprojectid, stepid),
    CONSTRAINT runtimeproject_fk1 FOREIGN KEY (stepid) REFERENCES steps (stepid),
    CONSTRAINT runtimeproject_fk2 FOREIGN KEY (runtimeprojectid) REFERENCES steps (stepid)
);


---------------------------------------------------------------------------------------
CREATE TABLE prodrunview (
  production number NOT NULL,
  runnumber number NOT NULL,
  CONSTRAINT prod_run_const UNIQUE (production, runnumber)
);

---------------------------------------------------------------------------------------
BEGIN
  dbms_scheduler.create_job (
     job_name             => 'produpdatejob',
     job_type             => 'PLSQL_BLOCK',
     job_action           => 'BEGIN BKUTILITIES.updateProdOutputFiles(); END;',
     repeat_interval      => 'FREQ=MINUTELY; interval=10',
     start_date           => systimestamp,
     enabled              => TRUE
     );
END;
 /

 BEGIN
  dbms_scheduler.create_job (
     job_name             => 'prodrunupdatejob',
     job_type             => 'PLSQL_BLOCK',
     job_action           => 'BEGIN BKUTILITIES.updateprodrunview(); END;',
     repeat_interval      => 'FREQ=MINUTELY; interval=20',
     start_date           => systimestamp,
     enabled              =>  TRUE
     );
END;
 /
