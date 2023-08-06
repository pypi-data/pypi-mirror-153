import os
import gseapy
import plotly.graph_objects as go
import tempfile


COLORS = ["lavender", "rosybrown", "snow", "mistyrose", "salmon",
          "peachpuff", "bisque", "antiquewhite", "wheat", "mistyrose",
          "honeydew", "mediumaquamarine", "lightcyan", "skyblue", "lightgray",
          "thistle", "pink", "seashell", "lightsteelblue", "ivory"]


REF = {
    "bp": "GO_Biological_Process_2021",
    "cc": "GO_Cellular_Component_2021",
    "mf": "GO_Molecular_Function_2021",
    "pw": "KEGG_2016",
    "KEGG": "KEGG_2016",
    "Reactome": "Reactome_2016",
    "WikiPathways": "WikiPathways_2016",
    "MSigDB_C": "MSigDB_Computational",
    "MSigDB_O_S": "MSigDB_Oncogenic_Signatures",
}


class Gene:
    """this saves a genes module, BP term, CC term, MF term & pathway"""

    def __init__(self, name="", cluster=""):
        self.name = name
        self.cluster = cluster
        self.bp_terms = []
        self.cc_terms = []
        self.mf_terms = []
        self.pathways = []
        self.reactome_pathways = []
        self.Wiki_pathways = []
        self.MSigDB_C_pathways = []
        self.MSigDB_O_S_pathways = []

    def add_bp_term(self, bp_term=""):
        self.bp_terms.append(bp_term)

    def add_cc_term(self, cc_term=""):
        self.cc_terms.append(cc_term)

    def add_mf_term(self, mf_term=""):
        self.mf_terms.append(mf_term)

    def add_pathway(self, pathway=""):
        self.pathways.append(pathway)

    def add_reactome_pathway(self, pathway=""):
        self.reactome_pathways.append(pathway)

    def add_wiki_pathway(self, pathway=""):
        self.Wiki_pathways.append(pathway)

    def add_msigdb_c_pathway(self, pathway=""):
        self.MSigDB_C_pathways.append(pathway)

    def add_msigdb_o_s_pathway(self, pathway=""):
        self.MSigDB_O_S_pathways.append(pathway)

    def add_positions(self, node_positions):
        new_attributes = []
        for attributes in self.__dict__.values():
            if attributes == self.name or attributes == self.cluster:
                continue
            for attr in attributes:
                if attr not in node_positions:
                    new_attributes.append(attr)
        return new_attributes


# clustering
def get_genes(data):

    genes_1 = []
    genes_2 = []
    cluster = 0
    if data.get("sample"):
        if data.get("mode") == "KeyPathwayMiner":
            genes_1, cluster = get_genes_kpm("static/sample_data/KPM", 0)
        elif data.get("mode") == "BiCoN":
            genes_1, cluster = get_genes_bicon("static/sample_data/BiCoN", "results.csv", 0)
    else:
        upload_dir = data.get("temp") + "/uploads/"
        if data.get("mode") == "KeyPathwayMiner":
            genes_1, cluster = get_genes_kpm(upload_dir, 0)
        elif data.get("mode") == "BiCoN":
            genes_1, cluster = get_genes_bicon(upload_dir, data.get("file").filename, 0)
        elif data.get("mode") == "Upload own clusters":
            genes_1, cluster = get_genes_standard(upload_dir, 0)

    if data.get("sample_2"):
        if data.get("mode_2") == "KeyPathwayMiner":
            genes_2, _ = get_genes_kpm("static/sample_data/KPM", cluster)
        if data.get("mode_2") == "BiCoN":
            genes_2, _ = get_genes_bicon("static/sample_data/BiCoN", "results.csv", cluster)
    else:
        upload_dir = data.get("temp") + "/uploads/second/"
        if data.get("mode_2") == "KeyPathwayMiner":
            genes_2, _ = get_genes_kpm(upload_dir, cluster)
        if data.get("mode_2") == "BiCoN":
            genes_2, _ = get_genes_bicon(upload_dir, data.get("file_2").filename, cluster)
        if data.get("mode_2") == "Upload own clusters":
            genes_2, _ = get_genes_standard(upload_dir, cluster)

    return genes_1, genes_2


