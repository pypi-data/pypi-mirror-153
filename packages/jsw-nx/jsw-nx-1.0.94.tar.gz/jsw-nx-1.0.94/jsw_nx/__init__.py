import pkg_resources

version = pkg_resources.get_distribution('jsw-nx').version
__version__ = version

# next base
from jsw_nx.base.every import every
from jsw_nx.base.filter import filter
from jsw_nx.base.find import find
from jsw_nx.base.find_index import find_index
from jsw_nx.base.flatten import flatten
from jsw_nx.base.foreach import foreach
from jsw_nx.base.forin import forin
from jsw_nx.base.get import get
from jsw_nx.base.getenv import getenv
from jsw_nx.base.includes import includes
from jsw_nx.base.index import index
from jsw_nx.base.map import map
from jsw_nx.base.mix import mix
from jsw_nx.base.noop import noop
from jsw_nx.base.noop import noop_scrapy_parse
from jsw_nx.base.parse_int import parse_int
from jsw_nx.base.reduce import reduce
from jsw_nx.base.set import set
from jsw_nx.base.some import some
from jsw_nx.base.type import type

# ruby style
from jsw_nx.rubify.times import times
from jsw_nx.rubify.to_a import to_a
from jsw_nx.rubify.to_b import to_b
from jsw_nx.rubify.to_f import to_f
from jsw_nx.rubify.to_i import to_i
from jsw_nx.rubify.to_n import to_n
from jsw_nx.rubify.to_s import to_s

# next packages
from jsw_nx.packages.days import days
from jsw_nx.packages.param import param
from jsw_nx.packages.parse_cookie import parse_cookie
from jsw_nx.packages.qs import qs
from jsw_nx.packages.tmpl import tmpl
from jsw_nx.packages.deep_each import deep_each
from jsw_nx.packages.get_domain import get_domain
from jsw_nx.packages.html2text import html2text
from jsw_nx.packages.is_process_alive import is_process_alive
from jsw_nx.packages.md5 import md5
from jsw_nx.packages.notify import notify
from jsw_nx.packages.replace_dict_all import replace_dict_all
from jsw_nx.packages.sleep_random import sleep_random
from jsw_nx.packages.uniq import uniq
from jsw_nx.packages.uniq_in_order import uniq_in_order
from jsw_nx.packages.urljoin import urljoin

# next classes
from jsw_nx.classes.configuration import Configuration
from jsw_nx.classes.date import Date
from jsw_nx.classes.fileutils import FileUtils as fileutils
from jsw_nx.classes.tar import Tar as tar
from jsw_nx.classes.json import JSON
from jsw_nx.classes.pm2_manager import Pm2Manager
from jsw_nx.classes.yaml import Yaml
from jsw_nx.classes.ymd import Ymd
