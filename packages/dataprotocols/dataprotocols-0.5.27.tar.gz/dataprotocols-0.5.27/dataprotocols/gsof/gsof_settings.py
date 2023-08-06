from networktools.time import timestamp
gsof_table_names = {
    1: "TIME",
    2: "LATLONHEIGHT",
    3: "ECEF",
    4: "Local Datum Position".upper(),
    5: "Local_Zone_Position".upper(),
    6: "ECEF_DELTA",
    7: "TPlane_ENU".upper(),
    8: "Velocity".upper(),
    9: "DOP",
    10: "Clock_Info".upper(),
    11: "Position_VCV".upper(),
    12: "SIGMA",
    13: "GPS_SV_Brief".upper(),
    14: "GPS_SV_Detail".upper(),
    15: "Receiver_Serial_Number".upper(),
    16: "UTC",
    27: "Attitude".upper(),
    33: "All_SV_Brief".upper(),
    48: "All_SV_Detail".upper(),
    # http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/GSOFmessages_ReceivedBaseInfo.html
    35: "Received_Base_Info".upper(),
    37: "Batt_Mem".upper(),
    40: "L-Band".upper(),
    41: "BASE_POSITION_AND_QUALITY_INDICATOR",
}
gsof_field_names = {
    1: ('GPS_TIME', 'GPS_WEEK', 'SVN_NUM', 'FLAG_1', 'FLAG_2', 'INIT_NUM'),
    2: ('LATITUDE', 'LONGITUDE', 'HEIGHT'),
    3: ('X_POS', 'Y_POS', 'Z_POS'),
    4: ('LOCAL_DATUM_ID', 'LOCAL_DATUM_LAT', 'LOCAL_DATUM_LON', 'LOCAL_DATUM_HEIGHT', 'OPRT'),
    5: ('LOCAL_DATUM_ID', 'LOCAL_ZONE_ID', 'LOCAL_ZONE_NORTH', 'LOCAL_ZONE_EAST', 'LOCAL_DATUM_HEIGHT'),
    6: ('DELTA_X', 'DELTA_Y', 'DELTA_Z'),
    7: ('DELTA_EAST', 'DELTA_NORTH', 'DELTA_UP'),
    8: ('VEL_FLAG', 'VELOCITY', 'HEADING', 'VERT_VELOCITY'),
    9: ('PDOP', 'HDOP', 'VDOP', 'TDOP'),
    10: ('CLOCK_FLAG', 'CLOCK_OFFSET', 'FREQ_OFFSET'),
    # http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/GSOFmessages_PositionVCV.html
    11: ('POSITION_RMS_VCV', 'VCV_XX', 'VCV_XY', 'VCV_XZ', 'VCV_YY', 'VCV_YZ', 'VCV_ZZ', 'UNIT_VAR_VCV', 'NUM_EPOCHS_VCV'),
    12: ('POSITION_RMS_SIG', 'SIG_EAST', 'SIG_NORT', 'COVAR_EN', 'SIG_UP', 'SEMI_MAJOR', 'SEMI_MINOR', 'ORIENTATION', 'UNIT_VAR_SIG', 'NUM_EPOCHS_SIG'),
    13: ('NUM_SV', 'PRN', 'SV_FG1', 'SV_FG2'),
    14: ('PRN', 'FLAGS1', 'FLAGS2', 'ELEVATION', 'AZIMUTH', 'SNR_L1', 'SNR_L2'),
    15: 'SERIAL_NUM',
    16: ('GPS_MS_OF_WEEK', 'GPS_WEEK', 'UTC_OFFSET', 'CT_FLAGS'),
    27: ('GPS_TIME', 'FLAGS', 'N_SV', 'CALC_MODE', '', 'PITCH', 'YAW', 'ROLL',
         'MSRANGE', 'PDOP', 'PITCHV', 'YAWV', 'ROLLV', 'PITCH_YAW_COVAR',
         'PITCH_ROLL_COVAR', 'YAW_ROLL_COVAR', 'MSRANGE_VAR'),
    33: ('NUM_SV', 'SVSYS', 'SVFLAG_1', 'SVFLAG_2'),
    48: ('PRN', 'SV_SYSTEM', 'SV_FLAG1', 'SV_FLAG2', 'ELEVATION', 'AZIMUTH', 'SNR_FIRST', 'SNR_SECOND', 'SNR_THIRD'),
    35: ('FLAGS', 'BASE_NAME', 'BASE_ID', 'BASE_LAT', 'BASE_LON', 'BASE_HEIGHT'),
    37: ('BATT_CAPACITY', 'REMAINING_MEM'),
    40: ('SAT_NAME', 'SAT_FREQ', 'SAT_BITRATE', 'SNR', 'HP/XP_MODE', 'VBS_MODE',
         'BEAM_MODE', 'O_MOTION', '3SHTHRES', '3SVTHRES', 'NMEA', 'IQ_RATIO',
         'EST_BER', 'TOT_UNIQ_WORDS', 'TOT_BAD_U_W_BITS', 'TOT_VITERBI', 'TOT_CORRECT_VITERBI',
         'TOT_BAD_MSG', 'MEAS_F_FLAG', 'MEAS_F'),
    41: ('GPS_TIME', 'GPS_WEEK_NR', 'LATITUDE', 'LONGITUDE', 'HEIGHT', 'QI')
}

# print(rec_field_names)
"""
   C source code:
    https://www.trimble.com/OEM_ReceiverHelp/v5.11/en/AppNote_GSOFMsging.html#LBand

 """
gsof_rec = {
    1: '>LH4B',
    2: '>3d',
    3: '>3d',
    4: '>8s3dB',
    5: '>2s3d',
    6: '>3d',
    7: '>3d',
    8: '>B3f',
    9: '>4f',
    10: '>B2d',
    11: '>8fh',
    12: '>9fh',
    13: ('>B', '>3B'),
    # 13 *number of sv
    14: ('>B','>4BH2B'),
    # http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/Default.html#GSOFmessages_SVDetail.html
    15: '>l',
    16: '>l2hB',
    27: '>L4B4dH7f',
    33: ('>B', '>4B'),
    # http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/Default.html#GSOFmessages_AllSVBrief.html
    # 33 *number of sv
    48: ('>B', '>5BB3B'),##BIG ???
    #http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/Default.html#GSOFmessages_AllSVDetail.html
    35: '>B8B2B3d',
    37: '>Hd',
    40: '>5BfHf5B2fB2f6LBd',
    # INCOMPLETE: http://www.trimble.com/OEM_ReceiverHelp/v4.85/en/Default.html#GSOFmessages_LBand.html
    41: '>lh3dB'
}

from networktools.time import timestamp

def logfile(station):
    return './logs/gsof_%s_%s.log' % (station, str(timestamp())[:-7] )


