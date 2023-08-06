import os
import re
from typing import List

import pandas as pd
import snowflake.connector
import sqlparse

from .redshift_operator import RedshiftOperator
from ..sql_utils import convert_to_snowflake_syntax


def migrate_metadata_from_redshift(
    rs_db: str,
    sf_db: str,
    schemas_list: List = [],
    tables_list: List = [],
    create_tables: bool = False,
    logging: bool = True,
    verbose: bool = True,
):
    print("Starting the metadata migration process | Redshift -> Snowflake")
    ro = RedshiftOperator(database=rs_db)
    ddl_model = ro.get_DDL(
        verbose=verbose, schema_names=schemas_list, table_names=tables_list
    )
    ddl_model.fillna("", inplace=True)

    if schemas_list != []:
        ddl_model = ddl_model[ddl_model.schema_name.isin(schemas_list)]
    if tables_list != []:
        ddl_model = ddl_model[ddl_model.table_name.isin(tables_list)]

    print("Connecting to Snowflake...")
    sf = SnowflakeOperator(snowflake_database=sf_db.upper())
    print("Done!")

    if logging:
        if os.path.exists("query_log_errors.txt"):
            os.remove("query_log_errors.txt")

    if create_tables:
        print("Creating tables if they don't already exist...")
        # Some of these corrections below must be done because 'year', 'level', 'region', 'names' are SQL Syntax Names
        # and AWS parse them as strings when creating the column names. However, Snowflake parses it otherwise because
        # it can distinguish the column names and the SQL Variables as different things.
        ddl_model.create_query = ddl_model.create_query.apply(
            lambda x: x.replace('"year"', "year ")
            .replace('"level" ', "level ")
            .replace('"region" ', "region ")
            .replace('"names" ', "names ")
            .replace('"type" ', "type ")
            .replace('"role" ', "role ")
            .replace('"provider" ', "provider ")
            .replace('"location" ', "location ")
        )
        sf.execute_metadata_query(
            ddl_model.create_query.values, logging=logging, correct_syntax=True
        )

    print("Migrating Table Descriptions...")
    sf.execute_metadata_query(ddl_model.table_description.values, logging=logging)

    print("Migrating Columns Descriptions...")
    ddl_model.columns_description = ddl_model.columns_description.apply(
        lambda x: x.replace('."year"', ".year")
        .replace('."level"', ".level")
        .replace('."region"', ".region")
        .replace('."names"', ".names")
        .replace('."type"', ".type")
        .replace('."role"', ".role")
        .replace('."provider"', ".provider")
        .replace('."location"', ".location ")
    )
    sf.execute_metadata_query(ddl_model.columns_description.values, logging=logging)

    print("Migrating Primary Keys...")
    sf.execute_key_query(ddl_model, key="primary", logging=logging)

    print("Migrating Unique Keys...")
    sf.execute_key_query(ddl_model, key="unique", logging=logging)

    print("Migrating Foreign Keys...")
    sf.execute_metadata_query(ddl_model.foreign_keys.values, logging=logging)

    sf.conn.cursor().close()
    sf.conn.close()
    print("All metadata have been migrated successfully !")


# def update_to_snowflake(self):
#     snow = SnowflakeOperator()
#     print("process prices")
#     snow.conn.cursor().execute(f"""    delete from OIP_PREMIUM.PRICE_TRACKER.drug_prices where (global_drug_id LIKE '{self.country_code}%');
#     """)
#     snow.copy_from_S3(s3_prefix=os.path.join("udm", "price_tracker"), s3_file=f"{self.country_code}__drug_prices",
#               database="OIP_PREMIUM", schema="PRICE_TRACKER", table="drug_prices")
#     print("process products")
#     snow.conn.cursor().execute(f"""    delete from OIP_PREMIUM.PRICE_TRACKER.drug_products where (global_drug_id LIKE '{self.country_code}%');
#     """)
#     snow.copy_from_S3(s3_prefix=os.path.join("udm", "price_tracker"), s3_file=f"{self.country_code}__drug_products",
#               database="OIP_PREMIUM", schema="PRICE_TRACKER", table="drug_products")


