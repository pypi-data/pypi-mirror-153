from rrdata.common import engine
from rrdata.common import read_df_from_table

def update_sql_table_from_df(df,table_name, con=engine(db_name='rrdata')): #TODO
    # Create the temporary table using pandas (can speed this up with method above if needed)
    df.to_sql('temporary_table', con=con, if_exists='replace')
    # Define a string that will run as a SQL command when executed
    # uses SQL UPDATE to update table_to_be_updated from temporary_table
    sql = f"""
        UPDATE {table_name} AS f
        SET col1 = t.col1
        FROM temporary_table AS t
        WHERE f.id = t.id
    """
    with engine().begin() as conn:     
        conn.execute(sql)
        print(f"update {table_name} with df finish!")


if __name__ == "__main__":
    
    data = read_df_from_table('stock_list_tspro')
    update_sql_table_from_df(data,'stock_list_test')