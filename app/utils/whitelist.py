#app/utils/is_whitelisted.py

from app.core.config import WHITELIST

def is_whitelisted(path: str, method: str)->bool:
    for rule in WHITELIST:
        rule_path = rule['path']
        rule_method = rule['method']

        method_match = (rule_method == "*" or rule_method == method)

        if rule_path.endswith('/'):
            #前缀匹配
            path_match = path.startswith(rule_path)
        else:
            #精确匹配
            path_match = (rule_path == path)
        
        if method_match and path_match:
            return True
    
    return False

