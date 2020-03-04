import json
import logging
import tornado.options
from Elasticsearch.Functions import post_in_es, find_all_es, find_by_id_es, find_by_name_es, delete_by_id_es, \
    update_by_id_es
from MySQL.Functions import *
from Redis.Functions import *
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler


class Api:
    def __init__(self, run_for_tests=False):
        url = [(r"/api/users", Handler),
               (r"/api/users/([0-9]+)", HandlerWithId)]
        tornado.options.parse_command_line()
        Application(url).listen(8080)
        if run_for_tests:
            IOLoop.instance().add_callback(IOLoop.instance().stop)
            IOLoop.instance().start()
        else:
            IOLoop.instance().start()


class HandlerWithId(RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self, id):
        redis_user = find_by_id_redis(id)
        sql_user = find_by_id_sql(id)
        es_user = find_by_id_es(id)
        if redis_user is None and sql_user is None and es_user is None:
            logging.warn("Tried to search by id that doesnt exist")
            self.write("Entry doesnt exist")
        else:
            logging.info("Showing entry by id")
            user = find_by_id_sql(id)
            self.write("MYSQL\n")
            self.write({"id": user.id, "name": user.name})
            self.write("\nREDIS\n")
            self.write(redis_user)
            self.write("\nELASTIC SEARCH\n")
            self.write(es_user)

    def delete(self, id):
        try:
            if delete_by_id_redis(id) and delete_by_id_sql(id) and delete_by_id_es(id):
                logging.info("Deleted entry by id")
                self.write("Deleted entry with id : " + id)
            else:
                logging.warn("Tried to delete by id that doesnt exist")
                self.write("Entry Doesn't Exist")
        except Exception as e:
            self.write(("Cannot DELETE Exception : " + str(e)))

    def put(self, id):
        new_entry = json.loads(self.request.body)
        if find_by_id_es(id) is None and find_by_id_redis(id) is None and find_by_id_sql(id) is None:
            logging.warn("Tried to update entry that doesnt exist")
            self.write("Entry Doesn't Exist")
        elif int(new_entry['id']) != int(id):
            logging.warn("Tried to change id while updating")
            self.write("Cannot change id")
        elif not new_entry.has_key('name') or not new_entry.has_key('id'):
            logging.warn("Entered invalid body")
            self.write("Invalid Body")
        elif update_by_id_redis(id, new_entry) and update_by_id_sql(id, new_entry) and update_by_id_es(id, new_entry):
            logging.info("Updated Entry")
            self.write("Updated Entry")
        elif new_entry['name'] is None or new_entry['id'] is None:
            logging.info("Tried to update with field empty")
            self.write("Can't be left empty")


class Handler(RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        id_param = self.get_argument(name='id', default=None, strip=True)
        name_param = self.get_argument(name='name', default=None, strip=True)

        # FOR PRINTING ALL USERS
        if id_param is None and name_param is None:
            sql_all = find_all_sql()
            redis_all = find_all_redis()
            es_all = find_all_es()
            if sql_all is None and redis_all is None and es_all is None:
                logging.warn("Tried to GET with nothing to show")
                self.write("No Entry to Show")
            else:
                logging.info("Showing all entries")
                self.write("MYSQL\n")
                for i in sql_all:
                    self.write({"id": i.id, "name": i.name})
                self.write("\nREDIS\n")
                for i in redis_all:
                    self.write(i)
                self.write("\nELASTIC SEARCH\n")
                for i in es_all:
                    self.write(i["_source"])

        # FOR PRINTING BY ID
        elif name_param is None:
            sql_id_user = find_by_id_sql(id_param)
            redis_id_user = find_by_id_redis(id_param)
            es_id_user = find_by_id_es(id_param)
            if sql_id_user is None and redis_id_user is None and es_id_user is None:
                logging.warn("Trying to search by id that doesnt exist")
                self.write("Entry doesnt exist")
            else:
                logging.info("Showing entry by id")
                self.write("MYSQL\n")
                self.write({"id": sql_id_user.id, "name": sql_id_user.name})
                self.write("\nREDIS\n")
                self.write(redis_id_user)
                self.write("\nELASTIC SEARCH\n")
                self.write(es_id_user)

        # FOR PRINTING BY NAME
        else:
            sql_name_all = find_by_name_sql(name_param)
            redis_name_all = find_by_name_redis(name_param)
            es_name_all = find_by_name_es(name_param)
            if sql_name_all is None:
                logging.warn("Tried to search by name that doesnt exist")
                self.write("Entry doesnt exist")
            else:
                logging.info("Showing entry by name")
                self.write("MYSQL\n")
                for i in sql_name_all:
                    self.write({"id": i.id, "name": i.name})
                self.write("\nREDIS\n")
                for i in redis_name_all:
                    self.write(i)
                self.write("\nELASTIC SEARCH\n")
                for i in es_name_all:
                    self.write(i["_source"])

    def post(self):
        try:
            new_entry = json.loads(self.request.body)
            if find_by_id_sql(new_entry['id']) is None \
                    and find_by_id_redis(new_entry['id']) is None \
                    and find_by_id_es(new_entry['id']) is None:
                post_in_sql(new_entry)
                post_in_redis(new_entry)
                post_in_es(new_entry)
                logging.info("Posting data")
                self.write("Added new entry")
            elif not new_entry.has_key('name') or not new_entry.has_key('id'):
                logging.warn("Entered invalid body")
                self.write("Invalid Body")
            elif new_entry['name'] is None or new_entry['id'] is None:
                logging.warn("Tried to leave field blank")
                self.write("Can't be left empty")
            else:
                logging.warn("Tried to POST with existing id")
                self.write("ID already exists")
        except Exception as e:
            self.write("Couldn't POST Exception : " + str(e))


if __name__ == '__main__':
    Api().__init__()
