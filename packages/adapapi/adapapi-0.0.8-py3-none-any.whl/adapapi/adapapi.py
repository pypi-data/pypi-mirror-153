import requests
import json
import os
import pandas as pd
import zipfile
import timeit
import time
import io
import math
import glog as log


class Appen:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers={
            "Authorization": f"Token token={self.api_key}",
        }
        
    def job_summary(self, job_id):
        """Getting job stats

        Args:
            job_id (int): ADAP Job ID

        Returns:
            dict: Returns golden_units, all_units, ordered_units, completed_units_estimate, needed_judgments, all_judgments, tainted_judgments, completed_gold_estimate, completed_non_gold_estimate
        """
        params = {}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}/ping.json', params=params, headers=self.headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            return json.loads(response.text)

    def upload(self, data_to_upload, job_id=None):
        """Uploads CSV (specify path), list of dictionaries, a single dictionary, or DataFrame. If no job ID is specified, a new job will be created.

        Args:
            data_to_upload (pd.DataFrame_or_str_or_list_or_dict): DataFrame object, path to CSV file, list of dictionaries, or single dictionary
            job_id (int): ADAP Job ID. If None then a new job will be created
        """
        if isinstance(data_to_upload, (pd.DataFrame, str)):
            # works
            if isinstance(data_to_upload, str):
                data_to_upload = pd.read_csv(data_to_upload)
            payload = data_to_upload.to_json(orient='records', lines=True)
        elif isinstance(data_to_upload, (dict, list)):
            try:
                data_to_upload = pd.DataFrame(data_to_upload)
            except:
                data_to_upload = pd.DataFrame({k: [v] for k, v in data_to_upload.items()})
            payload = data_to_upload.to_json(orient='records', lines=True)
        else:
            log.error(f'Invalid input data type {type(data_to_upload)}')
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        params = {'force': 'true'}

        if job_id == None:
            response = requests.post(f'https://api.appen.com/v1/jobs/upload.json', data=payload, params=params, headers=headers)
            job_id = json.loads(response.text)['id']
        else:
            response = requests.put(f'https://api.appen.com/v1/jobs/{job_id}/upload.json', data=payload, params=params, headers=headers)

        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            json.loads(response.text)['id']
            log.info(f'---- Uploaded {len(data_to_upload.index)} rows to job ID {job_id}')

    def split_column(self, job_id, columnname, character):
        """Corresponds to the "Split Column" button in platform UI. This operation will split the contents of a column on a certain character, transforming strings into arrays of strings.

        Args:
            job_id (int): ADAP Job ID
            columnname (str): Column name
            character (str): Delimiting character 
        """

        params = {'on': columnname, 'with': character}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}/units/split', params=params, headers = self.headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            log.info(json.loads(response.text))

    def job_json(self, job_id):
        """Get job json

        Args:
            job_id (int): ADAP Job ID

        Returns:
            dict: Job JSON
        """
        params = {}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}.json', params=params, headers = self.headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            return(json.loads(response.text))

    def duplicate_job(self, job_id, include_uploaded_rows=False, include_tq=False):
        """Duplicate ADAP job

        Args:
            job_id (int): ADAP Job ID
            include_uploaded_rows (bool): Flag to include previously uploaded rows. Includes test questions if present. Default set to False. 
            include_tq (bool): Flag to include test questions only.

        Returns:
            int: New ADAP Job ID
        """
        params = {'all_units': str(include_uploaded_rows).lower(), 'gold': str(include_tq).lower()}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}/copy.json', params=params, headers = self.headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            return json.loads(response.text)['id']

    def update_job_json(self, job_id, indict):
        """Updating job settings

        Args:
            job_id (int): ADAP Job ID
            indict (dict): Dictionary of items to update within job json
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {}
        payload.update({'job': indict})

        response = requests.put(f'https://api.appen.com/v1/jobs/{job_id}.json', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            read_response = json.loads(response.text)
            try:
                updated_stuff = {k: read_response[k] for k, v in payload['job'].items()}
            except:
                updated_stuff = read_response
            log.info(f'---- Status code: {response.status_code} \n---- Updated:\n{updated_stuff}')

    def tag_get(self, job_id):
        """Tagging jobs. https://developer.appen.com/#tag/Manage-Job-Settings/paths/~1jobs~1{job_id}~1tags/post

        Args:
            job_id (int): ADAP Job ID

        Returns:
            list: List of tags attached to ADAP Job
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}/tags', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            return json.loads(response.text)

    def tag_add(self, job_id, tag):
        """Adding new tags. https://developer.appen.com/#tag/Manage-Job-Settings/paths/~1jobs~1{job_id}~1tags/post

        Args:
            job_id (int): ADAP Job ID
            tag (str): For multiple tags, delimit by comma. eg. 'tag1, tag2'
        """
        tag = ','.join([x.strip() for x in tag.split(',')])
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {
            'tags': tag
        }
        response = requests.post(f'https://api.appen.com/v1/jobs/{job_id}/tags', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            log.info(json.loads(response.text))

    def tag_replace(self, job_id, tag):
        """Replacing existing tags with new tags. https://developer.appen.com/#tag/Manage-Job-Settings/paths/~1jobs~1{job_id}~1tags/post

        Args:
            job_id (int): ADAP Job ID
            tag (str): For multiple tags, delimit by comma. eg. 'tag1, tag2'
        """
        tag = ','.join([x.strip() for x in tag.split(',')])
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {
            'tags': tag
        }
        response = requests.put(f'https://api.appen.com/v1/jobs/{job_id}/tags', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            log.info(json.loads(response.text))

    def filter_jobs_by_tag(self, tag):
        """Retrieves list of job IDs with associated tag. 
        More information https://developer.appen.com/#tag/Account-Info/paths/~1jobs.json/get

        Args:
            tag (str): For multiple tags, delimit by comma. eg. 'tag1, tag2'

        Returns:
            list: List of job IDs with tag
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        list_job_ids = []
        startNum = 1
        while True:
            payload = {
                'tags': [x.strip() for x in tag.split(',')],
                'page': startNum
            }
            response = requests.get(f'https://api.appen.com/v1/jobs.json', data=json.dumps(payload), headers=headers)
            if response.status_code != 200:
                log.error(f'---- Status code: {response.status_code} \n {response.text}')
                break
            else:
                read_response = json.loads(response.text)
                job_ids = [x['id'] for x in read_response]
                if len(job_ids) == 0:
                    break
                else:
                    list_job_ids.extend(job_ids)
                    startNum += 1
        return list_job_ids

    def regenerate_jobid(self, job_id, reporttype):
        """Regenerates ADAP job

        Args:
            job_id (int_or_list): ADAP Job ID. If a list of job IDs provided, will regenerate them sequentially
            reporttype (str): ADAP report type -- full, aggregated, json, gold_report, workset, source
        """
        params = {'type': reporttype}

        reportoption = ['full', 'aggregated', 'json', 'gold_report', 'workset', 'source']
        if reporttype not in reportoption:
            log.error(f'Invalid report type {reporttype}. Please select one of the following: {reportoption}')
            return

        def regenerate(job_id):

            response = requests.post(f'https://api.appen.com/v1/jobs/{job_id}/regenerate', params=params, headers = self.headers)
            if response.status_code != 200:
                log.error(f'---- Status code: {response.status_code} -- {response.text}')
            else:
                log.info(f'---- Status code: {response.status_code} -- Regenerating {params["type"].upper()} report {job_id}')
        if isinstance(job_id, list):
            for jid in job_id:
                regenerate(jid)
        else:
            regenerate(job_id)

    def download_jobid(self, job_id, reporttype, to_csv=False):
        """Recommended to regenerate report first. Downloads ADAP report to DataFrame object or CSV file.

        Args:
            job_id (int): ADAP Job ID
            reporttype (str): ADAP report type -- full, aggregated, json, gold_report, workset, source
            to_csv (bool): True if report should be saved to CSV, False if report to output as DataFrame object

        Returns:
            Pandas dataframe: Pandas dataframe of report
        """
        reportoption = ['full', 'aggregated', 'json', 'gold_report', 'workset', 'source']
        if reporttype not in reportoption:
            log.error(f'Invalid report type {reporttype}. Please select one of the following: {reportoption}')
            return

        params = {'type': reporttype}
        counter = 0
        time_start = timeit.default_timer()
        log.info(f"Running download command for {reporttype.upper()} report {job_id}")

        while True:
            response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}.csv', params=params, headers = self.headers)
            counter += 1
            log.info(f"-- Response: {response.status_code} -- Count:{counter}")
            if response.status_code == 200:
                log.info(f"-- Generation for job ID {job_id} complete")
                break
            time.sleep(30)
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}.csv', params=params, headers = self.headers)
        while not response.ok:
            log.error(f"Download Failed: Attempting re-download {params['type'].upper()} report {job_id}")
            response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}.csv', params=params, headers = self.headers)
            time.sleep(30)

        time_end = timeit.default_timer()
        elapsed_minutes = round((time_end - time_start) / 60, 2)
        log.info(f'Download {reporttype} report complete for job {job_id} ---- Elapsed minutes: {elapsed_minutes}')

        if to_csv:
            fname = f'{params["type"]}_{job_id}.zip'
            with open(fname, 'wb') as f:
                f.write(response.content)

            log.info(f'-- Extracting {fname}')
            with zipfile.ZipFile(fname) as file:
                file.extractall()
            os.remove(fname)
        else:
            zf = zipfile.ZipFile(io.BytesIO(response.content))
            fname = zf.namelist()[0]
            if reporttype == 'json':
                zipname = f'{params["type"]}_{job_id}.zip'
                with open(zipname, 'wb') as f:
                    f.write(response.content)
                log.info(f'-- Extracting {zipname}')
                with zipfile.ZipFile(zipname) as file:
                    file.extractall()
                os.remove(zipname)
                jsondata = []
                with open(fname) as f:
                    for line in f:
                        jsondata.append(json.loads(line))
                return(jsondata)
            else:
                df = pd.read_csv(zf.open(fname))
                return(df)

    def download_jobid_list(self, list_job_ids, reporttype, outfile_concat=False):
        """Download reports from a list of job IDs

        Args:
            list_job_ids (list): list of job IDs
            reporttype (str): ADAP report type -- full, aggregated, json, gold_report, workset, source
            outfile_concat (boolean): Option to concat all of the downloaded reports into one Pandas dataframe. Default is set to False.

        Returns:
            Pandas dataframe: Dependent on outfile_concat flag, will return concatenated dataframe of all listed job IDs
        """
        reportoption = ['full', 'aggregated', 'json', 'gold_report', 'workset', 'source']
        if reporttype not in reportoption:
            info.error(f'Invalid report type {reporttype}. Please select one of the following: {reportoption}')
            return

        df_list = []
        params = {'type': reporttype}
        for jid in list_job_ids:
            counter = 0
            time_start = timeit.default_timer()
            log.info(f"Running download command for {params['type'].upper()} report {jid}")

            while True:
                response = requests.get(f'https://api.appen.com/v1/jobs/{jid}.csv', params=params, headers=self.headers)
                counter += 1
                log.info(f"-- Response: {response.status_code} -- Count:{counter}")
                if response.status_code == 200:
                    log.info(f"-- Generation for job ID {jid} complete")
                    break
                time.sleep(30)
            response = requests.get(f'https://api.appen.com/v1/jobs/{jid}.csv', params=params, headers=self.headers)
            while not response.ok:
                log.error(f"Download Failed: Attempting re-download {params['type'].upper()} report {jid}")
                response = requests.get(f'https://api.appen.com/v1/jobs/{jid}.csv', params=params, headers=self.headers)
                time.sleep(30)

            fname = f'{params["type"]}_{jid}.zip'
            time_end = timeit.default_timer()
            elapsed_minutes = round((time_end - time_start) / 60, 2)
            log.info(f'Download complete for job {jid} Saving report as {fname} ---- Elapsed minutes: {elapsed_minutes}')
            with open(fname, 'wb') as f:
                f.write(response.content)

            log.info(f'-- Extracting {fname}')
            with zipfile.ZipFile(fname) as file:
                file.extractall()

            if outfile_concat:
                df = pd.read_csv(fname)
                df['jobid'] = jid
                df_list.append(df)
            os.remove(fname)

        if outfile_concat:
            if len(list_job_ids) == 1:
                outfile_concate_name = list_job_ids[0]
            else:
                outfile_concate_name = f'{list_job_ids[0]}_and{len(list_job_ids)}jobs'
            final_df = pd.concat(df_list, sort=False)
            final_df.to_csv(f'{outfile_concate_name}_{len(final_df.index)}.csv', encoding='utf-8', index=False)
            log.info(f"--- Completed processing {outfile_concate_name}. Total Rows: {len(final_df.index)}")
            return(final_df)

    def bonus_contributor(self, job_id, worker_id, amount_in_cents):
        """Max at one time is $20.00 or 2000 cents

        Args:
            job_id (int): ADAP Job ID
            worker_id (int): ADAP Contributor ID
            amount_in_cents (int): Amount in cents. The max amount to bonus per API request is $20.00. Function will split out your amount in max $20.00 chunks + remainder if more than $20.00 is to be bonused.
        """
        def max_twenty(some):
            if some/2000 < 0:
                return([some])
            else:
                bonus_list = []
                multiple = math.floor(some/2000)
                remainder = some % 2000
                for i in range(multiple):
                    bonus_list.append(2000)
                if remainder != 0:
                    bonus_list.append(remainder)
                return(bonus_list)

        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        list_bonus_chunk = max_twenty(amount_in_cents)

        for bonus_chunk in list_bonus_chunk:
            payload = {'amount': bonus_chunk}
            response = requests.post(f'https://api.appen.com/v1/jobs/{job_id}/workers/{worker_id}/bonus.json', data=json.dumps(payload), headers=headers)
            if response.status_code != 200:
                log.error(f'---- Status code: {response.status_code} \n {response.text}')
            else:
                read_response = json.loads(response.text)
                log.info(read_response)
        print(f'Bonused {worker_id} ${sum(list_bonus_chunk)/100}')

    def unit_json(self, job_id, unit_id):
        """Get unit json

        Args:
            job_id (int): ADAP Job ID
            unit_id (int): ADAP Unit ID

        Returns:
            dict: Unit JSON
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        params = {}
        response = requests.get(f'https://api.appen.com/v1/jobs/{job_id}/units/{unit_id}.json', params=params, headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            return(json.loads(response.text))

    def get_unit_state(self, job_id, unit_id):
        """Retrieves current unit state within job

        Args:
            job_id (int): ADAP Job ID
            unit_id (int): ADAP Unit ID

        Returns:
            dict: Dictionary containing _unit_id and _unit_state
        """
        try:
            j = self.unit_json(job_id, unit_id)
            return ({'_unit_id': unit_id, '_unit_state': j['state']})
        except Exception as e:
            return({'_unit_id': unit_id, 'error_msg': e})

    def get_unit_state_row(self, job_id, row):
        """Retrieves current unit state within job. To be used when row data needs to be returned.

        Args:
            job_id (int): ADAP Job ID
            row (Pandas Series or dictionary): Row from ADAP report 

        Returns:
            dict: Dictionary containing all data within row and _unit_state
        """
        unit_id = row['_unit_id']
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {}
        try:
            response = requests.get(
                f'https://api.appen.com/v1/jobs/{job_id}/units/{unit_id}.json', data=json.dumps(payload), headers=headers)
            if response.status_code != 200:
                msg = f'For unit_id {unit_id} -- Status code: {response.status_code} \n {response.text}'
                row.update({'error_msg': msg})
                return(row)
            else:
                read_response = json.loads(response.text)
                row.update({'_unit_state': read_response['state']})
                return (row)
        except Exception as e:
            row.update({'error_msg': e})
            return(row)

    def update_unit_state(self, job_id, unit_id, state):
        """Updating unit state

        Args:
            job_id (int): ADAP job ID
            unit_id (int): ADAP Unit ID
            state (str): One of the following -- new, golden, finalized, canceled, deleted
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {
            'unit': {'state': state}
        }
        response = requests.put(
            f'https://api.appen.com/v1/jobs/{job_id}/units/{unit_id}.json', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'-- Unit ID {unit_id} -- Status code: {response.status_code} -- {response.text}')
        else:
            response_text = json.loads(response.text)
            log.info(f'-- Unit ID {unit_id} -- Status code: {response.status_code} -- Updated unit state: {response_text["state"]}')

    def delete_unit(self, job_id, unit_id):
        """Units cannot be deleted from a running or paused job.

        Args:
            job_id (int): ADAP job ID
            unit_id (int): ADAP Unit ID
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        payload = {
        }
        response = requests.delete(f'https://api.appen.com/v1/jobs/{job_id}/units/{unit_id}.json', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'-- Unit ID {unit_id} -- Status code: {response.status_code} \n {response.text}')
        else:
            log.info(f'-- Unit ID {unit_id} -- Status code: {response.status_code} \n {response.text}')

    def deprecate_job(self, job_id):
        """Deprecating an ADAP job.

        Args:
            job_id (int): ADAP job ID
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        params = {}
        response = requests.delete(f'https://api.appen.com/v1/jobs/{job_id}.json', params=params, headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code} \n {response.text}')
        else:
            log.info('---- Success!')
            read_response = json.loads(response.text)
            return(read_response)

    def internal_launch(self, job_id, units_to_launch):
        """Launching job internally

        Args:
            job_id (int): ADAP Job ID
            units_to_launch (int or str): Provide number of units to launch OR use "all" to launch all units.

        Returns:
            int: Number of units launched
        """
        headers = {'content-type': 'application/json'}
        headers.update(self.headers)
        if units_to_launch == 'all':
            units_to_launch = self.job_summary(job_id)['all_units']

        payload = {
            'channels': ['cf_internal'],
            'debit': {'units_count': units_to_launch}
        }
        response = requests.post(f'https://api.appen.com/v1/jobs/{job_id}/orders.json', data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            log.error(f'---- Status code: {response.status_code}\n{response.text}')
        else:
            response_text = json.loads(response.text)
            log.info(f'---- Status code: {response.status_code} \n {response_text}')
            return response_text['nuggeted_units_count']
