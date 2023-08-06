import logstash


def stash_logging_handler(app):
    # logstash_handler
    # stash_handler = logstash.LogstashHandler(app.config.get('ELK_HOST'), app.config.get('ELK_PORT'))
    stash_handler = logstash.LogstashHandler("127.0.0.1", 5959, tags="dz")
    return stash_handler
