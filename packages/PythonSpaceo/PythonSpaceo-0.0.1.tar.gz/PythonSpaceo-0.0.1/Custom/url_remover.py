# Remove url - which you don't want to show in swagger
def preprocessing_filter_spec(endpoints):
    filtered = []
    for (path, path_regex, method, callback) in endpoints:
        if not path.endswith("/json") and not path.endswith("/yaml") and not path.endswith("/auth/post/ajax/friend/") and not path.endswith("/user-authentication/verify-email")  and not path.endswith("/api/schema/"):
            filtered.append((path, path_regex, method, callback))
    return filtered