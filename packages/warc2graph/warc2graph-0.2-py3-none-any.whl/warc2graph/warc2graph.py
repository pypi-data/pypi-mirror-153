# This file is part of warc2graph.
#
# warc2graph is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# warc2graph is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with warc2graph.  If not, see <https://www.gnu.org/licenses/>.
import os.path
import sys

from warc2graph import linkextraction
from warc2graph import graphs
from warc2graph import __version__

from datetime import datetime
import time


def create_model(*args, **kwargs):
    print("'extract_links' is depreciated. Please use 'link2graph' instead", file=sys.stderr)
    return create_graph(*args, **kwargs)


def create_graph(input_data, input_type="warc", methods="all", merge_results=True, blacklist=None,
                 store_content=True, count_tags=False, collect_metadata=True, metadata=None, tagset="all",
                 custom_tagset=None):
    """Main function of module. Creates network graph representing archived or live websites.
    
    Parameters
    ----------
    input_data : str or list
        The data that is to be modelled. Either a path to a warc file or a list of links to the live web.

    input_type : str, optional
        Declares the type of the input explicitly, either "warc" or "live".

    methods : str or list, optional
        Which method or methods should be used for link extraction? Currently implemented: 
        "wmd", "bs4" and "rep". Also "all" is accepted and is set as default.

    merge_results : bool, optional
        Ignored if only one method is selected. Should results of methods be merged to one result or be output as a 
        dict containing results for different methods.
    
    blacklist : list, optional
        List of domains that will be ignored.

    store_content : bool, optional
        Should the html-text be stored in the model? Default: True.

    count_tags : bool, optional
        If True, counts of all tags will be stored as attributes for all nodes.

    collect_metadata : bool, optional
        Extract plaintext (with removed boilerplates), title, date and author from each html.

    metadata : dict, optional
        Metadata describing the whole website. Will be added as attributes of the whole graph. If nothing is passed,
        the name of the (first) warc file or the first url will be used.

    tagset : str
        Choose the set of tags you want to use. Either "all", "a_only", "html_only", "no_scripts" or custom.
        See documentation for further info.

    custom_tagset : list
        If tagset is set to "custom", give a list of tuples containing the tag and the attribute you want to extract
        the links from.


    Returns
    -------
    networkx.DiGraph or dict
        If merge_results==True or results are only generated using one method, a networkx.DiGraph modelling the input
        is returned. Otherwise it returns a dict with methods as keys and corresponding generated models as
        networkx.DiGraph as values.
    """
    parameters = locals()  # store for metadata

    start = time.time()  # measure duration of process

    # get links
    links, node_attributes = linkextraction.extract_links(input_data, input_type, methods, merge_results, blacklist,
                                                          store_content, count_tags, collect_metadata, tagset,
                                                          custom_tagset)

    # prepare metadata
    if metadata is None:
        if type(input_data) is not list:
            name = input_data
        else:
            name = input_data[0]

        work_md = {"file_name": os.path.basename(name)}

    else:
        work_md = metadata
        if "file_name" not in work_md:
            if type(input_data) is not list:
                name = input_data
            else:
                name = input_data[0]
            work_md["file_name"] = os.path.basename(name)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    graph_md = {"timestamp": timestamp, "version": __version__, "parameters": parameters}
    metadata = {"work_metadata": work_md, "graph_metadata": graph_md}

    # create graph(s)
    if not merge_results:
        output = {}
        for method, met_links in links.items():
            output[method] = networks.links2graph(met_links, metadata, node_attributes)

    else:
        output = graphs.links2graph(links, metadata, node_attributes)

    # create more meta data
    output.graph["graph_metadata"]["n_nodes"] = len(output.nodes)
    output.graph["graph_metadata"]["n_edges"] = len(output.nodes)
    runtime = time.time() - start
    output.graph["graph_metadata"]["runtime"] = runtime

    return output
