from getting_and_setting.mi_api import mi_api_execute
from getting_and_setting.mi_models import MiError
from functools import partial
from itertools import chain
from tempfile import NamedTemporaryFile
import argparse
import pandas as pd
import os


def procedure(endpoint: str, mfno: str):
    get_distorders = partial(mi_api_execute, endpoint=endpoint, program='MMS100MI', transaction='GetLine', CONO=100)
    get_disthead = partial(mi_api_execute, endpoint=endpoint, program='MMS100MI', transaction='GetHead')
    get_facilities = partial(mi_api_execute, endpoint=endpoint, program='CRS008MI', transaction='ListFacility', CONO=100)
    get_materials = partial(mi_api_execute, endpoint=endpoint, program='MOS100MI', transaction='SelMaterials', CONO=100, maxrecs=0)
    get_workorder = partial(mi_api_execute, endpoint=endpoint, program='MOS100MI', transaction='Get', CONO=100)
    get_preallocs = partial(mi_api_execute, endpoint=endpoint, program='MWS120MI', transaction='Select', CONO=100, maxrecs=0)
    get_itemwarehouse = partial(mi_api_execute, endpoint=endpoint, program='MMS200MI', transaction='GetItmWhsBasic', CONO=100)

    facilities = map(
        lambda x: x['FACI'],
        filter(
            lambda x: x['DIVI'] == '158', get_facilities().records
        )
    )

    materials = list(
        filter(
            lambda x: not isinstance(x, MiError),
            map(
                lambda x: get_materials(MFNO=mfno, FACI=x),
                facilities
            )
        )
    )

    if len(materials) != 1:
        raise LookupError(f'Workorder {mfno} not found!')

    materials = materials[0].records
    workorder = get_workorder(
        MFNO=materials[0]['MFNO'],
        FACI=materials[0]['FACI'],
        PRNO=materials[0]['PRNO']
    ).records[0]

    preallocs = list(
        chain(
                *map(
                        lambda x: get_preallocs(FWHS=x, TWHS=workorder['WHLO']).records,
                        ['CEA', 'CEB']
                )
        )
)

    result_list = []

    for material in materials:
        result = {'material': material}
        for prealloc in preallocs:
                if material['MFNO'].strip() == prealloc['DRDN'].strip() and material['MSEQ'].strip() == prealloc['DRDL'].strip():
                        result['prealloc'] = prealloc
                        result['distorder'] = get_distorders(TRNR=prealloc['ARDN'], PONR=prealloc['ARDL'].strip()).records[0]
                        result['disthead'] = get_disthead(TRNR=prealloc['ARDN']).records[0]
                        result['itemwarehouse'] = get_itemwarehouse(ITNO=material['MTNO'], WHLO=result['distorder']['WHLO']).records[0]

        result_list.append(result)


    final_results = pd.DataFrame(
        {
            'Work Order': x['material']['MFNO'],
            'Material Line': x['material']['MSEQ'].strip(),
            'Material': x['material']['MTNO'].strip(),
            'Warehouse': x['material']['WHLO'].strip(),
            'Status': x['material']['WMST'].strip(),
            'Plan Whs.': x['material']['PWHL'].strip(),
            'Reservation date': x['material']['RDAT'].strip(),
            'Ref Order': x['prealloc']['ARDN'] if x.get('prealloc') else None,
            'Ref Order Line': x['prealloc']['ARDL'].strip() if x.get('prealloc') else None,
            'Ref Transaction Date': x['distorder']['TRDT'].strip() if x.get('distorder') else None,
            'Ref Transaction Status': x['distorder']['TRSH'].strip() if x.get('distorder') else None,
            'Ref Transaction Warehouse': x['distorder']['WHLO'].strip() if x.get('distorder') else None,
            'Ref Transaction Type': x['disthead']['TRTP'].strip() if x.get('disthead') else None,
            'Source Warehouse': x['itemwarehouse']['SUWH'].strip() if x.get('itemwarehouse') else None

        }
        for x
        in result_list
    )

    f = NamedTemporaryFile(mode='w', prefix='WO_Lines', suffix='.xlsx')
    f.close()
    final_results.to_excel(f.name)
    os.system(f'start excel.exe {f.name}')


def main():
    parser = argparse.ArgumentParser(description='Get WO data')
    parser.add_argument('endpoint', action='store')
    parser.add_argument('mfno', action='store')
    args = parser.parse_args()

    procedure(args.endpoint, args.mfno)

if __name__ == '__main__':
    main()