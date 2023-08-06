from networktools.time import timestamp

# uint8_t
PROTOCOL_VERSION = 2.3
PV_INT = int(PROTOCOL_VERSION*10)


ERYO_TABLE_REC = dict(
    ERYO_HEADER=">2bHb",
    POSITION_BLOCK=">bHIHH8s8sbb4db",
    POS_VAR_BLOCK=">7f",
    TROPO_VAR_BLOCK=">4f",
    SAT_HDR=">Hf",
    SAT_INFO_BLOCK=">3BbH",
    NEU_DISP_HDR=">3dH",
    NEU_DISP_BLOCK=">3f",
    VELOCITY_HDR=">H",
    VELOCITY_BLOCK=">3f",
    NEU_VAR_BLOCK=">6f",
    VEL_VAR_BLOCK=">6f",
    ERYO_TRAILER=">H",
)

ERYO_TABLE_NAMES = {
    1: "ERYO_HEADER",
    2: "POSITION_BLOCK",
    3: "POS_VAR_BLOCK",
    4: "TROPO_VAR_BLOCK",
    5: "SAT_HDR",
    6: "SAT_INFO_BLOCK",
    7: "NEU_DISP_HDR",
    8: "NEU_DISP_BLOCK",
    9: "VELOCITY_HDR",
    10: "VELOCITY_BLOCK",
    11: "NEU_VAR_BLOCK",
    12: "VEL_VAR_BLOCK",
    13: "ERYO_TRAILER",
}

ETN_reverse = {value: key for key, value in ERYO_TABLE_NAMES.items()}


ERYO_FIELD_NAMES = {
    1: ("SYNC_MARKER_1", "SYNC_MARKER_2", "BYTE_COUNT", "MESSAGE_ID"),
    2: ("ERYO_VERSION",
        "GPS_WEEK",
        "GPS_MILLISECONDS",
        "SITE_INDEX",
        "SITES_THIS_EPOCH",
        "SITE_ID",
        "SOLUTION_ID",
        "ECEF_FRAME",
        "AMBIGUITY_RES",
        "XYZ_ZENITH_X",  "XYZ_ZENITH_Y", "XYZ_ZENITH_Z",
        "TROPO_ZENITH_DELAY",
        "FLAGS"),
    3: ("SCALE_FACTOR", "X_VAR", "Y_VAR", "Z_VAR", "YX_COV", "YZ_COV", "ZX_COV"),
    4: ("T_VARIANCE", "TX_COV", "TY_COV", "TZ_COV"),
    5: ("SAT_BLOCK_COUNT", "GDOP"),
    6: ("CONSTELLATION", "SAT_NUMBER", "SIGNAL_FLAGS",
        "PRN_ELEVATION", "PRN_AZIMUTH"),
    7: ("X", "Y", "Z"),
    8: ("N", "E", "U"),
    9: ("VELOCITY_BLOCK_COUNT"),
    10: ("VX", "VY", "VZ"),
    11: ("N_POS_VAR", "E_POS_VAR", "U_POS_VAR",
         "EN_POS_COV", "EU_POS_COV", "UN_POS_COV"),
    12: ("N_VEL_VAR", "E_VEL_VAR", "U_VEL_VAR",
         "EN_VEL_COVAR", "EU_VEL_COVAR", "UN_VEL_COVAR"),
    13: ("CHECKSUM",),
}

nros = [1 << i for i in range(8)]
MSG_ID = dict(zip(nros, ["NEU", "VEL", "RES2", "RES3", "RES4", "NET_PPP", "RES6",
                         "RT_POST"]))


# para comparación binaria FLAG & valor->010101
BLOCKS_FLAGS = dict(
    POS_VAR=1 << 0,
    TROPO_VAR=1 << 1,
    SAT_INFO=1 << 2,
    NEU_DISP=1 << 3,
    VELOCITY=1 << 4,
    NEU_VAR=1 << 5,
    VEL_VAR=1 << 6,
    RES=1 << 7,
)

