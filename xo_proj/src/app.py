#app.py
from os import getenv
from flask import Flask
from web.route import routes
from domain.service import MinimaxGameService
from datasource.repository import GameRepository
from di.container import Container
from prometheus_flask_exporter import PrometheusMetrics
from flask_jwt_extended import JWTManager


#from datasource.sql.sql_service import SQLService


#SQLService.run()
repository = GameRepository()
Container.register('repository', repository)
service = MinimaxGameService()
Container.register('service', service)

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
# Настроим Prometheus metrics, обязательно до Blueprint
metrics = PrometheusMetrics(app)


# JWT
app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')  # секрет для подписи JWT, желательно вынести в .env
jwt = JWTManager(app)

app.secret_key = getenv('SECRET_KEY')  # Для создания и защиты сессий фласк
#Регистрируем Blueprint в основном приложении
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
