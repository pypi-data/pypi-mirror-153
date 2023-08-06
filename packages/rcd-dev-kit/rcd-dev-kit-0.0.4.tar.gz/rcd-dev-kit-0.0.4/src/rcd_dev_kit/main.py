from typing import List

import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os

from src.rcd_dev_kit.database_manager.s3_operator import S3Operator
from src.rcd_dev_kit.database_manager.redshift_operator import RedshiftOperator, send_to_redshift
from src.rcd_dev_kit.database_manager.snowflake_operator import SnowflakeOperator


from sqlalchemy.engine.default import DefaultDialect
import sqlalchemy
import snowflake.connector
import sqlparse

##########
##########
#########

import re

# SOURCE: https://gist.github.com/tamiroze/dc0bdd596ed2c6b70fe921061401e739

###################################################################
### RegExes for Oracle dialect that Snowflake doesn't support #####
###################################################################
# VARCHAR2(n BYTE) => VARCHAR(n)
varchar2_re = re.compile('(.*)(VARCHAR2\((\d+)(\s+.+)?\))(.*)', re.IGNORECASE)

# CHAR(n BYTE) => CHAR(n)
char_re = re.compile('(.*)(CHAR\((\d+)(\s+.+)\))(.*)', re.IGNORECASE)

# DEFAULT SYSDATE => deleted (OK only because data loaded from table should already have date)
# Snowflake DEFAULT must be literal
default_sysdate_re = re.compile('(.*)\ (DEFAULT SYSDATE)\ (.*)', re.IGNORECASE)

# SYSDATE => CURRENT_TIMESTAMP()
#sysdate_re = re.compile('(.*)\ (SYSDATE)\ (.*)', re.IGNORECASE)
sysdate_re = re.compile('(.*[,\(\s])(SYSDATE)([,\)\s].*)', re.IGNORECASE)

# SEGMENT CREATION type => ignore
segment_creation_re = re.compile('(.*)\ (SEGMENT\s+CREATION\s+(?:IMMEDIATE|DEFERRED))(.*)', re.IGNORECASE)

# NOT NULL ENABLE => NOT NULL
not_null_enable_re = re.compile('(.*)(NOT\s+NULL\s+ENABLE)(.*)', re.IGNORECASE)

# find prior period, e.g. trunc(col,'MM')-1 => dateadd('MM', -1, trunc(col, 'MM'))
prior_period_re = re.compile('(.*)(TRUNC\(\s*(.+?),\s*(\'.+?\')\s*\)\s*(-?\s*\d+))(.*)', re.IGNORECASE)

# add months, e.g. add_months(trunc(col, 'MM'), -5) => dateadd(month, -5, col)
add_months_re = re.compile('(.*)(ADD_MONTHS\(\s*TRUNC\(\s*(.+?),\s*(\'.+?\')\s*\),\s*(-?\s*\d+))(.*)', re.IGNORECASE)

###################################################################
## RegExes for SQL-Server dialect that Snowflake doesn't support ##
###################################################################
# NULL (explicit NULL constraint) -- ignore
null_constraint_re = re.compile('(.*)((?<!NOT)\s+NULL(?!::))(.*)', re.IGNORECASE)
is_null_condition_re = re.compile('.*IS NULL.*', re.IGNORECASE)

# NVARCHAR => VARCHAR
nvarchar_re = re.compile('(.*)\ (NVARCHAR)(.*)', re.IGNORECASE)

# NVARCHAR => VARCHAR
nchar_re = re.compile('(.*)\ (NCHAR)(.*)', re.IGNORECASE)

# ON PRIMARY => ignore
on_primary_re = re.compile('(.*)\ (ON PRIMARY)(.*)', re.IGNORECASE)

# DATETIME => TIMESTAMP
datetime_re = re.compile('(.*)\ (DATETIME)(.*)', re.IGNORECASE)

# BIT => BOOLEAN
bit_re = re.compile('(.*)\ (BIT)(.*)', re.IGNORECASE)

###################################################################
### RegExes for Redshift dialect that Snowflake doesn't support ###
###################################################################
# DISTKEY(col) => ignore
# DISTKEY => ignore
distkey_re = re.compile('(.*)(\s*DISTKEY\s*(?:\(.*?\))?)(.*)', re.IGNORECASE)

# SORTKEY(col) => ignore
sortkey_re = re.compile('(.*)(\s*SORTKEY\s*\(.*?\))(.*)', re.IGNORECASE)

# SORTKEY => ignore through end of statement
sortkey_multiline_re = re.compile('(.*)(\s*SORTKEY\s*\(?\s*$)(.*)', re.IGNORECASE)

# ENCODE type => ignore
encode_re = re.compile('(.*)(\sENCODE\s+.+?)((?:,|\s+|$).*)', re.IGNORECASE)

# DISTSTYLE type => ignore
diststyle_re = re.compile('(.*)(\s*DISTSTYLE\s+.+?)((?:,|\s+|$).*)', re.IGNORECASE)

# 'now'::character varying => current_timestamp
now_character_varying_re = re.compile('(.*)(\'now\'::(?:character varying|text))(.*)', re.IGNORECASE)

# bpchar => char
bpchar_re = re.compile('(.*)(bpchar)(.*)', re.IGNORECASE)

# character varying => varchar
character_varying_re = re.compile('(.*)(character varying)(.*)')

