:: pytest -s --html=report.html --self-contained-html
:: or
:: pytest -s --html=report.html --self-contained-html -m xiaobai_web
:: 报告在当前目录生产
pytest -s --html=report.html --self-contained-html -o log_cli=true -o log_cli_level=INFO