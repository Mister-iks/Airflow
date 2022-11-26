from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

from custom_class.Utils import Utils


spark = SparkSession.builder.appName('spark_demo').getOrCreate()
utils = Utils("./dags/data/input_files/employee.csv",  {
    "owner": "Ibrahima",
    "start_date": datetime.now(),
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
})


def extractSuperEmployee():
    """
    This function retrieves employees who have a salary greater than 2000
    then saves them in another file named custom.csv
    """
    data = spark.read.csv(utils.get_file_path(), header=True)
    data.filter(data['salaire'] > 2000).toPandas().to_csv(
        "./dags/data/output_files/custom.csv", header=None, index=None, sep=',', mode='a')


def extractEmployeeByCountry():
    """
    This function group employee by country then save them in another file named custom_1
    """
    data = spark.read.csv(utils.get_file_path(), header=True)
    data.groupBy("country").agg(F.max('salaire')).toPandas().to_csv(
        "./dags/data/output_files/custom_1.csv", header=None, index=None, sep=',', mode='a')


with DAG("processing_employee_data", schedule_interval="@daily", default_args=utils.get_args(), catchup=False) as dag:

    extract_super_employee = PythonOperator(
        task_id="super_employee",
        python_callable=extractSuperEmployee
    )
    group_employee = PythonOperator(
        task_id="group_employee",
        python_callable=extractEmployeeByCountry
    )

    send_email = EmailOperator(
        task_id='send_email',
        to='teraangacoding.community@gmail.com',
        subject='Sccesfully DAG',
        html_content='<p>Les taches sont éxecutés.<p>'
    )

    print_owner = BashOperator(
        task_id="print_owner",
        bash_command=f"echo Bonjour {utils.args.get('owner')}"

    )

    extract_super_employee >> group_employee >> (send_email, print_owner)
