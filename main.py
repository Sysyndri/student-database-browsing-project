from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)


def connect():
    """
    Функция для создания соединения с сервером MySQL.
    :return: Возвращает соединение с сервером MySQL
    """
    try:
        # Устанавливаем соединение с сервером MySQL
        connection = pymysql.connect(
            host='127.127.126.26',
            port=3306,
            user='root',
            password=''
        )

        return connection

    except Exception as ex:
        print(f"Соединение не установлено, ошибка: {ex}")


@app.route('/')
def index():
    """
    Функция для создания начальной страницы сайта по адресу http://127.0.0.1:5000
    :return: возвращает шаблон страницы для вывода на сайт
    """
    conn = connect()
    if conn is None:
        error = "Ошибка подключения к базе данных."
        name_error = "Ошибка №500"
        text = "Пожалуйста проверьте подключение к базе данных и попробуйте снова"

        return render_template(template_name_or_list="error.html", error=error, name_error=name_error, text=text)

    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]

    finally:
        cursor.close()
        conn.close()

    return render_template(template_name_or_list="index.html", title="Базы данных", database=databases, db_name='')


@app.route('/show/<db_name>')
def show(db_name):
    """
    Функция для создания страницы сайта по адресу http://127.0.0.1:5000/show/db_name
    :param db_name: название базы данных к которой мы подключаемся.
    :return: Возвращает шаблон страницы для вывода на сайт
    """
    conn = connect()
    if conn is None:
        error = "Ошибка подключения к базе данных."
        name_error = "Ошибка №500"
        text = "Пожалуйста проверьте подключение к базе данных и попробуйте снова"

        return render_template(template_name_or_list="error.html", error=error, name_error=name_error, text=text)

    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name}")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        count_table = len(tables)

    finally:
        cursor.close()
        conn.close()

    return render_template(template_name_or_list="table.html", title=db_name, database=tables,
                           db_name=db_name, count_table=count_table)


@app.route('/show_tables/<db_name>/<table_name>', methods=['GET'])
def show_tables(db_name, table_name):
    """
    Функция для создания страницы сайта по адресу http://127.0.0.1:5000/show_table/db_name/table_name
    :param db_name: название базы данных к которой мы подключаемся.
    :param table_name: Название таблицы внутри db_name для вывода информации.
    :return: Возвращает шаблон страницы для вывода на сайт
    """
    conn = connect()
    if conn is None:
        error = "Ошибка подключения к базе данных."
        name_error = "Ошибка №500"
        text = "Пожалуйста проверьте подключение к базе данных и попробуйте снова"

        return render_template(template_name_or_list="error.html", error=error, name_error=name_error, text=text)

    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"DESCRIBE {table_name}")
        table = cursor.fetchall()
        date = [dat for dat in table]
        count_date = len(date)
        print(date)
        # len_th = len(date[0])

        name_tab = [mx[0] for mx in date]
        mx = []
        mn = []

        for name in name_tab:
            cursor.execute(f"SELECT MAX({name}) FROM {table_name}")
            m = cursor.fetchall()[0]
            mx.append(m)

        for name in name_tab:
            cursor.execute(f"SELECT MIN({name}) FROM {table_name}")
            m = cursor.fetchall()[0]
            mn.append(m)

        len_mx_mn = len(mx)

    finally:
        cursor.close()
        conn.close()

    return render_template(
        template_name_or_list="struct_table.html", title=table_name, database=table, db_name=db_name,
        table_name=table_name, count_date=count_date, date=date, mx=mx, mn=mn, len_mx_mn=len_mx_mn)


@app.route('/show_table/<db_name>/<table_name>', methods=['GET'])
def show_table(db_name, table_name):
    """
    Функция для создания страницы сайта по адресу http://127.0.0.1:5000/show_table/db_name/table_name
    :param db_name: название базы данных к которой мы подключаемся.
    :param table_name: Название таблицы внутри db_name для вывода информации.
    :return: Возвращает шаблон страницы для вывода на сайт
    """
    conn = connect()
    if conn is None:
        error = "Ошибка подключения к базе данных."
        name_error = "Ошибка №500"
        text = "Пожалуйста проверьте подключение к базе данных и попробуйте снова"

        return render_template(template_name_or_list="error.html", error=error, name_error=name_error, text=text)

    page = request.args.get('page', 1, type=int)  # Текущая страница, по умолчанию 1
    page_one = request.args.get('page_one', 50, type=int)  # Количество записей на странице, по умолчанию 50
    offset = (page - 1) * page_one

    try:
        cursor = conn.cursor()
        cursor.execute(f"USE {db_name}")
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_date = cursor.fetchone()[0]
        total_page = (total_date + page_one - 1) // page_one

        cursor.execute(f"SELECT * FROM {table_name} LIMIT {page_one} OFFSET {offset}")
        date = cursor.fetchall()
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in cursor.fetchall()]
        count_date = len(date)

    finally:
        cursor.close()
        conn.close()

    return render_template(
        template_name_or_list="table_date.html", title=table_name, database=columns, db_name=db_name,
        table_name=table_name, date=date, count_date=count_date, page=page, total_page=total_page, page_one=page_one)


if __name__ == "__main__":
    app.run(debug=True)
