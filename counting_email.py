import sqlite3
import re

conn = sqlite3.connect("email_org.sqlite")
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS Counts
""")

cur.execute("""
    CREATE TABLE Counts (org TEXT, count INTEGER)
""")

fname = input("Enter file name: ")
if (len(fname) < 1): fname = "mbox.txt"
fh = open(fname)
for line in fh:
    if not line.startswith("From:"): continue
    match = re.search(r"@(\S+)", line)
    if not match: continue    
    domain = match.group()[1:]
    print(domain)
    cur.execute("SELECT count FROM Counts WHERE org = ?", (domain,))
    row = cur.fetchone()
    if row is None:
        cur.execute("""
            INSERT INTO Counts (org, count) 
            VALUES (?, 1)
        """, (domain,))
    else:
        cur.execute("""
            UPDATE Counts SET count = count + 1 WHERE org = ?
        """, (domain,))
    conn.commit()

print("Creating report")
sqlstr = "SELECT org, count FROM Counts ORDER BY count DESC"

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

conn.close()

print("Finished")
