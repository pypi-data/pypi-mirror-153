import pandas as pd
import numpy as np
import datetime as dt
from typing import Any, Dict, List

from google.cloud import bigquery
# from google.cloud.bigquery.job import NotFound
from google.cloud.exceptions import BadRequest
from google.oauth2 import service_account
import requests

class GCPALM:
    def __init__(self, project, dataset, credentials, verify, credentials_file):

        self.project = project
        self.dataset = dataset
        self.credentials = credentials
        if self.credentials is not None:
            session = requests.Session()
            session.get('https://oauth2.googleapis.com/', verify=verify)
            if credentials_file:
                self.gcp_service_account_credential = service_account.Credentials.from_service_account_file(self.credentials)
            else:
                self.gcp_service_account_credential = service_account.Credentials.from_service_account_info(self.credentials)
            self.bq_client = bigquery.Client(
                credentials=self.gcp_service_account_credential,
                project=self.gcp_service_account_credential.project_id,
            )

    def read_data_from_query(self, table_name, fields: List[str], sarg: str = None, distinct = False, array_like = False,
                            array_query_params = None) -> pd.DataFrame:
        """Reads data from the handlers table into a dataframe

        Args:
            fields (List[str]): list of fields to read

        Returns:
            pd.DataFrame: query result as a dataframe
        """
        # Create the fields list
        full_table_ref = self.project + "." + self.dataset + "." + table_name
        fields_to_select = ""
        # If the only element is "*", just use that
        if len(fields) == 1 and fields[0] == "*":
            fields_to_select = "*"
        else:
            for field_in_list in fields:
                fields_to_select += field_in_list + ", "
            # Trim the last ", "
            fields_to_select = fields_to_select[:-2]
        # Build the query
        if distinct:
            if sarg is None:
                select_query = f"SELECT DISTINCT {fields_to_select} FROM `{full_table_ref}`"
            else:
                select_query = f"SELECT DISTINCT {fields_to_select} FROM `{full_table_ref}` WHERE {sarg}"
        else:
            if sarg is None:
                select_query = f"SELECT {fields_to_select} FROM `{full_table_ref}`"
            else:
                select_query = f"SELECT {fields_to_select} FROM `{full_table_ref}` WHERE {sarg}"
        # Execute the query
        # Catch errors form BQ
        if not array_like:
            try:
                result_df = self.bq_client.query(select_query).to_arrow().to_pandas()
            except NotFound as not_found:
                # Raise a wrapping Exception
                raise EMCBQNotFoundException(
                    expression=f"{not_found!r}", message="Project, dataset or table not found"
                ) from not_found
            # Return the dataframe
            return result_df
        else:
            try:
                if len(array_query_params) == 1:
                    job_config = bigquery.QueryJobConfig(
                        query_parameters = [
                            bigquery.ArrayQueryParameter(array_query_params[0][0], array_query_params[0][1], array_query_params[0][2])
                            ]
                    )
                    result_df = self.bq_client.query(select_query, job_config = job_config).to_arrow().to_pandas()
                elif len(array_query_params) == 2:
                    job_config = bigquery.QueryJobConfig(
                        query_parameters = [
                            bigquery.ArrayQueryParameter(array_query_params[0][0], array_query_params[0][1], array_query_params[0][2]),
                            bigquery.ArrayQueryParameter(array_query_params[1][0], array_query_params[1][1], array_query_params[1][2])
                            ]
                    )
                    result_df = self.bq_client.query(select_query, job_config = job_config).to_arrow().to_pandas()
                elif len(array_query_params) == 3:
                    job_config = bigquery.QueryJobConfig(
                        query_parameters = [
                            bigquery.ArrayQueryParameter(array_query_params[0][0], array_query_params[0][1], array_query_params[0][2]),
                            bigquery.ArrayQueryParameter(array_query_params[1][0], array_query_params[1][1], array_query_params[1][2]),
                            bigquery.ArrayQueryParameter(array_query_params[2][0], array_query_params[2][1], array_query_params[2][2]),
                            ]
                    )
                    result_df = self.bq_client.query(select_query, job_config = job_config).to_arrow().to_pandas()
                else:
                    raise ValueError("array_query_params length is not supported by this function.")
            except NotFound as not_found:
                raise EMCBQNotFoundException(
                    expression=f"{not_found!r}", message="Project, dataset or table not found"
                ) from not_found

            return result_df


    def extract_companies(self):
        table_list = ['equity', 'fixed_income', 'fondos', 'forwards', 'futures', 'mutual_fund', 'offshore', 'options', 'other',
                      'otras_inversiones', 'pacts', 'real_estate', 'swaps']
        company_list = []
        complete_df = pd.DataFrame()
        for table in table_list:
            try:
                temp_df = self.read_data_from_query(table_name = table, fields = ['company_id', 'company_name', 'activo_respalda_reserva_valor_fondo'], distinct = True)
                complete_df = pd.concat([complete_df, temp_df], axis = 0)
            except:
                pass

        fund_map = complete_df.groupby('company_id')['activo_respalda_reserva_valor_fondo'].apply(lambda x: [x.unique().tolist()]).to_dict()
        name_map = complete_df.groupby('company_id')['company_name'].apply(lambda x: [x.unique().tolist()]).to_dict()

        for k, v in fund_map.items():
            if k in name_map:
                name_map[k].extend(v)

        name_map.pop('MISSING', None)

        return name_map

    def extract_company_target_port(self, company_id):
        table_list = ['equity', 'fixed_income', 'fondos', 'forwards', 'futures', 'mutual_fund', 'offshore', 'options', 'other',
                      'otras_inversiones', 'pacts', 'real_estate', 'swaps']
        target_ports = []
        for table in table_list:
            try:
                ports = self.read_data_from_query(table_name = table, fields = ['activo_respalda_reserva_valor_fondo'],
                                                  sarg = "company_id = " + "'{}'".format(company_id), distinct = True)
                target_ports.append(ports)
            except:
                pass

        return list(pd.concat(target_ports, axis = 0)['activo_respalda_reserva_valor_fondo'].unique())

    def extract_company_available_dates(self, company_id):
        table_list = ['equity', 'fixed_income', 'forwards', 'futures', 'mutual_fund', 'offshore', 'options', 'other',
                      'pacts', 'real_estate', 'swaps']
        date_list = []
        for table in table_list:
            try:
                dates = self.read_data_from_query(table_name = table, fields = ['period'],
                                                  sarg = "company_id = " + "'{}'".format(company_id), distinct = True)
                date_list.append(dates)
            except:
                pass

        return list(pd.concat(date_list, axis = 0)['period'].unique())

    def extract_companies_available_ac(self, asset_class_list, company_list = None):

        if company_list is None:
            company_list = []

        array_query_params = [['companies', 'STRING', company_list]]

        for ac in asset_class_list:
            if not company_list:
                company_list.append(list(self.read_data_from_query(table_name = ac, fields = ['company_id'], distinct = True)['company_id'].values))
            else:
                company_list.append(list(self.read_data_from_query(table_name = ac, fields = ['company_id'], distinct = True,
                                                                    sarg = "company_id in UNNEST (@companies)", array_like = True,
                                                                    array_query_params = array_query_params)['company_id'].values))

        asset_class_dict = dict(zip(asset_class_list, company_list))

        return asset_class_dict

    def summarize_company(self, company_id, target_port, date = None, tipo_valor = 'valor_razonable'):

        def locate_range(row):
            duration_intervals = {'0 a 1': [0, 365], '1 a 3': [365, 365 * 3], '3 a 5': [365 * 3, 365 * 5],
                                 '5 a 7': [365 * 5, 365 * 7], '7 a 10': [365 * 7, 365 * 10]}
            for key, value in duration_intervals.items():
                if row['dias_a_vencimiento'] in range(value[0], value[1]):
                    return key
            return 'Mayor a 10'

        assert type(company_id) == list and type(target_port) == list, "company_id and target_port params must be lists"

        seil_eq = self.read_data_from_query(table_name = 'seil_instruments', fields = ['descripcion', 'codigo'])
        seil_eq = dict(zip(list(seil_eq['codigo']), list(seil_eq['descripcion'])))

        array_query_params = [['companies', 'STRING', company_id], ['target_port', 'STRING', target_port]]
        curr_eq = {'PROM': 'USD', '$$': 'CLP', 'UF': 'UF'}
        assets_df = []
        available_dates = {}
        vectorize_fun = np.vectorize(lambda x: x.strftime('%Y-%m-%d'))
        # Fixed income summary
        temp_fi = {}
        seg_agg_fi = {}
        fi_col_list = ['nemotecnico', 'unidad_monetaria', 'valor_nominal', 'clasificacion_riesgo', 'fecha_vencimiento', 'valor_razonable', 'company_id', 'period',
                       'activo_respalda_reserva_valor_fondo', 'tipo_instrumento']
        groupby_list_fi = ['unidad_monetaria', 'clasificacion_riesgo', 'duracion', 'tipo_instrumento']
        try:
            fixed_income_dates = self.read_data_from_query(table_name = 'fixed_income', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                            array_like = True, array_query_params = array_query_params)
            available_dates['Fixed income'] = list(vectorize_fun(fixed_income_dates['period'].unique()))
        except:
            fixed_income_dates = None
        if fixed_income_dates is not None:
            if date is not None:
                fixed_income = self.read_data_from_query(table_name = 'fixed_income', fields=fi_col_list, sarg="period = " + "'{}'".format(date['Fixed income'] if type(date) == dict else date))
                fixed_income = fixed_income.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                fixed_income = fixed_income[(fixed_income['company_id'] == company_id[0]) & (fixed_income['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not fixed_income.empty:
                    fixed_income['dias_a_vencimiento'] = (fixed_income['fecha_vencimiento'] - fixed_income['period']).dt.days
                    fixed_income['duracion'] = fixed_income.apply(func = locate_range, axis = 1)
                    seg_mon = fixed_income.groupby(by = 'unidad_monetaria').sum()[tipo_valor] / fixed_income.groupby(by = 'unidad_monetaria').sum()[tipo_valor].sum()
                    seg_cal = fixed_income.groupby(by = 'clasificacion_riesgo').sum()[tipo_valor] / fixed_income.groupby(by = 'clasificacion_riesgo').sum()[tipo_valor].sum()
                    seg_dur = fixed_income.groupby(by = 'duracion').sum()[tipo_valor] / fixed_income.groupby(by = 'duracion').sum()[tipo_valor].sum()
                    seg_tipo = fixed_income.groupby(by = 'tipo_instrumento').sum()[tipo_valor] / fixed_income.groupby(by = 'tipo_instrumento').sum()[tipo_valor].sum()
                    seg_agg_fi = pd.DataFrame(fixed_income.groupby(by = groupby_list_fi).sum()[tipo_valor] / fixed_income.groupby(by = groupby_list_fi).sum()[tipo_valor].sum())
                    temp_fi_output = dict(zip(['Moneda', 'Calificación crediticia', 'Duración', 'Tipo instrumento'], [seg_mon, seg_cal, seg_dur, seg_tipo]))
                    temp_fi = temp_fi_output
                    assets_fi = fixed_income.loc[:, ['nemotecnico', tipo_valor, 'unidad_monetaria']]
                    assets_fi['asset_class'] = 'Renta fija'
                    assets_df.append(assets_fi)
            else:
                fixed_income = self.read_data_from_query(table_name = 'fixed_income', fields=fi_col_list, sarg="period = " + "'{}'".format(max(available_dates['Fixed income'])))
                fixed_income = fixed_income.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                fixed_income = fixed_income[(fixed_income['company_id'] == company_id[0]) & (fixed_income['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                fixed_income['dias_a_vencimiento'] = (fixed_income['fecha_vencimiento'] - fixed_income['period']).dt.days
                fixed_income['duracion'] = fixed_income.apply(func = locate_range, axis = 1)
                seg_mon = fixed_income.groupby(by = 'unidad_monetaria').sum()[tipo_valor] / fixed_income.groupby(by = 'unidad_monetaria').sum()[tipo_valor].sum()
                seg_cal = fixed_income.groupby(by = 'clasificacion_riesgo').sum()[tipo_valor] / fixed_income.groupby(by = 'clasificacion_riesgo').sum()[tipo_valor].sum()
                seg_dur = fixed_income.groupby(by = 'duracion').sum()[tipo_valor] / fixed_income.groupby(by = 'duracion').sum()[tipo_valor].sum()
                seg_tipo = fixed_income.groupby(by = 'tipo_instrumento').sum()[tipo_valor] / fixed_income.groupby(by = 'tipo_instrumento').sum()[tipo_valor].sum()
                seg_agg_fi = pd.DataFrame(fixed_income.groupby(by = groupby_list_fi).sum()[tipo_valor] / fixed_income.groupby(by = groupby_list_fi).sum()[tipo_valor].sum())
                temp_fi_output = dict(zip(['Moneda', 'Calificación crediticia', 'Duración', 'Tipo instrumento'], [seg_mon, seg_cal, seg_dur, seg_tipo]))
                temp_fi = temp_fi_output
                assets_fi = fixed_income.loc[:, ['nemotecnico', tipo_valor, 'unidad_monetaria']]
                assets_fi['asset_class'] = 'Renta fija'
                assets_fi['reported_period'] = max(available_dates['Fixed income'])
                assets_df.append(assets_fi)

        # Equity summary
        temp_equity = {}
        seg_agg_equity = {}
        equity_col_list = ['unidad_monetaria', 'valor_razonable', 'nemonico', 'company_id', 'period', 'activo_respalda_reserva_valor_fondo', 'tipo_instrumento']
        groupby_list_equity = ['unidad_monetaria', 'tipo_instrumento']
        try:
            equity_dates = self.read_data_from_query(table_name = 'equity', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                    array_like = True, array_query_params = array_query_params)
            available_dates['Equity'] = list(vectorize_fun(equity_dates['period'].unique()))
        except:
            equity_dates = None
        if equity_dates is not None:
            if date is not None:
                equity = self.read_data_from_query(table_name = 'equity', fields = equity_col_list, sarg="period = " + "'{}'".format(date['Equity'] if type(date) == dict else date))
                equity = equity.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                equity = equity[(equity['company_id'] == company_id[0]) & (equity['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not equity.empty:
                    seg_mon = equity.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / equity.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                    seg_tipo = equity.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / equity.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                    seg_agg_equity = pd.DataFrame(equity.groupby(by = groupby_list_equity).sum()['valor_razonable'] / equity.groupby(by = groupby_list_equity).sum()['valor_razonable'].sum())
                    temp_equity_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                    temp_equity = temp_equity_output
                    assets_equity = equity.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria']]
                    assets_equity['asset_class'] = 'Equity'
                    assets_df.append(assets_equity)
            else:
                equity = self.read_data_from_query(table_name = 'equity', fields = equity_col_list, sarg="period = " + "'{}'".format(max(available_dates['Equity'])))
                equity = equity.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                equity = equity[(equity['company_id'] == company_id[0]) & (equity['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                seg_mon = equity.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / equity.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                seg_tipo = equity.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / equity.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                seg_agg_equity = pd.DataFrame(equity.groupby(by = groupby_list_equity).sum()['valor_razonable'] / equity.groupby(by = groupby_list_equity).sum()['valor_razonable'].sum())
                temp_equity_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                temp_equity = temp_equity_output
                assets_equity = equity.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria']]
                assets_equity['asset_class'] = 'Equity'
                assets_equity['reported_period'] = max(available_dates['Equity'])
                assets_df.append(assets_equity)

        # Mutual fund summary
        temp_mut_fund = {}
        seg_agg_mutfund = {}
        mut_fund_col_list = ['nemonico', 'unidades', 'unidad_monetaria', 'valor_razonable', 'company_id', 'activo_respalda_reserva_valor_fondo',
                            'tipo_instrumento', 'period']
        groupby_list_mutfund = ['unidad_monetaria', 'tipo_instrumento']
        try:
            mut_fund_dates = self.read_data_from_query(table_name = 'mutual_fund', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                    array_like = True, array_query_params = array_query_params)
            available_dates['Mutual funds'] = list(vectorize_fun(mut_fund_dates['period'].unique()))
        except:
            mut_fund_dates = None
        if mut_fund_dates is not None:
            if date is not None:
                mut_funds = self.read_data_from_query(table_name = 'mutual_fund', fields = mut_fund_col_list, sarg = "period = " + "'{}'".format(date['Mutual funds'] if type(date) == dict else date))
                mut_funds = mut_funds.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                mut_funds = mut_funds[(mut_funds['company_id'] == company_id[0]) & (mut_funds['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not mut_funds.empty:
                    seg_mon = mut_funds.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / mut_funds.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                    seg_tipo = mut_funds.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / mut_funds.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                    seg_agg_mutfund = pd.DataFrame(mut_funds.groupby(by = groupby_list_mutfund).sum()['valor_razonable'] / mut_funds.groupby(by = groupby_list_mutfund).sum()['valor_razonable'].sum())
                    temp_mutfund_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                    temp_mut_fund = temp_mutfund_output
                    assets_mfunds = mut_funds.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria']]
                    assets_mfunds['asset_class'] = 'Mutual fund'
                    assets_df.append(assets_mfunds)
            else:
                mut_funds = self.read_data_from_query(table_name = 'mutual_fund', fields = mut_fund_col_list, sarg = "period = " + "'{}'".format(max(available_dates['Mutual funds'])))
                mut_funds = mut_funds.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                mut_funds = mut_funds[(mut_funds['company_id'] == company_id[0]) & (mut_funds['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                seg_mon = mut_funds.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / mut_funds.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                seg_tipo = mut_funds.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / mut_funds.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                seg_agg_mutfund = pd.DataFrame(mut_funds.groupby(by = groupby_list_mutfund).sum()['valor_razonable'] / mut_funds.groupby(by = groupby_list_mutfund).sum()['valor_razonable'].sum())
                temp_mutfund_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                temp_mut_fund = temp_mutfund_output
                assets_mfunds = mut_funds.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria']]
                assets_mfunds['asset_class'] = 'Mutual fund'
                assets_mfunds['reported_period'] = max(available_dates['Mutual funds'])
                assets_df.append(assets_mfunds)

        # Real estate summary
        temp_re = {}
        seg_agg_re = {}
        real_estate_col_list = ['codigo_nemotecnico', 'fecha_compra', 'ciudad', 'valor_final', 'company_id', 'period', 'activo_respalda_reserva_valor_fondo',
                                'tipo_de_inmueble', 'tipo_instrumento']
        groupby_list_re = ['tipo_de_inmueble', 'tipo_instrumento']
        try:
            re_dates = self.read_data_from_query(table_name = 'real_estate', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                array_like = True, array_query_params = array_query_params)
            available_dates['Real estate'] = list(vectorize_fun(re_dates['period'].unique()))
        except:
            re_dates = None
        if re_dates is not None:
            if date is not None:
                real_estate = self.read_data_from_query(table_name = 'real_estate', fields = real_estate_col_list, sarg = "period = " + "'{}'".format(date['Real estate'] if type(date) == dict else date))
                real_estate = real_estate.replace({'tipo_instrumento': seil_eq})
                real_estate = real_estate[(real_estate['company_id'] == company_id[0]) & (real_estate['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not real_estate.empty:
                    seg_re = real_estate.groupby(by = 'tipo_de_inmueble').sum()['valor_final'] / real_estate.groupby(by = 'tipo_de_inmueble').sum()['valor_final'].sum()
                    seg_tipo = real_estate.groupby(by = 'tipo_instrumento').sum()['valor_final'] / real_estate.groupby(by = 'tipo_instrumento').sum()['valor_final'].sum()
                    seg_agg_re = pd.DataFrame(real_estate.groupby(by = groupby_list_re).sum()['valor_final'] / real_estate.groupby(by = groupby_list_re).sum()['valor_final'].sum())
                    temp_re_output = dict(zip(['Tipo de inmueble', 'Tipo instrumento'], [seg_re, seg_tipo]))
                    temp_re = temp_re_output
                    assets_re = real_estate.loc[:, ['codigo_nemotecnico', 'valor_final']]
                    assets_re['unidad_monetaria'] = np.nan
                    assets_re['asset_class'] = 'Real estate'
                    assets_df.append(assets_re)
            else:
                real_estate = self.read_data_from_query(table_name = 'real_estate', fields = real_estate_col_list, sarg = "period = " + "'{}'".format(max(available_dates['Real estate'])))
                real_estate = real_estate.replace({'tipo_instrumento': seil_eq})
                real_estate = real_estate[(real_estate['company_id'] == company_id[0]) & (real_estate['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                seg_re = real_estate.groupby(by = 'tipo_de_inmueble').sum()['valor_final'] / real_estate.groupby(by = 'tipo_de_inmueble').sum()['valor_final'].sum()
                seg_tipo = real_estate.groupby(by = 'tipo_instrumento').sum()['valor_final'] / real_estate.groupby(by = 'tipo_instrumento').sum()['valor_final'].sum()
                seg_agg_re = pd.DataFrame(real_estate.groupby(by = groupby_list_re).sum()['valor_final'] / real_estate.groupby(by = groupby_list_re).sum()['valor_final'].sum())
                temp_re_output = dict(zip(['Tipo de inmueble', 'Tipo instrumento'], [seg_re, seg_tipo]))
                temp_re = temp_re_output
                assets_re = real_estate.loc[:, ['codigo_nemotecnico', 'valor_final']]
                assets_re['unidad_monetaria'] = np.nan
                assets_re['asset_class'] = 'Real estate'
                assets_re['reported_period'] = max(available_dates['Real estate'])
                assets_df.append(assets_re)


        # Offshore summary
        temp_offshore = {}
        seg_agg_offshore = {}
        offshore_col_list = ['codigo_individualizacion_nemotecnico', 'moneda', 'fecha_vencimiento', 'activo_respalda_reserva_valor_fondo', 'company_id',
                            'period', 'clasificaicon_riesgo', 'valor_nominal', 'tipo_instrumento']
        groupby_offshore_list = ['moneda', 'clasificaicon_riesgo', 'duracion', 'tipo_instrumento']
        try:
            offshore_dates = self.read_data_from_query(table_name = 'offshore', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                    array_like = True, array_query_params = array_query_params)
            available_dates['Offshore'] = list(vectorize_fun(offshore_dates['period'].unique()))
        except:
            offshore_dates = None
        if offshore_dates is not None:
            if date is not None:
                offshore = self.read_data_from_query(table_name = 'offshore', fields=offshore_col_list, sarg="period = " + "'{}'".format(date['Offshore'] if type(date) == dict else date))
                offshore = offshore.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                offshore = offshore[(offshore['company_id'] == company_id[0]) & (offshore['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not offshore.empty:
                    offshore['dias_a_vencimiento'] = (offshore['fecha_vencimiento'] - offshore['period']).dt.days
                    offshore['duracion'] = offshore.apply(func = locate_range, axis = 1)
                    seg_mon = offshore.groupby(by = 'moneda').sum()['valor_nominal'] / offshore.groupby(by = 'moneda').sum()['valor_nominal'].sum()
                    seg_cal = offshore.groupby(by = 'clasificaicon_riesgo').sum()['valor_nominal'] / offshore.groupby(by = 'clasificaicon_riesgo').sum()['valor_nominal'].sum()
                    seg_dur = offshore.groupby(by = 'duracion').sum()['valor_nominal'] / offshore.groupby(by = 'duracion').sum()['valor_nominal'].sum()
                    seg_tipo = offshore.groupby(by = 'tipo_instrumento').sum()['valor_nominal'] / offshore.groupby(by = 'tipo_instrumento').sum()['valor_nominal'].sum()
                    seg_agg_offshore = pd.DataFrame(offshore.groupby(by = groupby_offshore_list).sum()[tipo_valor] / offshore.groupby(by = groupby_offshore_list).sum()[tipo_valor].sum())
                    temp_offshore_output = dict(zip(['Moneda', 'Calificación crediticia', 'Duración', 'Tipo instrumento'], [seg_mon, seg_cal, seg_dur, seg_tipo]))
                    temp_offshore = temp_offshore_output
                    assets_offshore = offshore.loc[:, ['codigo_individualizacion_nemotecnico', 'valor_nominal', 'moneda']]
                    assets_offshore['asset_class'] = 'Offshore'
                    assets_df.append(assets_offshore)
            else:
                offshore = self.read_data_from_query(table_name = 'offshore', fields=offshore_col_list, sarg="period = " + "'{}'".format(max(available_dates['Offshore'])))
                offshore = offshore.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                offshore = offshore[(offshore['company_id'] == company_id[0]) & (offshore['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                offshore['dias_a_vencimiento'] = (offshore['fecha_vencimiento'] - offshore['period']).dt.days
                offshore['duracion'] = offshore.apply(func = locate_range, axis = 1)
                seg_mon = offshore.groupby(by = 'moneda').sum()['valor_nominal'] / offshore.groupby(by = 'moneda').sum()['valor_nominal'].sum()
                seg_cal = offshore.groupby(by = 'clasificaicon_riesgo').sum()['valor_nominal'] / offshore.groupby(by = 'clasificaicon_riesgo').sum()['valor_nominal'].sum()
                seg_dur = offshore.groupby(by = 'duracion').sum()['valor_nominal'] / offshore.groupby(by = 'duracion').sum()['valor_nominal'].sum()
                seg_tipo = offshore.groupby(by = 'tipo_instrumento').sum()['valor_nominal'] / offshore.groupby(by = 'tipo_instrumento').sum()['valor_nominal'].sum()
                seg_agg_offshore = pd.DataFrame(offshore.groupby(by = groupby_offshore_list).sum()['valor_nominal'] / offshore.groupby(by = groupby_offshore_list).sum()['valor_nominal'].sum())
                temp_offshore_output = dict(zip(['Moneda', 'Calificación crediticia', 'Duración', 'Tipo instrumento'], [seg_mon, seg_cal, seg_dur, seg_tipo]))
                temp_offshore = temp_offshore_output
                assets_offshore = offshore.loc[:, ['codigo_individualizacion_nemotecnico', 'valor_nominal', 'moneda']]
                assets_offshore['asset_class'] = 'Offshore'
                assets_offshore['reported_period'] = max(available_dates['Offshore'])
                assets_df.append(assets_offshore)

        # Others summary
        temp_others = {}
        seg_agg_others = {}
        others_col_list = ['nemotecnico', 'unidad_monetaria', 'valor_razonable', 'company_id', 'activo_respalda_reserva_valor_fondo', 'period',
                          'tipo_instrumento']
        groupby_list_others = ['unidad_monetaria', 'tipo_instrumento']
        try:
            others_dates = self.read_data_from_query(table_name = 'other', fields = ['period'], sarg="company_id IN UNNEST(@companies) and activo_respalda_reserva_valor_fondo in UNNEST (@target_port)", distinct = True,
                                                    array_like = True, array_query_params = array_query_params)
            available_dates['Others'] = list(vectorize_fun(others_dates['period'].unique()))
        except:
            others_dates = None
        if others_dates is not None:
            if date is not None:
                others = self.read_data_from_query(table_name = 'other', fields = others_col_list, sarg = "period = " + "'{}'".format(date['Others'] if type(date) == dict else date))
                others = others.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                others = others[(others['company_id'] == company_id[0]) & (others['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                if not others.empty:
                    seg_mon = others.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / others.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                    seg_tipo = others.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / others.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                    seg_agg_others = pd.DataFrame(others.groupby(by = groupby_list_others).sum()['valor_razonable'] / others.groupby(by = groupby_list_others).sum()['valor_razonable'].sum())
                    temp_others_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                    temp_others = temp_others_output
                    assets_others = others.loc[:, ['nemotecnico', 'valor_razonable', 'unidad_monetaria']]
                    assets_others['asset_class'] = 'Otros'
                    assets_df.append(assets_others)
            else:
                others = self.read_data_from_query(table_name = 'other', fields = others_col_list, sarg = "period = " + "'{}'".format(max(available_dates['Others'])))
                others = others.replace({'unidad_monetaria': curr_eq, 'tipo_instrumento': seil_eq})
                others = others[(others['company_id'] == company_id[0]) & (others['activo_respalda_reserva_valor_fondo'].isin(target_port))]
                seg_mon = others.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / others.groupby(by = 'unidad_monetaria').sum()['valor_razonable'].sum()
                seg_tipo = others.groupby(by = 'tipo_instrumento').sum()['valor_razonable'] / others.groupby(by = 'tipo_instrumento').sum()['valor_razonable'].sum()
                seg_agg_others = pd.DataFrame(others.groupby(by = groupby_list_others).sum()['valor_razonable'] / others.groupby(by = groupby_list_others).sum()['valor_razonable'].sum())
                temp_others_output = dict(zip(['Moneda', 'Tipo instrumento'], [seg_mon, seg_tipo]))
                temp_others = temp_others_output
                assets_others = others.loc[:, ['nemotecnico', 'valor_razonable', 'unidad_monetaria']]
                assets_others['asset_class'] = 'Otros'
                assets_others['reported_period'] = max(available_dates['Others'])
                assets_df.append(assets_others)

        if date is not None:
            for df in assets_df:
                df.columns = ['Nemotecnico', 'Valor razonable', 'Unidad monetaria', 'Clase de activo']
        else:
            for df in assets_df:
                df.columns = ['Nemotecnico', 'Valor razonable', 'Unidad monetaria', 'Clase de activo', 'Último periodo reportado']

        elements = [seg_agg_equity, seg_agg_mutfund, seg_agg_re, seg_agg_others]
        for element in elements:
            if type(element) != dict:
                element.reset_index(inplace = True)
                element.columns = ['Unidad monetaria', 'Tipo instrumento', 'Valor razonable']

        elements = [seg_agg_fi, seg_agg_offshore]
        for element in elements:
            if type(element) != dict:
                element.reset_index(inplace = True)
                element.columns = ['Unidad monetaria', 'Clasificacion riesgo', 'Duracion', 'Tipo instrumento', 'Valor razonable']

        if type(seg_agg_re) != dict:
            seg_agg_re.reset_index(inplace = True)
            if 'index' in seg_agg_re.columns:
                seg_agg_re.drop(labels = ['index'], axis = 1, inplace = True)
            seg_agg_re.columns = ['Tipo de inmueble', 'Tipo instrumento', 'Valor razonable']

        assets_df = pd.concat(assets_df, axis = 0).reset_index(drop = True)
        available_dates = {k: [str(v) for v in v] for k, v in available_dates.items()}

        complete_agg_port = []
        complete_port_value = assets_df['Valor razonable'].sum()
        if fixed_income_dates is not None:
            agg_fi_for_comp = pd.DataFrame(fixed_income.groupby(by = groupby_list_fi).sum()[tipo_valor] / complete_port_value)
            agg_fi_for_comp.rename(columns = {tipo_valor: 'Peso'}, inplace = True)
            agg_fi_for_comp.reset_index(inplace = True)
            agg_fi_for_comp = agg_fi_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
            agg_fi_for_comp.set_index(['unidad_monetaria', 'clasificacion_riesgo', 'duracion', 'tipo_instrumento'], inplace = True)
            agg_fi_for_comp['id'] = agg_fi_for_comp.index.map(lambda x: '_'.join(x)) + ' Index'
            agg_fi_for_comp['Clase de activo'] = 'Renta fija'
            complete_agg_port.append(agg_fi_for_comp)
        if offshore_dates is not None:
            agg_offshore_for_comp = pd.DataFrame(offshore.groupby(by = groupby_offshore_list).sum()['valor_nominal'] / complete_port_value)
            agg_offshore_for_comp.rename(columns = {'valor_nominal': 'Peso'}, inplace = True)
            agg_offshore_for_comp.reset_index(inplace = True)
            agg_offshore_for_comp = agg_offshore_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
            agg_offshore_for_comp.set_index(['moneda', 'clasificaicon_riesgo', 'duracion', 'tipo_instrumento'], inplace = True)
            agg_offshore_for_comp['id'] = agg_offshore_for_comp.index.map(lambda x: '_'.join(x)) + ' Index'
            agg_offshore_for_comp['Clase de activo'] = 'Offshore'
            complete_agg_port.append(agg_offshore_for_comp)
        if equity_dates is not None:
            eq_agg_for_comp = pd.DataFrame(equity.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / complete_port_value).reset_index()
            eq_agg_for_comp.columns = ['Moneda', 'Peso']
            eq_agg_for_comp['id'] = 'eq_moneda'
            eq_agg_for_comp['Clase de activo'] = 'Equity'
            complete_agg_port.append(eq_agg_for_comp)
        if mut_fund_dates is not None:
            mutfund_agg_for_comp = pd.DataFrame(mut_funds.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / complete_port_value).reset_index()
            mutfund_agg_for_comp.columns = ['Moneda', 'Peso']
            mutfund_agg_for_comp['id'] = 'mutfund_moneda'
            mutfund_agg_for_comp['Clase de activo'] = 'Mutual fund'
            complete_agg_port.append(mutfund_agg_for_comp)
        if re_dates is not None:
            re_agg_for_comp = pd.DataFrame(real_estate.groupby(by = 'tipo_de_inmueble').sum()['valor_final'] / complete_port_value).reset_index()
            re_agg_for_comp.columns = ['Tipo de inmueble', 'Peso']
            re_agg_for_comp['id'] = 're_tipo_inmueble'
            re_agg_for_comp['Clase de activo'] = 'Real estate'
            complete_agg_port.append(re_agg_for_comp)
        if others_dates is not None:
            others_agg_for_comp = pd.DataFrame(others.groupby(by = 'unidad_monetaria').sum()['valor_razonable'] / complete_port_value).reset_index()
            others_agg_for_comp.columns = ['Moneda', 'Peso']
            others_agg_for_comp['id'] = 'otros'
            others_agg_for_comp['Clase de activo'] = 'Otros'
            complete_agg_port.append(others_agg_for_comp)

        complete_agg_port = pd.concat(complete_agg_port, axis = 0).reset_index(drop = True)
        complete_agg_port = complete_agg_port[['id', 'Clase de activo', 'Peso']]

        return {'Renta fija': temp_fi, 'Equity': temp_equity, 'Mutual fund': temp_mut_fund, 'Offshore': temp_offshore,
                'Real estate': temp_re, 'Otros': temp_others}, {'Renta fija agregado': seg_agg_fi, 'Equity agregado': seg_agg_equity, 'Offshore agregado': seg_agg_offshore,
                'Mutual fund agregado': seg_agg_mutfund, 'Real estate agregado': seg_agg_re, 'Otros agregado': seg_agg_others}, assets_df, complete_agg_port, available_dates, complete_port_value

    def delta_company(self, company_id, target_port):
        _, _, _, _, av_dates, _ = self.summarize_company(company_id, target_port, tipo_valor = 'valor_nominal')
        last_reported = self.summarize_company(company_id, target_port, date = {k: max(v) for k, v in av_dates.items()}, tipo_valor = 'valor_nominal')
        before_last = self.summarize_company(company_id, target_port, date = {k: max([v for v in v if v < max(v)]) for k, v in av_dates.items()}, tipo_valor = 'valor_nominal')

        output_1 = {k: dict() for k in last_reported[0].keys()}
        for key, value in last_reported[0].items():
            for element in list(value.keys()):
                output_1[key][element] = pd.concat([last_reported[0][key][element], before_last[0][key][element]], axis = 1)
                output_1[key][element].columns = ['Último reportado', 'Penúltimo reportado']
                output_1[key][element][['Último reportado', 'Penúltimo reportado']].fillna(0, inplace = True)
                output_1[key][element]['Desviación'] = output_1[key][element]['Último reportado'] - output_1[key][element]['Penúltimo reportado']

        output_2 = {k: dict() for k in last_reported[1].keys()}
        for key, value in last_reported[1].items():
            for element in list(value.keys()):
                output_2[key] = pd.concat([last_reported[1][key].set_index([x for x in last_reported[1][key].columns if x != 'Valor razonable']), before_last[1][key].set_index([x for x in last_reported[1][key].columns if x != 'Valor razonable'])], axis = 1)
                output_2[key].columns = ['Último reportado', 'Penúltimo reportado']
                output_2[key][['Último reportado', 'Penúltimo reportado']].fillna(0, inplace = True)
                output_2[key]['Desviación'] = output_2[key]['Último reportado'] - output_2[key]['Penúltimo reportado']

        last_reported[2].fillna('FALTA', inplace = True)
        before_last[2].fillna('FALTA', inplace = True)
        before_last[2]['id'] = before_last[2]['Nemotecnico'] + '_' + before_last[2]['Unidad monetaria'] + '_' + before_last[2]['Clase de activo']
        last_reported[2]['id'] = last_reported[2]['Nemotecnico'] + '_' + last_reported[2]['Unidad monetaria'] + '_' + last_reported[2]['Clase de activo']
        output_3 = last_reported[2].merge(before_last[2], how = 'outer', on = 'id')
        output_3 = output_3.loc[:, ['id', 'Valor razonable_x', 'Valor razonable_y']]
        output_3.columns = ['id', 'Último reportado', 'Penúltimo reportado']
        output_3.set_index('id', inplace = True, drop = True)
        output_3.fillna(0, inplace = True)
        output_3['Desviación'] = output_3['Último reportado'] - output_3['Penúltimo reportado']

        output_4 = last_reported[3].merge(before_last[3], how = 'outer', on = 'id')
        output_4 = output_4.loc[:, ['id', 'Peso_x', 'Peso_y']]
        output_4.set_index('id', inplace = True, drop = True)
        output_4.columns = ['Último reportado', 'Penúltimo reportado']
        output_4.fillna(0, inplace = True)
        output_4['Desviación'] = output_4['Último reportado'] - output_4['Penúltimo reportado']

        return output_1, output_2, output_3, output_4

    def summarize_market(self, target_group_port = ['VIDA', 'GENERAL'], dates = ['2018-12-31', '2025-12-31'], companies = None, tipo_valor = 'valor_razonable',
                         kick_companies = True, slice_delta = False):

        def locate_range(row):
            duration_intervals = {'0 a 1': [0, 365], '1 a 3': [365, 365 * 3], '3 a 5': [365 * 3, 365 * 5],
                                 '5 a 7': [365 * 5, 365 * 7], '7 a 10': [365 * 7, 365 * 10]}
            for key, value in duration_intervals.items():
                if row['dias_a_vencimiento'] in range(value[0], value[1]):
                    return key
            return 'Mayor a 10'

        seil_eq = self.read_data_from_query(table_name = 'seil_instruments', fields = ['descripcion', 'codigo'])
        seil_eq = dict(zip(list(seil_eq['codigo']), list(seil_eq['descripcion'])))

        eq = {'VIDA': ['VIDA', 'IDA N', 'IVIDE', 'OTRVI'], 'GENERAL': ['GRAL', 'GRLS']}
        target_ports = [eq[x] for x in target_group_port]
        target_ports = [item for sublist in target_ports for item in sublist]

        target_dates = [x.strftime('%Y-%m-%d') for x in list(pd.date_range(dates[0], dates[1]))]
        curr_eq = {'PROM': 'USD', '$$': 'CLP', 'UF': 'UF'}

        if companies is None:
            companies = list(self.extract_companies().keys())

        array_query_params = [['companies', 'STRING', companies], ['target_ports', 'STRING', target_ports], ['target_dates', 'DATE', target_dates]]

        table_cols = {'fixed_income': ['nemotecnico', 'unidad_monetaria', 'valor_nominal', 'clasificacion_riesgo', 'fecha_vencimiento', 'valor_razonable', 'company_id', 'period',
                    'activo_respalda_reserva_valor_fondo', 'tipo_instrumento'], 'equity': ['unidad_monetaria', 'valor_razonable', 'nemonico', 'company_id', 'period', 'activo_respalda_reserva_valor_fondo', 'tipo_instrumento'],
                    'mutual_fund': ['nemonico', 'unidades', 'unidad_monetaria', 'valor_razonable', 'company_id', 'activo_respalda_reserva_valor_fondo', 'period', 'tipo_instrumento'],
                    'offshore': ['codigo_individualizacion_nemotecnico', 'moneda', 'fecha_vencimiento', 'activo_respalda_reserva_valor_fondo', 'company_id',
                    'period', 'clasificaicon_riesgo', 'valor_nominal', 'tipo_instrumento'], 'real_estate': ['codigo_nemotecnico', 'fecha_compra', 'ciudad', 'valor_final', 'company_id', 'period', 'activo_respalda_reserva_valor_fondo',
                    'tipo_de_inmueble', 'tipo_instrumento'], 'other': ['nemotecnico', 'unidad_monetaria', 'valor_razonable', 'company_id', 'activo_respalda_reserva_valor_fondo', 'period', 'tipo_instrumento']}
        tables = {'fixed_income': [], 'equity': [], 'mutual_fund': [], 'offshore': [], 'real_estate': [], 'other': []}
        assets_df = {k: [] for k in target_group_port}

        for key, value in table_cols.items():
            try:
                tables[key].append(self.read_data_from_query(table_name = key, fields = value,
                                   sarg="company_id IN UNNEST (@companies) and activo_respalda_reserva_valor_fondo IN UNNEST (@target_ports) and period IN UNNEST (@target_dates)",
                                   array_like = True, array_query_params = array_query_params))
                if 'unidad_monetaria' in tables[key][0].columns:
                    tables[key][0] = tables[key][0].replace({'unidad_monetaria': curr_eq})
                elif 'moneda' in tables[key][0].columns:
                    tables[key][0] = tables[key][0].replace({'moneda': curr_eq})
                if 'tipo_instrumento' in tables[key][0].columns:
                    tables[key][0] = tables[key][0].replace({'tipo_instrumento': seil_eq})
            except Exception as e:
                print(e)
                print("No data found on the {} table".format(key))
                tables[key].append(pd.DataFrame())

        tables = {k: v[0] for k, v in tables.items()}
        for key, value in tables.items():
            if not value.empty:
                # Slices df - last available date (or previous before last if slice_delta) for each company and each target_port
                if not slice_delta:
                    tables[key] = tables[key][tables[key].groupby(by = ['company_id', 'activo_respalda_reserva_valor_fondo'])['period'].transform('max') == tables[key]['period']]
                else:
                    tables[key] = tables[key][tables[key].groupby(by = ['company_id', 'activo_respalda_reserva_valor_fondo'])['period'].transform('max') != tables[key]['period']]
                    tables[key] = tables[key][tables[key].groupby(by = ['company_id', 'activo_respalda_reserva_valor_fondo'])['period'].transform('max') == tables[key]['period']]

        if kick_companies:
            # Kicks companies that haven't reported an asset class during the selected period out but have had it historically
            asset_class_for_comp = self.extract_companies_available_ac(['fixed_income', 'equity', 'mutual_fund', 'real_estate', 'offshore', 'other'], companies)
            kick_comp = {k: [] for k in target_group_port}
            for k1, v1 in kick_comp.items():
                for k2, v2 in tables.items():
                    if not v2.empty:
                        table_companies = list(tables[k2][tables[k2]['activo_respalda_reserva_valor_fondo'].isin(eq[k1])]['company_id'].unique())
                        kick_comp[k1].append([x for x in asset_class_for_comp[k2] if x not in table_companies])

            kick_comp = {k: [item for sublist in v for item in sublist] for k, v in kick_comp.items()}
            kick_comp = {k: list(dict.fromkeys(v)) for k, v in kick_comp.items()}

        # Fixed income summary
        seg_agg_fi = {k: [] for k in target_group_port}
        if not tables['fixed_income'].empty:
            groupby_list_fi = ['unidad_monetaria', 'clasificacion_riesgo', 'duracion', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        fixed_income_temp = tables['fixed_income'][(tables['fixed_income']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['fixed_income']['company_id'].isin(kick_comp[key]))]
                    else:
                        fixed_income_temp = tables['fixed_income'][tables['fixed_income']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    fixed_income_temp.loc[:, 'dias_a_vencimiento'] = (fixed_income_temp['fecha_vencimiento'] - fixed_income_temp['period']).dt.days
                    fixed_income_temp.loc[:, 'duracion'] = fixed_income_temp.apply(func = locate_range, axis = 1)
                    seg_agg_fi[key].append(pd.DataFrame(fixed_income_temp.groupby(by = groupby_list_fi).sum()[tipo_valor] / fixed_income_temp.groupby(by = groupby_list_fi).sum()[tipo_valor].sum()))
                    assets_fi = fixed_income_temp.loc[:, ['nemotecnico', tipo_valor, 'unidad_monetaria', 'tipo_instrumento']]
                    assets_fi['asset_class'] = 'Renta fija'
                    assets_df[key].append(assets_fi)

        # Equity summary
        seg_agg_eq = {k: [] for k in target_group_port}
        if not tables['equity'].empty:
            groupby_list_equity = ['unidad_monetaria', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        equity_temp = tables['equity'][(tables['equity']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['equity']['company_id'].isin(kick_comp[key]))]
                    else:
                        equity_temp = tables['equity'][tables['equity']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    seg_agg_eq[key].append(pd.DataFrame(equity_temp.groupby(by = groupby_list_equity).sum()['valor_razonable'] / equity_temp.groupby(by = groupby_list_equity).sum()['valor_razonable'].sum()).reset_index())
                    assets_eq = equity_temp.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria', 'tipo_instrumento']]
                    assets_eq['asset_class'] = 'Equity'
                    assets_df[key].append(assets_eq)

        # Mutual fund summary
        seg_agg_mf = {k: [] for k in target_group_port}
        if not tables['mutual_fund'].empty:
            groupby_list_mutfund = ['unidad_monetaria', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        mutual_fund_temp = tables['mutual_fund'][(tables['mutual_fund']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['mutual_fund']['company_id'].isin(kick_comp[key]))]
                    else:
                        mutual_fund_temp = tables['mutual_fund'][tables['mutual_fund']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    seg_agg_mf[key].append(pd.DataFrame(mutual_fund_temp.groupby(by = groupby_list_mutfund).sum()['valor_razonable'] / mutual_fund_temp.groupby(by = groupby_list_mutfund).sum()['valor_razonable'].sum()).reset_index())
                    assets_mf = mutual_fund_temp.loc[:, ['nemonico', 'valor_razonable', 'unidad_monetaria', 'tipo_instrumento']]
                    assets_mf['asset_class'] = 'Mutual fund'
                    assets_df[key].append(assets_mf)

        # Real estate summary
        seg_agg_re = {k: [] for k in target_group_port}
        if not tables['real_estate'].empty:
            groupby_list_re = ['tipo_de_inmueble', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        real_estate_temp = tables['real_estate'][(tables['real_estate']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['real_estate']['company_id'].isin(kick_comp[key]))]
                    else:
                        real_estate_temp = tables['real_estate'][tables['real_estate']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    seg_agg_re[key].append(pd.DataFrame(real_estate_temp.groupby(by = groupby_list_re).sum()['valor_final'] / real_estate_temp.groupby(by = groupby_list_re).sum()['valor_final'].sum()).reset_index())
                    assets_re = real_estate_temp.loc[:, ['codigo_nemotecnico', 'valor_final', 'tipo_instrumento']]
                    assets_re['unidad_monetaria'] = np.nan
                    assets_re = assets_re.loc[:, ['codigo_nemotecnico', 'valor_final', 'unidad_monetaria', 'tipo_instrumento']]
                    assets_re['asset_class'] = 'Real estate'
                    assets_df[key].append(assets_re)

        # Offshore summary
        seg_agg_offshore = {k: [] for k in target_group_port}
        if not tables['offshore'].empty:
            groupby_offshore_list = ['moneda', 'clasificaicon_riesgo', 'duracion', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        offshore_temp = tables['offshore'][(tables['offshore']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['offshore']['company_id'].isin(kick_comp[key]))]
                    else:
                        offshore_temp = tables['offshore'][tables['offshore']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    offshore_temp.loc[:, 'dias_a_vencimiento'] = (offshore_temp['fecha_vencimiento'] - offshore_temp['period']).dt.days
                    offshore_temp.loc[:, 'duracion'] = offshore_temp.apply(func = locate_range, axis = 1)
                    seg_agg_offshore[key].append(pd.DataFrame(offshore_temp.groupby(by = groupby_offshore_list).sum()['valor_nominal'] / offshore_temp.groupby(by = groupby_offshore_list).sum()['valor_nominal'].sum()))
                    assets_offshore = offshore_temp.loc[:, ['codigo_individualizacion_nemotecnico', 'valor_nominal', 'moneda', 'tipo_instrumento']]
                    assets_offshore['asset_class'] = 'Offshore'
                    assets_df[key].append(assets_offshore)

        # Other summary
        seg_agg_other = {k: [] for k in target_group_port}
        if not tables['other'].empty:
            groupby_list_other = ['unidad_monetaria', 'tipo_instrumento']
            for key, value in eq.items():
                if key in target_group_port:
                    if kick_companies:
                        other_temp = tables['other'][(tables['other']['activo_respalda_reserva_valor_fondo'].isin(value)) & (~tables['other']['company_id'].isin(kick_comp[key]))]
                    else:
                        other_temp = tables['other'][tables['other']['activo_respalda_reserva_valor_fondo'].isin(value)]
                    seg_agg_other[key].append(pd.DataFrame(other_temp.groupby(by = groupby_list_other).sum()['valor_razonable'] / other_temp.groupby(by = groupby_list_other).sum()['valor_razonable'].sum()).reset_index())
                    assets_other = other_temp.loc[:, ['nemotecnico', 'valor_razonable', 'unidad_monetaria', 'tipo_instrumento']]
                    assets_other['asset_class'] = 'Other'
                    assets_df[key].append(assets_other)

        for key, value in assets_df.items():
            if assets_df[key]:
                for df in assets_df[key]:
                    df.columns = ['Nemotecnico', 'Valor razonable', 'Unidad monetaria', 'Tipo instrumento', 'Clase de activo']
                assets_df[key] = pd.concat(assets_df[key], axis = 0).reset_index(drop = True)

        output_list = [seg_agg_fi, seg_agg_offshore]
        for element in output_list:
            for key, value in element.items():
                if element[key]:
                    value[0].reset_index(inplace = True)
                    value[0].columns = ['Unidad monetaria', 'Clasificacion riesgo', 'Duracion', 'Tipo instrumento', 'Peso']

        output_list = [seg_agg_eq, seg_agg_mf, seg_agg_other]
        for element in output_list:
            for key, value in element.items():
                if element[key]:
                    value[0].columns = ['Unidad monetaria', 'Tipo instrumento', 'Peso']

        for key, value in seg_agg_re.items():
            if seg_agg_re[key]:
                value[0].columns = ['Tipo de inmueble', 'Tipo instrumento', 'Peso']

        complete_agg_port = {k: [] for k in target_group_port}
        complete_port_value = {k: v['Valor razonable'].sum() for k, v in assets_df.items()}
        for target in target_group_port:
            if seg_agg_fi[target]:
                if kick_companies:
                    fixed_income_temp = tables['fixed_income'][(tables['fixed_income']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['fixed_income']['company_id'].isin(kick_comp[target]))]
                else:
                    fixed_income_temp = tables['fixed_income'][tables['fixed_income']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                fixed_income_temp['dias_a_vencimiento'] = (fixed_income_temp['fecha_vencimiento'] - fixed_income_temp['period']).dt.days
                fixed_income_temp['duracion'] = fixed_income_temp.apply(func = locate_range, axis = 1)
                agg_fi_for_comp = pd.DataFrame(fixed_income_temp.groupby(by = groupby_list_fi).sum()[tipo_valor] / complete_port_value[target])
                agg_fi_for_comp.rename(columns = {tipo_valor: 'Peso'}, inplace = True)
                agg_fi_for_comp.reset_index(inplace = True)
                agg_fi_for_comp = agg_fi_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                agg_fi_for_comp.set_index(['unidad_monetaria', 'clasificacion_riesgo', 'duracion', 'tipo_instrumento'], inplace = True)
                agg_fi_for_comp['id'] = agg_fi_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                agg_fi_for_comp['Clase de activo'] = 'Renta fija'
                complete_agg_port[target].append(agg_fi_for_comp)
            if seg_agg_offshore[target]:
                if kick_companies:
                    offshore_temp = tables['offshore'][(tables['offshore']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['offshore']['company_id'].isin(kick_comp[target]))]
                else:
                    offshore_temp = tables['offshore'][tables['offshore']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                offshore_temp['dias_a_vencimiento'] = (offshore_temp['fecha_vencimiento'] - offshore_temp['period']).dt.days
                offshore_temp['duracion'] = offshore_temp.apply(func = locate_range, axis = 1)
                agg_offshore_for_comp = pd.DataFrame(offshore_temp.groupby(by = groupby_offshore_list).sum()['valor_nominal'] / complete_port_value[target])
                agg_offshore_for_comp.rename(columns = {'valor_nominal': 'Peso'}, inplace = True)
                agg_offshore_for_comp.reset_index(inplace = True)
                agg_offshore_for_comp = agg_offshore_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                agg_offshore_for_comp.set_index(['moneda', 'clasificaicon_riesgo', 'duracion', 'tipo_instrumento'], inplace = True)
                agg_offshore_for_comp['id'] = agg_offshore_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                agg_offshore_for_comp['Clase de activo'] = 'Offshore'
                complete_agg_port[target].append(agg_offshore_for_comp)
            if seg_agg_eq[target]:
                if kick_companies:
                    equity_temp = tables['equity'][(tables['equity']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['equity']['company_id'].isin(kick_comp[target]))]
                else:
                    equity_temp = tables['equity'][tables['equity']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                eq_agg_for_comp = pd.DataFrame(equity_temp.groupby(by = groupby_list_equity).sum()['valor_razonable'] / complete_port_value[target]).reset_index()
                eq_agg_for_comp.rename(columns = {'valor_razonable': 'Peso'}, inplace = True)
                eq_agg_for_comp.reset_index(inplace = True)
                eq_agg_for_comp = eq_agg_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                eq_agg_for_comp.set_index(['unidad_monetaria', 'tipo_instrumento'], inplace = True)
                eq_agg_for_comp['id'] = eq_agg_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                eq_agg_for_comp['Clase de activo'] = 'Equity'
                complete_agg_port[target].append(eq_agg_for_comp)
            if seg_agg_mf[target]:
                if kick_companies:
                    mutual_fund_temp = tables['mutual_fund'][(tables['mutual_fund']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['mutual_fund']['company_id'].isin(kick_comp[target]))]
                else:
                    mutual_fund_temp = tables['mutual_fund'][tables['mutual_fund']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                mutfund_agg_for_comp = pd.DataFrame(mutual_fund_temp.groupby(by = groupby_list_mutfund).sum()['valor_razonable'] / complete_port_value[target]).reset_index()
                mutfund_agg_for_comp.rename(columns = {'valor_razonable': 'Peso'}, inplace = True)
                mutfund_agg_for_comp.reset_index(inplace = True)
                mutfund_agg_for_comp = mutfund_agg_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                mutfund_agg_for_comp.set_index(['unidad_monetaria', 'tipo_instrumento'], inplace = True)
                mutfund_agg_for_comp['id'] = mutfund_agg_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                mutfund_agg_for_comp['Clase de activo'] = 'Mutual fund'
                complete_agg_port[target].append(mutfund_agg_for_comp)
            if seg_agg_re[target]:
                if kick_companies:
                    real_estate_temp = tables['real_estate'][(tables['real_estate']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['real_estate']['company_id'].isin(kick_comp[target]))]
                else:
                    real_estate_temp = tables['real_estate'][tables['real_estate']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                re_agg_for_comp = pd.DataFrame(real_estate_temp.groupby(by = groupby_list_re).sum()['valor_final'] / complete_port_value[target]).reset_index()
                re_agg_for_comp.rename(columns = {'valor_final': 'Peso'}, inplace = True)
                re_agg_for_comp.reset_index(inplace = True)
                re_agg_for_comp = re_agg_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                re_agg_for_comp.set_index(['tipo_de_inmueble', 'tipo_instrumento'], inplace = True)
                re_agg_for_comp['id'] = re_agg_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                re_agg_for_comp['Clase de activo'] = 'Real estate'
                complete_agg_port[target].append(re_agg_for_comp)
            if seg_agg_other[target]:
                if kick_companies:
                    other_temp = tables['other'][(tables['other']['activo_respalda_reserva_valor_fondo'].isin(eq[target])) & (~tables['other']['company_id'].isin(kick_comp[target]))]
                else:
                    other_temp = tables['other'][tables['other']['activo_respalda_reserva_valor_fondo'].isin(eq[target])]
                other_agg_for_comp = pd.DataFrame(other_temp.groupby(by = groupby_list_other).sum()['valor_razonable'] / complete_port_value[target]).reset_index()
                other_agg_for_comp.rename(columns = {'valor_razonable': 'Peso'}, inplace = True)
                other_agg_for_comp.reset_index(inplace = True)
                other_agg_for_comp = other_agg_for_comp.replace({'tipo_instrumento': {v: k for k, v in seil_eq.items()}})
                other_agg_for_comp.set_index(['unidad_monetaria', 'tipo_instrumento'], inplace = True)
                other_agg_for_comp['id'] = other_agg_for_comp.index.map(lambda x: ''.join(x).replace(' ', '')) + ' Index'
                other_agg_for_comp['Clase de activo'] = 'Other'
                complete_agg_port[target].append(other_agg_for_comp)

        for key, value in complete_agg_port.items():
            complete_agg_port[key] = pd.concat(complete_agg_port[key], axis = 0).reset_index(drop = True)
            complete_agg_port[key] = complete_agg_port[key][['id', 'Clase de activo', 'Peso']]

        return {'Renta fija': seg_agg_fi, 'Equity': seg_agg_eq, 'Mutual fund': seg_agg_mf, 'Offshore': seg_agg_offshore, 'Real estate': seg_agg_re, 'Other': seg_agg_other}, complete_agg_port

    def delta_market(self, target_group_port = ['VIDA', 'GENERAL'], dates = ['2018-12-31', '2025-12-31'], companies = None, kick_companies = True):

        last_reported = self.summarize_market(target_group_port = target_group_port, dates = dates, companies = companies,
                                             kick_companies = kick_companies, slice_delta = False)
        before_last = self.summarize_market(target_group_port = target_group_port, dates = dates, companies = companies,
                                             kick_companies = kick_companies, slice_delta = True)

        output_1 = {k: dict() for k in list(last_reported[0].keys())}
        for k1, v1 in last_reported[0].items():
            for k2, v2 in last_reported[0][k1].items():
                cols = [x for x in last_reported[0][k1][k2][0].columns if x != 'Peso']
                last_reported[0][k1][k2][0]['id'] = last_reported[0][k1][k2][0].loc[:, cols].apply('_'.join, axis = 1)
                before_last[0][k1][k2][0]['id'] = before_last[0][k1][k2][0].loc[:, cols].apply('_'.join, axis = 1)
                output_1[k1][k2] = last_reported[0][k1][k2][0].merge(before_last[0][k1][k2][0], how = 'outer', on = 'id').loc[:, ['id', 'Peso_x', 'Peso_y']]
                output_1[k1][k2].columns = ['id', 'Último reportado', 'Penúltimo reportado']
                output_1[k1][k2][['Último reportado', 'Penúltimo reportado']].fillna(0, inplace = True)
                output_1[k1][k2]['Desviación'] = output_1[k1][k2]['Último reportado'] - output_1[k1][k2]['Penúltimo reportado']
                temp_df = output_1[k1][k2]['id'].str.split('_', expand = True)
                temp_df.columns = cols
                output_1[k1][k2] = pd.concat([temp_df, output_1[k1][k2]], axis = 1)

        output_2 = {k: np.nan for k in list(last_reported[1].keys())}
        for k, v in last_reported[1].items():
            output_2[k] = last_reported[1][k].merge(before_last[1][k], how = 'outer', on = 'id')
            output_2[k]['Clase de activo'] = output_2[k].loc[:, 'Clase de activo_x'].fillna('todrop') + '_' + output_2[k].loc[:, 'Clase de activo_y'].fillna('todrop')
            output_2[k]['Clase de activo'] = output_2[k]['Clase de activo'].apply(lambda x: x.split('_')[0] if x.split('_')[0] != 'todrop' else x.split('_')[1])
            output_2[k] = output_2[k].loc[:, ['id', 'Clase de activo', 'Peso_x', 'Peso_y']]
            output_2[k].columns = ['id', 'Clase de activo', 'Último reportado', 'Penúltimo reportado']
            output_2[k][['Último reportado', 'Penúltimo reportado']].fillna(0, inplace = True)
            output_2[k]['Desviación'] = output_2[k]['Último reportado'] - output_2[k]['Penúltimo reportado']

        return output_1, output_2

    def map_portfolio(self, portfolio, asset_data, asset_eq):

        portfolio['id'] = portfolio['id'].apply(lambda x: x.replace(' Index', ''))
        grouped = portfolio.groupby('id').sum().reset_index()
        merged_df = grouped.merge(asset_eq, how = 'left', on = 'id')
        merged_df = merged_df.drop_duplicates(subset=['id'])
        eq_dict = dict(zip(asset_data['TickerBenchmark'], asset_data['Asset']))
        merged_df['ticker'].replace(eq_dict, inplace = True)
        merged_df['ticker'].fillna('Missing', inplace = True)
        merged_df = merged_df.loc[:, ['ticker', 'id', 'Peso']]
        mapped_port = merged_df.groupby('ticker').sum()
        mapped_port.index.name = 'Asset'
        missing_data = list(merged_df[merged_df['ticker'] == 'Missing']['id'].unique())
        return mapped_port, missing_data

    def calculate_aums(self, company_port_dict = None):
        """
        Extracts AuM for a given company's portfolio. If company_port_dict is None, extracts entire database.
        Parameters -
        -- company_port_dict - dictionary with keys: company_id, values: list of company's portfolios
        """
        output_df = pd.DataFrame()
        if company_port_dict is None:
            company_port_dict = self.extract_companies()
            for key, value in company_port_dict.items():
                for port in value[1]:
                    print(key, port)
                    try:
                        _, _, _, _, available_dates, aum = self.summarize_company([key], [port])
                        ref_date = max({k: max(v) for k, v in available_dates.items()}.values())
                        temp_df = pd.DataFrame({'Company id': [key], 'Company portfolio': [port], 'AuM': [aum], 'Reference date': [ref_date]})
                        output_df = pd.concat([output_df, temp_df], axis = 0)
                    except:
                        temp_df = pd.DataFrame({'Company id': [key], 'Company portfolio': [port], 'AuM': [np.nan], 'Reference date': [np.nan]})
                        output_df = pd.concat([output_df, temp_df], axis = 0)
            return output_df
        else:
            for key, value in company_port_dict.items():
                for port in value:
                    try:
                        _, _, _, _, available_dates, aum = self.summarize_company([key], [port])
                        ref_date = max({k: max(v) for k, v in available_dates.items()}.values())
                        temp_df = pd.DataFrame({'Company id': [key], 'Company portfolio': [port], 'AuM': [aum], 'Reference date': [ref_date]})
                        output_df = pd.concat([output_df, temp_df], axis = 0)
                    except:
                        temp_df = pd.DataFrame({'Company id': [key], 'Company portfolio': [port], 'AuM': [np.nan], 'Reference date': [np.nan]})
                        output_df = pd.concat([output_df, temp_df], axis = 0)
            return output_df

    def company_funds(self, company_id, target_port, date = None):
        pass

if __name__ == "__main__":
    pass
