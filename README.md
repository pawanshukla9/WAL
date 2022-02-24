
# Write-Ahead Logging (WAL) Protocol in the Database System for Data Integrity

The objective of our project is to implement the Write-Ahead Logging (WAL) technique to maintain atomicity and durability in database systems. Any changes to the database are first recorded in the log before changes are written to the database. We do not have to flush data to disk in every transaction commit with this procedure, and this is because in case of any crash, we will be able to recover the database using the logs.
