rule all:
    input:
        "output/report.csv"

rule seed_taxonomy:
    output:
        touch(".snakemake_markers/01_seed.done")
    shell:
        "python3 scripts/01_seed_taxonomy.py"

rule process_audio:
    input:
        ".snakemake_markers/01_seed.done"
    output:
        touch(".snakemake_markers/03_audio.done")
    shell:
        "python3 scripts/03_process_audio.py"

rule generate_report:
    input:
        ".snakemake_markers/03_audio.done"
    output:
        "output/report.csv"
    shell:
        "python3 scripts/04_generate_report.py"