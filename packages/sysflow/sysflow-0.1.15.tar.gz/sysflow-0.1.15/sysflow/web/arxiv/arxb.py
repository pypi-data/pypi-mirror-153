import io
import re
import tarfile
import xml.etree.ElementTree
from urllib.error import HTTPError

import arxiv2bib
import bibtexparser
import requests
from pybtex.database import parse_string
from pybtex.utils import OrderedCaseInsensitiveDict
from requests.exceptions import RequestException

"""
This file contains various utility functions.
"""
import argparse
import re
import unicodedata
from itertools import chain, islice


def parse_args():
    desc = "get the bib for an arxiv paper"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # arxiv arg
    arx_arg = add_argument_group("arxiv")

    parser.add_argument("--input", "-i", type=argparse.FileType("r"), help="input file")
    parser.add_argument("--output", "-o", help="bibtex output file")

    args = parser.parse_known_args()

    return args


# Huge URL regex taken from https://gist.github.com/gruber/8891611
URL_REGEX = re.compile(
    r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"
)
_SLUGIFY_STRIP_RE = re.compile(r"[^\w\s-]")
_SLUGIFY_HYPHENATE_RE = re.compile(r"[\s]+")


def replace_all(text, replace_dict):
    """
    Replace multiple strings in a text.
    .. note::
        Replacements are made successively, without any warranty on the order \
        in which they are made.
    :param text: Text to replace in.
    :param replace_dict: Dictionary mapping strings to replace with their \
            substitution.
    :returns: Text after replacements.
    >>> replace_all("foo bar foo thing", {"foo": "oof", "bar": "rab"})
    'oof rab oof thing'
    """
    for i, j in replace_dict.items():
        text = text.replace(i, j)
    return text


def map_or_apply(function, param):
    """
    Map the function on ``param``, or apply it, depending whether ``param`` \
            is a list or an item.
    :param function: The function to apply.
    :param param: The parameter to feed the function with (list or item).
    :returns: The computed value or ``None``.
    """
    try:
        if isinstance(param, list):
            return [next(iter(function(i))) for i in param]
        else:
            return next(iter(function(param)))
    except StopIteration:
        return None


def clean_whitespaces(text):
    """
    Remove multiple whitespaces from text. Also removes leading and trailing \
    whitespaces.
    :param text: Text to remove multiple whitespaces from.
    :returns: A cleaned text.
    >>> clean_whitespaces("this  is    a text with    spaces")
    'this is a text with spaces'
    """
    return " ".join(text.strip().split())


def remove_duplicates(some_list):
    """
    Remove the duplicates from a list.
    :param some_list: List to remove duplicates from.
    :returns: A list without duplicates.
    >>> remove_duplicates([1, 2, 3, 1])
    [1, 2, 3]
    >>> remove_duplicates([1, 2, 1, 2])
    [1, 2]
    """
    return list(set(some_list))


def batch(iterable, size):
    """
    Get items from a sequence a batch at a time.
    .. note:
        Adapted from
        https://code.activestate.com/recipes/303279-getting-items-in-batches/.
    .. note:
        All batches must be exhausted immediately.
    :params iterable: An iterable to get batches from.
    :params size: Size of the batches.
    :returns: A new batch of the given size at each time.
    >>> [list(i) for i in batch([1, 2, 3, 4, 5], 2)]
    [[1, 2], [3, 4], [5]]
    """
    item = iter(iterable)
    while True:
        batch_iterator = islice(item, size)
        try:
            yield chain([next(batch_iterator)], batch_iterator)
        except StopIteration:
            return


