__version__ = "v0.3.3"

import argparse
import re
import os
import os.path
import pandas
import sys
import textwrap
import statistics
import copy
import csv
import gzip
import collections
from alive_progress import alive_it

from .utils import *

###################################################################
# 2021.10.04 added more warnings to merge
# 2021.11.20 revamped merge to be a two step process allowing for edits
# 2022.01.02 fixed a bug in the merge_sampleset that was misnaming file

# TODO rename write_fastq_from_mergedsheet

###################################################################
# INITIALIZE GLOBAL VARIABLES #####################################
###################################################################

subcommands = {}

global_samples_tsv_header = [
    "sample_name",
    "sample_set",
    "replicate",
    "probe_set",
    "fw",
    "rev",
    "library_prep",
]

global_samples_tsv_header_optional = [
    "capture_plate",
    "quadrant",
    "capture_plate_row",
    "capture_plate_column",
    "384_column",
    "sample_plate",
    "sample_plate_column",
    "sample_plate_row",
    "FW_plate",
    "REV_plate",
    "owner",
]

global_samples_tsv_oldnames = {
    "Library Prep": "library_prep",
    "384 Column": "384_column",
    "row": "sample_plate_row",
    "column": "sample_plate_column",
    "Sample Set": "sample_set",
}

# Below are all the different headers in found in *sample_tsv files. Generated
# via:
# find . -maxdepth 2 -name '*samples.tsv' -exec head -1  {} \; | tr ' ' 'x'  | xargs -n 1 | sort | uniq

# 384xColumn
# capture_plate
# capture_plate_column
# capture_plate_row
# CapturexPlatexLocation
# CapturexPlatexName
# column
# diff
# fw
# FW_plate
# library_prep
# LibraryxPrep
# owner
# probe_set
# quadrant
# replicate
# rev
# REV_plate
# row
# sample_name
# sample_plate
# sample_set
# SamplexSet

###################################################################
###################################################################

###################################################################
#  MAIN        ####################################################
###################################################################


def main(args):
    """Main allows selection of the main subcommand (aka function).
    Each subcommand launches a separate function. The pydoc subcommand
    launches pydoc on this overall program file.
    :param args: the main command line arguments passed minus subcommand
    """
    # print globals().keys()
    # print "ARGUMENTS", args

    if len(args) == 0 or args[0] in [
        "h",
        "help",
        "-h",
        "--h",
        "--help",
        "-help",
    ]:
        verbosity = "shortDesc"
        if args[0] in ["help", "--help", "-help"]:
            verbosity = "longDesc"
        print("VERSION:", __version__)
        print("USAGE: python3 -m mipscripts [-h] subcommand [suboptions]")
        print("DESCRIPTION: various scripts complementing MIPTools pipelines")
        print("SUBCOMMANDS:")
        # tw=TextWrap()
        for k in subcommands.keys():
            text = subcommands[k][verbosity]
            text = textwrap.dedent(text)
            if text:
                text = "%s:   %s " % (k, text)
                print(
                    textwrap.fill(
                        text,
                        80,
                        initial_indent="",
                        subsequent_indent="         ",
                    )
                )
        print("HELP:")
        print("-h/-help   short / long  subcommand descriptions")
        print("For specific options: python3 -m mipscripts [subcommand] --help")
    elif args[0] in subcommands.keys():
        globals()[args[0]](args[1:])
    else:
        print(f"ERROR: Unknown subcommand '{args[0]}'")
        print("\u2022 Use '-h' for a list of subcommands.")
        sys.exit(-1)
    sys.exit(0)


# ------------------------------------------------------------------------------
###############################################################################
####  MERGE FASTQs and SAMPLESHEET for MIPSET  ################################
###############################################################################
# ------------------------------------------------------------------------------
shortDescText = (
    "calculate # of reads for each sample set in a fastq directory of a run"
)
longDescText = (
    """this simply counts the number of fastq reads for a sample set """
)
subcommands["seqrun_stats"] = {
    "shortDesc": shortDescText,
    "longDesc": longDescText,
}


