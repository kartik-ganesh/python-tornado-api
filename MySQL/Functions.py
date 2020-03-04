from MySQL.Connection_MySQL import Connection
from MySQL.entity import Employee


def find_all_sql():
    connection = Connection()
    all_user = connection.get_session().query(Employee).all()
    if all_user:
        return all_user
    else:
        return None


def find_by_id_sql(id):
    connection = Connection()
    user = connection.get_session().query(Employee).filter(Employee.id == id).first()
    return user


def find_by_name_sql(name):
    connection = Connection()
    user = connection.get_session().query(Employee).filter(Employee.name == name).all()
    if user:
        return user
    else:
        return None


def post_in_sql(new_entry):
    connection = Connection()
    connection.get_session().add(Employee(id=new_entry['id'], name=new_entry['name']))
    connection.get_session().commit()


def delete_by_id_sql(id):
    connection = Connection()
    if find_by_id_sql(id) is None:
        return False
    else:
        connection.get_session().query(Employee).filter(Employee.id == id).delete()
        connection.get_session().commit()
        return True


def update_by_id_sql(id, new_entry):
    if find_by_id_sql(id) is None:
        return False
    else:
        connection = Connection()
        updated_entry = Employee(id=new_entry['id'], name=new_entry['name'])
        connection.get_session().query(Employee).filter(Employee.id == id).update(
            {'id': updated_entry.id, 'name': updated_entry.name})
        connection.get_session().commit()
        return True
