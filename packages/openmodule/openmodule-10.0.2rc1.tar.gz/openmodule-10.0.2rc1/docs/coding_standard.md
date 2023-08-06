# Openmodule Coding Standard

::: warning
Adhere to the me or the boss will hit you!!!
:::

## Models
* All Messages or RPC requests MUST be defined as pydantic models in either `openmodule/models` or in `src/models` to avoid confusion about datatypes.

* All Models MUST be must inherit `OpenModuleModel` or one of its children

* ZMQ Messages MUST inherit `ZMQMessage`



## Database
* All database models must be defined within either `openmodule/models` or in the directory `src/database`

* All database model names have to end with Model, i.e. TestModel(Base)

* All database interactions MUST be defined in functions under `src/database/database.py`. There are no other access of the database in any other file.

* All functions in `src/database/database.py` MUST have the database/session as first parameter: `def stuff(db, ...)`

* All table names MUST use "_" as separator

* For single object queries only use `query.one()` and `query.first()`