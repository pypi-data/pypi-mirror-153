import sys
from lxml import etree
from treport.report import Report, get_config, XSD_FILE_NAME
from treport.logger import get_logger
import argparse
import os

default_config_file_name = 'treport.ini'
description = 'Программа предназначена для формирования отчетов, имеющих табличное представление'
parameters = {}


def get_params_report_list(path_to_params_reports_file, code_report):
    params_report = {}
    xsd_f = open(XSD_FILE_NAME)
    xml_f = open(path_to_params_reports_file)
    xsd_doc = etree.parse(xsd_f)
    xml_doc = etree.parse(xml_f)
    xmlschema = etree.XMLSchema(xsd_doc)
    if xmlschema.validate(xml_doc):
        logger.info('CLI: Проверка XML-файла ' + path_to_params_reports_file + ' проведена, файл корректен')
        xml_root = xml_doc.getroot()[0]
        for item_report in xml_root:
            if item_report.attrib['codeReport'] == code_report:
                logger.info(f'Чтение блока параметров отчета {code_report}')
                params = item_report[4]  # Параметры отчета
                logger.info(f'Параметры отчета {code_report}')
                for item_params in params:
                    for child_parametr in item_params:
                        if child_parametr.tag == 'parametrName':
                            params_report[item_params.attrib['id']] = child_parametr.text


    return params_report


if __name__ == '__main__':
    logger = get_logger(__name__)
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('-c', '--config', action='store',
                                   help='Указывается путь конфигурационному файлу')
    arg_parser.add_argument('-r', '--report', action='store',
                            help='Код формируемого отчета')
    arg_parser.add_argument('-pf', '--parameters-file', action='store', help='Файл с параметрами отчета')
    arg_parser.add_argument('-p', '--parameters', action='store', help='Параметры отчета. Например: "param_name1:value_param1;param_name2:value_param2"')

    args = arg_parser.parse_args()

    # Проверка наличия параметра config
    if args.config:
        configfile = args.config
    else:
        if os.path.exists(default_config_file_name):
            configfile = default_config_file_name
        else:
            logger.error('Файл treport.ini не найден, используйте параметр --config')
            sys.exit()
    logger.info(f'Конфигурационный файл {configfile}')

    # Проверка наличия параметра report
    if args.report:
        report_code = args.report
    else:
        logger.error(f'Параметр --report обязательный для использования')
        sys.exit()

    # Проверка наличия параметров parameters-file или parameters
    if args.parameters_file:
        with open(args.parameters_file) as f:
            list_parameters = f.readlines()
        for item in list_parameters:
            parameters[item.split('=')[0]] = item.split('=')[1].replace("\n", "")

        if args.parameters:
            parameters_str: str = args.parameters
            list_parameters = []
            for item in parameters_str.split(';'):
                list_parameters.append(item)

            for item in list_parameters:
                parameters[item.split(':')[0]] = item.split(':')[1]

    else:
        if args.parameters:
            parameters_str: str = args.parameters
            list_parameters = []
            for item in parameters_str.split(';'):
                list_parameters.append(item)

            for item in list_parameters:
                parameters[item.split(':')[0]] = item.split(':')[1]
        else:
            logger.error(f'Параметр --parameters обязательный для использования')
            sys.exit()

    db_url, path_to_params_reports_file = get_config(configfile)
    report = Report(report_code, path_to_params_reports_file, parameters, db_url)

    if report.isCorrect:
        report.contentReport.save(report.outDir + report.report_file_name)
        report.logger.info(f'Файл {report.outDir + report.report_file_name} сохранен')