def get_genes_kpm(directory, start):
    genes = []
    cluster = start
    for file in os.listdir(directory):
        if file.endswith("-NODES-.txt"):
            cluster += 1
            with open(os.path.join(directory, file), 'r') as f:
                for line in f:
                    name = line.strip()
                    gene = Gene(name=name, cluster=str(cluster))
                    genes.append(gene)
    return genes, cluster+1


def get_genes_bicon(directory, file, start):
    genes = []
    if directory is not None:
        fi = (os.path.join(directory, file))
    else:
        fi = file
    with open(fi, 'r') as f:
        for line in f:
            gene_array = line.split(",")
            if gene_array[0] == "":
                continue
            genes1_string = gene_array[1]
            genes2_string = gene_array[2]
            genes1 = genes1_string.split("|")
            genes2 = genes2_string.split("|")
            for name in genes1:
                gene = Gene(name=name, cluster=str(start))
                genes.append(gene)
            for name in genes2:
                gene = Gene(name=name, cluster=str(start+1))
                genes.append(gene)
            return genes, start+2


def get_genes_standard(directory, start):
    genes = []
    cluster = start
    for file in os.listdir(directory):
        cluster += 1
        with open(os.path.join(directory, file), 'r') as f:
            for line in f:
                name = line.strip()
                gene = Gene(name=name, cluster=str(cluster))
                genes.append(gene)
    return genes, cluster+1


# enriching
def read_gene_sets(data):
    gene_sets = []
    if data.get("bp"):
        gene_sets.append(REF["bp"])
    if data.get("cc"):
        gene_sets.append(REF["cc"])
    if data.get("mf"):
        gene_sets.append(REF["mf"])
    if data.get("pw"):
        gene_sets.append(REF["KEGG"])
    if data.get("KEGG"):
        if "KEGG_2016" not in gene_sets:
            gene_sets.append(REF["KEGG"])
    if data.get("Reactome"):
        gene_sets.append(REF["Reactome"])
    if data.get("WikiPathways"):
        gene_sets.append(REF["WikiPathways"])
    if data.get("MSigDB_C"):
        gene_sets.append(REF["MSigDB_C"])
    if data.get("MSigDB_O_S"):
        gene_sets.append(REF["MSigDB_O_S"])
    return gene_sets


def enrich(genes, output_directory, gene_sets, cutoff):
    sig_genes = []
    for gene in genes:
        sig_genes.append(gene.name)
    for gene_set in gene_sets:
        gseapy.enrichr(gene_list=sig_genes,
                       description=gene_set[0:len(gene_set) - 5],
                       gene_sets=gene_set,
                       outdir=output_directory,
                       cutoff=cutoff
                       )