def remove_urls(text):
    """
    Remove URLs from a given text (only removes http, https and naked domains \
    URLs).
    :param text: The text to remove URLs from.
    :returns: The text without URLs.
    >>> remove_urls("foobar http://example.com https://example.com foobar")
    'foobar foobar'
    """
    return clean_whitespaces(URL_REGEX.sub("", text))


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens to have nice filenames.
    From Django's "django/template/defaultfilters.py".
    >>> slugify("El pingüino Wenceslao hizo kilómetros bajo exhaustiva lluvia y frío, añoraba a su querido cachorro. ortez ce vieux whisky au juge blond qui fume sur son île intérieure, à Γαζέες καὶ μυρτιὲς δὲν θὰ βρῶ πιὰ στὸ χρυσαφὶ ξέφωτο いろはにほへとちりぬるを Pchnąć w tę łódź jeża lub ośm skrzyń fig กว่าบรรดาฝูงสัตว์เดรัจฉาน")
    'El_pinguino_Wenceslao_hizo_kilometros_bajo_exhaustiva_lluvia_y_frio_anoraba_a_su_querido_cachorro_ortez_ce_vieux_whisky_au_juge_blond_qui_fume_sur_son_ile_interieure_a_Pchnac_w_te_odz_jeza_lub_osm_skrzyn_fig'
    """
    try:
        unicode_type = unicode
    except NameError:
        unicode_type = str
    if not isinstance(value, unicode_type):
        value = unicode_type(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = unicode_type(_SLUGIFY_STRIP_RE.sub("", value).strip())
    return _SLUGIFY_HYPHENATE_RE.sub("_", value)


# https://github.com/Phyks/libbmc/blob/master/libbmc/repositories/arxiv.py

# Append arXiv to the valid identifiers list
__valid_identifiers__ = ["repositories.arxiv"]


ARXIV_IDENTIFIER_FROM_2007 = r"\d{4}\.\d{4,5}(v\d+)?"
ARXIV_IDENTIFIER_BEFORE_2007 = (
    r"("
    + (
        "|".join(
            [
                "astro-ph.GA",
                "astro-ph.CO",
                "astro-ph.EP",
                "astro-ph.HE",
                "astro-ph.IM",
                "astro-ph.SR",
                "cond-math.dis-nn",
                "cond-math.mtrl-sci",
                "cond-math.mes-hall",
                "cond-math.other",
                "cond-math.quant-gas",
                "cond-math.soft",
                "cond-math.stat-mech",
                "cond-math.str-el",
                "cond-math.supr-con",
                "gr-qc",
                "hep-ex",
                "hep-lat",
                "hep-ph",
                "hep-th",
                "math-ph",
                "nlin.AO",
                "nlin.CG",
                "nlin.CD",
                "nlin.SI",
                "nlin.PS",
                "nucl-ex",
                "nucl-th",
                "physics.acc-ph",
                "physics.ao-ph",
                "physics.atom-ph",
                "physics.atm-clus",
                "physics.bio-ph",
                "physics.chem-ph",
                "physics.class-ph",
                "physics.comp-ph",
                "physics.data-an",
                "physics.flu-dyn",
                "physics.gen-ph",
                "physics.geo-ph",
                "physics.hist-ph",
                "physics.ins-det",
                "physics.med-ph",
                "physics.optics",
                "physics.ed-ph",
                "physics.soc-ph",
                "physics.plasm-ph",
                "physics.pop-ph",
                "physics.space-ph",
                "physics.quant-ph",
                "math.AG",
                "math.AT",
                "math.AP",
                "math.CT",
                "math.CA",
                "math.CO",
                "math.AC",
                "math.CV",
                "math.DG",
                "math.DS",
                "math.FA",
                "math.GM",
                "math.GN",
                "math.GT",
                "math.GR",
                "math.HO",
                "math.IT",
                "math.KT",
                "math.LO",
                "math.MP",
                "math.MG",
                "math.NT",
                "math.NA",
                "math.OA",
                "math.OC",
                "math.PR",
                "math.QA",
                "math.RT",
                "math.RA",
                "math.SP",
                "math.ST",
                "math.SG",
                "cs.AI",
                "cs.CL",
                "cs.CC",
                "cs.CE",
                "cs.CG",
                "cs.GT",
                "cs.CV",
                "cs.CY",
                "cs.CR",
                "cs.DS",
                "cs.DB",
                "cs.DL",
                "cs.DM",
                "cs.DC",
                "cs.ET",
                "cs.FL",
                "cs.GL",
                "cs.GR",
                "cs.AR",
                "cs.HC",
                "cs.IR",
                "cs.IT",
                "cs.LG",
                "cs.LO",
                "cs.MS",
                "cs.MA",
                "cs.MM",
                "cs.NI",
                "cs.NE",
                "cs.NA",
                "cs.OS",
                "cs.OH",
                "cs.PF",
                "cs.PL",
                "cs.RO",
                "cs.SI",
                "cs.SE",
                "cs.SD",
                "cs.SC",
                "cs.SY",
                "q-bio.BM",
                "q-bio.CB",
                "q-bio.GN",
                "q-bio.MN",
                "q-bio.NC",
                "q-bio.OT",
                "q-bio.PE",
                "q-bio.QM",
                "q-bio.SC",
                "q-bio.TO",
                "q-fin.CP",
                "q-fin.EC",
                "q-fin.GN",
                "q-fin.MF",
                "q-fin.PM",
                "q-fin.PR",
                "q-fin.RM",
                "q-fin.ST",
                "q-fin.TR",
                "stat.AP",
                "stat.CO",
                "stat.ML",
                "stat.ME",
                "stat.OT",
                "stat.TH",
            ]
        )
    )
    + r")/\d+"
)
# Regex is fully enclosed in a group for findall to match it all
REGEX = re.compile(
    "((arxiv:)?(("
    + ARXIV_IDENTIFIER_FROM_2007
    + ")|("
    + ARXIV_IDENTIFIER_BEFORE_2007
    + ")))",
    re.IGNORECASE,
)

# Base arXiv URL used as id sometimes
ARXIV_URL = "http://arxiv.org/abs/{arxiv_id}"
# Eprint URL used to download sources
ARXIV_EPRINT_URL = "http://arxiv.org/e-print/{arxiv_id}"


def get_latest_version(arxiv_id):
    """
    Find the latest version of a given arXiv eprint.
    :param arxiv_id: The (canonical) arXiv ID to query.
    :returns: The latest version on eprint as a string, or ``None``.
    >>> get_latest_version('1401.2910')
    '1401.2910v1'
    >>> get_latest_version('1401.2910v1')
    '1401.2910v1'
    >>> get_latest_version('1506.06690v1')
    '1506.06690v2'
    >>> get_latest_version('1506.06690')
    '1506.06690v2'
    """
    # Get updated bibtex
    # Trick: strip the version from the arXiv id, to query updated BibTeX for
    # the preprint and not the specific version
    arxiv_preprint_id = strip_version(arxiv_id)
    updated_bibtex = bibtexparser.loads(get_bibtex(arxiv_preprint_id))
    updated_bibtex = next(iter(updated_bibtex.entries_dict.values()))

    try:
        return updated_bibtex["eprint"]
    except KeyError:
        return None


def strip_version(arxiv_id):
    """
    Remove the version suffix from an arXiv id.
    :param arxiv_id: The (canonical) arXiv ID to strip.
    :returns: The arXiv ID without the suffix version
    >>> strip_version('1506.06690v1')
    '1506.06690'
    >>> strip_version('1506.06690')
    '1506.06690'
    """
    return re.sub(r"v\d+\Z", "", arxiv_id)


def is_valid(arxiv_id):
    """
    Check that a given arXiv ID is a valid one.
    :param arxiv_id: The arXiv ID to be checked.
    :returns: Boolean indicating whether the arXiv ID is valid or not.
    >>> is_valid('1506.06690')
    True
    >>> is_valid('1506.06690v1')
    True
    >>> is_valid('arXiv:1506.06690')
    True
    >>> is_valid('arXiv:1506.06690v1')
    True
    >>> is_valid('arxiv:1506.06690')
    True
    >>> is_valid('arxiv:1506.06690v1')
    True
    >>> is_valid('math.GT/0309136')
    True
    >>> is_valid('abcdf')
    False
    >>> is_valid('bar1506.06690foo')
    False
    >>> is_valid('mare.GG/0309136')
    False
    """
    match = REGEX.match(arxiv_id)
    return (match is not None) and (match.group(0) == arxiv_id)


def get_bibtex(arxiv_id):
    """
    Get a BibTeX entry for a given arXiv ID.
    .. note::
        Using awesome https://pypi.python.org/pypi/arxiv2bib/ module.
    :param arxiv_id: The canonical arXiv id to get BibTeX from.
    :returns: A BibTeX string or ``None``.
    >>> get_bibtex('1506.06690')
    "@article{1506.06690v2,\\nAuthor        = {Lucas Verney and Lev Pitaevskii and Sandro Stringari},\\nTitle         = {Hybridization of first and second sound in a weakly-interacting Bose gas},\\nEprint        = {1506.06690v2},\\nDOI           = {10.1209/0295-5075/111/40005},\\nArchivePrefix = {arXiv},\\nPrimaryClass  = {cond-mat.quant-gas},\\nAbstract      = {Using Landau's theory of two-fluid hydrodynamics we investigate the sound\\nmodes propagating in a uniform weakly-interacting superfluid Bose gas for\\nvalues of temperature, up to the critical point. In order to evaluate the\\nrelevant thermodynamic functions needed to solve the hydrodynamic equations,\\nincluding the temperature dependence of the superfluid density, we use\\nBogoliubov theory at low temperatures and the results of a perturbative\\napproach based on Beliaev diagrammatic technique at higher temperatures.\\nSpecial focus is given on the hybridization phenomenon between first and second\\nsound which occurs at low temperatures of the order of the interaction energy\\nand we discuss explicitly the behavior of the two sound velocities near the\\nhybridization point.},\\nYear          = {2015},\\nMonth         = {Jun},\\nUrl           = {http://arxiv.org/abs/1506.06690v2},\\nFile          = {1506.06690v2.pdf}\\n}"
    >>> get_bibtex('1506.06690v1')
    "@article{1506.06690v1,\\nAuthor        = {Lucas Verney and Lev Pitaevskii and Sandro Stringari},\\nTitle         = {Hybridization of first and second sound in a weakly-interacting Bose gas},\\nEprint        = {1506.06690v1},\\nDOI           = {10.1209/0295-5075/111/40005},\\nArchivePrefix = {arXiv},\\nPrimaryClass  = {cond-mat.quant-gas},\\nAbstract      = {Using Landau's theory of two-fluid hydrodynamics we investigate the sound\\nmodes propagating in a uniform weakly-interacting superfluid Bose gas for\\nvalues of temperature, up to the critical point. In order to evaluate the\\nrelevant thermodynamic functions needed to solve the hydrodynamic equations,\\nincluding the temperature dependence of the superfluid density, we use\\nBogoliubov theory at low temperatures and the results of a perturbative\\napproach based on Beliaev diagrammatic technique at higher temperatures.\\nSpecial focus is given on the hybridization phenomenon between first and second\\nsound which occurs at low temperatures of the order of the interaction energy\\nand we discuss explicitly the behavior of the two sound velocities near the\\nhybridization point.},\\nYear          = {2015},\\nMonth         = {Jun},\\nUrl           = {http://arxiv.org/abs/1506.06690v1},\\nFile          = {1506.06690v1.pdf}\\n}"
    """
    # Fetch bibtex using arxiv2bib module
    try:
        bibtex = arxiv2bib.arxiv2bib([arxiv_id])
    except HTTPError:
        bibtex = []

    for bib in bibtex:
        if isinstance(bib, arxiv2bib.ReferenceErrorInfo):
            continue
        else:
            # Return fetched bibtex
            return bib.bibtex()
    # An error occurred, return None
    return None


def extract_from_text(text):
    """
    Extract arXiv IDs from a text.
    :param text: The text to extract arXiv IDs from.
    :returns: A list of matching arXiv IDs, in canonical form.
    >>> sorted(extract_from_text('1506.06690 1506.06690v1 arXiv:1506.06690 arXiv:1506.06690v1 arxiv:1506.06690 arxiv:1506.06690v1 math.GT/0309136 abcdf bar1506.06690foo mare.GG/0309136'))
    ['1506.06690', '1506.06690v1', 'math.GT/0309136']
    """
    # Remove the leading "arxiv:".
    return remove_duplicates(
        [
            re.sub("arxiv:", "", i[0], flags=re.IGNORECASE)
            for i in REGEX.findall(text)
            if i[0] != ""
        ]
    )


def to_url(arxiv_ids):
    """
    Convert a list of canonical DOIs to a list of DOIs URLs.
    :param dois: List of canonical DOIs.
    :returns: A list of DOIs URLs.
    >>> to_url('1506.06690')
    'http://arxiv.org/abs/1506.06690'
    >>> to_url('1506.06690v1')
    'http://arxiv.org/abs/1506.06690v1'
    """
    if isinstance(arxiv_ids, list):
        return [ARXIV_URL.format(arxiv_id=arxiv_id) for arxiv_id in arxiv_ids]
    else:
        return ARXIV_URL.format(arxiv_id=arxiv_ids)


def to_canonical(urls):
    """
    Convert a list of arXiv IDs to a list of canonical IDs.
    :param dois: A list of DOIs URLs.
    :returns: List of canonical DOIs. ``None`` if an error occurred.
    >>> to_canonical('http://arxiv.org/abs/1506.06690')
    '1506.06690'
    >>> to_canonical('http://arxiv.org/abs/1506.06690v1')
    '1506.06690v1'
    >>> to_canonical(['http://arxiv.org/abs/1506.06690'])
    ['1506.06690']
    >>> to_canonical('aaa') is None
    True
    """
    return map_or_apply(extract_from_text, urls)


def from_doi(doi):
    """
    Get the arXiv eprint id for a given DOI.
    .. note::
        Uses arXiv API. Will not return anything if arXiv is not aware of the
        associated DOI.
    :param doi: The DOI of the resource to look for.
    :returns: The arXiv eprint id, or ``None`` if not found.
    >>> from_doi('10.1209/0295-5075/111/40005')
    # Note: Test do not pass due to an arXiv API bug.
    '1506.06690'
    """
    try:
        request = requests.get(
            "http://export.arxiv.org/api/query",
            params={"search_query": "doi:%s" % (doi,), "max_results": 1},
        )
        request.raise_for_status()
    except RequestException:
        return None
    root = xml.etree.ElementTree.fromstring(request.content)
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        arxiv_id = entry.find("{http://www.w3.org/2005/Atom}id").text
        # arxiv_id is an arXiv full URL. We only want the id which is the last
        # URL component.
        return arxiv_id.split("/")[-1]
    return None


def to_doi(arxiv_id):
    """
    Get the associated DOI for a given arXiv eprint.
    .. note::
        Uses arXiv API. Will not return anything if arXiv is not aware of the
        associated DOI.
    :param eprint: The arXiv eprint id.
    :returns: The DOI if any, or ``None``.
    >>> to_doi('1506.06690v1')
    '10.1209/0295-5075/111/40005'
    >>> to_doi('1506.06690')
    '10.1209/0295-5075/111/40005'
    """
    try:
        request = requests.get(
            "http://export.arxiv.org/api/query",
            params={"id_list": arxiv_id, "max_results": 1},
        )
        request.raise_for_status()
    except RequestException:
        return None
    root = xml.etree.ElementTree.fromstring(request.content)
    for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
        doi = entry.find("{http://arxiv.org/schemas/atom}doi")
        if doi is not None:
            return doi.text
    return None


def get_sources(arxiv_id):
    """
    Download sources on arXiv for a given preprint.
    .. note::
        Bulk download of sources from arXiv is not permitted by their API. \
                You should have a look at http://arxiv.org/help/bulk_data_s3.
    :param eprint: The arXiv id (e.g. ``1401.2910`` or ``1401.2910v1``) in a \
            canonical form.
    :returns: A ``TarFile`` object of the sources of the arXiv preprint or \
            ``None``.
    """
    try:
        request = requests.get(ARXIV_EPRINT_URL.format(arxiv_id=arxiv_id))
        request.raise_for_status()
        file_object = io.BytesIO(request.content)
        return tarfile.open(fileobj=file_object)
    except (RequestException, AssertionError, tarfile.TarError):
        return None


def get_bbl(arxiv_id):
    """
    Get the .bbl files (if any) of a given preprint.
    .. note::
        Bulk download of sources from arXiv is not permitted by their API. \
                You should have a look at http://arxiv.org/help/bulk_data_s3.
    :param arxiv_id: The arXiv id (e.g. ``1401.2910`` or ``1401.2910v1``) in \
            a canonical form.
    :returns: A list of the full text of the ``.bbl`` files (if any) \
            or ``None``.
    """
    tar_file = get_sources(arxiv_id)
    bbl_files = [i for i in tar_file.getmembers() if i.name.endswith(".bbl")]
    bbl_files = [
        tar_file.extractfile(member).read().decode(tarfile.ENCODING)
        for member in bbl_files
    ]
    return bbl_files


# doi2bib
# https://github.com/bibcure/doi2bib


def get_bib(doi):
    """
    Parameters
    ----------
        doi: str
    Returns
    -------
        found: bool
        bib: str
    """
    bare_url = "http://api.crossref.org/"
    url = "{}works/{}/transform/application/x-bibtex"
    url = url.format(bare_url, doi)
    r = requests.get(url)
    found = False if r.status_code != 200 else True
    bib = r.content
    bib = str(bib, "utf-8")
    return found, bib


def get_json(doi):
    """
    Parameters
    ----------
        doi: str
    Returns
    -------
        found: bool
        item: dict
            Response from crossref
    """
    bare_url = "http://api.crossref.org/"
    url = "{}works/{}"
    url = url.format(bare_url, doi)
    r = requests.get(url)
    found = False if r.status_code != 200 else True
    item = r.json()

    return found, item


def doi2_bib(doi, abbrev_journal=True, add_abstract=True):
    """
    Parameters
    ----------
        doi: str
        abbrev_journal: bool
            If True try to abbreviate the journal name
    Returns
    -------
        found: bool
        bib: str
            The bibtex string
    """
    found, bib = get_bib(doi)
    if found and abbrev_journal:

        found, item = get_json(doi)
        if found:
            abbreviated_journal = item["message"]["short-container-title"]
            if add_abstract and "abstract" in item["message"].keys():
                abstract = item["message"]["abstract"]
                bi = bibtexparser.loads(bib)
                bi.entries[0]["abstract"] = abstract
                bib = bibtexparser.dumps(bi)

            if len(abbreviated_journal) > 0:
                abbreviated_journal = abbreviated_journal[0].strip()
                bib = re.sub(
                    r"journal = \{[^>]\}",
                    "journal = {" + abbreviated_journal + "}",
                    bib,
                )
    return found, bib


# convert to google scholar
# https://github.com/jiamings/scholar-bibtex-keys/blob/master/gsbib/scholar_bibtex_keys.py
def obtain_replace_keys(bib_data):
    """
    Obtain Google Scholar style keys from parsed bibliography data.
    """
    keys, new_keys = [], []
    for key in bib_data.entries.keys():
        try:
            author_last_name = (
                bib_data.entries[key].persons["author"][0].last_names[0].lower()
            )
        except:
            print(key)
        try:
            year = bib_data.entries[key].fields["year"]
        except:
            year = ""
        title_first_word = (
            re.search(r"\w+", bib_data.entries[key].fields["title"]).group(0).lower()
        )
        new_key = author_last_name + year + title_first_word
        keys.append(key)
        new_keys.append(new_key)
    return keys, new_keys


def update_arxiv_information(bib_data):
    """
    Include arxiv information in journal field.
    """
    for key, entry in bib_data.entries.items():
        if "Eprint" in bib_data.entries[key].fields:
            bib_data.entries[key].fields["journal"] = "arXiv preprint arXiv:{}".format(
                bib_data.entries[key].fields["Eprint"]
            )
    return bib_data


def convert_bibtex_keys(input_file: str):
    """
    Convert keys in a bibtex file to Google Scholar format.
    @input_file: string, input file name.
    @output_file: string, output file name.
    """
    bib_data = parse_string(input_file, bib_format="bibtex")
    keys, new_keys = obtain_replace_keys(bib_data)
    new_entries = OrderedCaseInsensitiveDict()
    for key, new_key in zip(keys, new_keys):
        new_entries[new_key] = bib_data.entries[key]
    bib_data.entries = new_entries
    bib_data = update_arxiv_information(bib_data)
    return bib_data.to_string(bib_format="bibtex")


# utils
# https://github.com/bibcure/doi2bib/blob/master/doi2bib/bin/doi2bib
def save_output_bibs(bibs, output_file):
    try:
        with io.open(output_file, "w", encoding="utf-8") as bibfile:
            for bib in bibs:
                bibfile.write("{}\n".format(bib))

    except TypeError:
        print("Can't save in output file\n")
        print(bibs)

def remove_abs(s): 
    # remove the abs section the arxiv bib
    return re.sub(r'(?!\n)[^\S\n\t]*Abstract[^\S\n\t]*=[^\S\n\t]*[\"\'\{][\s\S]*?[\"\'\}][^\S\n\t]*,[^\S\n\t]*\n', '', s)

def arxb(arv_id):
    arv_id = to_canonical(arv_id)
    if is_valid(arv_id):
        doi_id = to_doi(arv_id)
        if doi_id:
            found, bib_file = get_bib(doi_id)
            assert found
        else:
            bib_file = get_bibtex(arv_id)
            bib_file = remove_abs(bib_file)
    else:
        doi_id = arv_id
        found, bib_file = get_bib(doi_id)
        assert found

    # fix the url
    return convert_bibtex_keys(bib_file).replace(r'\%2', '%2')   


def main():
    global args
    args = parse_args()

    inlinearvid = len(args[1]) > 0
    if inlinearvid:
        arvids = args[1]
    else:
        arvids = args[0].input.read()
        arvids = map(lambda a: a.strip(), arvids.split("\n"))
        arvids = filter(lambda title: title != "", arvids)

    bibs = list(map(arxb, arvids))

    if inlinearvid:
        print("\n".join(bibs))
    else:
        if args[0].output:
            save_output_bibs(bibs, args[0].output)
        else:
            outfile = args[0].input.name
            outfile = outfile.split(".")
            outfile[-2] = outfile[-2] + "_convert"
            outfile[-1] = "bib"
            outfile = ".".join(outfile)
            save_output_bibs(bibs, outfile)


if __name__ == "__main__":
    # Note down some potential useful lib: https://github.com/yuchenlin/rebiber
    # Usage I:
    # python arxb.py 1506.06690v2  2012.20323

    # Using II:
    # test.md
    # 1506.06690v2
    # 1506.06691
    # 1506.06692
    # 2012.20323
    # python arxb.py -i test.md

    main()
