#!/usr/bin/env python
import psycopg2 as pg
from xml.etree.ElementTree import iterparse
import sys
import time
from itertools import islice, chain


def create_default_keys(keys):
    """Returns a dictionary containing None for all keys."""
    return dict(((k, None) for k in keys))


def create_mogrify_template(keys):
    """Return the template string for mogrification for the given keys."""
    return ('(' + ', '.join(['%(' + k + ')s' for k in keys]) + ')')


def create_mogrified_tuple(cursor, keys, templ, attribs):
    """
    The passed data in `attribs` is augmented with default data (NULLs) and the
    order of data in the tuple is the same as in the list of `keys`.
    """
    columns = create_default_keys(keys)
    columns.update(attribs)
    return cursor.mogrify(templ, columns).decode("utf-8")


def generate_parsed_xml(filepath):
    # xml reader iterable
    fxml = iterparse(filepath, events=("start", "end"))

    xml = iter(fxml)  # turn it into an iterator
    event, root = xml.__next__()  # get the root element
    for event, elem in xml:
        if(event == "end" and elem.tag == "row"):
            yield elem.attrib
            # clear the children nodes of the root to avoid memory consumption
        root.clear()


def batch(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.__next__()], batchiter)


if __name__ == '__main__':
    table = 'Posts'
    dbname = 'stackoverflow'
    posts_file = 'Data/Posts.xml'
    username = None
    password = None
    port = '5433'
    host = None
    keys = [
        'Id',
        'PostTypeId',
        'AcceptedAnswerId',
        'ParentId',
        'CreationDate',
        'Score',
        'ViewCount',
        'Body',
        'OwnerUserId',
        'LastEditorUserId',
        'LastEditorDisplayName',
        'LastEditDate',
        'LastActivityDate',
        'Title',
        'Tags',
        'AnswerCount',
        'CommentCount',
        'FavoriteCount',
        'ClosedDate',
        'CommunityOwnedDate'
    ]

    create_table_sql = '''
        DROP TABLE IF EXISTS Posts CASCADE;
        CREATE TABLE Posts (
            Id                     int PRIMARY KEY   ,
            PostTypeId             int not NULL      ,
            AcceptedAnswerId       int               ,
            ParentId               int               ,
            CreationDate           timestamp not NULL,
            Score                  int               ,
            ViewCount              int               ,
            Body                   text              ,
            OwnerUserId            int               ,
            LastEditorUserId       int               ,
            LastEditorDisplayName  text              ,
            LastEditDate           timestamp         ,
            LastActivityDate       timestamp         ,
            Title                  text              ,
            Tags                   text              ,
            AnswerCount            int               ,
            CommentCount           int               ,
            FavoriteCount          int               ,
            ClosedDate             timestamp         ,
            CommunityOwnedDate     timestamp
        );
    '''

    create_indexes_sql = '''
        CREATE INDEX posts_post_type_id_idx ON Posts (PostTypeId)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_score_idx ON Posts (Score)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_creation_date_idx ON Posts (CreationDate)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_owner_user_id_idx ON Posts (OwnerUserId)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_answer_count_idx ON Posts (AnswerCount)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_comment_count_idx ON Posts (CommentCount)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_favorite_count_idx ON Posts (FavoriteCount)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_viewcount_idx ON Posts (ViewCount)
            WITH (FILLFACTOR = 100);
        CREATE INDEX posts_accepted_answer_id_idx ON Posts (AcceptedAnswerId)
            WITH (FILLFACTOR = 100);
    '''

    template = create_mogrify_template(keys)
    start_time = time.time()

    db_connection_string = "dbname={}".format(dbname)
    db_connection_string += ' port={}'.format(port)

    if host is not None:
        db_connection_string += ' host={}'.format(host)

    if username is not None:
        db_connection_string += ' user={}'.format(username)

    if password is not None:
        db_connection_string += ' password={}'.format(password)

    try:
        with pg.connect(db_connection_string) as conn:
            with conn.cursor() as cur:
                try:
                    with open(posts_file, 'r') as xml:
                        # Pre-processing (dropping/creation of tables)
                        print('Pre-processing ...')
                        cur.execute(create_table_sql)
                        conn.commit()
                        print('Pre-processing took {} seconds'.format(time.time() - start_time))

                        # Handle content of the table
                        start_time = time.time()
                        print('Processing data ...')
                        for rows in batch(generate_parsed_xml(xml), 1000):
                            mogrified_values = [create_mogrified_tuple(cur, keys, template, row_attribs) for row_attribs in rows]
                            valuesStr = ',\n'.join(mogrified_values)

                            if len(valuesStr) > 0:
                                cmd = 'INSERT INTO ' + table + \
                                      ' VALUES\n' + valuesStr + ';'
                                cur.execute(cmd)
                                conn.commit()

                        print('Table processing took {} seconds'.format(time.time() - start_time))

                        # Post-processing (creation of indexes)
                        start_time = time.time()
                        print('Post processing ...')
                        cur.execute(create_indexes_sql)
                        conn.commit()
                        print('Post processing took {} seconds'.format(time.time() - start_time))

                except IOError as e:
                    print("Could not read from file {}.".format(posts), file=sys.stderr)
                    print("IOError: {0}".format(e.strerror), file=sys.stderr)
    except pg.Error as e:
        print("Error in dealing with the database.", file=sys.stderr)
        print("pg.Error ({0}): {1}".format(
            e.pgcode, e.pgerror), file=sys.stderr)
        print(str(e), file=sys.stderr)
    except pg.Warning as w:
        print("Warning from the database.", file=sys.stderr)
        print("pg.Warning: {0}".format(str(w)), file=sys.stderr)