# assigning terms & pathways
def read_data(genes, directory, only_best, cutoff):
    for file in os.listdir(directory):
        if file.endswith("reports.txt"):
            with open(os.path.join(directory, file), 'r') as f:
                for line in f:
                    if line.startswith("Gene_set"):
                        continue
                    line = line.strip()
                    words = line.split("\t")
                    score = float(words[4])
                    if score < cutoff:
                        term_genes = words[9].split(";")
                        for gene in genes:
                            if gene.name.upper() in term_genes:
                                if file.startswith("GO_Biological_Process"):
                                    if only_best:
                                        if len(gene.bp_terms) == 0:
                                            gene.add_bp_term(bp_term=words[1])
                                    else:
                                        gene.add_bp_term(bp_term=words[1])
                                elif file.startswith("GO_Cellular_Component"):
                                    if only_best:
                                        if len(gene.cc_terms) == 0:
                                            gene.add_cc_term(cc_term=words[1])
                                    else:
                                        gene.add_cc_term(cc_term=words[1])
                                elif file.startswith("GO_Molecular_Function"):
                                    if only_best:
                                        if len(gene.mf_terms) == 0:
                                            gene.add_mf_term(mf_term=words[1])
                                    else:
                                        gene.add_mf_term(mf_term=words[1])
                                elif file.startswith("KEGG"):
                                    if only_best:
                                        if len(gene.pathways) == 0:
                                            gene.add_pathway(pathway=words[1])
                                    else:
                                        gene.add_pathway(pathway=words[1])
                                elif file.startswith("Reactome"):
                                    if only_best:
                                        if len(gene.reactome_pathways) == 0:
                                            gene.add_reactome_pathway(pathway=words[1])
                                    else:
                                        gene.add_reactome_pathway(pathway=words[1])
                                elif file.startswith("WikiPathways"):
                                    if only_best:
                                        if len(gene.Wiki_pathways) == 0:
                                            gene.add_wiki_pathway(pathway=words[1])
                                    else:
                                        gene.add_wiki_pathway(pathway=words[1])
                                elif file.startswith("MSigDB_Computational"):
                                    if only_best:
                                        if len(gene.MSigDB_C_pathways) == 0:
                                            gene.add_msigdb_c_pathway(pathway=words[1])
                                    else:
                                        gene.add_msigdb_c_pathway(pathway=words[1])
                                elif file.startswith("MSigDB_Oncogenic_Signatures"):
                                    if only_best:
                                        if len(gene.MSigDB_O_S_pathways) == 0:
                                            gene.add_msigdb_o_s_pathway(pathway=words[1])
                                    else:
                                        gene.add_msigdb_o_s_pathway(pathway=words[1])


