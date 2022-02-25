
# Write-Ahead Logging (WAL) Protocol in the Database System 

The objective of our project is to implement the Write-Ahead Logging (WAL) technique to maintain atomicity and durability in database systems. Any changes to the database are first recorded in the log before changes are written to the database. We do not have to flush data to disk in every transaction commit with this procedure, and this is because in case of any crash, we will be able to recover the database using the logs.

Problem Statement:

If a program is in the middle of performing some operation and the machine it runs loses power, the program would need necessary information whether the process was only fully or partially succeeded or failed when the machine restarted. If a write-ahead log is used in such a scenario, the program can check these logs and compare what it was supposed to be doing to what was actually done. 

Based on this comparison, the program could decide to either undo or complete the operation it had started or keep things as they are. Therefore, the transaction gets persisted in the log first. The data files can be rolled forward or rolled back in the event of an abrupt shutdown.

References:
[1] “Documentation: 9.1: Write-Ahead Logging (WAL).” PostgreSQL, https://www.postgresql.org/docs/9.1/wal-intro.html.
[2] “Writing A Database: Part 2 — Write Ahead Log | by Daniel Chia.” Medium, 21 September 2017, https://medium.com/@daniel.chia/writing-a-database-part-2-write-ahead-log-2463f5cec67a.

