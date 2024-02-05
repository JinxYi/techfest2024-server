import mysql.connector

def create_mysql_table():
    # Replace these values with your MySQL server information
    host = "localhost"
    user = "root"
    password = "root1234"

    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )

    # Create a cursor object to interact with the MySQL server
    cursor = connection.cursor()

    # Define the name of the database to be created
    database_name = "flashcard_db"

    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    # Switch to the newly created database
    cursor.execute(f"USE {database_name}")

    # Define the SQL query to create a table within the database
    create_table_query =  """
    CREATE TABLE IF NOT EXISTS flashcards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        question TEXT,
        answer TEXT
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit the changes to the MySQL server
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_mysql_table()
    print("Database and table has been created")