# generating results
def get_results(genes, mode, from_own, font_size):
    node_positions = {}
    position = 0

    for gene in genes:
        cluster_string = "cluster " + gene.cluster
        if cluster_string not in node_positions:
            node_positions[cluster_string] = position
            position += 1

    for gene in genes:
        for attr in gene.add_positions(node_positions):
            node_positions[attr] = position
            position += 1

    data = []
    for gene in genes:

        if mode == "GO":
            if from_own:
                first = gene.pathways
            else:
                first = []
            second = gene.bp_terms
            third = gene.cc_terms
            fourth = gene.mf_terms
            fifth = []
        else:
            if from_own:
                first = gene.pathways
            else:
                first = []
            second = gene.reactome_pathways
            third = gene.Wiki_pathways
            fourth = gene.MSigDB_C_pathways
            fifth = gene.MSigDB_O_S_pathways

        if len(first) != 0:
            for fir in first:
                data.append(
                    dict(
                        source=node_positions["cluster " + gene.cluster],
                        target=node_positions[fir],
                        genes=[gene.name],
                        value=1,
                        cluster="cluster " + gene.cluster
                    )
                )
                if len(second) != 0:
                    for sec in second:
                        data.append(
                            dict(
                                source=node_positions[fir],
                                target=node_positions[sec],
                                genes=[gene.name],
                                value=1,
                                cluster="cluster " + gene.cluster
                            )
                        )
                        if len(third) != 0:
                            for thi in third:
                                data.append(
                                    dict(
                                        source=node_positions[sec],
                                        target=node_positions[thi],
                                        genes=[gene.name],
                                        value=1,
                                        cluster="cluster " + gene.cluster
                                    )
                                )
                                if len(fourth) != 0:
                                    for fou in fourth:
                                        data.append(
                                            dict(
                                                source=node_positions[thi],
                                                target=node_positions[fou],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                        if len(fifth) != 0:
                                            for fif in fifth:
                                                data.append(
                                                    dict(
                                                        source=node_positions[fou],
                                                        target=node_positions[fif],
                                                        genes=[gene.name],
                                                        value=1,
                                                        cluster="cluster " + gene.cluster
                                                    )
                                                )
                                        else:
                                            continue
                                else:
                                    if len(fifth) != 0:
                                        for fif in fifth:
                                            data.append(
                                                dict(
                                                    source=node_positions[thi],
                                                    target=node_positions[fif],
                                                    genes=[gene.name],
                                                    value=1,
                                                    cluster="cluster " + gene.cluster
                                                )
                                            )
                                    else:
                                        continue
                        else:
                            if len(fourth) != 0:
                                for fou in fourth:
                                    data.append(
                                        dict(
                                            source=node_positions[sec],
                                            target=node_positions[fou],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                                    if len(fifth) != 0:
                                        for fif in fifth:
                                            data.append(
                                                dict(
                                                    source=node_positions[fou],
                                                    target=node_positions[fif],
                                                    genes=[gene.name],
                                                    value=1,
                                                    cluster="cluster " + gene.cluster
                                                )
                                            )
                                    else:
                                        continue
                            else:
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[sec],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                else:
                    if len(third) != 0:
                        for thi in third:
                            data.append(
                                dict(
                                    source=node_positions[fir],
                                    target=node_positions[thi],
                                    genes=[gene.name],
                                    value=1,
                                    cluster="cluster " + gene.cluster
                                )
                            )
                            if len(fourth) != 0:
                                for fou in fourth:
                                    data.append(
                                        dict(
                                            source=node_positions[thi],
                                            target=node_positions[fou],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                                    if len(fifth) != 0:
                                        for fif in fifth:
                                            data.append(
                                                dict(
                                                    source=node_positions[fou],
                                                    target=node_positions[fif],
                                                    genes=[gene.name],
                                                    value=1,
                                                    cluster="cluster " + gene.cluster
                                                )
                                            )
                                    else:
                                        continue
                            else:
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[thi],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                    else:
                        if len(fourth) != 0:
                            for fou in fourth:
                                data.append(
                                    dict(
                                        source=node_positions[fir],
                                        target=node_positions[fou],
                                        genes=[gene.name],
                                        value=1,
                                        cluster="cluster " + gene.cluster
                                    )
                                )
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[fou],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                        else:
                            if len(fifth) != 0:
                                for fif in fifth:
                                    data.append(
                                        dict(
                                            source=node_positions[fir],
                                            target=node_positions[fif],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                            else:
                                continue
        else:
            if len(second) != 0:
                for sec in second:
                    data.append(
                        dict(
                            source=node_positions["cluster " + gene.cluster],
                            target=node_positions[sec],
                            genes=[gene.name],
                            value=1,
                            cluster="cluster " + gene.cluster
                        )
                    )
                    if len(third) != 0:
                        for thi in third:
                            data.append(
                                dict(
                                    source=node_positions[sec],
                                    target=node_positions[thi],
                                    genes=[gene.name],
                                    value=1,
                                    cluster="cluster " + gene.cluster
                                )
                            )
                            if len(fourth) != 0:
                                for fou in fourth:
                                    data.append(
                                        dict(
                                            source=node_positions[thi],
                                            target=node_positions[fou],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                                    if len(fifth) != 0:
                                        for fif in fifth:
                                            data.append(
                                                dict(
                                                    source=node_positions[fou],
                                                    target=node_positions[fif],
                                                    genes=[gene.name],
                                                    value=1,
                                                    cluster="cluster " + gene.cluster
                                                )
                                            )
                                    else:
                                        continue
                            else:
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[thi],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                    else:
                        if len(fourth) != 0:
                            for fou in fourth:
                                data.append(
                                    dict(
                                        source=node_positions[sec],
                                        target=node_positions[fou],
                                        genes=[gene.name],
                                        value=1,
                                        cluster="cluster " + gene.cluster
                                    )
                                )
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[fou],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                        else:
                            if len(fifth) != 0:
                                for fif in fifth:
                                    data.append(
                                        dict(
                                            source=node_positions[sec],
                                            target=node_positions[fif],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                            else:
                                continue
            else:
                if len(third) != 0:
                    for thi in third:
                        data.append(
                            dict(
                                source=node_positions["cluster " + gene.cluster],
                                target=node_positions[thi],
                                genes=[gene.name],
                                value=1,
                                cluster="cluster " + gene.cluster
                            )
                        )
                        if len(fourth) != 0:
                            for fou in fourth:
                                data.append(
                                    dict(
                                        source=node_positions[thi],
                                        target=node_positions[fou],
                                        genes=[gene.name],
                                        value=1,
                                        cluster="cluster " + gene.cluster
                                    )
                                )
                                if len(fifth) != 0:
                                    for fif in fifth:
                                        data.append(
                                            dict(
                                                source=node_positions[fou],
                                                target=node_positions[fif],
                                                genes=[gene.name],
                                                value=1,
                                                cluster="cluster " + gene.cluster
                                            )
                                        )
                                else:
                                    continue
                        else:
                            if len(fifth) != 0:
                                for fif in fifth:
                                    data.append(
                                        dict(
                                            source=node_positions[thi],
                                            target=node_positions[fif],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                            else:
                                continue
                else:
                    if len(fourth) != 0:
                        for fou in fourth:
                            data.append(
                                dict(
                                    source=node_positions["cluster " + gene.cluster],
                                    target=node_positions[fou],
                                    genes=[gene.name],
                                    value=1,
                                    cluster="cluster " + gene.cluster
                                )
                            )
                            if len(fifth) != 0:
                                for fif in fifth:
                                    data.append(
                                        dict(
                                            source=node_positions[fou],
                                            target=node_positions[fif],
                                            genes=[gene.name],
                                            value=1,
                                            cluster="cluster " + gene.cluster
                                        )
                                    )
                            else:
                                continue
                    else:
                        if len(fifth) != 0:
                            for fif in fifth:
                                data.append(
                                    dict(
                                        source=node_positions["cluster " + gene.cluster],
                                        target=node_positions[fif],
                                        genes=[gene.name],
                                        value=1,
                                        cluster="cluster " + gene.cluster
                                    )
                                )
                        else:
                            continue

    if len(data) == 0:
        return None

    for entry in data:
        for next_entry in data:
            if entry["source"] == next_entry["source"] \
                    and entry["target"] == next_entry["target"] \
                    and entry["cluster"] == next_entry["cluster"] \
                    and next_entry["genes"][0] not in entry["genes"]:
                entry["genes"].append(next_entry["genes"][0])
                entry["value"] += 1

    found_start_ends = []
    filtered_data = []

    for entry in data:
        if (entry["source"], entry["target"], set(entry["genes"])) not in found_start_ends:
            found_start_ends.append((entry["source"], entry["target"], set(entry["genes"])))
            filtered_data.append(entry)

    s_data = {
        "type": "sankey",
        "orientation": "h",
        "node": {
            "pad": 15,
            "thickness": 30,
            "line": {
                "color": "black",
                "width": 0.5
            },
            "label": list(node_positions.keys()),
            "color": "blue"
        },
        "link": {
            "source": [],
            "target": [],
            "value": [],
            "label": [],
            "color": [],
            "line": {
                "color": "black",
                "width": 0.1
            }   # maybe leaving this part out for smoother plots
        },
        "textfont": dict(color="black", size=font_size),
    }

    for entry in filtered_data:
        s_data.get("link").get("source").append(entry["source"])
        s_data.get("link").get("target").append(entry["target"])
        s_data.get("link").get("value").append(entry["value"])
        s_data.get("link").get("label").append(entry["genes"])
        s_data.get("link").get("color").append(COLORS[node_positions[entry["cluster"]]])

    return s_data


# generating comparison results
def get_comp_results(genes_1, genes_2, font_size):
    node_positions = {}
    position = 0

    for gene in genes_1:
        cluster_string = "cluster " + gene.cluster
        if cluster_string not in node_positions:
            node_positions[cluster_string] = position
            position += 1

    for gene in genes_2:
        cluster_string = "cluster " + gene.cluster
        if cluster_string not in node_positions:
            node_positions[cluster_string] = position
            position += 1

    data = []
    for gene in genes_1:
        for gene_2 in genes_2:
            if gene.name == gene_2.name:
                data.append(
                    dict(
                        source=node_positions["cluster " + gene.cluster],
                        target=node_positions["cluster " + gene_2.cluster],
                        genes=[gene.name],
                        value=1,
                        cluster="cluster " + gene.cluster
                    )
                )
                break

    if len(data) == 0:
        return None

    for entry in data:
        for next_entry in data:
            if entry["source"] == next_entry["source"] \
                    and entry["target"] == next_entry["target"] \
                    and entry["cluster"] == next_entry["cluster"] \
                    and next_entry["genes"][0] not in entry["genes"]:
                entry["genes"].append(next_entry["genes"][0])
                entry["value"] += 1

    found_start_ends = []
    filtered_data = []

    for entry in data:
        if (entry["source"], entry["target"], set(entry["genes"])) not in found_start_ends:
            found_start_ends.append((entry["source"], entry["target"], set(entry["genes"])))
            filtered_data.append(entry)

    s_data = {
        "type": "sankey",
        "orientation": "h",
        "node": {
            "pad": 15,
            "thickness": 30,
            "line": {
                "color": "black",
                "width": 0.5
            },
            "label": list(node_positions.keys()),
            "color": "blue"
        },
        "link": {
            "source": [],
            "target": [],
            "value": [],
            "label": [],
            "color": [],
            "line": {
                "color": "black",
                "width": 0.1
            },  # maybe leaving this part out for smoother plots
            "textfont": dict(color="black", size=font_size),
        }
    }

    for entry in filtered_data:
        s_data.get("link").get("source").append(entry["source"])
        s_data.get("link").get("target").append(entry["target"])
        s_data.get("link").get("value").append(entry["value"])
        s_data.get("link").get("label").append(entry["genes"])
        s_data.get("link").get("color").append(COLORS[node_positions[entry["cluster"]]])

    return s_data


# showing the Plotly plots
def show_plots(go_data, pw_data, comp_data):
    if go_data is not None:
        fig = go.Figure(data=go_data)
        fig.show()
    if pw_data is not None:
        fig_2 = go.Figure(data=pw_data)
        fig_2.show()
    if comp_data is not None:
        fig_3 = go.Figure(data=comp_data)
        fig_3.show()


# cleaning working directories
def clean_directories(directories):
    for directory in directories:
        for file in os.listdir(directory):
            if not file.endswith(".log"):
                os.remove(os.path.join(directory, file))


# main method for app
def sankey(data):

    gsea_dir = data.get("temp") + "/gsea/"

    genes_1, genes_2 = get_genes(data)
    if len(genes_1) == 0:
        return

    gene_sets = read_gene_sets(data)
    cutoff = float(data.get("cutoff"))

    only_best = True
    if data.get("all"):
        only_best = False

    enrich(genes_1, gsea_dir, gene_sets, cutoff)
    read_data(genes_1, gsea_dir, only_best, cutoff)

    go_data = None
    pw_data = None
    comp_data = None
    if data.get("bp") \
            or data.get("cc") \
            or data.get("mf") \
            or data.get("pw"):
        go_data = get_results(genes_1, "GO", data.get("pw"))
    if data.get("KEGG") \
            or data.get("Reactome") \
            or data.get("WikiPathways") \
            or data.get("MSigDB_C") \
            or data.get("MSigDB_O_S"):
        pw_data = get_results(genes_1, "PW", data.get("KEGG"))
    if len(genes_2) != 0:
        comp_data = get_comp_results(genes_1, genes_2)

    return go_data, pw_data, comp_data


# main method for package use
def run(**kwargs):

    mode = kwargs.get("mode")
    data = kwargs.get("data")
    mode_2 = kwargs.get("mode_2")
    data_2 = kwargs.get("data_2")
    gsea_dir = kwargs.get("gsea_dir")
    go_terms = kwargs.get("GO")
    pw = kwargs.get("PW")
    all_flag = kwargs.get("all")
    cutoff = kwargs.get("cutoff")
    font_size = kwargs.get("font_size")

    file_path = os.path.realpath(__file__)
    file_dir = file_path[0:len(file_path) - len(os.path.basename(__file__))]
    sample_data_dir = file_dir[0:len(file_dir) - 4] + "sample_data/"

    print("reading data...")
    if data is None:
        if mode == "KPM":
            data = sample_data_dir + "KPM/"
        elif mode == "BiCoN":
            data = sample_data_dir + "BiCoN/results.csv"
        elif mode == "custom":
            print(f"data needs to be provided for mode: {mode}")
            return -1
        else:
            print(f"invalid mode: {mode}")
            return -1
    if mode == "KPM":
        genes_1, cluster = get_genes_kpm(data, 0)
    elif mode == "BiCoN":
        genes_1, cluster = get_genes_bicon(None, data, 0)
    elif mode == "custom":
        genes_1, cluster = get_genes_standard(data, 0)
    else:
        print(f"invalid mode: {mode}")
        return -1

    print("reading second data...")
    genes_2 = []
    if data_2 is None:
        if mode_2 == "KPM":
            data_2 = sample_data_dir + "KPM/"
        elif mode_2 == "BiCoN":
            data_2 = sample_data_dir + "BiCoN/results.csv"
        elif mode_2 == "custom":
            print(f"data needs to be provided for mode: {mode_2}")
            return -1
        else:
            print(f"invalid mode: {mode_2}")
            return -1
    if mode_2 == "KPM":
        genes_2, _ = get_genes_kpm(data_2, cluster)
    elif mode_2 == "BiCoN":
        genes_2, _ = get_genes_bicon(None, data_2, cluster)
    elif mode_2 == "custom":
        genes_2, _ = get_genes_standard(data_2, cluster)
    elif mode_2 is None:
        pass
    else:
        print(f"invalid mode: {mode_2}")
        return -1

    print("defining gene sets...")
    perform_go_analysis = False
    perform_pw_analysis = False

    length = 0
    gene_sets = []
    from_go = False
    if go_terms is not None:
        for gene_set_key in go_terms:
            if gene_set_key not in gene_sets:
                if gene_set_key not in REF.keys():
                    print(f"unknown apafea gen set index: {gene_set_key}. Please check github for valid indices.")
                    continue
                gene_sets.append(REF[gene_set_key])
                if gene_set_key == "KEGG":
                    from_go = True
        if len(gene_sets) != 0:
            perform_go_analysis = True
            length = len(gene_sets)

    from_pw = False
    if pw is not None:
        for pathway_key in pw:
            if pathway_key not in gene_sets:
                if pathway_key not in REF.keys():
                    print(f"unknown apafea gen set index: {pathway_key}. Please check github for valid indices.")
                    continue
                gene_sets.append(REF[pathway_key])
                if pathway_key == "KEGG":
                    from_pw = True
        if len(gene_sets) > length:
            perform_pw_analysis = True

    print("enriching...")
    if gsea_dir is None:
        tmp_dir = tempfile.TemporaryDirectory()
        gsea_dir = tmp_dir.name
    enrich(genes_1, gsea_dir, gene_sets, cutoff)

    print("associating genes with GO-Terms/Pathways...")
    only_best = True
    if all_flag is not None:
        if all_flag:
            only_best = False
    if cutoff is None:
        cutoff = 0.05
    read_data(genes_1, gsea_dir, only_best, cutoff)

    print("creating results...")
    go_data = None
    pw_data = None
    comp_data = None
    if font_size is None:
        font_size = 1
    if perform_go_analysis:
        go_data = get_results(genes_1, "GO", from_go, font_size)
    if perform_pw_analysis:
        pw_data = get_results(genes_1, "PW", from_pw, font_size)
    if len(genes_2) != 0:
        comp_data = get_comp_results(genes_1, genes_2, font_size)

    print("showing results...")
    show_plots(go_data, pw_data, comp_data)