# interleaved => ignore
interleaved_re = re.compile('(.*)(interleaved)(.*)', re.IGNORECASE)

# identity(start, 0, ([0-9],[0-9])::text) => identity(start, 1)
identity_re = re.compile('(.*)\s*DEFAULT\s*"identity"\(([0-9]*),.*?(?:.*?::text)\)(.*)', re.IGNORECASE)

###################################################################
### RegExes for Netezza dialect that Snowflake doesn't support ####
###################################################################
## casting syntax
# INT4(expr) => expr::INTEGER
int4_re = re.compile('(.*)\ (INT4\s*\((.*?)\))(.*)', re.IGNORECASE)

########################################################################
### RegExes for common/standard types that Snowflake doesn't support ###
########################################################################
bigint_re = re.compile('(.*)\ (BIGINT)(.*)', re.IGNORECASE)
smallint_re = re.compile('(.*)\ (SMALLINT)(.*)', re.IGNORECASE)
floatN_re = re.compile('(.*)\ (FLOAT\d+)(.*)', re.IGNORECASE)

# CREATE [type] INDEX => ignore through end of statement
index_re = re.compile('(.*)(CREATE(?:\s+(?:UNIQUE|BITMAP))?\ INDEX)(.*)', re.IGNORECASE)

# ALTER TABLE ... ADD PRIMARY KEY => ignore
pk_re = re.compile('(.*)(ALTER\s+TABLE\s+.*ADD\s+PRIMARY\s+KEY)(.*)', re.IGNORECASE)

# SET ... TO => ignore
set_re = re.compile('(.*)(SET\s+.*TO)(.*)', re.IGNORECASE)

statement_term_re = re.compile('(.*);(.*)', re.IGNORECASE)

def make_snow(sqlin, sqlout, no_comments):
    ### processing mode
    comment_lines = None
    term_re = None
    query_input = open(sqlin, 'r')
    sf_output = open(sqlout, 'w+')

    for line in query_input:
        ### state variables
        pre = None
        clause = None
        post = None
        comment = None

        sql = line.rstrip()
        sql = sql.replace('[', '').replace(']', '')

        # print >> sys.stdout, 'input: ' + sql

        if comment_lines:
            result = term_re.match(sql)
            if result:
                comment_lines = None
                term_re = None
            sql = '-- {0}'.format(sql)

        # VARCHAR2(n BYTE) => VARCHAR(n)
        result = varchar2_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)     # varchar2 clause
            cnt = result.group(3)
            discard = result.group(4)
            post = result.group(5)
            sql = '{0}{1}({2}){3}\t\t-- {4}'.format(pre, clause[0:7], cnt, post, clause)

        # CHAR(n BYTE) => CHAR(n)
        result = char_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)     # char clause
            cnt = result.group(3)
            discard = result.group(4)
            post = result.group(5)
            sql = '{0}{1}({2}){3}\t\t-- {4}'.format(pre, clause[0:4], cnt, post, clause)

        # DEFAULT SYSDATE => deleted (OK only because data loaded from table should already have date)
        result = default_sysdate_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} {1}\t\t-- {2}'.format(pre, post, clause)

        # NVARCHAR => VARCHAR
        result = nvarchar_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} VARCHAR {1}\t\t-- {2}'.format(pre, post, clause)

        # NCHAR => CHAR
        result = nchar_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} CHAR {1}\t\t-- {2}'.format(pre, post, clause)

        # DATETIME => TIMESTAMP
        result = datetime_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} TIMESTAMP {1}\t\t-- {2}'.format(pre, post, clause)

        # BIGINT => INTEGER
        #result = bigint_re.match(sql)
        #if result:
        #    pre = result.group(1)
        #    clause = result.group(2)
        #    post = result.group(3)
        #    sql = '{0} INTEGER {1}\t\t-- {2}'.format(pre, post, clause)

        # SMALLINT => INTEGER
        #result = smallint_re.match(sql)
        #if result:
        #    pre = result.group(1)
        #    clause = result.group(2)
        #    post = result.group(3)
        #    sql = '{0} INTEGER {1}\t\t-- {2}'.format(pre, post, clause)

        # BIT => BOOLEAN
        result = bit_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} BOOLEAN {1}\t\t-- {2}'.format(pre, post, clause)

        # FLOAT8 => FLOAT
        result = floatN_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} FLOAT {1}\t\t-- {2}'.format(pre, post, clause)

        # NULL (without NOT) => implicit nullable
        result = null_constraint_re.match(sql)
        if result and is_null_condition_re.match(sql):
            # we are in query or DML, so not looking at a constraint
            result = None
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # ON PRIMARY => ignore
        result = on_primary_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # DISTKEY(col) => ignore
        result = distkey_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # SORTKEY(col) => ignore
        result = sortkey_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # SORTKEY => ignore through end of statement
        result = sortkey_multiline_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0};\n-- {2} {1}'.format(pre, post, clause)
            comment_lines = 1
            term_re = statement_term_re

        # ENCODE type => ignore
        result = encode_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # DISTSTYLE type => ignore
        result = diststyle_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}{1}\t\t-- {2}'.format(pre, post, clause)

        # 'now'::(character varying|text) => current_timestamp
        result = now_character_varying_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}CURRENT_TIMESTAMP{1} --{2}'.format(pre,post,clause)

        # bpchar => char
        result = bpchar_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}char{1} --{2}'.format(pre,post,clause)

        result = character_varying_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}varchar{1}  --{2}'.format(pre,post,clause)

        # interleaved => ignore
        result = interleaved_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} {1} --{2}'.format(pre,post,clause)

        result = identity_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0} IDENTITY({1},1) {2}'.format(pre,clause,post)

        # SEGMENT CREATION type => ignore
        result = segment_creation_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0};;\n-- {2} {1}'.format(pre, post, clause)
            comment_lines = 1
            term_re = statement_term_re

        # ALTER TABLE ... ADD PRIMARY KEY => ignore
        result = index_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}-- {2} {1}'.format(pre, post, clause)
            comment_lines = 1
            term_re = statement_term_re

        # INDEX CREATION => ignore through end of statement
        result = pk_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}-- {2} {1}'.format(pre, post, clause)
            comment_lines = 1
            term_re = statement_term_re

        # SET ... TO => ignore
        result = set_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}-- {2} {1}'.format(pre, post, clause)
            comment_lines = 1
            term_re = statement_term_re

        # NOT NULL ENABLE => NOT NULL
        result = not_null_enable_re.match(sql)
        if result:
            pre = result.group(1)
            clause = result.group(2)
            post = result.group(3)
            sql = '{0}NOT NULL{1}\t\t-- {2}'.format(pre, post, clause)

        ## DML transformations that might appear multiple times per line
        dml_repeat = True
        while dml_repeat:
            dml_repeat = False

            # determine prior period
            # e.g. trunc(sysdate,'MM')-1
            result = prior_period_re.match(sql)
            if result:
                pre = result.group(1)
                clause = result.group(2)
                col = result.group(3)
                units = result.group(4)
                offset = result.group(5)
                post = result.group(6)
                sql = '{0}dateadd({4}, {5}, trunc({3}, {4}))'.format(pre, post, clause, col, units, offset)
                comment = append_comment(comment, clause, no_comments)
                dml_repeat = True

            # add_months
            # e.g. add_months(trunc(sysdate, 'MM'), -5) => dateadd('MM', -5, trunc(current_timestamp, 'MM'))
            result = add_months_re.match(sql)
            if result:
                raise Exception("Snowflake now has add_months() function -- verify can use as-is")

            # SYSDATE => CURRENT_TIMESTAMP()
            result = sysdate_re.match(sql)
            if result:
                pre = result.group(1)
                clause = result.group(2)
                post = result.group(3)
                sql = '{0} CURRENT_TIMESTAMP() {1}'.format(pre, post, clause)
                comment = append_comment(comment, clause, no_comments)
                dml_repeat = True

            # INT4(expr) => expr::INTEGER
            result = int4_re.match(sql)
            if result:
                pre = result.group(1)
                clause = result.group(2)
                col = result.group(3)
                post = result.group(4)
                sql = '{0} {3}::integer {1}'.format(pre, post, clause, col)
                comment = append_comment(comment, clause, no_comments)
                dml_repeat = True

        # write out possibly modified line
        sf_output.write(sql)
        if comment:
            sf_output.write('\t\t-- {0}'.format(comment))
        sf_output.write('\n')
        continue

