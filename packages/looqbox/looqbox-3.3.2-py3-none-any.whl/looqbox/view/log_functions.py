from looqbox.global_calling import GlobalCalling


__all__ = ["log_query"]


def log_query(*args):
    query_list = GlobalCalling.looq.query_list
    queries = [*args]

    for query in queries:
        query_list = query_list.append(query)

    print(query_list)