class SnowflakeOperator:
    def __init__(
        self,
        snowflake_user=None,
        snowflake_password=None,
        snowflake_account=None,
        snowflake_warehouse=None,
        snowflake_role=None,
        snowflake_database=None,
    ) -> None:

        self.snowflake_user = (
            os.environ.get("SNOWFLAKE_USER")
            if snowflake_user is None
            else snowflake_user.upper()
        )
        self.snowflake_password = (
            os.environ.get("SNOWFLAKE_PASSWORD")
            if snowflake_password is None
            else snowflake_password
        )
        self.snowflake_account = (
            os.environ.get("SNOWFLAKE_ACCOUNT")
            if snowflake_account is None
            else snowflake_account.upper()
        )
        self.snowflake_warehouse = (
            os.environ.get("SNOWFLAKE_WAREHOUSE")
            if snowflake_warehouse is None
            else snowflake_warehouse.upper()
        )
        self.snowflake_role = (
            os.environ.get("SNOWFLAKE_ROLE")
            if snowflake_role is None
            else snowflake_role.upper()
        )
        self.snowflake_database = (
            os.environ.get("SNOWFLAKE_DATABASE")
            if snowflake_database is None
            else snowflake_database.upper()
        )

        self.conn = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account,
            warehouse=self.snowflake_warehouse,
            role=self.snowflake_role,
            database=self.snowflake_database,
        )

    def truncate(self, database, schema, table):
        sql = f"truncate table {database}.{schema}.{table} ;"
        self.conn.cursor().execute(sql)

    def copy_from_S3(self, s3_prefix, s3_file, database, schema, table):
        self.conn.cursor().execute(
            f"""
            COPY INTO {database}.{schema}.{table} 
            FROM s3://{os.environ.get("S3_DATAMART_BUCKET")}/{s3_prefix}/{s3_file}
            CREDENTIALS = (
            aws_key_id='{os.environ.get("AWS_ACCESS_KEY_ID")}',
            aws_secret_key='{os.environ.get("AWS_SECRET_ACCESS_KEY")}'
            )
            FILE_FORMAT=(field_delimiter='|', SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"', NULL_IF=(''))
            FORCE = TRUE
            """
            )

    def correct_syntax(self, query: str, no_comments: bool = False) -> str:
        """
        Also, snowflake has a specific SQL syntax. If we get a SQL from another SGBD, we must firstly
        correct the syntax into the snowflake constraints.

        Args:
            query: String containing the SQL script.
            no_comments:

        Returns: The same query but snowflake-compatible.
        """
        return convert_to_snowflake_syntax(query, no_comments)

    def execute_metadata_query(
        self, query: List[str], logging: bool = False, correct_syntax=False
    ):
        # The snowflake python API allows only one command per request. That's why we must split the input query into
        # a list of commands.
        # Also, snowflake has a specific SQL syntax. If we get a SQL from another database manager, we must firstly
        # correct the syntax into the snowflake constraints.
        if correct_syntax:
            queries_list = "".join(
                self.correct_syntax(command)
                for command in query
                if not re.match(r"^\s*$", command)
            )
        else:
            queries_list = "".join(
                command for command in query if not re.match(r"^\s*$", command)
            )
        queries_list = sqlparse.split(queries_list)

        for command in queries_list:
            try:
                self.conn.cursor().execute(f"{command.strip()};")
            except snowflake.connector.errors.ProgrammingError as e:
                if ("does not exist or not authorized" not in str(e)) or (
                    "Empty SQL statement" not in str(e)
                ):
                    if logging:
                        print(
                            f"Problem found. Skipping command. Check the query_log_errors.txt for more details."
                        )
                        log_file = open("query_log_errors.txt", "a+")
                        log_file.write(f"{command}\n")
                        print(e)
                        log_file.close()
                    else:
                        print(f"Problem found. Skipping command...")

    def execute_key_query(
        self, df: pd.DataFrame, key: str = "primary", logging: bool = False
    ):
        for row in range(len(df)):
            if key == "primary":
                if df.iloc[row, 2] != "":
                    drop_key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} DROP PRIMARY KEY;"
                    key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} ADD PRIMARY KEY ({df.iloc[row, 2]});"
                    skip = False
                else:
                    skip = True

            elif key == "unique":
                if (df.iloc[row, 3] != "") and (df.iloc[row, 3] != df.iloc[row, 2]):
                    drop_key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} DROP UNIQUE ({df.iloc[row, 3]});"
                    key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} ADD UNIQUE ({df.iloc[row, 3]});"
                    skip = False
                else:
                    skip = True

            if not skip:
                try:
                    self.conn.cursor().execute(key_query)
                except snowflake.connector.errors.ProgrammingError as e:
                    if "already exists" in str(e):
                        self.conn.cursor().execute(drop_key_query)
                        self.conn.cursor().execute(key_query)
                    else:
                        if ("does not exist or not authorized" not in str(e)) or (
                            "Empty SQL statement" not in str(e)
                        ):
                            if logging:
                                print(
                                    f"Problem found. Skipping command. Check the query_log_errors.txt for more details."
                                )
                                log_file = open("query_log_errors.txt", "a+")
                                log_file.write(f"{key_query}\n")
                                print(e)
                                log_file.close()
                            else:
                                print(f"Problem found. Skipping command...")