def append_comment(old_comment, new_comment, no_comments):
    if no_comments:
        return None
    if old_comment and new_comment:
        return '{0} // {1}'.format(old_comment, new_comment)
    if not old_comment:
        return new_comment
    return old_comment

# ##### MAIN #####
# if __name__ == "__main__":
#
#     parser = argparse.ArgumentParser(description='Convert SQL dialects to Snowflake.')
#     parser.add_argument('--no_comments', action='store_true',
#         help='suppress comments with changes (default: show changes)')
#     parser.add_argument('inputfile', action='store', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
#         help='input SQL file in other-vendor dialect (default: stdin)')
#     parser.add_argument('outputfile', action='store', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
#         help='output SQL file in Snowflake dialect (default: stdout)')
#     args=parser.parse_args();
#
#     #with etl_util.error_reporting():
#     make_snow(args.inputfile, args.outputfile, args.no_comments)
#     args.inputfile.close()
#     args.outputfile.close()
#     #print >> sys.stderr, "done translating " + args.inputfile.name

def convert_to_snowflake_syntax(query, no_comments=False):
    # Open the file in reading mode
    ifile = open("inputfile.txt", mode = 'w+')
    ifile.write(query)
    ifile.close()

    make_snow("inputfile.txt", "outputfile.txt", no_comments)
    print("Done translating the syntax to SF-Compatible SQL.")

    # Run bash command to read the file
    ofile = open("outputfile.txt", 'r')
    sn_query = ofile.read()
    ofile.close()

    # Remove the temporary file
    #os.remove("inputfile.txt")
    #os.remove("outputfile.txt")

    return sn_query
#########
#########
#########

