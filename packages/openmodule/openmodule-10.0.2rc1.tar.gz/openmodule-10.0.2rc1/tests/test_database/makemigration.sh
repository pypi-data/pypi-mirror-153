#!/usr/bin/env bash
if [ "$#" -lt 2 ] ; then
  echo "usage: $(basename $0) -m 'migration name'"
  exit 1
fi

# cleanup and environment setup
pushd $(dirname $0)/.. > /dev/null || exit 1
mkdir -p ../sqlite/
rm -f ../sqlite/migration_database.sqlite3

# migrate to head, and make migrations
echo "alembic -c test_database/alembic.ini revision --autogenerate -m ${@:2}"
PYTHONPATH=.:../ alembic -c test_database/alembic.ini upgrade head
PYTHONPATH=.:../ alembic -c test_database/alembic.ini revision --autogenerate -m "${@:2}"
rm -f ../sqlite/migration_database.sqlite3

# sometimes the created migration is immediately broken (e.g. awkward null constraints)
echo "Running migrations to check if they actually work..."
PYTHONPATH=.:../ alembic -c test_database/alembic.ini upgrade head
rm -f ../sqlite/migration_database.sqlite3
