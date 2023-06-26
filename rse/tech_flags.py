# work in progress

# THESE GET EVALUATED FROM THE TOP DOWN, SO DEFAULT VALUES SHOULD BE PLACED HIGHER UP AND CAN BE OVERRIDDEN AS NEEDED

tech_flags_dict = dict()

tech_flags_dict['_'] = {
    # 'unibody': 0,  # this is a vehicle attribute, not an RSE attribute (see 'application_id')
    'start_stop': 0,

    # clear powertrain flags
    'ice': 0,
    'mhev': 0,
    'hev': 0,
    'phev': 0,
    'fcv': 0,  # for future use
    'hev_truck': 0,  # for future use
    'high_eff_alternator': 0,  # for future use

    # clear engine tech flags
    'deac_pd': 0,
    'deac_fc': 0,
    'cegr': 0,
    'atk2': 0,
    'gdi': 0,
    'turb12': 0,
    'turb11': 0,
    'gas_fuel': 0,
    'diesel_fuel': 0,

    # clear TRX tech flags
    'trx10': 0,
    'trx11': 0,
    'trx12': 0,
    'trx21': 0,
    'trx22': 0,
    'ecvt': 0,
}

# tech_flags_dict['car'] = {'unibody': 1}

tech_flags_dict['SS1'] = {'start_stop': 1}

tech_flags_dict['PS'] = {'hev': 1}
tech_flags_dict['P2'] = {'hev': 1}
tech_flags_dict['PHEV'] = {'hev': 0, 'phev': 1}
tech_flags_dict['ICE'] = {'ice': 1}
tech_flags_dict['P0'] = {'mhev': 1}
tech_flags_dict['BEV'] = {'bev': 1}

tech_flags_dict['DEAC_D'] = {'deac_pd': 1}
tech_flags_dict['DEAC_C'] = {'deac_fc': 1}

tech_flags_dict['ATK'] = {  # engine_2018_Toyota_A25AFKS_2L5_Tier3
    'cegr': 1,  # maybe?
    'gdi': 1,
    'gas_fuel': 1,
}

tech_flags_dict['GDI'] = {  # engine_2013_Chevrolet_Ecotec_LCV_2L5_Reg_E10
    'gdi': 1,
    'gas_fuel': 1,
}

tech_flags_dict['DHE'] = {  # engine_Toyota_2L5_TNGA_Proto_Hyb_Engine_paper_image_OM_Tier_3
    'gdi': 1,
    'gas_fuel': 1,
}

tech_flags_dict['MILLER'] = {  # engine_Volvo_VEP_LP_Gen3_2L0_Miller_paper_image_OM_Tier_3 / engine_Geely_1L5_Miller_GHE_paper_image_OM_Tier_3
    'atk2': 1,
    'gdi': 1,
    'turb12': 1,
    'gas_fuel': 1,
}

tech_flags_dict['TDS'] = {  # engine_2016_Honda_L15B7_1L5_Tier3 / engine_2015_Ford_EcoBoost_2L7_Tier3
    'cegr': 1,  # maybe?
    'turb12': 1,
    'gas_fuel': 1,
}

tech_flags_dict['TDS11'] = {  # engine_2013_Ford_EcoBoost_1L6_LEVIII
    'cegr': 0,  # maybe?
    'turb12': 1,
    'gas_fuel': 1,
}

tech_flags_dict['DIESEL'] = {  # engine_GTP_2020_GM_Duramax_3L0_Diesel_report_image_Diesel
    'cegr': 1,
    'turb11': 1,
    'diesel_fuel': 1,
}

tech_flags_dict['PFI'] = {  # engine_GTP_base_2020_Ford_7L3_report_image_Tier3
    'gas_fuel': 1,
}

tech_flags_dict['TRX10'] = {'trx10': 1}
tech_flags_dict['TRX11'] = {'trx11': 1}
tech_flags_dict['TRX12'] = {'trx12': 1}
tech_flags_dict['TRX21'] = {'trx21': 1}
tech_flags_dict['TRX22'] = {'trx22': 1}
tech_flags_dict['ECVT'] = {'ecvt': 1}

tech_flags_dict['FWD'] = {'drive_system': 2}
tech_flags_dict['RWD'] = {'drive_system': 2}
tech_flags_dict['AWD'] = {'drive_system': 4}

# FUTURE WORK:
# tech_flags_dict['FWD'] = {'drive_system': 'FWD'}
# tech_flags_dict['RWD'] = {'drive_system': 'RWD'}
# tech_flags_dict['AWD'] = {'drive_system': 'AWD'}

tech_flags_dict['SLA'] = {'application_id': 'SLA'}
tech_flags_dict['HLA'] = {'application_id': 'HLA'}


def apply_tech_flags(rse_df, rse_name):
    """

    Parameters
    ----------
    rse_df
    rse_name

    Returns
    -------

    """
    # set tech_flags
    for k in tech_flags_dict:
        if k == 'all' or '%s' % k in rse_name:
            rse_df = rse_df.assign(**tech_flags_dict[k])

    return rse_df