def seqrun_stats(args):
    """commandline routine to examine a sequencing run and determin statistics for performance."""
    aparser = argparse.ArgumentParser(
        prog=os.path.basename(__file__) + " seqrun_stats",
        description="provide read# stats for a sequencing run based on the fastq directory",
        epilog="Note: currently this just scans fastqs--and R1 to save time --nothing fancy.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    aparser.add_argument(
        "--samplesheet",
        required=True,
        action="append",
        help="samplesheet to run on",
    )
    aparser.add_argument(
        "--maingrp",
        required=False,
        help="main grouping for stats",
        default="sample_set",
    )
    aparser.add_argument(
        "--subgrp", required=False, help="sub grouping for stats"
    )
    args = aparser.parse_args(args=args)

    for samplesheet in args.samplesheet:
        # Convert header to snake case
        header_to_snake_case(path=samplesheet, overwrite=True)

        # Initialize a counter for the number of sample sets
        num_sample_sets = collections.Counter()

        # Initialize the grouping dictionary
        groupings = {}

        # Load the sample sheet header and data into memory for fast retrieval
        # Also update the number of sample per sample set
        sampledict = []
        header = []
        with open(samplesheet) as samplefile:
            dictreader = csv.DictReader(samplefile, delimiter="\t")
            header = dictreader.fieldnames
            for row in dictreader:
                sampledict.append(row)
                num_sample_sets.update({row["sample_set"]: 1})

        # Error if arguments are not correct
        if args.maingrp not in header:
            print("ERROR: '--maingrp' invalid.")
            print(f"\u2022 User entered '{args.maingrp}'.")
            print(f"\u2022 Available options: {header}.")
            exit()
        if args.subgrp and args.subgrp not in header:
            print("ERROR: '--subgrp' invaluid.")
            print(f"\u2022 User entered '{args.maingrp}'.")
            print(f"\u2022 Available options: {header}.")
            exit()

        print("####################### FASTQS / READS ########################")
        fastqdir = os.path.dirname(samplesheet) + "/fastq"
        fastqs = os.listdir(fastqdir)
        fqss = [f for f in fastqs if "_R1_" in f]

        # Count the number of fastq reads in each fastq file
        fastqlen = {}
        bar = alive_it(fqss)
        for fq in bar:
            reads = 0
            with gzip.open(f"{fastqdir}/{fq}", mode="rt") as f:
                for line in f:
                    if line.startswith("@"):
                        reads += 1
            fastqlen[fq] = reads
            bar.title("Counting the number of FASTQ reads")

        # Save all fastq file names
        fqfiles = fastqlen.keys()

        # For each row in our data, check if there are multiple fastqs and, if
        # not, set the read count
        for row in sampledict:
            # Define identifier to compare fastqs
            fqname = "{}-{}-{}_".format(
                row["sample_name"], row["sample_set"], row["replicate"]
            )

            # Use regex to check if the fastq name appears multiple times
            regex = re.compile("^" + fqname)
            fqmatchs = list(filter(regex.match, fqfiles))

            if len(fqmatchs) > 1:
                # Throw an error
                print(
                    "ERROR: More than one FASTQ for the sampleset repetition.",
                    fqmatchs,
                    fqname,
                )
                print(
                    "\u2022 This may be because all the fastqs were not erased before"
                )
                print(
                    "  an updated sample sheet was demultiplexed (different S###)."
                )
                exit()
            elif len(fqmatchs) == 1:
                # Set read count
                row["read_count"] = fastqlen[fqmatchs[0]]

            # Create groupings
            # TODO - we don't do anything with the grouping variables
            groupings[row[args.maingrp]] = {}
            if args.subgrp:
                groupings[row[args.maingrp]][row[args.subgrp]] = 1

        # If there were undetermined reads let the user know
        if "Undetermined_S0_R1_001.fastq.gz" in fastqlen:
            cnt = fastqlen["Undetermined_S0_R1_001.fastq.gz"]
            print(f"There were {cnt} undetermined reads from demultipelxing.")

        # Create updated sample sheet
        print("Creating an updated samplesheet with read counts.")
        sheet_root = os.path.splitext(samplesheet)[0]
        read_cnt_path = f"{sheet_root}_readcnt.tsv"
        with open(read_cnt_path, mode="wt") as samplesheetout:
            header.append("read_count")
            dictwriter = csv.DictWriter(
                samplesheetout, delimiter="\t", fieldnames=header
            )
            dictwriter.writeheader()
            for row in sampledict:
                dictwriter.writerow(row)

        print("########################### SAMPLES ###########################")
        print("PER SAMPLE SET SUMMARY:")
        # print(f"SAMPLE GROUPINGS AND # SAMPLES: {groupings}")

        # Print some summary stats on reads for each sample set.
        # Read the read count file in
        read_cnt_data = pandas.read_csv(read_cnt_path, sep="\t")
        for key in num_sample_sets:
            # Print sample set name and number of samples
            print(f"Sample set {key} ({num_sample_sets[key]:,} samples):")

            # Filter data to sample set and isolate reads
            filter_data = read_cnt_data[read_cnt_data.sample_set == key]
            num_samples = filter_data.shape[0]
            reads = filter_data.read_count

            # Print summary stats
            print(f"... TOTAL read pairs: {sum(reads):,}")
            print(f"... MEAN read pairs: {int(statistics.mean(reads)):,}")
            print(f"... MEDIAN read pairs: {statistics.median(reads):,}")

            # Deciles
            if num_samples > 1:
                quantiles = [
                    f"{round(q):,}" for q in statistics.quantiles(reads)
                ]
                print(f"... QUANTILES for read pairs: {quantiles}")


