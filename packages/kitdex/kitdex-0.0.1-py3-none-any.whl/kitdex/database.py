"""
The Kitdex database module includes marshmallow schema for the yaml
representation of the database and also the mython class for the same
database: KitDexDB
"""

import os
import subprocess
from copy import deepcopy

import yaml
from marshmallow import Schema, fields, pre_load, post_load, ValidationError, post_dump

from kitdex.utilities import HashableDict, natural_keys

class ThingSchema(Schema):
    """
    Schema for individual things withing the KitDex database
    """
    name = fields.Str(required=True)
    location = fields.Str(required=True)
    alt_names = fields.List(cls_or_instance=fields.Str,
                            missing=list)

    @pre_load
    def stringify_loc(self, in_data, **_):
        """
        Ensure that all locations are strings
        """
        if 'location' in in_data:
            in_data['location'] = str(in_data['location'])
        return in_data

    @post_load
    def make_hashable(self, data, **_):
        """
        Ensure that the dictionary for the thing is hashable
        by giving converting it to a class with a hash method
        """
        data['alt_names'] = tuple(data['alt_names'])
        return HashableDict(data)

    @post_dump
    def remove_empties(self, thing, **_): #pylint: disable=no-self-use
        """
        Remove unused keys when dumping
        """
        optional_keys = ["alt_names"]
        for key in optional_keys:
            if thing[key] in [None,[]]:
                del thing[key]
        return thing


class KitDexDBSchema(Schema):
    """
    Overall schema of the yaml representation of the KitDex database
    """
    valid_locations = fields.List(cls_or_instance=fields.Str,
                                  missing=[])
    things = fields.List(cls_or_instance=fields.Nested(ThingSchema),
                         missing=[])

    @pre_load
    def stringify_loc(self, in_data, **_):
        """
        Ensure that all locations are strings
        """
        if in_data is None:
            return {}
        if 'valid_locations' in in_data and isinstance(in_data['valid_locations'], list):
            for i, loc in enumerate(in_data['valid_locations']):
                in_data['valid_locations'][i] = str(loc)
        return in_data

    @post_load
    def validation(self, data, **_):
        """
        Check that all things have a valid (predefined) location
        and that thing names are not duplicated
        """
        data['valid_locations'].sort(key=natural_keys)
        self.check_locations(data)
        self.check_duplicates(data)
        return data

    def check_locations(self, data):
        """
        Check that all things have a valid (predefined) location
        """
        for thing in data['things']:
            if thing['location'] not in data['valid_locations']:
                raise ValidationError(f"{thing['location'] } is not a valid location.")
        return data

    def check_duplicates(self, data):
        """
        Check that no thing has duplicated name
        """
        names = [thing['name'] for thing in data['things']]
        if len(set(names)) != len(names):
            duplicates = set([name for name in names if names.count(name) > 1])
            raise ValidationError(f"The following tools are duplicated: {duplicates}."
                                  " Use an unambiguous definition for the name, and the"
                                  " ambiguous definition for the alt-name.")


