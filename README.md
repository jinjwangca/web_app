## Project Overview
This project offers valuable insights into the US stock market by highlighting the top 20
gainers, losers, and most actively traded tickers. Gain a clearer understanding of market
trends with comprehensive data on the best-performing stocks, those experiencing
significant declines, and the most frequently traded securities in the US market. Utilizing
cutting-edge market intelligence, these unique alternative datasets are designed to elevate
your trading strategies and enhance market research, taking them to the next level.
This project consists of three distinct applications: Web, Data Analyzer, and Data Collector.
The end user interacts with the Web application, which responds with data processed by
the Data Analyzer. The Data Analyzer retrieves data from a database populated by the Data
Collector, and then analyzes and organizes the data into a refined reporting format. Data
Collector collects data from public APIs(Alpha Vantage API) and save the data into
database.

RabbitMQ message queue facilitates communication between the Data Collector and the
Data Analyzer. After each data collection, the Data Collector sends a message to RabbitMQ
message queue to signal the Data Analyzer to perform its analysis.

MongoDB is used to store data retrieved from public APIs because of its flexibility in data
schema. MongoDB is a NoSQL database that stores data in a flexible, JSON-like format.
This allows for easy handling of varying data structures, which is useful when dealing with
diverse and potentially inconsistent data from public APIs.

The applications are hosted on Heroku, a platform as a service (PaaS) that enables
developers to build, run, and operate applications entirely in the cloud.
## Product environment
• https://jinjwang-web-app-f1c83a735e77.herokuapp.com/

• Hosting on Heroku

• Messaging with Rabbitmq using CloudAMQP

• Data persistence with Mongodb

### How to test live application
• Go to https://jinjwang-web-app-f1c83a735e77.herokuapp.com/

• Click the button Top 20 Gainers. It will navigate to a page that displays the top
20 gainers in the US market from the previous trading day.

• Back and click the button Top 20 Losers. It will navigate to a page that displays
the top 20 losers in the US market from the previous trading day.

• Back and click the button Top 20 Most Active Traded Tickers. It will navigate to a
page that displays the top 20 most active traded tickers in the US market from
the previous trading day.

• Metrics is displayed at https://jinjwang-web-appf1c83a735e77.herokuapp.com/metrics

### Web application, basic form, reporting
• HTML pages, CSS, JavaScript

• HTML pages are under folder src/applications/web/templates
### Data collection
• Data collection application fetches data from public API, and saves the data into
Mongodb, then sends a message to RabbitMQ message queue to signal data
analyzer application to analyze data. Data collector is scheduled to run once a
day.

• Data collector interacts with Mongodb by calling CRUD operations implemented
in /src/components/DatabaseGateway.py

• Data collector application is in src/applications/collector/app.py

• The service is run by command: python src/applications/collector/app.py
### Data analyzer
• Data analyzer application retrieves data from Mongodb, then analyzes data and
saves the processed data back into Mongodb. It is triggered by messages in the
RabbitMQ message queue sent by the data collector application.

• Data analyzer interacts with Mongodb by calling CRUD operations implemented
in /src/components/DatabaseGateway.py

• Data analyzer application is in src/applications/analyzer/app.py

• The service is run by command: python src/applications/analyzer/app.py
### Unit test
• Unit tests in src/tests/unit/TestWebAppGetReportData.py (test_get_gainer_data
mocks objects using @patch.object)

• Unit tests in src/tests/unit/TestDatabaseGateway.py
### Data persistence
• Data persistence with mongodb (MongoDB.com)

• Data analyzer and data collection applications interact with Mongodb by calling
CRUD operations implemented in /src/components/DatabaseGateway.py
### API endpoints
• /gainer

• /loser

• /active

• /metrics

• /health-check

• API endpoints are in src/applications/web/app.py
### Integration test
• Integration tests in src/tests/integration/TestWebAp.py
### Using mock objects or any test doubles
• Unit tests in src/tests/unit/TestWebAppGetReportData.py (test_get_gainer_data
mocks objects using @patch.object)
### Production monitoring:
• /metrics uses the prometheus client library to return metrics and 200 OK

• /health endpoint that responds to 200 OK

• Monitor and Metrics Endpoints are implemented in src/applications/web/app.py
### Event collaboration messaging
• Messaging with Rabbitmq using CloudAMQP

• Data collector application fetches data from public API, and saves the data into
Mongodb, then sends a message to rabbitmq message queue to signal data
analyzer application to analyze data.
### Continuous Integration / Continuous Delivery
• For CI, I use github actions to test changes in the main branch.

• For CD, I use Heroku, a platform as a service (PaaS) that enables developers to
build, run, and operate applications entirely in the cloud.

• .github/workflows/deploy.yml
### How to install dependencies
• Start the virtual environment with source env/bin/activate

• Install requirements with pip install -r requirements.txt

• Get the environment variables

i) MONGODBURI

ii) RABBITMQURL

iii) TRADEINFOURL
https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apik
ey=demo

iv) PYTHONPATH env var value needs to be src
### How to run unit tests and integration tests
• Install dependencies

• python src/tests/unit/TestWebAppGetReportData.py

• python src/tests/unit/TestDatabaseGateway.py

• Go to src/tests/integration/, then run pytest TestWebAp.py
### How to run servers
• web: gunicorn src.applications.web.app:app

• analyzer: python3 src/applications/analyzer/app.py

• collector: python3 src/applications/collector/app.py

When deploying to production using Heroku, Heroku starts each process with
commands defined in Procfile