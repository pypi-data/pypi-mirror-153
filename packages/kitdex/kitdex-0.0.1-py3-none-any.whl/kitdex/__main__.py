#!/usr/bin/env python

"""
This module includes the KitDex flask server and the
command line options to start it.
"""

import os
import argparse
import socket
import flask
from flask import request
import webview
from jinja2 import Environment, FileSystemLoader

from kitdex.database import KitDexDB




class KDServer(flask.Flask):
    """
    Main flask server for KitDex. This is run as a webview
    """

    def __init__(self, db):
        super().__init__(__name__)
        self._db = db

        tmpl_dir = os.path.join(os.path.dirname(__file__), 'templates')
        loader = FileSystemLoader([tmpl_dir])
        self._env = Environment(loader=loader, trim_blocks=True)
        self.add_url_rule("/", "render_index", self._render_index)
        self.add_url_rule("/edit/<path:thing_hash>",
                          "edit_thing",
                          self._edit_thing)
        self.add_url_rule("/new", "new_thing", self._new_thing)
        self.add_url_rule("/submit_edit/<path:thing_hash>",
                          "submit_edit_thing",
                          self._submit_edit_thing)
        self.add_url_rule("/editlocations",
                          "edit_locations",
                          self._edit_locations)
        self.add_url_rule("/submit_edited_locations",
                          "submit_edited_locations",
                          self._submit_edited_locations)
        self.add_url_rule("/renamelocation/<path:location>",
                          "rename_location",
                          self._rename_location)
        self.add_url_rule("/submit_rename_location/<path:location>",
                          "submit_rename_location",
                          self._submit_rename_location)
        self.add_url_rule("/pdf", "send_pdf", self._send_pdf)

    def run(self, host="localhost", port=7001, debug=None, load_dotenv=True, **options):
        """
        Starts the flask server
        """
        try:
            # Check the server isn't already running (only needed on Windows)
            sock = socket.create_connection((host, port), timeout=0.5)
            sock.close()
            # If we have made it past this, there is a server running - so we
            # should fail
            raise ServerAlreadyRunningError(f'A server is already running on "{host}"'
                                            f' port {port}.')
        except socket.timeout:
            pass  # If we couldn't connect, ignore the error
        except ConnectionError:
            pass # If we couldn't connect, ignore the error

        super().run(host, port, debug=debug, load_dotenv=load_dotenv, **options)

    def _render_index(self):


        tmpl = self._env.get_template("index.jinja")
        locations_empty = len(self._db.location_list) == 0
        html = tmpl.render(things=self._db.hashed_thing_list, locations_empty=locations_empty)
        return html

    def _edit_thing(self, thing_hash):
        thing_hash = int(thing_hash)
        thing = self._db.get_thing_by_hash(thing_hash)
        if thing is None:
            return 'Hash not found!? <br><a href="/">Return</a>'
        tmpl = self._env.get_template("update_thing.jinja")
        html = tmpl.render(subtitle = f'Edit {thing["name"]}',
                           url = f'/submit_edit/{thing_hash}',
                           locations = self._db.location_list,
                           thingname=thing['name'],
                           thinglocation=thing['location'],
                           thingalt='; '.join(thing['alt_names']))
        return html

    def _new_thing(self):
        tmpl = self._env.get_template("update_thing.jinja")
        html = tmpl.render(subtitle = 'New item',
                           url = '/submit_edit/new',
                           locations = self._db.location_list,
                           thingname=None,
                           thinglocation=None,
                           thingalt=None)
        return html

    def _submit_edit_thing(self, thing_hash):
        edited = request.args.to_dict()
        edited['alt_names'] = [i.strip() for i in edited['alt_names'].split(';')]
        edited['alt_names'] = [i for i in edited['alt_names'] if i != '']
        if thing_hash == 'new':
            ret = self._db.new_thing(edited)
        else:
            thing_hash = int(thing_hash)
            ret = self._db.update_thing_by_hash(thing_hash, edited)
        if ret is False:
            return 'Error updating database <br><a href="/">Return</a>'
        self._db.dump_modified_db()
        return flask.redirect('/')

    def _edit_locations(self):
        tmpl = self._env.get_template("update_locations.jinja")
        html = tmpl.render(used_locations=self._db.used_locations,
                           unused_locations='\n'.join(self._db.unused_locations))
        return html

    def _submit_edited_locations(self):
        args = request.args.to_dict()
        unused_locs = args['unused_locations']
        unused_locs = [i.strip() for i in unused_locs.split('\n')]
        unused_locs = [i for i in unused_locs if i != '']
        locations = self._db.used_locations + unused_locs
        locations = list(set(locations))
        ret = self._db.update_locations(locations)
        if ret is False:
            return 'Error updating database <br><a href="/">Return</a>'
        self._db.dump_modified_db()
        return flask.redirect('/')

    def _rename_location(self, location):
        if location not in self._db.location_list:
            return 'Cannot rename unknown location. <br><a href="/">Return</a>'
        tmpl = self._env.get_template("rename_location.jinja")
        html = tmpl.render(location=location)
        return html

    def _submit_rename_location(self, location):
        updated = request.args.to_dict()
        new_name = updated['new_location_name']
        ret = self._db.rename_location(location, new_name)
        if ret is False:
            return 'Error updating database <br><a href="/">Return</a>'
        self._db.dump_modified_db()
        return flask.redirect('/')

    def _send_pdf(self):
        return flask.send_file(self._db.to_pdf())

class ServerAlreadyRunningError(Exception):
    """
    Custom exception for if the KitDex server is already running.
    """

def run_kitdex(databasefile):
    """
    Starts the KitDex GUI. Use this if calling KitDex from within python.
    """
    kitdex_db = KitDexDB(databasefile)
    kds = KDServer(kitdex_db)
    webview.create_window('KitDex', kds)
    webview.start(debug=True)

def main():
    """This is what runs if you run `KitDex` from the terminal
    To run from inside python use `run_kitex`
    """

    parser = argparse.ArgumentParser(description='Start the KitDex editor.')
    parser.add_argument('databasefile',
                        help='Path of KitDex database to edit')
    parser.add_argument(
        "-n",
        '--new',
        help="Create new kitdex database",
        action="store_true",
    )
    args = parser.parse_args()
    if args.new:
        if not (args.databasefile.endswith(".yml") or args.databasefile.endswith(".yaml")):
            args.databasefile = args.databasefile+'.yml'
        if os.path.exists(args.databasefile):
            print('KitDex database already exists')
            exit(-1)
        open(args.databasefile, 'w').close()
    run_kitdex(args.databasefile)