TABLES_BY_FLAG = dict(
    POS_VAR=("POS_VAR_BLOCK",),
    TROPO_VAR=("TROPO_VAR_BLOCK",),
    SAT_INFO=("SAT_HDR", "SAT_INFO_BLOCK",),
    NEU_DISP=("NEU_DISP_HDR", "NEU_DISP_BLOCK"),
    VELOCITY=("VELOCITY_HDR", "VELOCITY_BLOCK"),
    NEU_VAR=("NEU_VAR_BLOCK",),
    VEL_VAR=("VEL_VAR_BLOCK",),
    RES=(),
)


lista = [(k, v) for k, v in ERYO_TABLE_NAMES.items()]

ERYO_LIST = sorted(lista, key=lambda e: e[0])


ERYO_REC = dict(
    ERYO_HEADER=">BBHB",  # 1,1,2,1
    POSITION_BLOCK=">BHIHH8s8sBB4dB",
    POS_VAR_BLOCK=">7f",
    TROPO_VAR_BLOCK=">4f",
    SAT_HDR=">Hf",
    SAT_INFO_BLOCK=">3BbH",
    NEU_DISP_HDR=">3dH",
    NEU_DISP_BLOCK=">3f",
    VELOCITY_HDR=">H",
    VELOCITY_BLOCK=">3f",
    NEU_VAR_BLOCK=">6f",
    VEL_VAR_BLOCK=">6f",
    ERYO_TRAILER=">H")

TABLES_SIZES = dict(
    ERYO_HEADER=5,
    POSITION_BLOCK=62,
    POS_VAR_BLOCK=28,
    TROPO_VAR_BLOCK=16,
    SAT_HDR=6,
    SAT_INFO_BLOCK=6,
    NEU_DISP_HDR=26,
    NEU_DISP_BLOCK=12,
    VELOCITY_HDR=2,
    VELOCITY_BLOCK=12,
    NEU_VAR_BLOCK=24,
    VEL_VAR_BLOCK=24,
    ERYO_TRAILER=2,
)


MSG_MAX_SIZE = sum(TABLES_SIZES.values())  # bytes

BUFF_MAX_SIZE = MSG_MAX_SIZE


def logfile(station):
    return './logs/gsof_%s_%s.log' % (station, str(timestamp())[:-7])


SYNC_MARKER_VALUE = {
    "first": b"\x9C",
    "second": b"\xA5",
}

"""
checksum_t eryo_calculateChecksum(
         const char * const buffer,
         const int buff_size)
{
  checksum_t sum=(checksum_t) 0;
  uint8_t *ptr, *last;
  ptr=(uint8_t *) &buffer[0];1
  last=(uint8_t *) &buffer[buff_size - 1];
  while (ptr <=last)
  {
    sum +=(checksum_t) *ptr++;
  }
  return sum;
}
"""


def eryo_checksum(buffer, buffsize):
    suma = 0  # checksum256(0)
    ptr = buffer[0]
    last = buffer[-1]
    while (ptr <= last):
        ptr += 1
        suma += ptr
    return suma


def binary(e): return "{0:8b}".format(e).replace(" ", "0")


lista = [1 << i for i in range(8)]
binarios = list(map(binary, lista))
bin_diccionario = dict(zip(lista, binarios))


"""
Satellite FLAGS
"""

CONSTELLATION = dict(
    GPS=0,
    GLONASS=1,
    GALILEO=2
)

CONS = {value: key for key, value in CONSTELLATION.items()}


SIGNALS = dict(
    EPHEMERIS_AVAIL=1 << 0,
    L1_TRACK=1 << 1,
    L2_TRACK=1 << 2,
    L3_TRACK=1 << 3,
    RES4=1 << 4,
    RES5=1 << 5,
    RES6=1 << 6,
    RES7=1 << 7
)

SIGNAL_SAT = {value: key for key, value in SIGNALS.items()}


def signal_check(value):
    signals = list(filter(lambda e: e[1] > 0,
                          [(signal, nro & value) for signal, nro in
                           SIGNALS.items()]))
    return [name for name, value in signals]
