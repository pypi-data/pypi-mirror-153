from .src import run


def main():
    run(
        mode="KPM",
        # data="/absolute/path/to/directory/",
        mode_2="BiCoN",
        # data_2="/absolute/path/to/results.csv",
        # gsea_dir="/absolute/path/to/gsea/directory/",
        GO=["bp",
            "cc",
            "mf",
            "pw"],
        PW=["KEGG",
            "Reactome",
            "WikiPathways",
            "MSigDB_C",
            "MSigDB_O_S"],
        all=False,
        cutoff=0.05,
    )


if __name__ == '__main__':
    main()