def migrate_metadata_from_redshift(rs_db: str, sf_db: str, schemas_list: List = [], tables_list: List = [],
                                   create_tables: bool = False, logging: bool= True, verbose:bool = True):
    print("Starting the metadata migration process | Redshift -> Snowflake")
    ro = RedshiftOperator(database=rs_db)
    ddl_model = ro.get_DDL(verbose=verbose, schema_names=schemas_list, table_names=tables_list)

    ddl_model = pd.read_csv("/opt/project/rcd_pyutils/ddl_output/ddl_model.txt", sep="\t", encoding="utf-8")
    ddl_model.fillna("", inplace=True)

    if schemas_list != []:
        ddl_model = ddl_model[ddl_model.schema_name.isin(schemas_list)]
    if tables_list != []:
        ddl_model = ddl_model[ddl_model.table_name.isin(tables_list)]

    print("Connecting to Snowflake...")
    sf = SnowflakeOperator(snowflake_database=sf_db)
    print("Done!")

    if logging:
        if os.path.exists("query_log_errors.txt"):
            os.remove("query_log_errors.txt")

    if create_tables:
        print("\nCreating tables if they don't already exist...")
        # Some of these corrections below must be done because 'year', 'level', 'region', 'names' are SQL Syntax Names
        # and AWS parse them as strings when creating the column names. However, Snowflake parses it otherwise because
        # it can distinguish the column names and the SQL Variables as different things.
        ddl_model.create_query = ddl_model.create_query.apply(lambda x: x.replace('"year"', "year ")
                                                              .replace('"level" ', "level ")
                                                              .replace('"region" ', "region ")
                                                              .replace('"names" ', "names ")
                                                              .replace('"type" ', "type ")
                                                              .replace('"role" ', "role ")
                                                              .replace('"provider" ', "provider ")
                                                              .replace('"location" ', "location "))
        sf.execute_metadata_query(ddl_model.create_query.values, logging=logging, correct_syntax=True)

    print("\nMigrating Table Descriptions...")
    sf.execute_metadata_query(ddl_model.table_description.values, logging=logging)

    print("\nMigrating Columns Descriptions...")
    ddl_model.columns_description = ddl_model.columns_description.apply(lambda x: x.replace('."year"', ".year")
                                                          .replace('."level"', ".level")
                                                          .replace('."region"', ".region")
                                                          .replace('."names"', ".names")
                                                          .replace('."type"', ".type")
                                                          .replace('."role"', ".role")
                                                          .replace('."provider"', ".provider")
                                                          .replace('."location"', ".location "))
    sf.execute_metadata_query(ddl_model.columns_description.values, logging=logging)

    print("\nMigrating Primary Keys...")
    sf.execute_key_query(ddl_model, key="primary", logging=logging)

    print("\nMigrating Unique Keys...")
    sf.execute_key_query(ddl_model, key="unique", logging=logging)

    print("\nMigrating Foreign Keys...")
    sf.execute_metadata_query(ddl_model.foreign_keys.values, logging=logging)

    sf.conn.cursor().close()
    sf.conn.close()
    print("All metadata have been migrated successfully !")

def main_main_main():
    load_dotenv(find_dotenv())

    ro = RedshiftOperator(database="oip")
    ddl_model = ro.get_DDL(verbose=True)

    sf = SnowflakeOperator()

    migrate_metadata_from_redshift(rs_db="oip",
                                   sf_db="oip_test",
                                   schemas_list=["emea_sales"],
                                   create_tables=True)

def main_main():
    load_dotenv(find_dotenv())

    ro = RedshiftOperator(database="oip")
    ddl_model = ro.get_DDL(verbose=True)

    df = ddl_model.copy()

    primary_key = [f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} ADD PRIMARY KEY ({df.iloc[row, 2]});"
                   if df.iloc[row, 2] != "" else "" for row in range(len(df))]
    df["primary_key_sql"] = primary_key


    opa = ddl_model[(ddl_model.columns_description.str.contains("é")) | (ddl_model.columns_description.str.contains("è"))].table_name.sort_values().unique()

    opa.columns_description.values[0]

    test__log = ddl_model[ddl_model.table_name == "ww__cancer_incidence"]

    command = test__log.columns_description.values[0]

    ctx = snowflake.connector.connect(user='DAVIBARRETO',
                                      password='Ecclesiasancta!1',
                                      account='xg19634.europe-west4.gcp',
                                      warehouse="COMPUTE_WH",
                                      role="ACCOUNTADMIN",
                                      database="OIP_TEST")
    cs = ctx.cursor()

    #ifile = open("inputfile.txt", mode='w+')
    #ifile.write(command)
    #ifile.close()

    # command = 'CREATE TABLE IF NOT EXISTS public.br__cancer_database__inca\n(\n\t"year" VARCHAR(8)   ENCODE lzo\n\t,gender VARCHAR(8)   ENCODE lzo\n\t,age_group_10 VARCHAR(16)   ENCODE lzo\n\t,age INTEGER   ENCODE az64\n\t,ethnicity VARCHAR(16)   ENCODE lzo\n\t,education VARCHAR(32)   ENCODE lzo\n\t,icd_10 VARCHAR(8)   ENCODE lzo\n\t,icd_o VARCHAR(8)   ENCODE lzo\n\t,tnm VARCHAR(8)   ENCODE lzo\n\t,tnm_t VARCHAR(8)   ENCODE lzo\n\t,tnm_t_description VARCHAR(32)   ENCODE lzo\n\t,tnm_n VARCHAR(8)   ENCODE lzo\n\t,tnm_n_description VARCHAR(64)   ENCODE lzo\n\t,tnm_m VARCHAR(8)   ENCODE lzo\n\t,tnm_m_description VARCHAR(32)   ENCODE lzo\n\t,diagnostic_year VARCHAR(8)   ENCODE lzo\n\t,basis_of_diagnosis VARCHAR(64)   ENCODE lzo\n\t,laterality_tumor VARCHAR(16)   ENCODE lzo\n\t,another_primary_tumor VARCHAR(16)   ENCODE lzo\n\t,previous_diagnoses_and_treatments VARCHAR(32)   ENCODE lzo\n\t,first_treatment VARCHAR(128)   ENCODE lzo\n\t,disease_status_first_treatment VARCHAR(64)   ENCODE lzo\n\t,cancer_family_history VARCHAR(16)   ENCODE lzo\n\t,alcohol_consumption VARCHAR(16)   ENCODE lzo\n\t,smoking VARCHAR(16)   ENCODE lzo\n)\nDISTSTYLE AUTO\n;'

    # command = convert_to_snowflake_syntax(command, no_comments=True)

    cs.execute(command)

    df = cs.fetch_pandas_all()


