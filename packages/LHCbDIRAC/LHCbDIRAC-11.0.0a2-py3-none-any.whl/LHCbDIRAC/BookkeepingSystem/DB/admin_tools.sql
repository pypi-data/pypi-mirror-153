/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

define USER = 'system'
define GRANTEE = 'lhcb_diracbookkeeping_users'

select 'GRANT SELECT ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('TABLE','VIEW')
    and owner = upper('&USER')
union
select 'GRANT SELECT ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('SEQUENCE')
    and owner = upper('&USER');

select 'CREATE SYNONYM '||  object_name || '  FOR &USER'||'.'||object_name||';' from ALL_OBJECTS
  where object_type in ('TABLE','VIEW')
    and owner = upper('&USER')
union
select 'CREATE SYNONYM '||  object_name || '  FOR &USER'||'.'||object_name||';'
from ALL_OBJECTS
  where object_type in ('SEQUENCE')
    and owner = upper('&USER');

----
select 'GRANT execute ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('TYPE')
    and owner = upper('&USER');

select 'CREATE SYNONYM '||  object_name || '  FOR
&USER'||'.'||object_name||';' from ALL_OBJECTS
  where object_type in ('TYPE')
    and owner = upper('&USER');


 ---------------------------------------------------------------------------
define USER = 'LHCB_DIRACBOOKKEEPING'
define GRANTEE = 'lhcb_DIRACbookkeeping_server'

#define USER = 'LHCB_BOOKKEEPING_int'
#define GRANTEE = 'LHCB_BOOKKEEPING_INT_W'

select 'GRANT SELECT, INSERT, UPDATE ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('TABLE','VIEW')
    and owner = upper('&USER')
union
select 'GRANT SELECT ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('SEQUENCE')
    and owner = upper('&USER');

select 'CREATE SYNONYM '||  object_name || '  FOR &USER'||'.'||object_name||';' from ALL_OBJECTS
  where object_type in ('TABLE','VIEW')
    and owner = upper('&USER')
union
select 'CREATE SYNONYM '||  object_name || '  FOR &USER'||'.'||object_name||';'
from ALL_OBJECTS
  where object_type in ('SEQUENCE')
    and owner = upper('&USER');


---

select 'GRANT execute ON ' || object_name || ' TO &GRANTEE;'
  from ALL_OBJECTS
  where object_type in ('TYPE')
    and owner = upper('&USER');

select 'CREATE SYNONYM '||  object_name || '  FOR
&USER'||'.'||object_name||';' from ALL_OBJECTS
  where object_type in ('TYPE')
    and owner = upper('&USER');
