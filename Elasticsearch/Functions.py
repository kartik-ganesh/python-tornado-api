import elasticsearch

es = elasticsearch.Elasticsearch()


def find_all_es():
    res = es.search(index="employee", body={"query": {"match_all": {}}})['hits']['hits']
    if res:
        return res
    else:
        return None


def find_by_id_es(id):
    res = es.search(index="employee", body={"query": {"match": {"id": id}}})['hits']['hits']
    print(res)
    if res:
        return res[0]["_source"]
    else:
        return None


def find_by_name_es(name):
    res = es.search(index="employee", body={"query": {"match": {"name": name}}})['hits']['hits']
    return res


def post_in_es(new_entry):
    es.index(index="employee", doc_type="employee", id=new_entry['id'], body=new_entry)
    return True


def delete_by_id_es(id):
    if find_by_id_es(id) is None:
        return False
    es.delete(index="employee", doc_type="employee", id=id)
    return True


def update_by_id_es(id, new_entry):
    if find_by_id_es(id) is None:
        return False
    es.update(index="employee", doc_type="employee", id=id, body={"doc": new_entry})
    return True