#######################################################################
#######################################################################
#######################################################################
shortDescText = "write fastqs from a mergedsheet.tsv after tsv has been created"
longDescText = """This can be combined with --skipfastqwrite in the main merge_sampleset
to allow for more complicated merges that might require further intermediate manipulation
of the tsv (deleting controls or renaming sample sets).  Idea is you can capture everything you
need and then fix the samplesheet so that the samples will be exactly what you want. 
"""
subcommands["merge_sampleset_write_fastq"] = {
    "shortDesc": shortDescText,
    "longDesc": longDescText,
}

# TODO - this should be changed to write_fastq_from_mergedsheet
def merge_sampleset_write_fastq(args):
    aparser = argparse.ArgumentParser(
        prog=os.path.basename(__file__) + " merge_sampleset",
        description="allows for creation of fastqs after editing of mergedsheet.tsv from a merge_sampleset --skipfastqwrite",
        epilog="Note: simply downloads fastqs in the fastq column using sample_name-sample_set-replicate",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    aparser.add_argument(
        "--mergedsheet",
        required=True,
        help=" sample sheet file paths (dir fastq must be in same dir as sheet)",
    )
    aparser.add_argument(
        "--newfastqdir",
        required=False,
        help="name of new fastq directory",
        default="mergedfastq",
    )
    aparser.add_argument(
        "--skipfastqwrite",
        action="store_true",
        help="dry run so you can see the errors",
    )
    aparser.add_argument(
        "--skipbadfastqs",
        action="store_true",
        help="keep running and just skip bad fastas",
    )
    args = aparser.parse_args(args=args)

    print("CREATING and CLEANING NEW FASTQ DIR:", args.newfastqdir)
    if len(args.newfastqdir) == 1:
        os.system("mkdir " + args.newfastqdir)
        os.system(f"rm {args.newfastqdir}/*")  # too lazy to check if exist
    else:
        print(f"ERROR: bad directory name ({args.newfastqdir})")
        exit()
    # total_bad = 0
    # total = good = 0

    with open(args.mergedsheet, newline="") as items_file:
        items_reader = csv.DictReader(items_file, delimiter="\t")
        # items_total = 0
        for item in items_reader:
            fastqs = item["fastq"].split(",")
            name = "{}-{}-{}".format(
                item["sample_name"], item["sample_set"], item["replicate"]
            )
            if not args.skipfastqwrite:
                print("...", name, "...")
            writeoperator = " > "
            if len(fastqs) % 2 == 0 and len(fastqs) > 1:
                for i in range(0, len(fastqs), 2):
                    if not args.skipfastqwrite:
                        os.system(
                            "cat  "
                            + fastqs[i]
                            + writeoperator
                            + args.newfastqdir
                            + "/"
                            + name
                            + "_R1_001.fastq.gz"
                        )
                        os.system(
                            "cat  "
                            + fastqs[i + 1]
                            + writeoperator
                            + args.newfastqdir
                            + "/"
                            + name
                            + "_R2_001.fastq.gz"
                        )
                    writeoperator = " >> "  # now appending after initial files
            else:
                if args.skipbadfastqs:
                    print("WARN bad fasta paths for ", name, "(", fastqs, ")")
                else:
                    print("ERROR: Bad FASTQ", name, fastqs)
                    print("\u2022 Skip bad FASTQs with '--skipbadfastqs'.")
                    exit(1)


#######################################################################
#######################################################################
#######################################################################
shortDescText = (
    "merge a sampleset from multiple samplesheets and sequencing runs"
)
longDescText = """This subprogram pulls sampleset(s) from multiple samplesheets
and merge the R1 and R2 fastq records based on defined criteria.  It is best to 
run one sampleset at a time.  Please use --skipfastqwrite to test your merge before
allowing the slower process of writing the merged fastqs.   Also, if you need to manipulate/edit
the tsv file you can create the merged fastqs subsequently from the edited version using
merge_sampleset_write_fastqs.

"""
subcommands["merge_sampleset"] = {
    "shortDesc": shortDescText,
    "longDesc": longDescText,
}


def merge_sampleset(args):
    """commandline routine to merge sequencing runs and mip captures for one or a few samplesets and probesets.
    NOTE:  best used for a singular probe_set and sample_set. Can create large fastq sets that are slow to run.
    """
    aparser = argparse.ArgumentParser(
        prog=os.path.basename(__file__) + " merge_sampleset",
        description="allows for flexible merging: preferable to analyze one sampleset by one probeset",
        epilog="Note: for output recommend using unique name for merged sheet based on set/probe/and other parameters",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    aparser.add_argument(
        "--set", required=True, action="append", help="sample_set to aggregate"
    )
    aparser.add_argument(
        "--probe",
        required=True,
        action="append",
        help="probe sets to include in merge",
    )
    aparser.add_argument(
        "--sheet",
        required=False,
        action="append",
        help=" sample sheet file paths (dir fastq must be in same dir as sheet)",
    )
    aparser.add_argument(
        "--mergeon",
        required=False,
        help="fields to merge on ",
        default="sample_name-sample_set-replicate",
    )
    aparser.add_argument(
        "--newsheet",
        required=False,
        help="name of new merged samplesheet",
        default="mergedsheet.tsv",
    )
    aparser.add_argument(
        "--newfastqdir",
        required=False,
        help="name of new fastq directory",
        default="mergedfastq",
    )
    aparser.add_argument(
        "--exclude",
        required=False,
        action="append",
        help="exclude (samples)  matching text pattern",
    )
    aparser.add_argument(
        "--addcolumn",
        required=False,
        action="append",
        help="add unexpected column name",
    )
    aparser.add_argument(
        "--skipfastqwrite",
        action="store_true",
        help="dry run skips fastq merge/write but makes tsv",
    )
    # aparser.add_argument("--ignoreoldnames", action='store_true',  help='ignore old names and include as column' )
    aparser.add_argument(
        "--renamereplicates",
        action="store_true",
        help="renumber the replicates based on order",
    )
    aparser.add_argument(
        "--collapse",
        action="store_true",
        help="collapse to unique values in columns (not needed for downstream MIPTools)",
    )
    aparser.add_argument(
        "--ignorereplicateredundancy",
        action="store_true",
        help="collapse multiple replicates within a samplesheet (error)",
    )

    # TODO: set default mergedsheet and fastq directory to set_probe

    args = aparser.parse_args(args=args)
    mergeonfields = args.mergeon.split("-")
    if args.addcolumn is None:  # this should be handled by argparse but not!
        args.addcolumn = []

    # Convert header to snake case
    for f in args.sheet:
        header_to_snake_case(path=f, overwrite=True)

    total_samples = []
    merged = {}
    # replicate={}
    header = global_samples_tsv_header[:]  # copy, modify
    header_optional = global_samples_tsv_header_optional[
        :
    ]  # copy, don't modify
    headers_to_rename = global_samples_tsv_oldnames  # don't modify

    print("CREATING and CLEANING NEW FASTQ DIR:", args.newfastqdir)
    if len(args.newfastqdir) == 1:
        os.system("mkdir " + args.newfastqdir)
        os.system(f"rm {args.newfastqdir}/*")  # too lazy to check if exist
    else:
        print(f"ERROR: bad directory name ({args.newfastqdir})")
        exit()

    print("PROCESSING SAMPLE SHEETS...")
    for thefile in args.sheet:
        print(f"LOADING FASTQ DIR {thefile} ...")
        print(header)

        fastqdir = os.path.dirname(thefile) + "/fastq"
        fastqs = os.listdir(fastqdir)
        fastqs = [f for f in fastqs if any(s in f for s in args.set)]
        # print ( "...   ",  len(fastqs)    , " fastqs in associated directory" )
        with open(thefile, newline="") as items_file:
            items_reader = csv.DictReader(items_file, delimiter="\t")
            items_total = 0
            items_kept = 0
            items_excluded = 0
            fastqs_kept = 0
            for item in items_reader:
                # rename old names to new names#
                # if items total
                for oldname in headers_to_rename:
                    if oldname in item:
                        item[headers_to_rename[oldname]] = item[oldname]
                        item.pop(oldname)
                        if items_total == 0:
                            print(
                                "... ... RENAMED old name '{}' to '{}'"
                            ).format(oldname, headers_to_rename[oldname])
                if items_total == 0:
                    # process the headerline to see what headers are present
                    # determine if we need to add another line to current header.
                    # print (item)
                    for name in item:
                        if name not in header:
                            if (
                                name in header_optional
                                or name in args.addcolumn
                            ):
                                print("... ... NOTE: ", name, " added to data ")
                                header.append(name)
                            else:
                                print("ERROR: Improper column name.")
                                print(
                                    f"\u2022 '{name}' is not a proper column name."
                                )
                                print("\u2022 Use '--addcolumn' to override.")
                                exit(1)

                items_total += 1
                if not any(s == item["sample_set"] for s in args.set):
                    continue
                if not any(p in item["probe_set"] for p in args.probe):
                    continue
                # keep item with proper probeset and sampleset
                items_kept += 1

                startfastqname = "{}-{}-{}_".format(
                    item["sample_name"], item["sample_set"], item["replicate"]
                )
                item["samplelist"] = thefile
                item["replicate_old"] = item["replicate"]
                item["fastq"] = [
                    fastqdir + "/" + i
                    for i in fastqs
                    if i.startswith(startfastqname)
                ]
                item["fastq"].sort()
                fastqs_kept += len(item["fastq"])
                item["mergeon"] = []
                for f in mergeonfields:
                    item["mergeon"].append(item[f])
                item["mergeon"] = "-".join(item["mergeon"])
                if args.exclude and any(
                    ele in item["mergeon"] for ele in args.exclude
                ):
                    items_excluded += 1
                    continue
                # print (startfastqname)
                # find the fastqs
                total_samples.append(item)
                merged[item["mergeon"]] = 0
                # replicate[item["sample_name"]+"-"+ item["sample_set"]]=1
            print("    ", items_excluded, " excluded samples")
            print(
                "   ",
                items_kept,
                " of ",
                items_total,
                " total with ",
                fastqs_kept,
                "fastqs kept",
            )
    # print ("HEADER",header)
    # print (EXtotal_samples[0:1])
    print(
        "Total samples ",
        len(total_samples),
        " merging into ",
        len(merged),
        " samples",
    )
    total_samples.sort(key=lambda x: x["mergeon"])

    print("############################")
    print("MERGE ALL THE SAMPLE SHEET ROWS ")
    # merge the list and copy the files ####################
    replicate = {}
    merged_samples = []
    count = 0
    header = header + [
        "fastq",
        "samplelist",
        "mergeon",
        "replicate_old",
    ]  # add on additional headers to report
    for mkey in sorted(merged):
        mergeset = [i for i in total_samples if i["mergeon"] == mkey]
        count += 1
        # print (count, mkey, "records:",len(mergeset))
        mergeditem = None
        name = None

        # Create a merge record from first one and add the others
        for item in mergeset:
            if mergeditem is None:
                mergeditem = copy.deepcopy(item)
                # make sure merged item has all the potential names from header
                # set file name and replicated based on new name and sampleset#
                for f in header:
                    if f in mergeditem:
                        mergeditem[f] = [mergeditem[f]]
                    else:
                        mergeditem[f] = ["NA"]
            else:
                # print ("MERGEDITEM", mergeditem)
                for f in header:
                    if f in item:
                        mergeditem[f].append(item[f])
                    else:
                        mergeditem[f].append("NA")

        # Collapse in mergeitem sampleset, name and mergeon and error if not the same
        for f in ["sample_name", "sample_set", "mergeon"]:
            mergeditem[f] = list(set(mergeditem[f]))
            if len(mergeditem[f]) == 1:
                mergeditem[f] = mergeditem[f][0]
            else:
                print(
                    "!ERROR! ", mergeditem[f], "for", f, " is not consistent!"
                )
                exit(1)

        # Set the replicate
        name = mergeditem["sample_name"] + "-" + mergeditem["sample_set"]
        mergeditem["replicate_old"] = mergeditem["replicate"]
        mergeditem["replicate"] = mergeditem["replicate"][0]
        if args.renamereplicates:
            # rename replicates based on name-set
            if name in replicate:
                replicate[name] += 1
            else:
                replicate[name] = 1
            mergeditem["replicate"] = replicate[name]
        else:
            # replicate name based on name-set-replicate exists than error
            name += "-" + mergeditem["replicate"]
            if name in replicate:
                print("!ERROR!", name, ") already exists!")
                exit(1)
            else:
                replicate[name] = 1

        # Collapse probesets
        mergeditem["probe_set"] = ",".join(mergeditem["probe_set"]).split(",")
        mergeditem["probe_set"] = list(set(mergeditem["probe_set"]))
        mergeditem["probe_set"].sort()
        mergeditem["probe_set"] = ",".join(mergeditem["probe_set"])
        merged_samples.append(mergeditem)
    print("################")
    print("MERGE THE FASTQS...")
    for mergeditem in merged_samples:
        # Merge the fastqs
        # Note that this is slow
        fastqname = "{}-{}-{}".format(
            mergeditem["sample_name"],
            mergeditem["sample_set"],
            mergeditem["replicate"],
        )
        writeoperator = " > "  # initial write
        for pair in mergeditem["fastq"]:
            if len(pair) == 0:
                # print ("emptty value")
                continue
            elif (len(pair) % 2) == 0:  # 2,4,6,8
                # expectation is each replicate record has pair of fastqs (R1 & R2)
                # potential to have more than one replicate in a sequencing run but that is weird
                # print (pair)
                if len(pair) > 2:
                    if args.ignorereplicateredundancy:
                        print(
                            "WARN: (",
                            mergeditem["mergeon"],
                            ") just taking one pair of fastqs -- likely duplicate or bad replicate numbers!",
                        )
                    else:
                        print(mergeditem)
                        print(
                            "!ERROR! More than just a single pair for replicate!",
                            pair,
                            "\nThis could be due to not properly numbering replicates!",
                            "\nOr multiple demultiplexing runs into same directory?",
                            "\nOr because you meant to...",
                            "\nTo override use --ignorereplicateredundancy!",
                        )
                        badcount = len(
                            [m for m in total_samples if len(m["fastq"]) > 2]
                        )
                        print("NOTE: ", badcount, "have more than  2 fastqs!")
                        print(
                            "NOTE: --ignorereplicateredundancy tosses the extra fastqs"
                        )
                        exit(1)

                if (
                    not args.skipfastqwrite
                ):  # this skips lengthy process of writing
                    print(
                        "...",
                        mergeditem["mergeon"],
                        "...",
                        pair[0][-65:],
                        "...",
                    )
                    os.system(
                        "cat  "
                        + pair[0]
                        + writeoperator
                        + args.newfastqdir
                        + "/"
                        + fastqname
                        + "_R1_001.fastq.gz"
                    )
                    os.system(
                        "cat  "
                        + pair[1]
                        + writeoperator
                        + args.newfastqdir
                        + "/"
                        + fastqname
                        + "_R2_001.fastq.gz"
                    )
                    writeoperator = " >> "  # now appending after initial files
                # else:
                #  for i in range (0, len(pair),2):
                #     print (pair[i],"\n   ", pair[i+1])
            else:
                print("ODD PAIR ERROR ", pair)
                print(" could a R1 or R2 fastq file been deleted???")
                exit(1)
            writeoperator = " >> "  # now appending
        # Make fields non-redundant (always make probeset)
        mergeditem["fastq"] = [
            fq for sublist in mergeditem["fastq"] for fq in sublist
        ]
        # print (mergeditem)
    # if args.collapse :
    #   uniquefields=fieldstocollapse
    #  for f in uniquefields :
    #  if f in mergeditem:
    #      #print (f, mergeditem[f])
    #     mergeditem[f]= list(set(mergeditem[f]))
    # for f in fieldstocollapse :
    #  if f in mergeditem:
    #    mergeditem[f]= ",".join(mergeditem[f])

    # print ("NEW COPY ", mergeditem)
    # write to a file ################################
    # write header and additional data from merge
    print("WRITING TSV: ", args.newsheet)
    with open(args.newsheet, "wt") as out_file:
        tsv_writer = csv.writer(out_file, delimiter="\t")
        tsv_writer.writerow(header)
        for item in merged_samples:
            row = []
            for f in header:
                if type(item[f]) is list:
                    if args.collapse:
                        item[f] = list(set(item[f]))
                    item[f] = ",".join(item[f])
                row.append(item[f])
            tsv_writer.writerow(row)


##########################################
##########################################
##########################################
##########################################
##########################################
# -----------------------------------------
# main is left to the bottom so that global variables can be populated
if __name__ == "__main__":
    print("SYS VERSION")
    print(sys.version)
    print("WORKING DIRECTORY:", os.getcwd())
    if len(sys.argv) == 1:
        sys.argv.append("--help")  # if no command then it is a cry for help
    main(sys.argv[1:])
