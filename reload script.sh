dropdb djdb
createdb djdb
psql -U nick -d djdb  -c 'CREATE EXTENSION btree_gist;'
rm -rf clinica/migrations/
python manage.py makemigrations clinica
python manage.py migrate