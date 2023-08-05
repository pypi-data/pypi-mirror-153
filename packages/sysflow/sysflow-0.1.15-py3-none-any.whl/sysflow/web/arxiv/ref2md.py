
import sys 
import argparse

def parse_args():
    desc = "change the format of the reference list to standard markdown on the web"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # latex path
    arx_arg = add_argument_group("ref")
    arx_arg.add_argument("path", type=str, help="the path of the markdown file")
    arx_arg.add_argument("--sid", type=int, default=1, help="the start index of the item")
    args = parser.parse_args()

    return args


def get_doi(line_str):
    import re 
    import requests

    regex_doi = '[doi|DOI][\s\.\:]{0,2}(10\.\d{4}[\d\:\.\-\/a-zA-Z]+)'
    doi_id = re.findall(regex_doi, line_str)
    if len(doi_id) == 0:
        return False 
    # there might be some period in the end
    doi_id = doi_id[0].strip('.')

    bare_url = "http://api.crossref.org/"

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

        url = "{}works/{}"
        url = url.format(bare_url, doi)
        r = requests.get(url)
        found = False if r.status_code != 200 else True
        item = r.json()

        return found, item

    found, doi_json = get_json(doi_id)

    if found: 
        title = doi_json['message']['title'][0]
        url = doi_json['message']['URL']
        
        return '[{}]({})'.format(title, url)
    return found 



def get_arxiv(line_str):
    import re 
    import requests

    ARXIV_IDENTIFIER_FROM_2007 = r"\d{4}\.\d{4,5}(v\d+)?"
    ARXIV_IDENTIFIER_BEFORE_2007 = r"(" + ("|".join([
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
        "physics",
        "quant-ph",
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
        "stat.TH"])) + r")/\d+"
    # Regex is fully enclosed in a group for findall to match it all
    regex_arxiv = "((arxiv:)?((" + ARXIV_IDENTIFIER_FROM_2007 + ")|(" + ARXIV_IDENTIFIER_BEFORE_2007 + ")))"

    # Base arXiv URL used as id sometimes
    ARXIV_URL = "http://arxiv.org/abs/{arxiv_id}"
    # Eprint URL used to download sources
    ARXIV_EPRINT_URL = "http://arxiv.org/e-print/{arxiv_id}"


    arxiv_id = re.findall(regex_arxiv, line_str)

    # print(arxiv_id)
    if len(arxiv_id) == 0:
        return False 
    # there might be some period in the end
    arxiv_id = arxiv_id[0][0]


    from xml.etree import ElementTree
    import sys
    import re
    import os

    if sys.version_info < (2, 6):
        raise Exception("Python 2.6 or higher required")

    # Python 2 compatibility code
    PY2 = sys.version_info[0] == 2
    if not PY2:
        from urllib.parse import urlencode
        from urllib.request import urlopen
        from urllib.error import HTTPError
        print_bytes = lambda s: sys.stdout.buffer.write(s)
    else:
        from urllib import urlencode
        from urllib2 import HTTPError, urlopen
        print_bytes = lambda s: sys.stdout.write(s)



    def arxiv_request(ids):
        """Sends a request to the arxiv API."""
        q = urlencode([
            ("id_list", ",".join(ids))
            ])
        xml = urlopen("http://export.arxiv.org/api/query?" + q)
        # xml.read() returns bytes, but ElementTree.fromstring decodes
        # to unicode when needed (python2) or string (python3)
        return ElementTree.fromstring(xml.read())
    
    ATOM = '{http://www.w3.org/2005/Atom}'

    xml = arxiv_request([arxiv_id])

    entries = xml.findall(ATOM + "entry")

    title = entries[0].find(ATOM + 'title').text.strip()

    url = 'https://arxiv.org/abs/%s' % arxiv_id

    return '[{}]({})'.format(title, url)

