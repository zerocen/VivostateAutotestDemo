# VivostateAutotestDemo

A automation testing framework demo.

## Technology

### Web UI Test

- pytest + selenium + yaml + allure, Page Object Model
- Data-driven testing and Keyword-driven testing

### API Test
- pytest + requests + yaml + allure, Page Object Modeling Way
- Data-driven testing


## Directory Structure

- **api_test**: API Test Code
    - *api*: API encapsulation code
    - *test_case*: Test case code

- **web_test**: Web Test Code
    - *page*: Web page object encapsulation code
    - *test_case*: Test case code

- **data**
    - *api*: API test case data
    - *page* Web test case data and keyword-driven data

- **utils**: Utility classes like configuration loader, yaml files loader and logger. 

- **config.yml**: Framework configuration file.

- **pytest.ini**: pytest configuration file.

- **runner.py**: The script for launching test.