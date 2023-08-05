"""Install big data related tools.
"""
import importlib
from typing import Union
import logging
from pathlib import Path
import re
from urllib.request import urlopen, urlretrieve
from argparse import Namespace
import tempfile
from tqdm import tqdm
import findspark
from .utils import (
    BASE_DIR,
    run_cmd,
    add_subparser,
    option_pip_bundle,
    is_win,
)


class ProgressBar(tqdm):
    """A class for reporting progress with urlretrieve.
    """
    def update_progress(self, block_num=1, block_size=1, total_size=None):
        """Update progress.
        """
        if total_size is not None:
            self.total = total_size
        self.update(block_num * block_size - self.n)


def get_spark_version() -> str:
    """Get the latest version of Spark.
    """
    logging.info("Parsing the latest version of Spark...")
    pattern = br"Latest Release \(Spark (\d.\d.\d)\)"
    with urlopen("https://spark.apache.org/downloads.html") as resp:
        for line in resp:
            match = re.search(pattern, line)
            if match:
                return match.group(1).decode()
    return "3.0.1"


def _download_spark(args: Namespace, spark_hdp: str, desfile: Path):
    mirrors = args.mirrors + (
        "http://archive.apache.org/dist/spark",
        "http://apache.mirrors.hoobly.com/spark",
        "http://apache.spinellicreations.com/spark",
        "http://mirror.cc.columbia.edu/pub/software/apache/spark",
        "http://mirror.cogentco.com/pub/apache/spark",
        "http://mirror.metrocast.net/apache/spark",
        "http://mirrors.advancedhosters.com/apache/spark",
        "http://mirrors.ibiblio.org/apache/spark",
        "http://apache.claz.org/spark",
        "http://apache.osuosl.org/spark",
        "http://ftp.wayne.edu/apache/spark",
        "http://mirror.olnevhost.net/pub/apache/spark",
        "http://mirrors.gigenet.com/apache/spark",
        "http://mirrors.koehn.com/apache/spark",
        "http://mirrors.ocf.berkeley.edu/apache/spark",
        "http://mirrors.sonic.net/apache/spark",
        "http://us.mirrors.quenda.co/apache/spark",
    )
    for mirror in mirrors:
        url = f"{mirror}/spark-{args.spark_version}/{spark_hdp}.tgz"
        try:
            logging.info("Downloading Spark from: %s", url)
            with ProgressBar(unit="B", unit_scale=True, miniters=1) as progress:
                urlretrieve(url, desfile, progress.update_progress)
            return
        except Exception:
            logging.info("Failed to download Spark from: %s", url)


def spark(args):
    """Install Spark.

    :param args: A Namespace object containing parsed command-line options.
    """
    # versions to install
    if not args.spark_version:
        args.spark_version = get_spark_version()
    if not args.hadoop_version:
        if args.spark_version.startswith("2."):
            args.hadoop_version = "2.7"
        else:
            args.hadoop_version = "3.2"
    # installation location
    dir_ = args.location.resolve()
    spark_hdp = f"spark-{args.spark_version}-bin-hadoop{args.hadoop_version}"
    spark_home = dir_ / spark_hdp
    desfile = Path(tempfile.mkdtemp()) / f"{spark_hdp}.tgz"
    if args.install:
        dir_.mkdir(exist_ok=True)
        _download_spark(args, spark_hdp, desfile)
        cmd = f"{args.prefix} tar -zxf {desfile} -C {dir_} && rm {desfile}"
        run_cmd(cmd)
    if args.config:
        # metastore db
        metastore_db = spark_home / "metastore_db"
        if is_win():
            metastore_db.mkdir(parents=True, exist_ok=True)
        else:
            run_cmd(
                f"{args.prefix} mkdir -p {metastore_db} && "
                f"{args.prefix} chmod -R 777 {metastore_db}"
            )
        # warehouse
        warehouse = spark_home / "warehouse"
        if is_win():
            warehouse.mkdir(parents=True, exist_ok=True)
        else:
            run_cmd(
                f"{args.prefix} mkdir -p {warehouse} && "
                f"{args.prefix} chmod -R 777 {warehouse}"
            )
        # spark-defaults.conf
        conf = (BASE_DIR / "spark/spark-defaults.conf"
               ).read_text().replace("$SPARK_HOME", str(spark_home))
        run_cmd(
            f"""echo '{conf}' | {args.prefix} tee \
                {spark_home / 'conf/spark-defaults.conf'} > /dev/null"""
        )
        logging.info(
            "Spark is configured to use %s as the metastore database and %s as the Hive warehouse.",
            metastore_db, warehouse
        )
        # create databases and tables
        if args.schema_dir:
            create_dbs(spark_home, args.schema_dir)
        if not is_win():
            run_cmd(f"{args.prefix} chmod -R 777 {metastore_db}")
    if args.uninstall:
        cmd = f"{args.prefix} rm -rf {spark_home}"
        run_cmd(cmd)


