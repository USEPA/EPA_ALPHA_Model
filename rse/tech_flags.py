# work in progress
# TODO: add BEV flags, make sure flags are correct for non-PHEV engines, etc...

tech_flags_dict = dict()

tech_flags_dict['car'] = {'unibody': 1}

tech_flags_dict['truck'] = {'unibody': 0}

tech_flags_dict['all'] = {'high_eff_alternator': 0}  # for now

tech_flags_dict['SS0'] = {'start_stop': 0}

tech_flags_dict['SS1'] = {'start_stop': 1}

tech_flags_dict['PHEV'] = {'ice': 0,
                           'mhev': 0,
                           'hev': 0,
                           'phev': 1,
                           'fcv': 0,
                           'hev_truck': 0}

tech_flags_dict['CVM'] = {'ice': 1,
                          'mhev': 0,
                          'hev': 0,
                          'phev': 0,
                          'fcv': 0,
                          'hev_truck': 0}

tech_flags_dict['P0'] = {'ice': 0,
                         'mhev': 1,
                         'hev': 0,
                         'phev': 0,
                         'fcv': 0,
                         'hev_truck': 0}

tech_flags_dict['PS'] = {'ice': 0,
                         'mhev': 0,
                         'hev': 1,
                         'phev': 0,
                         'fcv': 0,
                         'hev_truck': 0}

tech_flags_dict['GDI'] = {
    'deac_pd': 0,
    'deac_fc': 0,
    'cegr': 0,
    'atk2': 0,
    'gdi': 1,
    'turb12': 0,
    'turb11': 0,
    'gas_fuel': 1,
    'diesel_fuel': 0,
}

tech_flags_dict['DHE'] = tech_flags_dict['GDI']

tech_flags_dict['MILLER'] = {
    'deac_pd': 0,
    'deac_fc': 0,
    'cegr': 0,
    'atk2': 1,
    'gdi': 1,
    'turb12': 1,
    'turb11': 0,
    'gas_fuel': 1,
    'diesel_fuel': 0,
}

tech_flags_dict['FWD'] = {'fwd': 1,
                          # 'rwd': 0,
                          'awd': 0}

tech_flags_dict['RWD'] = {'fwd': 0,
                          # 'rwd': 1,
                          'awd': 0}

tech_flags_dict['AWD'] = {'fwd': 0,
                          # 'rwd': 0,
                          'awd': 1}

tech_flags_dict['TRX10'] = {'trx10': 1,
                            'trx11': 0,
                            'trx12': 0,
                            'trx21': 0,
                            'trx22': 0,
                            'ecvt': 0,
                            }

tech_flags_dict['TRX11'] = {'trx10': 0,
                            'trx11': 1,
                            'trx12': 0,
                            'trx21': 0,
                            'trx22': 0,
                            'ecvt': 0,
                            }

tech_flags_dict['TRX12'] = {'trx10': 0,
                            'trx11': 0,
                            'trx12': 1,
                            'trx21': 0,
                            'trx22': 0,
                            'ecvt': 0,
                            }

tech_flags_dict['TRX21'] = {'trx10': 0,
                            'trx11': 0,
                            'trx12': 0,
                            'trx21': 1,
                            'trx22': 0,
                            'ecvt': 0,
                            }

tech_flags_dict['TRX22'] = {'trx10': 0,
                            'trx11': 0,
                            'trx12': 0,
                            'trx21': 0,
                            'trx22': 1,
                            'ecvt': 0,
                            }

tech_flags_dict['ECVT'] = {'trx10': 0,
                           'trx11': 0,
                           'trx12': 0,
                           'trx21': 0,
                           'trx22': 0,
                           'ecvt': 1,
                           }


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
