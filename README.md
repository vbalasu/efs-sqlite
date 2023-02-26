# efs-sqlite

Completely serverless relational database powered by SQLite, EFS and AWS Lambda (Chalice).

You can visit it at the following location: 

https://19cx2ehing.execute-api.us-east-1.amazonaws.com/api/

The user is prompted to sign in with Google. Then the id token is passed along with a SQL query and database file path to the server.

On the server side, the database is opened from EFS (AWS Elastic File System), and the results are returned.

On the client side, the JSON response is parsed and displayed in a Handsontable spreadsheet

Key components:

- [app.py](app.py)
- [chalicelib/index.html](chalicelib/index.html)
- [.chalice/config.json](.chalice/config.json)