def ref2md(filein, sid):
    assert filein.endswith('.md') 
    fileout = filein.replace(".md", "_out.md")
    
    sys.stdout = open(fileout, "w")

    count = sid
    with open(filein, 'r') as f: 
        for line in f: 
            # skip the empty ones
            if line.strip() == '':
                continue
            
            line_doi = get_doi(line)
            line_arxiv = get_arxiv(line)

            if line_doi:
                print('{}. {}'.format(count, line_doi))
            elif line_arxiv:
                print('{}. {}'.format(count, line_arxiv))
            else:
                print(line)
            print()

            count += 1

    sys.stdout.close()


def main():
    global args
    args = parse_args()

    ref2md(args.path, args.sid)



if __name__ == "__main__":
    # usage:
    # 1. download the file into file.md

    md_file = """
1. A. Kulesza, B. Taskar, Determinantal point processes for machine learning, Found. Trends Mach. Learn. 5 (2012) 123–286. doi:10.1561/2200000044.

2. J. Fei, C.-N. Yeh, E. Gull, Nevanlinna Analytical Continuation, (2020) 1–6. http://arxiv.org/abs/2010.04572.

3. J. Nigam, S. Pozdnyakov, M. Ceriotti, Recursive evaluation and iterative contraction of $N$-body equivariant features, 121101 (2020). doi:10.1063/5.0021116.

4. S. Becker, M. Embree, J. Wittsten, M. Zworski, Spectral characterization of magic angles in twisted bilayer graphene, (2020) 1–14. http://arxiv.org/abs/2010.05279.

5. R.A. Lang, I.G. Ryabinkin, A.F. Izmaylov, Unitary transformation of the electronic Hamiltonian with an exact quadratic truncation of the Baker-Campbell-Hausdorff expansion, (2020) 1–38. doi:10.1021/acs.jctc.0c00170.

6. P. Jakobsen, F. Jensen, Representing Exact Electron Densities by a Single Slater Determinant in Finite Basis Sets, (2020). doi:10.1021/acs.jctc.0c01029.

7. D. Chaykin, C. Jansson, F. Keil, M. Lange, K.T. Ohlhus, S.M. Rump, Rigorous Lower Bounds for the Ground State Energy of Molecules by Employing Necessary N-Representability Conditions, J. Chem. Theory Comput. (2020). doi:10.1021/acs.jctc.0c00497.

8. P. V. Sriluckshmy, M. Nusspickel, E. Fertitta, G.H. Booth, Fully Algebraic and Self-consistent Effective Dynamics in a Static Quantum Embedding, (2020). http://arxiv.org/abs/2012.05837.

9. H.K. Tran, H.-Z. Ye, T. Van Voorhis, Bootstrap embedding with an unrestricted mean-field bath, J. Chem. Phys. 153 (2020) 214101. doi:10.1063/5.0029092.

10. D. Luo, G. Carleo, B.K. Clark, J. Stokes, Gauge equivariant neural networks for quantum lattice gauge theories, (2020). http://arxiv.org/abs/2012.05232.

11. Q. Gu, L. Zhang, J. Feng, Neural network representation of electronic structure from ab initio molecular dynamics, (2020) 1–8. http://arxiv.org/abs/2011.13774.

12. B. Leimkuhler, M. Sachs, Efficient Numerical Algorithms for the Generalized Langevin Equation, (2020) 1–33. http://arxiv.org/abs/2012.04245.

13. G.Q. Ai, et al Accurately computing electronic properties of materials using eigenenergies, (2020). https://arxiv.org/abs/2012.00921

14. Y. Chen, et al, Spectral signatures of many-body localization with interacting photons, (n.d.). https://arxiv.org/pdf/1709.07108.pdf

15. A. Hashim, R.K. Naik, A. Morvan, J.-L. Ville, B. Mitchell, J.M. Kreikebaum, M. Davis, E. Smith, C. Iancu, K.P. O’Brien, I. Hincks, J.J. Wallman, J. Emerson, I. Siddiqi, Randomized compiling for scalable quantum computing on a noisy superconducting quantum processor, (2020). http://arxiv.org/abs/2010.00215.

16. A. Nahum, S. Vijay, J. Haah, Operator Spreading in Random Unitary Circuits, Phys. Rev. X. 8 (2018) 021014. doi:10.1103/PhysRevX.8.021014.

17. C.W. Von Keyserlingk, T. Rakovszky, F. Pollmann, S.L. Sondhi, Operator Hydrodynamics, OTOCs, and Entanglement Growth in Systems without Conservation Laws, Phys. Rev. X. 8 (2018) 21013. doi:10.1103/PhysRevX.8.021013.

18. F. Arute, et al Observation of separated dynamics of charge and spin in the Fermi-Hubbard model, (2020). http://arxiv.org/abs/2010.07965.

20. S. Lu, M.C. Bañuls, J.I. Cirac, Algorithms for quantum simulation at finite energies, ArXiv. (2020) 1–18.

21. I.D. Kivlichan, N. Wiebe, R. Babbush, A. Aspuru-Guzik, Bounding the costs of quantum simulation of many-body physics in real space, J. Phys. A Math. Theor. 50 (2017) 305301. doi:10.1088/1751-8121/aa77b8.

22. M. Kolodrubetz, D. Sels, P. Mehta, A. Polkovnikov, Geometry and non-adiabatic response in quantum and classical systems, Phys. Rep. 697 (2017) 1–87. doi:10.1016/j.physrep.2017.07.001.

23. G. Verdon, J. Marks, S. Nanda, S. Leichenauer, J. Hidary, Quantum Hamiltonian-Based Models & the Variational Quantum Thermalizer Algorithm, (2019) 1–21.

24. X. Yuan, S. Endo, Q. Zhao, Y. Li, S.C. Benjamin, Theory of variational quantum simulation, Quantum. 3 (2019) 191. doi:10.22331/q-2019-10-07-191.

25. T. Giurgica-Tiron, I. Kerenidis, F. Labib, A. Prakash, W. Zeng, Low depth algorithms for quantum amplitude estimation, (2020) 1–27. http://arxiv.org/abs/2012.03348.

26. K. Bharti, T. Haug, Iterative Quantum Assisted Eigensolver, (2020) 1–10. http://arxiv.org/abs/2010.05638.

27. A. Roggero, C. Gu, A. Baroni, T. Papenbrock, Preparation of excited states on a quantum computer, (2020) 1–25. http://arxiv.org/abs/2009.13485.

28. S. Chakraborty, L. Novo, J. Roland, Finding a marked node on any graph via continuous-time quantum walks, Phys. Rev. A. 102 (2020). doi:10.1103/PhysRevA.102.022227.

29. A. Kardashin, A. Uvarov, D. Yudin, J. Biamonte, Certified variational quantum algorithms for eigenstate preparation, ArXiv. (2020) 1–9. doi:10.1103/PhysRevA.102.052610.

30. C. Lin, D. Sels, Y. Ma, Y. Wang, Stochastic optimal control formalism for an open quantum system, Phys. Rev. A. 102 (2020) 52605. doi:10.1103/PhysRevA.102.052605.

31. J. Helsen, I. Roth, E. Onorati, A.H. Werner, J. Eisert, A general framework for randomized benchmarking, (2020) 1–60. http://arxiv.org/abs/2010.07974.

32. D. Grinko, J. Gacon, C. Zoufal, S. Woerner, Iterative quantum amplitude estimation, ArXiv. (2019) 1–13.

33. B. Collins, P. Śniady, Integration with respect to the Haar measure on unitary, orthogonal and symplectic group, Commun. Math. Phys. 264 (2006) 773–795. doi:10.1007/s00220-006-1554-3.

34. Simulating Large Quantum Circuits on a Small Quantum Computer, https://arxiv.org/abs/1904.00102
    """

    # testing 
    fname = 'ref.md'
    sys.stdout = open(fname, "w")
    print(md_file)
    sys.stdout.close()
    

    ref2md(fname, 1)

