# netlink-sap-rfc

Tools for SAP RFC

# Connect

The default .XML files describing the landscape for SAPGUI are used for access via System ID.

### login_sid

Returns a Connection object.

| Parameter | Description                 | Default        |
|-----------|-----------------------------|----------------|
| sysid     | System ID (a.k.a. <SID>)    |                |
| client    | SAP Client (Mandant)        |                |
| passwd    | Password                    |                |
| user      | SAP user ID (BNAME)         | Logged on user |
| language  | Language                    | EN             |
| raw       | Don't convert date / time   | False          |


### sso

Returns a Connection object.

| Parameter | Description                 | Default        |
|-----------|-----------------------------|----------------|
| sysid     | System ID (a.k.a. <SID>)    |                |
| client    | SAP Client (Mandant)        |                |
| user      | SAP user ID (BNAME)         | Logged on user |
| language  | Language                    | EN             |
| raw       | Don't convert date / time   | False          |


 # Connection Object

Use one of the functions above to instantiate.

## Methods

Any Remote enabled Function Module can be called as a method (case-insensitive).

### close()

Close the connection. Should always be called before the program is finished, otherwise an error will be logged on the SAP system.

### select(table, *args, **kwargs)

Get contents of a table using `RFC_READ_TABLE`. Returns a list of Records.

Columns within a Record can be access by index (int), name (case-insensitive), or attribute (case-insensitive).

**table** (required) table name (case-insensitive)

***args** (optional) when specified, only the columns listed will be returned

****kwars** (optional) select rows (only equality is supported)

#### Example

records = rfc_connection.select('t000', 'mtext', 'ort01', mandt='000')

would return a list with one item:

```python
>>> records = c.select('t000', 'mtext', 'ort01', mandt='000')
>>> len(records)
1
>>> records[0][0]
'SAP SE'
>>> records[0][1]
'Walldorf'
>>> records[0]['mtext']
'SAP SE'
>>> records[0]['ort01']
'Walldorf'
>>> records[0].mtext
'SAP SE'
>>> records[0].ort01
'Walldorf'
```