class KitDexDB:
    """
    Python representation of the KitDex database file
    """
    def __init__(self, db_file):
        self._filename = db_file
        with open(db_file, 'r') as file_obj:
            yml_dict = yaml.safe_load(file_obj)
        self._db = KitDexDBSchema().load(yml_dict)

    @property
    def location_list(self):
        """
        Return all valid locations
        """
        return self._db['valid_locations']

    @property
    def dictionary(self):
        """
        Return a deep copy of the underlying dictionary
        """
        return deepcopy(self._db)

    @property
    def hashed_thing_list(self):
        """
        Return a list of all things. Each thing is a list with the follwing four
        elements: Thing-hash, thing-name, location, alternative names
        """
        out_list = []
        for thing in self._db['things']:
            alt_names = '; '.join(thing['alt_names'])
            out_list.append([hash(thing), thing['name'], thing['location'], alt_names])
        return out_list

    @property
    def _thing_hashes(self):
        return [hash(thing) for thing in self._db['things']]

    @property
    def used_locations(self):
        """
        Return a sorted list of all valid locations that are used
        """
        all_used_locations = [thing['location'] for thing in self._db['things']]
        return sorted(list(set(all_used_locations)), key=natural_keys)

    @property
    def unused_locations(self):
        """
        Return a sorted list of all valid locations that are unused
        """
        location_list = deepcopy(self._db['valid_locations'])
        for used_location in self.used_locations:
            location_list.pop(location_list.index(used_location))
        return sorted(location_list, key=natural_keys)

    def get_thing_by_hash(self, thing_hash):
        """
        Return a the thing dictionary that matches the thing hash.
        None is returned if hash is not found
        """
        hashes = self._thing_hashes
        if thing_hash in hashes:
            ind = hashes.index(thing_hash)
            return self._db['things'][ind]
        return None

    def update_thing_by_hash(self, thing_hash, updated_thing):
        """
        Replace thing dictionary by updated dictionary
        """
        new_db = deepcopy(self._db)
        hashes = self._thing_hashes
        if thing_hash not in hashes:
            raise RuntimeError('Cannot edit: hash not found')

        ind = hashes.index(thing_hash)
        new_db['things'][ind] = updated_thing
        return self._update_db(new_db)

    def new_thing(self, new_thing_dict):
        """
        Create a new thing and add it to this database
        """
        new_db = deepcopy(self._db)
        new_db['things'].append(new_thing_dict)
        return self._update_db(new_db)

    def update_locations(self, locations):
        """
        Replace the list of locations with new list
        """
        new_db = deepcopy(self._db)
        new_db['valid_locations'] = locations
        return self._update_db(new_db)

    def rename_location(self, location, new_name):
        """
        Rename a specific location and update all references to it
        """
        new_db = deepcopy(self._db)
        if location not in new_db['valid_locations']:
            raise RuntimeError('Cannot update unknown location')
        #Update location
        locations = new_db['valid_locations']
        locations[locations.index(location)] = new_name
        #Update any things stored in this location
        for thing in new_db['things']:
            if thing['location'] == location:
                thing['location'] = new_name
        return self._update_db(new_db)

    def _update_db(self, new_db):
        try:
            new_db = KitDexDBSchema().load(new_db)
        except ValidationError:
            return False
        self._db = new_db
        return True

    def dump_modified_db(self):
        """
        Write modified database to file
        """
        db_dumped = KitDexDBSchema().dump(self._db)
        with open(self._filename, 'w') as file_obj:
            file_obj.write(yaml.dump(db_dumped))

    def to_tuple_list(self):
        """
        Create a list of all name-location pairs. A pair is also created
        for each alt-name
        """
        out_tuples = []
        for thing in self._db['things']:
            out_tuples.append((thing['name'], thing['location']))
            if 'alt_names' in thing:
                for alt_name in thing['alt_names']:
                    out_tuples.append((alt_name, thing['location']))

        return sorted(list(set(out_tuples)), key=lambda out_tuple: natural_keys(out_tuple[0]))


    def to_tex(self):
        """
        Return a LaTeX representation of the database
        """
        out_tuples = self.to_tuple_list()
        tex = r"""\documentclass[twocolumn,10 pt]{article}
\usepackage{supertabular,booktabs}
\usepackage{ragged2e}
\usepackage[margin=1.5cm]{geometry}
\usepackage{fancyhdr, lastpage}
\pagestyle{fancy}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[C]{{\thepage} of \pageref{LastPage}}
\begin{document}
\tablehead{\hline {\bfseries What} & {\bfseries Where} \\ \hline}
\tabletail{\hline}
\begin{supertabular}{|p{.18\textwidth}p{.26\textwidth}|}
"""
        for out_tuple in out_tuples:
            tex += r'\hline\RaggedRight '+out_tuple[0]+'&'+out_tuple[1]+r'\\'+'\n'
        tex += r'\end{supertabular}'
        tex += r'\end{document}'
        return tex

    def to_pdf(self):
        """
        Create a PDF (via LaTeX) of the database information. Return the URI of the
        PDF.
        """
        tex = self.to_tex()
        cdir = os.getcwd()
        os.chdir("/tmp/")
        with open('index.tex', 'w') as file_obj:
            file_obj.write(tex)
        null_file = open(os.devnull, 'w')
        latex_run = ["pdflatex","--shell-escape","--interaction=nonstopmode","index"]
        subprocess.check_call(latex_run, stdout=null_file, stderr=subprocess.STDOUT)
        subprocess.check_call(latex_run, stdout=null_file, stderr=subprocess.STDOUT)
        os.chdir(cdir)

        return "/tmp/index.pdf"
