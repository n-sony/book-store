export FLASK_APP="cli:create"
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade
flask seed-db