# Defining main function
def main():
    load_dotenv(find_dotenv())


    ro = RedshiftOperator(database="oip")
    ddl_model = ro.get_DDL(verbose=True)




    query = open('/opt/project/rcd_pyutils/database_manager/v_generate_tbl_ddl.sql', 'r').read().replace("%", "%%")

    result = ro.conn.execution_options(autocommit=True).execute(sqlalchemy.text(query))
    result.close()

    print(f"🥳Table is copied to redshift from S3.\n")

    #query = f"select * " \
    #        f"from admin.v_generate_tbl_ddl " \
    #        f"where tablename='fr__definition_disorder__orphanet' and schemaname='reference';"

    query = f"select * " \
            f"from admin.v_generate_tbl_ddl"

    try:
        query = f"select * " \
                f"from admin.v_generate_tbl_ddl"

        ro = RedshiftOperator(database="oip")
        result = ro.conn.execute(sqlalchemy.text(query)).all()
        ro.conn.close()
        schema_names = list(set([record.schemaname for record in result]))

        # #result = ro.conn.execute(sqlalchemy.text(query)).all()
        # dfs = []
        # verbose = True
        # schema_names = None
        # table_names = None
        #
        # if not schema_names:
        #     schema_names = list(set([record.schemaname for record in result]))
        #
        # for schema in set(schema_names).difference(['pv_reference', 'platform', 'pv_intermediary_tables', 'pg_catalog', 'information_schema']):
        #     if verbose:
        #         print(schema)
        #     if not table_names:
        #         table_names = list(set([record.tablename for record in result if record.schemaname == schema]))
        #     for table in table_names:
        #         if verbose:
        #             print(f" - {table}")
        #         corrected_query = ""
        #         for record in result:
        #             if (record.schemaname == schema) and (record.tablename == table):
        #                 line = record.ddl.replace(" ", " ").replace("\'\"", "'").replace("\"\'", "'")
        #                 corrected_query += f"{line}"
        #         corrected_query = corrected_query.replace('\";\"', "semicolon").split(";")
        #
        #         create_sql = ";\n".join(statement.strip() for statement in corrected_query if "CREATE TABLE IF NOT EXISTS".lower() in statement.lower())
        #         comment_table_sql = ";\n".join(statement.strip() for statement in corrected_query if "COMMENT ON table".lower() in statement.lower())
        #         comment_columns_sql = ";\n".join([statement.strip() for statement in corrected_query if "COMMENT ON column".lower() in statement.lower()])
        #         foreign_key_sql = ";\n".join([statement.strip() for statement in corrected_query if "FOREIGN KEY".lower() in statement.lower()])
        #
        #         df = pd.DataFrame({"schema_name": schema,
        #                            "table_name": table,
        #                            "create_query": create_sql,
        #                            "table_description": comment_table_sql,
        #                            "columns_description": comment_columns_sql,
        #                            "foreign_keys": foreign_key_sql}, index=[1])
        #         dfs.append(df)
        #
        # print("DDL Data Model generated.")
        # ddl_model = pd.concat(dfs, ignore_index=True)

        verbose = True
        dfs = []
        for schema in set(schema_names).difference(['pv_reference', 'platform', 'pv_intermediary_tables', 'pg_catalog', 'information_schema']):
            if verbose:
                print(schema)
            table_names = list(set([record.tablename for record in result if record.schemaname == schema]))
            #for table in table_names:
            for table in ['be__retail_patient__atc4__inami']:
                if verbose:
                    print(f" - {table}")
                corrected_query = ""
                for record in result:
                    if (record.schemaname == schema) and (record.tablename == table):
                        #line = record.ddl.replace(" ", " ").replace("\'\"", "'").replace("\"\'", "'")
                        #line = record.ddl.replace(" ", " ").replace("\'\"", "__aux__").replace("\"\'", "__aux__").replace("'", "\\'").replace("__aux__", "'")
                        line = record.ddl.replace(" ", " ").replace("\'\"", "'").replace("\"\'", "'").replace("\"\"",'"')
                        if line.count("'") > 2:
                            line = "'".join([line.split("'")[0], "''".join(line.split("'")[1:-1]), line.split("'")[-1]])
                        corrected_query += f"{line}\n"

                corrected_query = corrected_query.replace(".year ", '."year" ').replace(".level ", '."level" ') \
                    .replace(".region ", '."region" ').replace(".names ", '."names" ').replace(".type ", '."type" ') \
                    .replace(".role ", '."role" ').replace(".provider ", '."provider" ').replace(".location ",
                                                                                                 '."location" ')
                corrected_query = sqlparse.split(corrected_query)

                create_sql = "".join([statement for statement in corrected_query if "CREATE TABLE IF NOT EXISTS".lower() in statement.lower()])
                create_sql = ";\n".join(create_sql.split(";\n")[1:])
                primary_key = re.findall(",PRIMARY KEY \((\w+)\)", create_sql)[-1] if len(re.findall(",PRIMARY KEY \((\w+)\)", create_sql)) > 0 else ""
                comment_table_sql = "".join([statement for statement in corrected_query if "COMMENT ON table".lower() in statement.lower()])
                comment_columns_sql = "\n".join([statement for statement in corrected_query if "COMMENT ON column".lower() in statement.lower()])
                foreign_key_sql = "\n".join([statement for statement in corrected_query if "FOREIGN KEY".lower() in statement.lower()])

                # Check if the column names agree with the SQL standards. It must not have accented letters or any special character.
                # For some reason, when we retrieve the DDL from Redshift, it gives the CREATE TABLE Sql correctly but not
                # the COMMENT ON Sql script. Whenever a column name has a non-ASCII name, we must parse it as string (under quotes).
                # This script down below corrects the COMMENT ON string with the quotes notation.
                sql_columns = re.findall("\n\t[,]*\"([.\S]+)\"\s+", create_sql)
                string_check = re.compile('[@\-!#$%^&*+()<>?/\|}{~:]')
                for var in sql_columns:
                    if not var.isascii() or (string_check.search(var) is not None):
                        comment_columns_sql = comment_columns_sql.replace(f".{var} IS", f'."{var}" IS')



                teste = f'CREATE TABLE IF NOT EXISTS emea_environment.fr__drug_directory\n(\n\tcip13_code VARCHAR(1000) NOT NULL  ENCODE lzo\n\t,cis_code+++ VARCHAR(1000)   ENCODE lzo\n\t,cis-label VARCHAR(1000)   ENCODE lzo\n\t,presentation_label VARCHAR(1000)   ENCODE lzo\n\t,brand VARCHAR(1000)   ENCODE lzo\n\t,brand_regroup VARCHAR(1000)   ENCODE lzo\n\t,owner_regroup VARCHAR(1000)   ENCODE lzo\n\t,atc5_code VARCHAR(1000)   ENCODE lzo\n\t,atc4_code VARCHAR(1000)   ENCODE lzo\n\t,atc3_code VARCHAR(1000)   ENCODE lzo\n\t,atc2_code VARCHAR(1000)   ENCODE lzo\n\t,atc1_code VARCHAR(1000)   ENCODE lzo\n\t,atc5_french_label VARCHAR(1000)   ENCODE lzo\n\t,atc4_french_label VARCHAR(1000)   ENCODE lzo\n\t,atc3_french_label VARCHAR(1000)   ENCODE lzo\n\t,atc2_french_label VARCHAR(1000)   ENCODE lzo\n\t,atc1_french_label VARCHAR(1000)   ENCODE lzo\n\t,atc5_english_label VARCHAR(1000)   ENCODE lzo\n\t,atc4_english_label VARCHAR(1000)   ENCODE lzo\n\t,atc3_english_label VARCHAR(1000)   ENCODE lzo\n\t,atc2_english_label VARCHAR(1000)   ENCODE lzo\n\t,atc1_english_label VARCHAR(1000)   ENCODE lzo\n\t,generic_type_code VARCHAR(1000)   ENCODE lzo\n\t,generic_type_label VARCHAR(1000)   ENCODE lzo\n\t,is_retail VARCHAR(1000)   ENCODE lzo\n\t,is_hospital VARCHAR(1000)   ENCODE lzo\n\t,is_brand VARCHAR(1000)   ENCODE lzo\n\t,PRIMARY KEY (cip13_code)\n)\nDISTSTYLE AUTO\n DISTKEY (cip13_code)\n;'
                teste = f'CREATE TABLE IF NOT EXISTS emea_environment.fr__medical_devices__region__yearly__sniiram\n(\n\tcode_lpp VARCHAR(259) NOT NULL  ENCODE lzo\n\t,label_lpp VARCHAR(259)   ENCODE lzo\n\t,categorie VARCHAR(259)   ENCODE lzo\n\t,label_categorie VARCHAR(259)   ENCODE lzo\n\t,sous_categorie_1 VARCHAR(259)   ENCODE lzo\n\t,label_sous_categorie_1 VARCHAR(259)   ENCODE lzo\n\t,sous_categorie_2 VARCHAR(259)   ENCODE lzo\n\t,label_sous_categorie_2 VARCHAR(259)   ENCODE lzo\n\t,label_region VARCHAR(259)   ENCODE lzo\n\t,periode VARCHAR(259)   ENCODE lzo\n\t,nombre_de_beneficiaires DOUBLE PRECISION   ENCODE RAW\n\t,"montant_remboursé" DOUBLE PRECISION   ENCODE RAW\n\t,base_de_remboursement DOUBLE PRECISION   ENCODE RAW\n\t,"quantité_rembousée" DOUBLE PRECISION   ENCODE RAW\n)\nDISTSTYLE AUTO\n DISTKEY (code_lpp)\n;'
                teste = f'CREATE TABLE IF NOT EXISTS emea_sales.be__retail_patient__atc4__inami\r\n(\r\n\tregistry_year VARCHAR(259)   ENCODE RAW\r\n\t,atc4_code VARCHAR(255) NOT NULL  ENCODE RAW\r\n\t,\"atc4-en\" VARCHAR(258)   ENCODE RAW\r\n\t,\"atc4_reimbursed-inami\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc4_reimbursed-patient\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc4_reimbursed-total\" DOUBLE PRECISION   ENCODE RAW\r\n\t,atc4_unit DOUBLE PRECISION   ENCODE RAW\r\n\t,atc4_patient DOUBLE PRECISION   ENCODE RAW\r\n\t,atc3_code VARCHAR(255)   ENCODE RAW\r\n\t,atc3_en VARCHAR(258)   ENCODE RAW\r\n\t,\"atc3_reimbursed-inami\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_reimbursed-patient\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_reimbursed-total\" DOUBLE PRECISION   ENCODE RAW\r\n\t,atc3_unit DOUBLE PRECISION   ENCODE RAW\r\n\t,atc3_ddd DOUBLE PRECISION   ENCODE RAW\r\n\t,atc3_patient DOUBLE PRECISION   ENCODE RAW\r\n\t,atc2_code VARCHAR(255)   ENCODE RAW\r\n\t,\"atc2-en\" VARCHAR(258)   ENCODE RAW\r\n\t,\"atc2_reimbursed-inami\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_reimbursed-patient\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_reimbursed-total\" DOUBLE PRECISION   ENCODE RAW\r\n\t,atc2_unit DOUBLE PRECISION   ENCODE RAW\r\n\t,atc2_ddd DOUBLE PRECISION   ENCODE RAW\r\n\t,atc2_patient DOUBLE PRECISION   ENCODE RAW\r\n\t,atc1_code VARCHAR(255)   ENCODE RAW\r\n\t,atc1_en VARCHAR(258)   ENCODE RAW\r\n\t,\"atc1_reimbursed-inami\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_reimbursed-patient\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_reimbursed-total\" DOUBLE PRECISION   ENCODE RAW\r\n\t,atc1_unit DOUBLE PRECISION   ENCODE RAW\r\n\t,atc1_ddd DOUBLE PRECISION   ENCODE RAW\r\n\t,atc1_patient DOUBLE PRECISION   ENCODE RAW\r\n\t,atc4_ddd DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_reimbursed-inami-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_reimbursed-patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_reimbursed-total-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_unit-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_ddd-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc3_patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_reimbursed-inami-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_reimbursed-patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_reimbursed-total-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_unit-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_ddd-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc2_patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_reimbursed-inami-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_reimbursed-patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_reimbursed-total-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_unit-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_ddd-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,\"atc1_patient-avg\" DOUBLE PRECISION   ENCODE RAW\r\n\t,PRIMARY KEY (atc4_code)\r\n)\r\nDISTSTYLE EVEN\r\n;'

                print(re.findall(",PRIMARY KEY \((\w+)\)", teste)[-1])

                sql_columns = re.findall("\n\t[,]*([.\S]+)\s+", teste)

                # Check if the column names agree with the SQL standards. It must not have accented letters or any special character.
                string_check = re.compile('[@\-!#$%^&*+()<>?/\|}{~:]')
                for col_name in sql_columns:
                    if not col_name.isascii() or (string_check.search(col_name) is not None):
                        teste = teste.replace(col_name, f'"{col_name}"')


                print(re.findall("\n\t,({\w*[@\-!#$%^&*+<>?/\|~:]+\w*}+)\s+", teste))

                print(re.findall("\n\t,({\w*[@\-!#$%^&*+()<>?/\|}{~:]+\w*}+)\s+", teste))


                string_check = re.compile('[@\-!#$%^&*+123456789()<>?/\|}{~:]')



                # create_sql = "".join([statement for statement in corrected_query if "CREATE TABLE IF NOT EXISTS".lower() in statement.lower()])
                # create_sql = re.sub("\s\s\s\s*", "\n\t", sqlparse.format(create_sql, reindent=True, keyword_case='upper', strip_comments=True, comma_first=True, wrap_after=1))
                #
                # comment_table_sql = "".join([statement for statement in corrected_query if "COMMENT ON table".lower() in statement.lower()])
                # comment_table_sql = re.sub("\s\s\s\s*", "\n\t", sqlparse.format(comment_table_sql, reindent=True, keyword_case='upper', strip_comments=True, comma_first=True, wrap_after=1))
                #
                # comment_columns_sql = "".join([statement for statement in corrected_query if "COMMENT ON column".lower() in statement.lower()])
                # comment_columns_sql = re.sub("\s\s\s\s*", "\n\t", sqlparse.format(comment_columns_sql, reindent=True, keyword_case='upper', strip_comments=True, comma_first=True, wrap_after=1))
                #
                # foreign_key_sql = "".join([statement for statement in corrected_query if "FOREIGN KEY".lower() in statement.lower()])
                # foreign_key_sql = re.sub("\s\s\s\s*", "\n\t", sqlparse.format(foreign_key_sql, reindent=True, keyword_case='upper', strip_comments=True, comma_first=True, wrap_after=1))
                df = pd.DataFrame({"schema_name": schema,
                                   "table_name": table,
                                   "create_query": create_sql,
                                   "table_description": comment_table_sql.strip(),
                                   "columns_description": comment_columns_sql.strip(),
                                   "foreign_keys": foreign_key_sql.strip()}, index=[1])
                dfs.append(df)

        print("Concatenating")
        ddl_model = pd.concat(dfs, ignore_index=True)

        print("Exporting model to file...")
        ddl_model.to_csv("/opt/project/rcd_pyutils/ddl_model.txt", sep="\t", encoding="utf-8", index=False)
        print("Finished!")

        ddl_model = pd.read_csv("/opt/project/rcd_pyutils/ddl_output/ddl_model.txt", sep="\t", encoding="utf-8")
        ctx = snowflake.connector.connect(user='DAVIBARRETO',
                                          password='Ecclesiasancta!1',
                                          account='xg19634.europe-west4.gcp',
                                          warehouse="COMPUTE_WH",
                                          role="ACCOUNTADMIN",
                                          database="OIP_TEST")
        cs = ctx.cursor()

        # table_description_query = ddl_model[ddl_model.schema_name == "reference"].fillna("").table_description.values
        #
        # table_description_query = [convert_to_snowflake_syntax(command) for command in table_description_query if not re.match(r'^\s*$', command)]
        #
        # col_description_query = ddl_model[ddl_model.schema_name == "reference"].fillna("").columns_description.values
        #
        # col_description_query = ";".join(convert_to_snowflake_syntax(command) for command in col_description_query if not re.match(r'^\s*$', command)).split(";")


        #for command in col_description_query.split(";"):
        #    cs.execute(f"{command};")

        command = f"create or replace TABLE OIP_TEST.ijbfzouefb.PL__DRUGS_MARKET__CHEMOTHERAPY__ACTIVE_SUBSTANCE_AGE__NFZ (" \
                  f"YEAR VARCHAR(8)," \
                  f"MOLECULE VARCHAR(64)," \
                  f"ACTSUB_NAME VARCHAR(128)," \
                  f"ACTSUB_CODE VARCHAR(16)," \
                  f"AGE VARCHAR(16)," \
                  f"PATIENT_NUMBER FLOAT," \
                  f"REFUND FLOAT);"

        command = '--DROP TABLE latam_environment.br__projection_census__ibge;\nCREATE TABLE IF NOT EXISTS latam_environment.br__projection_census__ibge\n(\n\tcode DOUBLE PRECISION   ENCODE RAW\n\t,"year" DOUBLE PRECISION   ENCODE RAW\n\t,age_group VARCHAR(8)   ENCODE lzo\n\t,gender VARCHAR(8)   ENCODE lzo\n\t,population DOUBLE PRECISION   ENCODE RAW\n)\nDISTSTYLE AUTO\n;'

        sqlparse.split(command)

        re.sub("\s\s\s\s*", "\n\t", sqlparse.format(command, reindent=True, keyword_case='upper', strip_comments=True, comma_first = True, wrap_after=1))

        sqlparse.parse(command)

        ifile = open("inputfile.txt", mode='w+')
        ifile.write(sqlparse.split(command)[-1])
        ifile.close()

        command = convert_to_snowflake_syntax(ddl_model.table_description.values[0], no_comments=True)
        try:
            cs.execute(command)
        except snowflake.connector.errors.ProgrammingError as e:
            if "does not exist or not authorized" not in str(e):
                print("oi")

        df = cs.fetch_pandas_all()


        for ddl in ["", "foreign_keys"]:
            queries = ddl_model[ddl_model.schema_name == "reference"].fillna("")[ddl].values
            queries_list = ";".join(convert_to_snowflake_syntax(command) for command in queries if not re.match(r'^\s*$', command)).split(";")

            index = 0
            for command in queries_list:
                log = open("query_log_errors.txt", "a+")
                index += 1
                try:
                    print(index)
                    cs.execute(f"{command.strip()};")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(f"Skipping: {index}")
                    log.write(f"{command}\n")
            log.close()








            aux = 0
            cs.execute("use database OIP_TEST;")
            for command in table_description_query:
                log = open("log_2.txt", "w+")
                aux += 1
                print(aux)
                log.write(command)
                log.close()
                cs.execute(f"{command.strip()};")

            print("Comments done !")

        aux = 0
        cs.execute("use database OIP_TEST;")
        for command in col_description_query:
            log = open("log_2.txt", "a")
            aux += 1
            print(aux)
            try:
                cs.execute(f"{command.strip()};")
            except snowflake.connector.errors.ProgrammingError as e:
                print("skipping")
                log.write(f"{command}\n")

        log.close()


        print("Comments done !")







        corrected_query = ""
        for record in result:
            print(record.tablename)

            line = record.ddl.replace(" ", " ").replace("\'\"", "'").replace("\"\'", "'")
            corrected_query += f"{line}\n"
            print(line)

        output_file = open("/opt/project/rcd_pyutils/database_manager/redshift_2.sql", "w+")
        output_file.write(corrected_query)
        output_file.close()


        queries = [q.strip() for q in corrected_query.split(";") if len(q) > 0]



        commented_lines = [q.strip() for q in queries if "--" in q[:5]]
        create_table_lines = [q.strip() for q in queries if "--" in q[:5]]



        result.close()
    except Exception as msg:
        print("Command skipped: ", msg)

    print(f"🥳Table is copied to redshift from S3.\n")

if __name__ == "__main__":
    main()

#class MyDialect(DefaultDialect):
#    supports_statement_cache = True