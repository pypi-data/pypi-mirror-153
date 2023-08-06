# Syngenta Digital DTA (Database Adapter)
A DRY multi-database normalizer.

## Features

  * Use the same package with multiple database engines
  * Able to validate your data against predefined schema in code (for no-schemas solutions)
  * Creates easy pub-sub architecture based on model changes
  * Local development support

## Philosophy

The dta philosophy is to use one pattern with multiple databases

The dta encourages pub-sub architecture by allowing for the automatic publishing of data over SNS.

## Installation

This is a [python](https://www.python.org/) module available through the
[pypi registry](https://pypi.org).

Before installing, [download and install python](https://www.python.org/downloads/).
python 3 or higher is required.

Installation is done using the
[`pip install`](https://packaging.python.org/tutorials/installing-packages/) command:

```bash
$ pip install syngenta_digital_dta
```

or

```bash
$ pipenv install syngenta_digital_dta
```

## Common Usage: DynamoDB

```python
import os
import syngenta_digital_dta

adapter = syngenta_digital_dta.adapter(
    engine='dynamodb',
    table=os.getenv('DYNAMODB_TABLE'),
    endpoint='http://localhost:4000',
    model_schema='v1-table-model',
    model_schema_file='application/openapi.yml',
    model_identifier='test_id',
    model_version_key='modified'
)
```

**Initialize Options**

Option Name              | Required | Type   | Description
:-----------             | :------- | :----- | :----------
`engine`                 | true     | string | name of supported db engine (dynamodb)
`table`                  | true     | string | name of dynamodb table
`endpoint`               | false    | string | url of the dynamodb table (useful for local development)
`model_schema`           | true     | string | key of openapi schema this is being set against
`model_schema_file`      | true     | string | path where your schema file can found (accepts JSON as well)
`model_identifier`       | true     | string | unique identifier key on the model
`model_version_key`      | true     | string | key that can be used as a version key (modified timestamps often suffice)
`author_identifier`      | false    | string | unique identifier of the author who made the change (optional)
`sns_arn`                | false    | string | sns topic arn you want to broadcast the changes to
`sns_attributes`         | false    | dict   | custom attributes in dict format; values should only be strings or numbers
`sns_default_attributes` | false    | boolean| determines if default sns attributes are included in sns message (model_identifier, model_version_key, model_schema, author_identifier)

**Examples**

### DynamoDB Create

```python
result = adapter.create(
	operation='insert', # or overwrite (optional); defaults to insert
	data=some_dict_to_insert_into_the_table,
)

result = adapter.insert(data=some_dict_to_insert_into_the_table) # alias
```

### DynamoDB Read

```python
result = adapter.read(
    operation='get', # or query or scan (optional); defaults to get
	query={
	   'Key': {
	        'example_id': '3'
	   }
    }
)

result = adapter.get(
	query={
	   'Key': {
	        'example_id': '3'
	   }
    }
)

results = adapter.read(
    operation='query',
    query={
        'IndexName': 'test_query_id',
        'Limit': 1,
        'KeyConditionExpression': 'test_query_id = :test_query_id',
        'ExpressionAttributeValues': {
            ':test_query_id': 'def345'
        }
    }
)
```

### DynamoDB Update

```python
result = adapter.update(
	data=some_dict_to_update_the_model,
	operation='get',
	query={
	   'Key': {
	        'example_id': '3'
	   }
    }
)
```

### DynamoDB Delete

```python
result = adapter.delete(
	query={
	   'Key': {
	        'example_id': '3'
	   }
    }
)
```

## Common Usage: Postgres & Redshift

```python
import os
import syngenta_digital_dta

adapter = syngenta_digital_dta.adapter(
    engine='postgres', # or redshift
    table='users',
    endpoint='localhost',
    database='dta',
    port=5439, # 5432 for redshift
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    model_schema='test-postgres-user-model',
    model_schema_file='tests/openapi.yml',
    model_identifier='user_id',
    model_version_key='modified',
    relationships={
        'addresses': 'user_id'
    }
)
```

**Initialize Options**

Option Name              | Required | Type   | Description
:-----------             | :------- | :----- | :----------
`engine`                 | true     | string | name of supported db engine (dynamodb)
`table`                  | true     | string | name of postgres table to work as primary query point
`endpoint`               | true     | string | url of the postgres cluster
`database`               | true     | string | name of the database to connect to
`port`                   | true     | int    | port of database (defaults to 5439)
`user`                   | true     | string | username for database access
`password`               | true     | string | password for database access
`model_schema`           | true     | string | key of openapi schema this is being set against
`model_schema_file`      | true     | string | path where your schema file can found (accepts JSON as well)
`model_identifier`       | true     | string | unique identifier key on the model
`model_version_key`      | true     | string | key that can be used as a version key (modified timestamps often suffice)
`autocommit`             | false    | boolean| will commit transactions automatically without direct call
`relationships`          | false    | dict   | key is the table with the relationship and value is the foreign key on that table (assumes your primary key name is equal to that table's foreign key)
`author_identifier`      | false    | string | unique identifier of the author who made the change (optional)
`sns_arn`                | false    | string | sns topic arn you want to broadcast the changes to
`sns_attributes`         | false    | dict   | custom attributes in dict format; values should only be strings or numbers
`sns_default_attributes` | false    | boolean| determines if default sns attributes are included in sns message (model_identifier, model_version_key, model_schema, author_identifier)[default: true]

**Examples**

### Postgres/Reshift Connect

```python
# will always pool and share connections
self.user_adapter.connect()
```

### Postgres/Reshift Create

```python
data = {
    'user_id': str(uuid.uuid4()),
    'email': 'somen.user@some-email.com',
    'first': 'Some',
    'last': 'User'
}
result = self.user_adapter.create(data=data, commit=True)
result = self.user_adapter.insert(data=data, commit=True) # alias
```

### Postgres/Reshift Update

```python
data = {
    'user_id': 'some-update-guid',
    'email': 'somen.user@some-email.com',
    'first': 'Some',
    'last': 'User'
}
result = self.user_adapter.update(data=data, commit=True)
```

### Postgres/Reshift Upsert

```python
data = {
    'user_id': 'some-update-guid',
    'email': 'somen.user@some-email.com',
    'first': 'Some',
    'last': 'User'
}
result = self.user_adapter.upsert(data=data, commit=True)
```

### Postgres/Reshift Delete

```python
self.user_adapter.delete('some-delete-guid', commit=True)
```

### Postgres/Reshift Read

```python
# will only return 1 row or None
result = self.user_adapter.read('some-read-guid')
result = self.user_adapter.get('some-read-guid') # alias

# all fields optional (defaults to SELECT * FROM {table} ORDER BY {model_identifier} ASC LIMIT 1000)
results = self.user_adapter.read_all(
    where={
        'first': 'first',
        'last': 'last',
    },
    limit=2,
    offset=1,
    orderby_column='first',
    orderby_sort='DESC'
)

# limited to get 1 relationship at a time
results = self.user_adapter.get_relationship('addresses', where={'user_id': 'some-user-relationship-guid'})

# only will allow read-only operations
# query and params are required; params can be empty dict
results = self.user_adapter.query(
    query='SELECT * FROM users WHERE user_id = %(identifier_value)s',
    params={
        'identifier_value':'some-query-relationship-guid'
    }
)
```

## Common Usage: Elasticsearch

```python
import os
import syngenta_digital_dta

# localhost connection
adapter = syngenta_digital_dta.adapter(
    engine='elasticsearch',
    index='users',
    endpoint='localhost',
    model_schema='test-elasticsearch-user-model',
    model_schema_file='tests/openapi.yml',
    model_identifier='user_id',
    model_version_key='modified'
)

# lambda connection (assumes lambda role has access)
adapter = syngenta_digital_dta.adapter(
    engine='elasticsearch',
    index='users',
    endpoint='localhost',
    model_schema='test-elasticsearch-user-model',
    model_schema_file='tests/openapi.yml',
    model_identifier='user_id',
    model_version_key='modified',
    authentication='lambda'
)

# traditional user password connection
adapter = syngenta_digital_dta.adapter(
    engine='elasticsearch',
    index='users',
    endpoint='localhost',
    model_schema='test-elasticsearch-user-model',
    model_schema_file='tests/openapi.yml',
    model_identifier='user_id',
    model_version_key='modified',
    authentication='user-password',
    user='root',
    password='root'
)
```

**Initialize Options**

Option Name              | Required | Type   | Description
:-----------             | :------- | :----- | :----------
`engine`                 | true     | string | name of supported db engine (dynamodb)
`index`                  | true     | string | name of postgres table to work as primary query point
`endpoint`               | true     | string | url of the postgres cluster
`model_schema`           | true     | string | key of openapi schema this is being set against
`model_schema_file`      | true     | string | path where your schema file can found (accepts JSON as well)
`model_identifier`       | true     | string | unique identifier key on the model
`model_version_key`      | true     | string | key that can be used as a version key (modified timestamps often suffice)
`port`                   | false    | int    | port of database (defaults to 9200 if localhost or 443 if not)
`author_identifier`      | false    | string | unique identifier of the author who made the change (optional)
`authentication`         | false    | string | either 'lamnbda' or 'user-password'
`user`                   | false    | string | only needed if authentication is user-password
`password`               | false    | string | only needed if authentication is user-password
`sns_arn`                | false    | string | sns topic arn you want to broadcast the changes to
`sns_attributes`         | false    | dict   | custom attributes in dict format; values should only be strings or numbers
`sns_default_attributes` | false    | boolean| determines if default sns attributes are included in sns message (model_identifier, model_version_key, model_schema, author_identifier) [default: true]


### Elasticsearch Connection

```python
# elasticsearch is auto-connected to a shared connection; use this to test that connection
self.adapter.connection.ping()
```

### Elasticsearch Set-up

```python
# will convert openapi schema, defined in init, to a mapping
self.adapter.create_template(
    name='users',
    index_patterns='users-*',
    special={'phone': 'keyword'} # (optional) can send mapping of special types otherwise will default based on schema type
)

# will use sensible defaults or you can pass in a custom settings kwargs['settings']
self.adapter.create_index(settings=some_optional_settings)
```

**OpenAPI Default Conversion**

OpenAPI Type                | Elasticsearch Mapping
:-----------                | :--------------------
array                       | none (not needed to be included)
array of objects            | nested
boolean                     | boolean
integer                     | integer
number                      | long
object (with properties)    | object
object (without properties) | flattened
string (no format)          | text
string (format date)        | date (with iso date format acceptance)
string (format date-time)   | date (with iso date format acceptance)
string (format email)       | text (with url email analyzer)
string (format ip)          | ip
string (format hostname)    | text (with url email analyzer)
string (format iri)         | text (with url email analyzer)
string (format url)         | text (with url email analyzer)


### Elasticsearch Create

```python
data = {
    'user_id': uuid.uuid4().hex,
    'email': 'somen.user@some-email.com',
    'first': 'Some',
    'last': 'User',
    'phone': 1112224444
}
self.adapter.create(data=data, refresh=True) # (optional) refresh defaults to True
```


### Elasticsearch Update

```python
updated_data = {
    'user_id': user_id,
    'email': 'peter.cruse@some-email.com',
    'first': 'Peter'
}
self.adapter.update(data=updated_data, refresh=True) # (optional) refresh defaults to True
```

### Elasticsearch Upsert

```python
data = {
    'user_id': upsert_id,
    'email': 'somen.user-upsert@some-email.com',
    'first': 'Some',
    'last': 'User',
    'phone': 1112224444
}
self.adapter.upsert(data=data, refresh=True) # (optional) refresh defaults to True
```

### Elasticsearch Delete

```python
self.adapter.delete(delete_id, refresh=True) # (optional) refresh defaults to True
```

### Elasticsearch Read

```python
response = self.adapter.get(get_id)

# returns single dictionary mapped to openapi model defined in init (or empty dict)
dict_response = self.adapter.get(get_id, normalize=True) # (optional) normalize defaults to False

# returns list of dictionaries mapped to openapi model defined in init (or empty array)
list_response = self.adapter.query(
    normalize=True, # (optional) normalize defaults to False
    query={
        'match': {
            'first': 'Normal'
        }
    }
)
```

## Common Usage: S3
```python
adapter = syngenta_digital_dta.adapter(
    engine='s3',
    endpoint=self.endpoint,
    bucket=self.bucket
)
```

**Initialize Options**

Option Name              | Required | Type   | Description
:-----------             | :------- | :----- | :----------
`engine`                 | true     | string | name of supported db engine (s3)
`bucket`                 | true     | string | name of bucket you are interfacing with
`endpoint`               | true     | string | url of the s3 endpoint (useful for local development)
`sns_arn`                | false    | string | sns topic arn you want to broadcast the changes to
`sns_attributes`         | false    | dict   | custom attributes in dict format; values should only be strings or numbers

`NOTE`: If you use the SNS functionality, all SNS messages are sent presigned urls for S3, not the actual data itself given the SNS message size limitations. Below is an an example payload:

```json
{
    "presigned_url": "https://some-s3-url"
}
```

### S3 Create (Single)

```python
# automatically converts dicts to json with flag
adapter.create(
    s3_path='test/test-create.json',
    data={'test': True},
    json=True
)
```

### S3 Create (Multipart)

```python
file = open('./tests/mock/example.json')
chunks = []
for piece in iter(file.read(6000000), ''):
    chunks.append(piece)
adapter.multipart_upload(chunks=chunks, s3_path='test/test-create.json')
```

### S3 Create (Stream)
```python
url = 'https://github.com/syngenta-digital/package-python-dta/archive/refs/heads/master.zip'
response = requests.get(url, stream=True)
self.adapter.upload_stream(data=response.content, s3_path='test/code-clone.zip')
```

### S3 Create (Pre-Signed UPLOAD URLs)

```python
presigned_upload_url = adapter.create_presigned_post_url(s3_path='test/test-create.json', expiration=3600)
```

### S3 Read (In Memory)

```python
# automatically converts json to dict with flag
result = adapter.read(
    s3_path='test/test-create.json',
    json=True
)
```

### S3 Read (Download to Disk)

```python
# automatically creates directory and child directories
file_path = adapter.download(s3_path='test/test-create.json', download_path='/tmp/unit-test-download/test.json')
```

### S3 Read (Pre-Signed URLs)

```python
presigned_url = adapter.create_presigned_read_url(s3_path='test/test-create.json', expiration=3600)
```

### S3 Delete

```python
adapter.delete(s3_path='test/test-create.json')
```


## Contributing
If you would like to contribute please make sure to follow the established patterns and unit test your code:

### Local Unit Testing

- In one tab, run `pipenv run local`
- In a second tab, run `RUN_MODE=unittest python -m unittest discover`
