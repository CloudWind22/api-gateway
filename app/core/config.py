#app/core/config.py

WHITELIST = [
    #完全匹配
    {"path": "/docs", "method": "GET"},
    {"path": "/openapi.json", "method": "GET"},
    {"path": "/login", "method": "POST"},
    {"path": "/register", "method": "POST"},

    #前缀匹配(通配)
    {"path": "/public/", "method": "*"},
    {"path": "/static/", "method": "*"}]