def _spark_args(subparser):
    subparser.add_argument(
        "-m",
        "--mirrors",
        dest="mirrors",
        nargs="+",
        default=(),
        help="The mirror of Apache Spark to use."
    )
    subparser.add_argument(
        "--sv",
        "--spark-version",
        dest="spark_version",
        help="The version of Spark to install."
    )
    subparser.add_argument(
        "--hv",
        "--hadoop-version",
        dest="hadoop_version",
        default="",
        help="The version of Hadoop to use."
    )
    subparser.add_argument(
        "--loc",
        "--location",
        dest="location",
        type=Path,
        default=Path(),
        help="The location (current work directory, by default) to install Spark to."
    )
    subparser.add_argument(
        "-s",
        "--schema",
        "--schema-dir",
        dest="schema_dir",
        type=Path,
        default=None,
        help="The path to a directory containing schema information." \
            "The directory contains subdirs whose names are databases to create." \
            "Each of those subdirs (database) contain SQL files of the format db.table.sql" \
            "which containing SQL code for creating tables."
    )


def _add_subparser_spark(subparsers):
    add_subparser(subparsers, "Spark", func=spark, add_argument=_spark_args)


def pyspark(args):
    """Install PySpark.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        cmd = f"{args.pip_install} pyspark findspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} pyspark findspark"
        run_cmd(cmd)


def _pyspark_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pyspark(subparsers):
    add_subparser(subparsers, "PySpark", func=pyspark, add_argument=_pyspark_args)


def dask(args):
    """Install the Python module dask.

    :param args: A Namespace object containing parsed command-line options.
    """
    if args.install:
        cmd = f"{args.pip_install} dask[complete]"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip_uninstall} dask"
        run_cmd(cmd)


def _dask_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_dask(subparsers):
    add_subparser(subparsers, "dask", func=dask, add_argument=_dask_args)


def _alter_spark_sql(sql: str, hadoop_local: Union[str, Path]) -> str:
    """Handle special paths in SQL code so that it can be used locally.

    :param sql: A SQL query.
    :param hadoop_local: The local path of Hadoop.
    :return: The altered SQL code which can be used locally.
    """
    sql = re.sub(r"viewfs://[^/]+/", "/", sql)
    prefixes = ["/sys/", "/apps", "/user"]
    for prefix in prefixes:
        sql = sql.replace(prefix, f"{hadoop_local}{prefix}")
    return sql


def _create_db(spark_session, dbase: Union[Path, str]) -> None:
    """Create a database and tables belong to the database.

    :param spark_session: A SparkSession object.
    :param dbase: A path containing information about the database to create.
        The directory name of the path is the name of the database,
        and the directory containing SQL files for creating Hive tables.
    """
    print("\n\n")
    if isinstance(dbase, str):
        dbase = Path(dbase)
    dbase = dbase.resolve()
    logging.info("Creating database %s...", dbase.stem)
    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {dbase.stem}")
    for path in dbase.glob("*.txt"):
        with path.open("r") as fin:
            table = fin.readline().strip()
            if spark_session.catalog._jcatalog.tableExists(table):  # pylint: disable=W0212
                logging.warning("The data table %s already exists.", table)
                continue
            fields = [line.strip() for line in fin]
        fields = (",\n" + " " * 16).join(fields)
        sql = f"""
            CREATE TABLE {table} (
                {fields}
            ) USING PARQUET
            """.rstrip()
        logging.info("Creating/replacing the data table %s:%s", table, sql)
        spark_session.sql(sql)


def create_dbs(spark_home: Union[str, Path], schema_dir: Union[Path, str]) -> None:
    """Create databases and tables belong to them.

    :param spark_home: The home of Spark installation.
    :param schema_dir: The path to a directory containing schema information.
    The directory contains subdirs whose names are databases to create.
    Each of those subdirs (database) contain SQL files of the format db.table.sql
    which containing SQL code for creating tables.
    """
    if isinstance(spark_home, Path):
        spark_home = str(spark_home)
    findspark.init(spark_home)
    spark_session = importlib.import_module("pyspark").sql.SparkSession \
        .builder.appName("Create_Empty_Hive_Tables").enableHiveSupport().getOrCreate()
    hadoop_local = Path.home() / ".hadoop"
    if not hadoop_local.is_dir():
        hadoop_local.mkdir(parents=True, exist_ok=True)
    if isinstance(schema_dir, str):
        schema_dir = Path(schema_dir)
    schema_dir = schema_dir.resolve()
    logging.info("Reading schema from the directory: %s", schema_dir)
    for path in schema_dir.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            _create_db(spark_session, path)


def _add_subparser_bigdata(subparsers):
    _add_subparser_dask(subparsers)
    _add_subparser_spark(subparsers)
    _add_subparser_pyspark(subparsers)
