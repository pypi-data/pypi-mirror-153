# Sample python script to run an EBSILON model from python
# via the EbsOpen COM API
# Requires pywin32 and a valid EBSILON license with EbsOpen option
# By: Milton Venetos, Wyatt Enterprises, LLC
# Copyright (C) October 18, 2017
# http://www.wyattllc.com
# 注意：引入本文件就需要可用的Ebsilon授权和EbsOpen授权

from enum import Enum
from typing import Optional

import win32com.client

from yangke.common.config import logger


class EbsKind(Enum):
    pipe_electric = 1009  # e_uom.epObjectKindPipeElectric
    comp1 = 10001  # e_uom.epObjectKindComp1
    comp2 = 10002  # e_uom.epObjectKindComp2
    comp3 = 10003  # e_uom.epObjectKindComp3
    comp4 = 10004  # e_uom.epObjectKindComp4
    comp5 = 10005  # e_uom.epObjectKindComp5
    comp6 = 10006  # e_uom.epObjectKindComp6
    comp7 = 10007  # e_uom.epObjectKindComp7
    comp8 = 10008  # e_uom.epObjectKindComp8
    comp9 = 10009  # e_uom.epObjectKindComp9
    comp10 = 10010  # e_uom.epObjectKindComp10
    comp11 = 10011  # e_uom.epObjectKindComp11
    comp12 = 10012  # e_uom.epObjectKindComp12
    comp13 = 10013  # e_uom.epObjectKindComp13
    comp14 = 10014  # e_uom.epObjectKindComp14
    comp15 = 10015  # e_uom.epObjectKindComp15
    comp16 = 10016  # e_uom.epObjectKindComp16
    comp17 = 10017  # e_uom.epObjectKindComp17
    comp18 = 10018  # e_uom.epObjectKindComp18
    comp19 = 10019  # e_uom.epObjectKindComp19
    comp20 = 10020  # e_uom.epObjectKindComp20
    comp21 = 10021  # e_uom.epObjectKindComp21
    comp22 = 10022  # e_uom.epObjectKindComp22
    comp23 = 10023  # e_uom.epObjectKindComp23
    comp24 = 10024  # e_uom.epObjectKindComp24
    comp25 = 10025  # e_uom.epObjectKindComp25
    comp26 = 10026  # e_uom.epObjectKindComp26
    comp27 = 10027  # e_uom.epObjectKindComp27
    comp28 = 10028  # e_uom.epObjectKindComp28
    comp29 = 10029  # e_uom.epObjectKindComp29

    comp30 = 10030  # e_uom.epObjectKindComp30
    comp31 = 10031  # e_uom.epObjectKindComp31
    comp32 = 10032  # e_uom.epObjectKindComp32
    comp33 = 10033  # e_uom.epObjectKindComp33
    comp34 = 10034  # e_uom.epObjectKindComp34
    comp35 = 10035  # e_uom.epObjectKindComp35
    comp36 = 10036  # e_uom.epObjectKindComp36
    comp37 = 10037  # e_uom.epObjectKindComp37
    comp38 = 10038  # e_uom.epObjectKindComp38
    comp39 = 10039  # e_uom.epObjectKindComp39

    comp40 = 10040  # e_uom.epObjectKindComp40
    comp41 = 10041  # e_uom.epObjectKindComp41
    comp42 = 10042  # e_uom.epObjectKindComp42
    comp43 = 10043  # e_uom.epObjectKindComp43
    comp44 = 10044  # e_uom.epObjectKindComp44
    comp45 = 10045  # e_uom.epObjectKindComp45
    comp46 = 10046  # e_uom.epObjectKindComp46
    comp47 = 10047  # e_uom.epObjectKindComp47
    comp48 = 10048  # e_uom.epObjectKindComp48
    comp49 = 10049  # e_uom.epObjectKindComp49

    comp50 = 10050  # e_uom.epObjectKindComp50
    comp51 = 10051  # e_uom.epObjectKindComp51
    comp52 = 10052  # e_uom.epObjectKindComp52
    comp53 = 10053  # e_uom.epObjectKindComp53
    comp54 = 10054  # e_uom.epObjectKindComp54
    comp55 = 10055  # e_uom.epObjectKindComp55
    comp56 = 10056  # e_uom.epObjectKindComp56
    comp57 = 10057  # e_uom.epObjectKindComp57
    comp58 = 10058  # e_uom.epObjectKindComp58
    comp59 = 10059  # e_uom.epObjectKindComp59

    comp60 = 10060  # e_uom.epObjectKindComp60
    comp61 = 10061  # e_uom.epObjectKindComp61
    comp62 = 10062  # e_uom.epObjectKindComp62
    comp63 = 10063  # e_uom.epObjectKindComp63
    comp64 = 10064  # e_uom.epObjectKindComp64
    comp65 = 10065  # e_uom.epObjectKindComp65
    comp66 = 10066  # e_uom.epObjectKindComp66
    comp67 = 10067  # e_uom.epObjectKindComp67
    comp68 = 10068  # e_uom.epObjectKindComp68
    comp69 = 10069  # e_uom.epObjectKindComp69

    comp70 = 10070  # e_uom.epObjectKindComp70
    comp71 = 10071  # e_uom.epObjectKindComp71
    comp72 = 10072  # e_uom.epObjectKindComp72
    comp73 = 10073  # e_uom.epObjectKindComp73
    comp74 = 10074  # e_uom.epObjectKindComp74
    comp75 = 10075  # e_uom.epObjectKindComp75
    comp76 = 10076  # e_uom.epObjectKindComp76
    comp77 = 10077  # e_uom.epObjectKindComp77
    comp78 = 10078  # e_uom.epObjectKindComp78
    comp79 = 10079  # e_uom.epObjectKindComp79

    comp80 = 10080  # e_uom.epObjectKindComp80
    comp81 = 10081  # e_uom.epObjectKindComp81
    comp82 = 10082  # e_uom.epObjectKindComp82
    comp83 = 10083  # e_uom.epObjectKindComp83
    comp84 = 10084  # e_uom.epObjectKindComp84
    comp85 = 10085  # e_uom.epObjectKindComp85
    comp86 = 10086  # e_uom.epObjectKindComp86
    comp87 = 10087  # e_uom.epObjectKindComp87
    comp88 = 10088  # e_uom.epObjectKindComp88
    comp89 = 10089  # e_uom.epObjectKindComp89

    comp90 = 10090  # e_uom.epObjectKindComp90
    comp91 = 10091  # e_uom.epObjectKindComp91
    comp92 = 10092  # e_uom.epObjectKindComp92
    comp93 = 10093  # e_uom.epObjectKindComp93
    comp94 = 10094  # e_uom.epObjectKindComp94
    comp95 = 10095  # e_uom.epObjectKindComp95
    comp96 = 10096  # e_uom.epObjectKindComp96
    comp97 = 10097  # e_uom.epObjectKindComp97
    comp98 = 10098  # e_uom.epObjectKindComp98
    comp99 = 10099  # e_uom.epObjectKindComp99

    comp100 = 10100  # e_uom.epObjectKindComp100
    comp101 = 10101  # e_uom.epObjectKindComp101
    comp102 = 10102  # e_uom.epObjectKindComp102
    comp103 = 10103  # e_uom.epObjectKindComp103
    comp104 = 10104  # e_uom.epObjectKindComp104
    comp105 = 10105  # e_uom.epObjectKindComp105
    comp106 = 10106  # e_uom.epObjectKindComp106
    comp107 = 10107  # e_uom.epObjectKindComp107
    comp108 = 10108  # e_uom.epObjectKindComp108
    comp109 = 10109  # e_uom.epObjectKindComp109

    comp110 = 10110  # e_uom.epObjectKindComp110
    comp111 = 10111  # e_uom.epObjectKindComp111
    comp112 = 10112  # e_uom.epObjectKindComp112
    comp113 = 10113  # e_uom.epObjectKindComp113
    comp114 = 10114  # e_uom.epObjectKindComp114
    comp115 = 10115  # e_uom.epObjectKindComp115
    comp116 = 10116  # e_uom.epObjectKindComp116
    comp117 = 10117  # e_uom.epObjectKindComp117
    comp118 = 10118  # e_uom.epObjectKindComp118
    comp119 = 10119  # e_uom.epObjectKindComp119

    comp120 = 10120  # e_uom.epObjectKindComp120
    comp121 = 10121  # e_uom.epObjectKindComp121
    comp122 = 10122  # e_uom.epObjectKindComp122
    comp123 = 10123  # e_uom.epObjectKindComp123
    comp124 = 10124  # e_uom.epObjectKindComp124
    comp125 = 10125  # e_uom.epObjectKindComp125
    comp126 = 10126  # e_uom.epObjectKindComp126
    comp127 = 10127  # e_uom.epObjectKindComp127
    comp128 = 10128  # e_uom.epObjectKindComp128
    comp129 = 10129  # e_uom.epObjectKindComp129

    comp130 = 10130  # e_uom.epObjectKindComp130
    comp131 = 10131  # e_uom.epObjectKindComp131
    comp132 = 10132  # e_uom.epObjectKindComp132
    comp133 = 10133  # e_uom.epObjectKindComp133
    comp134 = 10134  # e_uom.epObjectKindComp134
    comp135 = 10135  # e_uom.epObjectKindComp135
    comp136 = 10136  # e_uom.epObjectKindComp136
    comp137 = 10137  # e_uom.epObjectKindComp137
    comp138 = 10138  # e_uom.epObjectKindComp138
    try:  # 12版ebsilon不存在以下组件
        comp139 = 10139  # e_uom.epObjectKindComp139
        comp140 = 10140  # e_uom.epObjectKindComp140
        comp141 = 10141  # e_uom.epObjectKindComp141
        comp142 = 10142  # e_uom.epObjectKindComp142
        comp143 = 10143  # e_uom.epObjectKindComp143
        comp144 = 10144  # e_uom.epObjectKindComp144
        comp145 = 10145  # e_uom.epObjectKindComp145
        comp146 = 10146  # e_uom.epObjectKindComp146
        comp147 = 10147  # e_uom.epObjectKindComp147
        comp148 = 10148  # e_uom.epObjectKindComp148
        comp149 = 10149  # e_uom.epObjectKindComp149

        comp150 = 10150  # e_uom.epObjectKindComp150
        comp151 = 10151  # e_uom.epObjectKindComp151
        comp152 = 10152  # e_uom.epObjectKindComp152
        comp153 = 10153  # e_uom.epObjectKindComp153
        comp154 = 10154  # e_uom.epObjectKindComp154
        comp155 = 10155  # e_uom.epObjectKindComp155
        comp156 = 10156  # e_uom.epObjectKindComp156
        comp157 = 10157  # e_uom.epObjectKindComp157
    except AttributeError:
        pass


class EbsUnits(Enum):
    """
    Ebsilon的单位系统，包含了Ebsilon软件中定义的所有单位常量，在读写组件参数时会用到。参见ebsilon帮助文件EpUnit Enumeration
    """
    global e_uom
    # 流量
    lb_h: "lb_h" = 326  # e_uom.epUNIT_lb_h  # 磅/小时，流量单位
    kg_s: "kg/s" = 6  # e_uom.epUNIT_kg_s  # 流量单位kg/s
    # 功率
    MW: "MW" = 100  # e_uom.epUNIT_MW  # 功率单位，MW
    kW = 7  # e_uom.epUNIT_kW
    W = 216  # e_uom.epUNIT_W
    # 压力
    bar = 3  # e_uom.epUNIT_bar
    Pa = 203  # e_uom.epUNIT_Pa
    kPa = 217  # e_uom.epUNIT_kPa
    MPa = 123  # e_uom.epUNIT_MPa
    # 温度
    C = 372  # e_uom.epUNIT_C
    K = 12  # e_uom.epUNIT_K
    # 能量
    J = 297  # e_uom.epUNIT_J
    kJ = 296  # e_uom.epUNIT_kJ
    MJ = 298  # e_uom.epUNIT_MJ

    # 密度
    g_m3 = 301  # e_uom.epUNIT_g_m3
    # 转速
    unit_1_min = 17  # 试验测试得到的值
    # 其他
    int = 321  # e_uom.epUNIT_INTEGRAL
    text = 53  # e_uom.epUNIT_TEXT
    access_actual = -10  # e_uom.epUNITACCESS_ACTUAL
    access_si = -11  # e_uom.epUNITACCESS_SI
    ACCESS_Imperial = -12  # e_uom.epUNITACCESS_Imperial
    ACCESS_USC = -13  # e_uom.epUNITACCESS_USC
    # ERROR = e_uom.epUNIT_ERROR
    INVALID = 0  # e_uom.epUNIT_INVALID
    NONE = 1  # e_uom.epUNIT_NONE
    unit_1 = 2  # e_uom.epUNIT_1
    GrdC = 4  # e_uom.epUNIT_GrdC
    kJ_kg = 5  # e_uom.epUNIT_kJ_kg
    m3_kg = 8  # e_uom.epUNIT_m3_kg
    m3_s = 9  # e_uom.epUNIT_m3_s
    kmol_kmol = 13  # e_uom.epUNIT_kmol_kmol
    kg_kg = 14  # e_uom.epUNIT_kg_kg
    kW_K = 15  # e_uom.epUNIT_kW_K
    W_m2K = 16  # e_uom.epUNIT_W_m2K
    kJ_kWh = 18  # e_uom.epUNIT_kJ_kWh
    kJ_m3 = 21  # e_uom.epUNIT_kJ_m3
    kJ_m3K = 22  # e_uom.epUNIT_kJ_m3K
    kg_m3 = 23  # e_uom.epUNIT_kg_m3
    m = 24  # e_uom.epUNIT_m
    kJ_kgK_cp = 26  # e_uom.epUNIT_kJ_kgK_cp
    m2 = 27  # e_uom.epUNIT_m2
    kJ_kgK = 28  # e_uom.epUNIT_kJ_kgK
    kg_kg_x = 29  # e_uom.epUNIT_kg_kg_x
    kg_kg_xg = 30  # e_uom.epUNIT_kg_kg_xg
    kg_kmol = 31  # e_uom.epUNIT_kg_kmol
    kJ_kg_ncv = 32  # e_uom.epUNIT_kJ_kg_ncv
    m_s = 33  # e_uom.epUNIT_m_s
    kg_kg_x_rg = 34  # e_uom.epUNIT_kg_kg_x_rg
    FTYP_8 = 35  # e_uom.epUNIT_FTYP_8
    FTYP_9 = 36  # e_uom.epUNIT_FTYP_9
    mg_Nm3 = 37  # e_uom.epUNIT_mg_Nm3
    EUR_h = 38  # e_uom.epUNIT_EUR_h
    kW_kg = 39  # e_uom.epUNIT_kW_kg
    _1_m6 = 40  # e_uom.epUNIT_1_m6
    A = 41  # e_uom.epUNIT_A
    EUR_kWh = 42  # e_uom.epUNIT_EUR_kWh
    EUR_kg = 43  # e_uom.epUNIT_EUR_kg
    V = 44  # e_uom.epUNIT_V
    m3_m3 = 45  # e_uom.epUNIT_m3_m3
    kg = 46  # e_uom.epUNIT_kg
    EUR = 47  # e_uom.epUNIT_EUR
    m3 = 48  # e_uom.epUNIT_m3
    ph = 49  # e_uom.epUNIT_ph
    m2K_W = 51  # e_uom.epUNIT_m2K_W
    W_m2 = 52  # e_uom.epUNIT_W_m2
    TEXT = 53  # e_uom.epUNIT_TEXT
    Grd = 54  # e_uom.epUNIT_Grd
    m_geopot = 59  # e_uom.epUNIT_m_geopot
    t_h = 101  # e_uom.epUNIT_t_h
    GrdF = 102  # e_uom.epUNIT_GrdF
    Prz = 103  # e_uom.epUNIT_Prz
    psia = 104  # e_uom.epUNIT_psia
    btu_lb = 105  # e_uom.epUNIT_btu_lb
    klb_h = 106  # e_uom.epUNIT_klb_h
    ft3_lb = 107  # e_uom.epUNIT_ft3_lb
    Mft3_h = 108  # e_uom.epUNIT_Mft3_h
    R = 109  # e_uom.epUNIT_R
    lb_lb = 110  # e_uom.epUNIT_lb_lb
    kbtu_hF = 111  # e_uom.epUNIT_kbtu_hF
    btu_ft2hF = 112  # e_uom.epUNIT_btu_ft2hF
    lb_ft3 = 113  # e_uom.epUNIT_lb_ft3
    btu_lbF = 114  # e_uom.epUNIT_btu_lbF
    btu_kWh = 115  # e_uom.epUNIT_btu_kWh
    btu_ft3 = 116  # e_uom.epUNIT_btu_ft3
    btu_ft3F = 117  # e_uom.epUNIT_btu_ft3F
    ft = 118  # e_uom.epUNIT_ft
    rpm = 119  # e_uom.epUNIT_rpm
    hp = 120  # e_uom.epUNIT_hp
    ft2 = 121  # e_uom.epUNIT_ft2
    m3_h = 122  # e_uom.epUNIT_m3_h
    btu_lbF_cp = 124  # e_uom.epUNIT_btu_lbF_cp
    mbar = 125  # e_uom.epUNIT_mbar
    lb_lb_x = 126  # e_uom.epUNIT_lb_lb_x
    lb_lb_xg = 127  # e_uom.epUNIT_lb_lb_xg
    lb_kmol = 128  # e_uom.epUNIT_lb_kmol
    btu_lb_ncv = 129  # e_uom.epUNIT_btu_lb_ncv
    ft_s = 130  # e_uom.epUNIT_ft_s
    lb_lb_x_rg = 131  # e_uom.epUNIT_lb_lb_x_rg
    CENT_min = 132  # e_uom.epUNIT_CENT_min
    DM_h = 133  # e_uom.epUNIT_DM_h
    PFENNIG_min = 134  # e_uom.epUNIT_PFENNIG_min
    Prz_x = 137  # e_uom.epUNIT_Prz_x
    Prz_xg = 138  # e_uom.epUNIT_Prz_xg
    g_mol = 139  # e_uom.epUNIT_g_mol
    ppm = 140  # e_uom.epUNIT_ppm
    ppm_xg = 141  # e_uom.epUNIT_ppm_xg
    MW_kg = 142  # e_uom.epUNIT_MW_kg
    hp_lb = 143  # e_uom.epUNIT_hp_lb
    mg_m3 = 144  # e_uom.epUNIT_mg_m3
    _1_ft6 = 145  # e_uom.epUNIT_1_ft6
    kg_h = 146  # e_uom.epUNIT_kg_h
    mA = 147  # e_uom.epUNIT_mA
    t_s = 148  # e_uom.epUNIT_t_s
    EUR_MWh = 149  # e_uom.epUNIT_EUR_MWh
    CENT_kWh = 150  # e_uom.epUNIT_CENT_kWh
    EUR_t = 151  # e_uom.epUNIT_EUR_t
    CENT_kg = 152  # e_uom.epUNIT_CENT_kg
    kV = 153  # e_uom.epUNIT_kV
    g_kg = 158  # e_uom.epUNIT_g_kg
    mg_kg = 159  # e_uom.epUNIT_mg_kg
    Prz_vol = 160  # e_uom.epUNIT_Prz_vol
    ppm_vol = 161  # e_uom.epUNIT_ppm_vol
    ft3_ft3 = 162  # e_uom.epUNIT_ft3_ft3
    t = 164  # e_uom.epUNIT_t
    g = 165  # e_uom.epUNIT_g
    mg = 166  # e_uom.epUNIT_mg
    lb = 167  # e_uom.epUNIT_lb
    klb = 168  # e_uom.epUNIT_klb
    CENT = 169  # e_uom.epUNIT_CENT
    DM = 170  # e_uom.epUNIT_DM
    Pfennig = 171  # e_uom.epUNIT_Pfennig
    l_min = 172  # e_uom.epUNIT_l_min
    l_h = 173  # e_uom.epUNIT_l_h
    mV = 174  # e_uom.epUNIT_mV
    mm = 176  # e_uom.epUNIT_mm
    cm = 177  # e_uom.epUNIT_cm
    km = 178  # e_uom.epUNIT_km
    yd = 179  # e_uom.epUNIT_yd
    inch = 180  # e_uom.epUNIT_in
    mi = 181  # e_uom.epUNIT_mi
    mm2 = 182  # e_uom.epUNIT_mm2
    cm2 = 183  # e_uom.epUNIT_cm2
    L = 184  # e_uom.epUNIT_l
    km2 = 185  # e_uom.epUNIT_km2
    yd2 = 186  # e_uom.epUNIT_yd2
    in2 = 187  # e_uom.epUNIT_in2
    mi2 = 188  # e_uom.epUNIT_mi2
    ft3 = 189  # e_uom.epUNIT_ft3
    mm3 = 190  # e_uom.epUNIT_mm3
    cm3 = 191  # e_uom.epUNIT_cm3
    km3 = 192  # e_uom.epUNIT_km3
    yd3 = 193  # e_uom.epUNIT_yd3
    in3 = 194  # e_uom.epUNIT_in3
    mi3 = 195  # e_uom.epUNIT_mi3
    gal = 196  # e_uom.epUNIT_gal
    kg_Nm3 = 197  # e_uom.epUNIT_kg_Nm3
    tm3_h = 198  # e_uom.epUNIT_tm3_h
    Mm3_h = 199  # e_uom.epUNIT_Mm3_h
    mmWS = 201  # e_uom.epUNIT_mmWS
    mWS = 202  # e_uom.epUNIT_mWS
    kA = 204  # e_uom.epUNIT_kA
    l_s = 205  # e_uom.epUNIT_l_s
    Hz = 206  # e_uom.epUNIT_Hz
    mmHg = 207  # e_uom.epUNIT_mmHg
    mg_l = 208  # e_uom.epUNIT_mg_l
    at = 209  # e_uom.epUNIT_at
    kcal_kg = 210  # e_uom.epUNIT_kcal_kg
    kcal_kg_ncv = 211  # e_uom.epUNIT_kcal_kg_ncv
    kcal_kgK = 212  # e_uom.epUNIT_kcal_kgK
    kcal_kgK_cp = 213  # e_uom.epUNIT_kcal_kgK_cp
    kW_m2 = 214  # e_uom.epUNIT_kW_m2
    kcal_m2h = 215  # e_uom.epUNIT_kcal_m2h
    Nm_kg = 218  # e_uom.epUNIT_Nm_kg
    kVA = 219  # e_uom.epUNIT_kVA
    MVA = 220  # e_uom.epUNIT_MVA
    VA = 221  # e_uom.epUNIT_VA
    kVAr = 222  # e_uom.epUNIT_kVAr
    MVAr = 223  # e_uom.epUNIT_MVAr
    VAr = 224  # e_uom.epUNIT_VAr
    atm = 225  # e_uom.epUNIT_atm
    g_s = 226  # e_uom.epUNIT_g_s
    kg_ms = 227  # e_uom.epUNIT_kg_ms
    W_mK = 228  # e_uom.epUNIT_W_mK
    inHg = 229  # e_uom.epUNIT_inHg
    ft_geopot = 230  # e_uom.epUNIT_ft_geopot
    km_geopot = 231  # e_uom.epUNIT_km_geopot
    yd_geopot = 232  # e_uom.epUNIT_yd_geopot
    mi_geopot = 233  # e_uom.epUNIT_mi_geopot
    rad = 234  # e_uom.epUNIT_rad
    _1_Grd = 235  # e_uom.epUNIT_1_Grd
    _1_Grd2 = 236  # e_uom.epUNIT_1_Grd2
    _1_Grd3 = 237  # e_uom.epUNIT_1_Grd3
    _1_Grd4 = 238  # e_uom.epUNIT_1_Grd4
    _1_Grd5 = 239  # e_uom.epUNIT_1_Grd5
    _1_rad = 240  # e_uom.epUNIT_1_rad
    _1_rad2 = 241  # e_uom.epUNIT_1_rad2
    _1_rad3 = 242  # e_uom.epUNIT_1_rad3
    _1_rad4 = 243  # e_uom.epUNIT_1_rad4
    _1_rad5 = 244  # e_uom.epUNIT_1_rad5
    _1_K = 245  # e_uom.epUNIT_1_K
    _1_K2 = 246  # e_uom.epUNIT_1_K2
    _1_K3 = 247  # e_uom.epUNIT_1_K3
    _1_K4 = 248  # e_uom.epUNIT_1_K4
    _1_R = 249  # e_uom.epUNIT_1_R
    _1_R2 = 250  # e_uom.epUNIT_1_R2
    _1_R3 = 251  # e_uom.epUNIT_1_R3
    _1_R4 = 252  # e_uom.epUNIT_1_R4
    W_m = 253  # e_uom.epUNIT_W_m
    kW_m = 254  # e_uom.epUNIT_kW_m
    kcal_mh = 255  # e_uom.epUNIT_kcal_mh
    GrdK = 256  # e_uom.epUNIT_GrdK
    s = 257  # e_uom.epUNIT_s
    min = 258  # e_uom.epUNIT_min
    h = 259  # e_uom.epUNIT_h
    d = 260  # e_uom.epUNIT_d
    K_m = 261  # e_uom.epUNIT_K_m
    kJ_kgm = 262  # e_uom.epUNIT_kJ_kgm
    K_cm = 263  # e_uom.epUNIT_K_cm
    K_mm = 264  # e_uom.epUNIT_K_mm
    K_km = 265  # e_uom.epUNIT_K_km
    K_ft = 266  # e_uom.epUNIT_K_ft
    K_yd = 267  # e_uom.epUNIT_K_yd
    R_ft = 268  # e_uom.epUNIT_R_ft
    R_yd = 269  # e_uom.epUNIT_R_yd
    btu_lbft = 270  # e_uom.epUNIT_btu_lbft
    datetime = 271  # e_uom.epUNIT_datetime
    kW_kgK = 272  # e_uom.epUNIT_kW_kgK
    W_kgK = 273  # e_uom.epUNIT_W_kgK
    W_gK = 274  # e_uom.epUNIT_W_gK
    kbtu_lbhF = 275  # e_uom.epUNIT_kbtu_lbhF
    bar_m = 276  # e_uom.epUNIT_bar_m
    mbar_m = 277  # e_uom.epUNIT_mbar_m
    mbar_cm = 278  # e_uom.epUNIT_mbar_cm
    psia_ft = 279  # e_uom.epUNIT_psia_ft
    kt = 280  # e_uom.epUNIT_kt
    Mt = 281  # e_uom.epUNIT_Mt
    mN_m = 282  # e_uom.epUNIT_mN_m
    N_m = 283  # e_uom.epUNIT_N_m
    W_mK2 = 284  # e_uom.epUNIT_W_mK2
    W_mK3 = 285  # e_uom.epUNIT_W_mK3
    W_mK4 = 286  # e_uom.epUNIT_W_mK4
    m_K = 287  # e_uom.epUNIT_m_K
    m_K2 = 288  # e_uom.epUNIT_m_K2
    m2_s = 289  # e_uom.epUNIT_m2_s
    ft2_s = 290  # e_uom.epUNIT_ft2_s
    mm2_s = 291  # e_uom.epUNIT_mm2_s
    cm2_s = 292  # e_uom.epUNIT_cm2_s
    in2_s = 293  # e_uom.epUNIT_in2_s
    Pas = 294  # e_uom.epUNIT_Pas
    mPas = 295  # e_uom.epUNIT_mPas
    kWh = 299  # e_uom.epUNIT_kWh
    MWh = 300  # e_uom.epUNIT_MWh
    Nm3_s = 302  # e_uom.epUNIT_Nm3_s
    Nm3_h = 303  # e_uom.epUNIT_Nm3_h
    kNm3_h = 304  # e_uom.epUNIT_kNm3_h
    kg_m3K = 305  # e_uom.epUNIT_kg_m3K
    lb_ft3R = 306  # e_uom.epUNIT_lb_ft3R
    g_m3K = 307  # e_uom.epUNIT_g_m3K
    kg_lK = 308  # e_uom.epUNIT_kg_lK
    g_lK = 309  # e_uom.epUNIT_g_lK
    g_cm3K = 310  # e_uom.epUNIT_g_cm3K
    kJ_kgK2 = 311  # e_uom.epUNIT_kJ_kgK2
    btu_lbR2 = 312  # e_uom.epUNIT_btu_lbR2
    kg_l = 313  # e_uom.epUNIT_kg_l
    g_l = 314  # e_uom.epUNIT_g_l
    g_cm3 = 315  # e_uom.epUNIT_g_cm3
    kcal_kWh = 316  # e_uom.epUNIT_kcal_kWh
    mrad = 317  # e_uom.epUNIT_mrad
    kg2_kJs = 318  # e_uom.epUNIT_kg2_kJs
    lb2_btus = 319  # e_uom.epUNIT_lb2_btus
    kW_m2K = 320  # e_uom.epUNIT_kW_m2K
    INTEGRAL = 321  # e_uom.epUNIT_INTEGRAL
    P = 322  # e_uom.epUNIT_P
    cP = 323  # e_uom.epUNIT_cP
    St = 324  # e_uom.epUNIT_St
    cSt = 325  # e_uom.epUNIT_cSt
    lb_s = 327  # e_uom.epUNIT_lb_s
    klb_s = 328  # e_uom.epUNIT_klb_s
    oz_s = 329  # e_uom.epUNIT_oz_s
    oz_h = 330  # e_uom.epUNIT_oz_h
    y3_s = 331  # e_uom.epUNIT_y3_s
    ft3_s = 332  # e_uom.epUNIT_ft3_s
    in3_s = 333  # e_uom.epUNIT_in3_s
    gal_s = 334  # e_uom.epUNIT_gal_s
    y3_h = 336  # e_uom.epUNIT_y3_h
    ft3_h = 337  # e_uom.epUNIT_ft3_h
    in3_h = 338  # e_uom.epUNIT_in3_h
    gal_h = 339  # e_uom.epUNIT_gal_h
    kft3_s = 340  # e_uom.epUNIT_kft3_s
    kft3_h = 341  # e_uom.epUNIT_kft3_h
    m_h = 342  # e_uom.epUNIT_m_h
    km_h = 343  # e_uom.epUNIT_km_h
    y_s = 344  # e_uom.epUNIT_y_s
    in_s = 345  # e_uom.epUNIT_in_s
    y_h = 346  # e_uom.epUNIT_y_h
    ft_h = 347  # e_uom.epUNIT_ft_h
    mi_h = 348  # e_uom.epUNIT_mi_h
    W_mGrdC = 349  # e_uom.epUNIT_W_mGrdC
    W_mGrdC2 = 350  # e_uom.epUNIT_W_mGrdC2
    W_mGrdC3 = 351  # e_uom.epUNIT_W_mGrdC3
    W_mGrdC4 = 352  # e_uom.epUNIT_W_mGrdC4
    m_GrdC = 353  # e_uom.epUNIT_m_GrdC
    m_GrdC2 = 354  # e_uom.epUNIT_m_GrdC2
    bars_kg = 356  # e_uom.epUNIT_bars_kg
    barkg_kJ = 357  # e_uom.epUNIT_barkg_kJ
    barK_kW = 358  # e_uom.epUNIT_barK_kW
    ppm_kg = 359  # e_uom.epUNIT_ppm_kg
    ppm_x = 360  # e_uom.epUNIT_ppm_x
    ppm_x_rg = 361  # e_uom.epUNIT_ppm_x_rg
    Prz_kg = 362  # e_uom.epUNIT_Prz_kg
    Prz_x_rg = 363  # e_uom.epUNIT_Prz_x_rg
    g_kg_x = 364  # e_uom.epUNIT_g_kg_x
    mg_kg_x = 365  # e_uom.epUNIT_mg_kg_x
    g_kg_xg = 366  # e_uom.epUNIT_g_kg_xg
    mg_kg_xg = 367  # e_uom.epUNIT_mg_kg_xg
    g_kg_x_rg = 368  # e_uom.epUNIT_g_kg_x_rg
    mg_kg_x_rg = 369  # e_uom.epUNIT_mg_kg_x_rg
    _1_s = 370  # e_uom.epUNIT_1_s
    _1_h = 371  # e_uom.epUNIT_1_h
    F = 373  # e_uom.epUNIT_F
    inWS = 374  # e_uom.epUNIT_inWS
    cmWS = 375  # e_uom.epUNIT_cmWS
    kcal = 376  # e_uom.epUNIT_kcal
    cal = 377  # e_uom.epUNIT_cal
    kcal_h = 378  # e_uom.epUNIT_kcal_h
    lb_lbmole = 379  # e_uom.epUNIT_lb_lbmole
    lbmole_lbmole = 380  # e_uom.epUNIT_lbmole_lbmole
    kmol_lbmole = 381  # e_uom.epUNIT_kmol_lbmole
    lbmole_kmol = 382  # e_uom.epUNIT_lbmole_kmol
    MJ_m3 = 383  # e_uom.epUNIT_MJ_m3
    btu = 384  # e_uom.epUNIT_btu
    N = 385  # e_uom.epUNIT_N
    kN = 386  # e_uom.epUNIT_kN
    mN = 387  # e_uom.epUNIT_mN
    lbf = 388  # e_uom.epUNIT_lbf
    kp = 389  # e_uom.epUNIT_kp
    PS = 390  # e_uom.epUNIT_PS
    Torr = 391  # e_uom.epUNIT_Torr
    unit_1_m = 392  # e_uom.epUNIT_1_m
    unit_1_ft = 393  # e_uom.epUNIT_1_ft
    unit_1_mm = 394  # e_uom.epUNIT_1_mm
    unit_1_cm = 395  # e_uom.epUNIT_1_cm
    unit_1_km = 396  # e_uom.epUNIT_1_km
    unit_1_yd = 397  # e_uom.epUNIT_1_yd
    unit_1_in = 398  # e_uom.epUNIT_1_in
    unit_1_mi = 399  # e_uom.epUNIT_1_mi
    btu_h = 400  # e_uom.epUNIT_btu_h
    kbtu_h = 401  # e_uom.epUNIT_kbtu_h
    Mbtu_h = 402  # e_uom.epUNIT_Mbtu_h
    m2_W = 403  # e_uom.epUNIT_m2_W
    kJ_Nm3 = 404  # e_uom.epUNIT_kJ_Nm3
    MJ_Nm3 = 405  # e_uom.epUNIT_MJ_Nm3
    MJ_SCM = 406  # e_uom.epUNIT_MJ_SCM
    btu_SCF = 407  # e_uom.epUNIT_btu_SCF
    oz = 408  # e_uom.epUNIT_oz
    gr = 409  # e_uom.epUNIT_gr
    mg_SCM = 410  # e_uom.epUNIT_mg_SCM
    gr_SCF = 411  # e_uom.epUNIT_gr_SCF
    SCM_s = 412  # e_uom.epUNIT_SCM_s
    SCF_s = 413  # e_uom.epUNIT_SCF_s
    PATH = 414  # e_uom.epUNIT_PATH
    FOLDER = 415  # e_uom.epUNIT_FOLDER
    KERNELEXPRESSION = 416  # e_uom.epUNIT_KERNELEXPRESSION
    unit_1_kg = 417  # e_uom.epUNIT_1_kg
    kg_kg_1xg = 418  # e_uom.epUNIT_kg_kg_1xg
    mol_mol = 419  # e_uom.epUNIT_mol_mol
    mol_prz = 420  # e_uom.epUNIT_mol_prz
    mass_prz = 421  # e_uom.epUNIT_mass_prz
    mol_ppm = 422  # e_uom.epUNIT_mol_ppm
    ftH2O = 423  # e_uom.epUNIT_ftH2O
    mTorr = 424  # e_uom.epUNIT_mTorr
    oz_in2 = 425  # e_uom.epUNIT_oz_in2
    hPa = 426  # e_uom.epUNIT_hPa
    cmHg = 427  # e_uom.epUNIT_cmHg
    kg_cm2 = 428  # e_uom.epUNIT_kg_cm2
    g_cm2 = 429  # e_uom.epUNIT_g_cm2
    shton_s = 430  # e_uom.epUNIT_shton_s
    shton_h = 431  # e_uom.epUNIT_shton_h
    lgton_s = 432  # e_uom.epUNIT_lgton_s
    lgton_h = 433  # e_uom.epUNIT_lgton_h
    DOLLAR_h = 434  # e_uom.epUNIT_DOLLAR_h
    POUND_h = 435  # e_uom.epUNIT_POUND_h
    YEN_h = 436  # e_uom.epUNIT_YEN_h
    DOLLAR_kWh = 437  # e_uom.epUNIT_DOLLAR_kWh
    POUND_kWh = 438  # e_uom.epUNIT_POUND_kWh
    YEN_kWh = 439  # e_uom.epUNIT_YEN_kWh
    DOLLAR_kg = 440  # e_uom.epUNIT_DOLLAR_kg
    POUND_kg = 441  # e_uom.epUNIT_POUND_kg
    YEN_kg = 442  # e_uom.epUNIT_YEN_kg
    DOLLAR = 443  # e_uom.epUNIT_DOLLAR
    POUND = 444  # e_uom.epUNIT_POUND
    YEN = 445  # e_uom.epUNIT_YEN
    DOLLAR_s = 446  # e_uom.epUNIT_DOLLAR_s
    POUND_s = 447  # e_uom.epUNIT_POUND_s
    YEN_s = 448  # e_uom.epUNIT_YEN_s
    EUR_s = 449  # e_uom.epUNIT_EUR_s
    CENT_s = 450  # e_uom.epUNIT_CENT_s
    CENT_h = 451  # e_uom.epUNIT_CENT_h
    kNm3_s = 452  # e_uom.epUNIT_kNm3_s
    kJ_mol = 453  # e_uom.epUNIT_kJ_mol
    J_mol = 454  # e_uom.epUNIT_J_mol
    btu_mol = 455  # e_uom.epUNIT_btu_mol
    kcal_mol = 456  # e_uom.epUNIT_kcal_mol
    gal_min = 457  # e_uom.epUNIT_gal_min
    mSQRT_K_W = 458  # e_uom.epUNIT_mSQRT_K_W
    mSQRT_K_kW = 459  # e_uom.epUNIT_mSQRT_K_kW
    ftSQRT_Rk_W = 460  # e_uom.epUNIT_ftSQRT_Rk_W
    impgal = 461  # e_uom.epUNIT_impgal
    impgal_s = 462  # e_uom.epUNIT_impgal_s
    impgal_min = 463  # e_uom.epUNIT_impgal_min
    impgal_h = 464  # e_uom.epUNIT_impgal_h
    impgal_d = 465  # e_uom.epUNIT_impgal_d
    Mimpgal_d = 466  # e_uom.epUNIT_Mimpgal_d
    A_K = 467  # e_uom.epUNIT_A_K
    mA_K = 468  # e_uom.epUNIT_mA_K
    V_K = 469  # e_uom.epUNIT_V_K
    mV_K = 470  # e_uom.epUNIT_mV_K
    A_F = 471  # e_uom.epUNIT_A_F
    mA_F = 472  # e_uom.epUNIT_mA_F
    V_F = 473  # e_uom.epUNIT_V_F
    mV_F = 474  # e_uom.epUNIT_mV_F
    Ohm = 475  # e_uom.epUNIT_Ohm
    kOhm = 476  # e_uom.epUNIT_kOhm
    MOhm = 477  # e_uom.epUNIT_MOhm
    Farad = 478  # e_uom.epUNIT_Farad
    mFarad = 479  # e_uom.epUNIT_mFarad
    muFarad = 480  # e_uom.epUNIT_muFarad
    nFarad = 481  # e_uom.epUNIT_nFarad
    pFarad = 482  # e_uom.epUNIT_pFarad
    Henry = 483  # e_uom.epUNIT_Henry
    mHenry = 484  # e_uom.epUNIT_mHenry
    kHenry = 485  # e_uom.epUNIT_kHenry
    muHenry = 486  # e_uom.epUNIT_muHenry
    kJ_kgs = 487  # e_uom.epUNIT_kJ_kgs
    kJ_kgh = 488  # e_uom.epUNIT_kJ_kgh
    kWs_kg = 489  # e_uom.epUNIT_kWs_kg
    kWh_kg = 490  # e_uom.epUNIT_kWh_kg
    kWs_m3 = 491  # e_uom.epUNIT_kWs_m3
    kWh_m3 = 492  # e_uom.epUNIT_kWh_m3
    GrdR = 493  # e_uom.epUNIT_GrdR
    try:  # 12版ebsilon不存在以下单位
        Nm = 494  # e_uom.epUNIT_Nm
        kNm = 495  # e_uom.epUNIT_kNm
        lbf_ft = 496  # e_uom.epUNIT_lbf_ft
        ozf_in = 497  # e_uom.epUNIT_ozf_in
        lbf_in = 498  # e_uom.epUNIT_lbf_in
        ozf_ft = 499  # e_uom.epUNIT_ozf_ft
        dynm = 500  # e_uom.epUNIT_dynm
        Wh = 501  # e_uom.epUNIT_Wh
        Wh_kg = 502  # e_uom.epUNIT_Wh_kg
        Wh_m3 = 503  # e_uom.epUNIT_Wh_m3
        kJ_m2 = 504  # e_uom.epUNIT_kJ_m2
        kWh_m2 = 505  # e_uom.epUNIT_kWh_m2
        Wh_m2 = 506  # e_uom.epUNIT_Wh_m2
        btu_ft2 = 507  # e_uom.epUNIT_btu_ft2
        W_m3 = 508  # e_uom.epUNIT_W_m3
        kW_m3 = 509  # e_uom.epUNIT_kW_m3
        m2K_kW = 510  # e_uom.epUNIT_m2K_kW
        ft2hF_btu = 511  # e_uom.epUNIT_ft2hF_btu
        MJ_kg = 512  # e_uom.epUNIT_MJ_kg
        GJ_kg = 513  # e_uom.epUNIT_GJ_kg
        J_kg = 514  # e_uom.epUNIT_J_kg
        MJ_kWh = 515  # e_uom.epUNIT_MJ_kWh
        GJ_kWh = 516  # e_uom.epUNIT_GJ_kWh
        J_kWh = 517  # e_uom.epUNIT_J_kWh
        GJ_m3 = 518  # e_uom.epUNIT_GJ_m3
        J_m3 = 519  # e_uom.epUNIT_J_m3
        MJ_m3K = 520  # e_uom.epUNIT_MJ_m3K
        GJ_m3K = 521  # e_uom.epUNIT_GJ_m3K
        J_m3K = 522  # e_uom.epUNIT_J_m3K
        MJ_kgK_cp = 523  # e_uom.epUNIT_MJ_kgK_cp
        GJ_kgK_cp = 524  # e_uom.epUNIT_GJ_kgK_cp
        J_kgK_cp = 525  # e_uom.epUNIT_J_kgK_cp
        MJ_kgK = 526  # e_uom.epUNIT_MJ_kgK
        GJ_kgK = 527  # e_uom.epUNIT_GJ_kgK
        J_kgK = 528  # e_uom.epUNIT_J_kgK
        MJ_kg_ncv = 529  # e_uom.epUNIT_MJ_kg_ncv
        GJ_kg_ncv = 530  # e_uom.epUNIT_GJ_kg_ncv
        J_kg_ncv = 531  # e_uom.epUNIT_J_kg_ncv
        MJ_kgm = 532  # e_uom.epUNIT_MJ_kgm
        GJ_kgm = 533  # e_uom.epUNIT_GJ_kgm
        J_kgm = 534  # e_uom.epUNIT_J_kgm
        GW = 536  # e_uom.epUNIT_GW
        TW = 537  # e_uom.epUNIT_TW
        GJ_h = 538  # e_uom.epUNIT_GJ_h
        MJ_h = 539  # e_uom.epUNIT_MJ_h
        kJ_h = 540  # e_uom.epUNIT_kJ_h
        J_h = 541  # e_uom.epUNIT_J_h
        J_s = 542  # e_uom.epUNIT_J_s
        mg_s = 543  # e_uom.epUNIT_mg_s
        g_h = 544  # e_uom.epUNIT_g_h
        mg_h = 545  # e_uom.epUNIT_mg_h
        mug_s = 546  # e_uom.epUNIT_mug_s
        mug_h = 547  # e_uom.epUNIT_mug_h
        mug = 548  # e_uom.epUNIT_mug
        mum = 549  # e_uom.epUNIT_mum
        ml = 550  # e_uom.epUNIT_ml
        ml_s = 551  # e_uom.epUNIT_ml_s
        cm3_s = 552  # e_uom.epUNIT_cm3_s
        mm3_s = 553  # e_uom.epUNIT_mm3_s
        kW_mK = 554  # e_uom.epUNIT_kW_mK
        l_kg = 555  # e_uom.epUNIT_l_kg
        btu_hftK = 556  # e_uom.epUNIT_btu_hftK
        W_mm = 557  # e_uom.epUNIT_W_mm
        W_cm = 558  # e_uom.epUNIT_W_cm
        btu_hft = 559  # e_uom.epUNIT_btu_hft
        W_ft = 560  # e_uom.epUNIT_W_ft
        W_cm2 = 561  # e_uom.epUNIT_W_cm2
        btu_hft2 = 562  # e_uom.epUNIT_btu_hft2
        W_ft2 = 563  # e_uom.epUNIT_W_ft2
        MW_m3 = 564  # e_uom.epUNIT_MW_m3
        btu_hft3 = 565  # e_uom.epUNIT_btu_hft3
        W_ft3 = 566  # e_uom.epUNIT_W_ft3
        W_kg = 567  # e_uom.epUNIT_W_kg
        ms = 568  # e_uom.epUNIT_ms
        mus = 569  # e_uom.epUNIT_mus
        Promille = 570  # e_uom.epUNIT_Promille
        Promille_x = 571  # e_uom.epUNIT_Promille_x
        Promille_xg = 572  # e_uom.epUNIT_Promille_xg
        Promille_vol = 573  # e_uom.epUNIT_Promille_vol
        Promille_kg = 574  # e_uom.epUNIT_Promille_kg
        Promille_x_rg = 575  # e_uom.epUNIT_Promille_x_rg
        mol_promille = 576  # e_uom.epUNIT_mol_promille
        mass_promille = 577  # e_uom.epUNIT_mass_promille
        unit_1_W = 578  # e_uom.epUNIT_1_W
        unit_1_V = 579  # e_uom.epUNIT_1_V
    except AttributeError:
        pass

    @staticmethod
    def str2unit(string: str):
        """
        将常见的单位字符串转换为EbsUnits对象

        :param string:
        :return:
        """
        string = string.replace("/", "_")
        string = string.replace("℃", "GrdC")
        return eval(f"EbsUnits.{string}")


class EbsResult:
    def __init__(self, result=None, result_code=-1):
        self.result = result
        if self.result is not None:
            self.result_code = self.result[0]
        else:
            self.result_code = result_code

    def success(self, no_error_as_success=False):
        """
        计算结果是否成功

        :param no_error_as_success: 没有错误则认为成功，相当于只看计算结果中是否有错误，没有则认为成功，这种情况下，达到最大迭代步数也会认为成功
        :return:
        """
        if no_error_as_success:
            success_list = [0, 1, 2, 6, 7]
        else:
            success_list = [0, 1, 2]
        if self.result_code in success_list:
            return True
        else:
            return False

    def get_result_detail(self):
        """
        打印并返回计算结果的所有信息，会逐条返回每一条error或warning或comment信息。

        :return:
        """
        if self.result is None:
            logger.debug("结果中不包括详细信息，如需详细信息，请使用model.simulate()或model.simulate2()方法！")
            msg = self.get_result_summary()
            logger.debug(f"当前计算结果为：{msg}")
            return {"结果总结": msg}
        else:
            result_dict = {"结果总结": self.get_result_summary()}
            results = self.result[1]
            for i in range(results.Count):
                idx = i + 1
                item = results.Item(idx)
                description = item.Description
                component_name = item.Object.Name
                result_dict.update({
                    idx: {
                        "description": description,
                        "component": component_name,
                        "level": item.Level,
                    }
                })
                logger.debug(f"组件名：{component_name:^30s}消息：{description}")  # 格式含义，^居中，20字符串宽度，s表示字符串
            return result_dict

    def get_result_summary(self):
        """
        获取计算结果是否成功的提示信息，即计算结果提示框的信息，这并不是具体的错误信息。

        :return:
        """
        # Function to translate EBSILON Calculation Result Codes to text
        ebs_err_code_txt = "Unknown Error Code"
        if self.result_code == 0:
            ebs_err_code_txt = "Simulation Successful"
        if self.result_code == 1:
            ebs_err_code_txt = "Simulation Successful With Comments"
        if self.result_code == 2:
            ebs_err_code_txt = "Simulation Successful With Warnings"
        if self.result_code == 3:
            ebs_err_code_txt = "Simulation Failed With Errors"
        if self.result_code == 4:
            ebs_err_code_txt = "Simulation Failed with Errors before Calculation - Check Model set up"
        if self.result_code == 5:
            ebs_err_code_txt = "Simulation Failed - Fatal Error"
        if self.result_code == 6:
            ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached"
        if self.result_code == 7:
            ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached With Warnings"
        if self.result_code == 8:
            ebs_err_code_txt = "Simulation Failed - Maximum Simulation Duration Time Exceeded"
        if self.result_code == 9:
            ebs_err_code_txt = "Simulation Failed - Maximum Number of Iterations Reached With Errors"
        if self.result_code == 10:
            ebs_err_code_txt = "Simulation Failed - License Error"
        if self.result_code == 11:
            ebs_err_code_txt = "Simulation Failed- Already In Simulation Error"
        if self.result_code == 12:
            ebs_err_code_txt = "Simulation Failed - Internal Error"
        return ebs_err_code_txt


class EbsApp:
    def __init__(self, ebsilon=None):
        """
        Ebsilon软件对象，参见EbsOpen.Application帮助文件，为空则会自动创建该对象。

        :param ebsilon:
        """
        if ebsilon is None:
            self.app = None  # ebsilon内部的application类对象，代表了ebsilon软件本身
            self.e_uom: Optional[win32com.client.Constants] = None  # ebsilon的枚举常量集合
            # 初始化ebsilon，返回Ebsilon软件内置的Application类对象
            try:
                # app = win32com.client.dynamic.Dispatch("EbsOpen.Application") #late binding / dynamic dispatch
                ebsilon = win32com.client.gencache.EnsureDispatch(
                    "EbsOpen.Application")  # early binding / static dispatch
                self.e_uom = win32com.client.constants
            except:
                logger.debug("初始化Ebsilon时发生错误，请检查您的Ebsilon license")
                exit()

        self.app = ebsilon
        # self.about = ebsilon.AboutString
        self.com_class_id = ebsilon.COMCLSID
        self.com_progress_id = ebsilon.COMProgID
        self.computation_tool = ebsilon.ComputationTool
        self.configuration = ebsilon.Configuration
        self.ebsilon_professional_flag = ebsilon.EbsilonProfessionalFlag
        self.ebsilon_professional_license_values_layout2 = ebsilon.EbsilonProfessionalLicenseValuesLayout2
        self.ebsilon_professional_license_values_layout2_marshal_array = \
            ebsilon.EbsilonProfessionalLicenseValuesLayout2MarshalArrayAsVariant
        self.ebs_open_demo_mode = ebsilon.EbsOpenDemoMode
        # self.events = ebsilon.Events  # 初始化时报错，可能是个动态变量
        # self.intel_mkl_cnr_cbwr = ebsilon.Intel_MKL_CNR_CBWR
        self.is_dll = ebsilon.IsDll
        self.isProcess = ebsilon.IsProcess
        self.module_filename = ebsilon.ModuleFileName
        self.object_caster = ObjectCaster(ebsilon.ObjectCaster)
        self.position = ebsilon.Position
        self.version_string = ebsilon.ProductVersionString
        self.version_major = ebsilon.ProductVersionMajor
        self.version_minor = ebsilon.ProductVersionMinor
        self.version_serialization = ebsilon.SerializationVersion
        self.unit_converter = ebsilon.UnitConverter

    def open(self, filename, on_error_return_null: bool = True):
        model: EbsModel = EbsModel(self.app.Open(filename, on_error_return_null))
        if not model.exists():
            logger.debug(f"打开模型文件时出错，检查文件路径是否存在：{filename}，或尝试初始化EbsApp")
        return model

    def get_active_model(self):
        return EbsModel(self.app.ActiveModel)

    def get_models(self):
        models = []
        for m in self.app.Models:
            models.append(EbsModel(m))
        return models

    def show_window(self, show=None):
        if show is None:
            show = self.e_uom.epShowWindowShowNormal
        result: bool = self.app.ShowWindow(show)
        return result

    def get_application_string(self):
        return self.app.ApplicationString

    def describe(self):
        logger.info(self.get_application_string())

    def get_object_caster(self):
        return ObjectCaster(self.app.ObjectCaster)


class EbsModel:
    def __init__(self, model):
        """
        Ebsilon软件的模型类，考虑到动态更新成员变量和循环引用，将源对象的成员变量更改为对应的成员方法模式获取

        :param model: Ebsilon软件待封装的模型对象
        """
        self.model = model

    def set_value(self, component, abbr, value, unit: EbsUnits = None, save_flag=True):
        """
        设置模型中某个组件中的参数

        :param component: 组件名
        :param abbr: 参数名，缩写
        :param value: 参数数值
        :param unit: 单位，EbsUnits对象，默认使用参数现有的单位
        :param save_flag: 设置后是否保存模型，默认保存
        :return:
        """
        comp = self.object_by_context(component)  # 不能使用get_object
        comp.set_value(abbr=abbr, value=value, unit=unit, save_flag=save_flag)

    def get_value(self, component, abbr, unit=None):
        comp = self.object_by_context(component)
        return comp.get_value(abbr, unit)

    def get_active_profile(self):
        return EbsProfile(self.model.ActiveProfile)

    def get_compression_level(self):
        return self.model.CompressionLevel

    def get_compression_method(self):
        return self.model.CompressionMethod

    def has_calculation_equations(self):
        return self.model.HasCalculationEquations

    def get_calculation_equations(self):
        return self.model.CalculationEquations

    def has_calculation_errors(self):
        return self.model.HasCalculationErrors

    def get_calculation_errors(self):
        return self.model.CalculationErrors

    def has_validation_ebsilon_entries(self):
        return self.model.HasValidationEbsilonEntries

    def get_validation_ebsilon_entries(self):
        return self.model.ValidationEbsilonEntries

    def get_statistics(self):
        return self.model.Statistics

    def get_doa(self):
        return self.model.DOA

    def get_toa(self):
        return self.model.TOA

    def get_context(self):
        return self.model.Context

    def get_objects(self):
        """
        获取模型中的所有组件列表

        :return:
        """
        objects = []
        for obj in self.model.Objects:
            objects.append(EbsObject(obj))
        return objects

    def get_position(self):
        return self.model.Position

    def get_path(self):
        return self.model.Path

    def get_root_profile(self):
        return self.model.RootProfile

    def get_summary(self):
        return self.model.Summary

    def get_name(self):
        return str(self.model.Name)

    def get_configuration(self):
        return self.model.Configuration

    def get_events(self):
        return self.model.Events

    def get_app(self):  # 不能定义为成员变量self.app，否则和EbsApp的构造方法循环引用
        return EbsApp(self.model.Application)

    def activate(self):
        self.model.Activate()

    def activate_profile(self, name_or_id: "str or int"):
        """
        激活指定的Profile

        :param name_or_id:
        :return:
        """
        result: bool = self.model.ActivateProfile(name_or_id)
        return result

    def get_profile(self, name_or_id: "str or int" = None, waring=True):
        """
        获取模型中指定的Profile，如果不存在指定的profile，则返回None

        :param name_or_id:
        :param waring: 不存在时是否报警告
        :return:
        """
        if name_or_id is None:
            return EbsProfile(self.model.ActiveProfile)
        else:
            _tuple = self.model.GetProfile(name_or_id)
            if _tuple[0]:
                return EbsProfile(_tuple[1])
            else:
                if waring:
                    logger.warning(f"不存在指定的profile：{name_or_id}")
                return None

    def get_all_profiles(self):
        profiles = []
        i = 0
        _ = self.get_profile(i, waring=False)
        while _ is not None:
            profiles.append(_)
            i = i + 1
            _ = self.get_profile(i, waring=False)
        return profiles

    def get_position1(self, from_current_context: bool = True):
        return self.model.getPosition(from_current_context)

    def get_object(self, name: str, on_not_found_return_null=True):
        """
        根据组件名获取组件对象，该方法会获取到具体的组件对象，而不是统一的EbsObject类对象

        :param name:
        :param on_not_found_return_null:
        :return:
        """
        obj: EbsObject = self.object_by_context(name, on_not_found_return_null)
        if not obj.exists():  # 查找的组件不存在
            return None
        result = obj.cast_to_component()  # 将当前组件转换为对应的组件类对象
        return result

    def object_by_context(self, name: str, on_not_found_return_null=True):
        result: EbsObject = EbsObject(self.model.ObjectByContext(name, on_not_found_return_null))
        if not result.exists():
            logger.warning(f"不存在名为{name}的组件")
        return result

    def save(self):
        result: bool = self.model.Save()
        return result

    def save_as(self, filepath: str):
        """
        保存一个当前模型的副本，当前打开的模型变更为新保存的模型

        :param filepath:
        :return:
        """
        result: bool = self.model.SaveAs(filepath)
        return result

    def save_copy_as(self, filepath: str):
        """
        保存一个当前模型的副本，当前打开的模型不变
        :param filepath:
        :return:
        """
        result: bool = self.model.SaveCopyAs(filepath)
        return result

    def simulate(self):
        """
        对当前活动profile进行计算，计算返回提示信息，返回的提示信息过于丰富，不推荐使用，推荐使用simulate_new()方法
        :return:
        """
        result = None
        result = self.model.Simulate(result)  # Simulate方法需要传入形参
        result = EbsResult(result)
        return result

    def simulate2(self):
        """
        提示信息更丰富，会提示过时的设置，且提示信息比图形界面还丰富，不推荐使用

        :return:
        """
        result = None
        results = self.model.Simulate2(result)  # Simulate2方法需要传入形参
        results = EbsResult(results)
        return results

    def simulate_new(self):
        result = self.model.SimulateNew()  # SimulateNew方法不需要传入形参
        result = EbsResult(result_code=result)
        return result

    def describe(self, print_objects=False):
        logger.info(f"模型路径：{self.get_path()}")
        profiles = self.get_all_profiles()
        logger.info("该模型包含以下Profiles：")
        for prof in profiles:
            logger.info(f"id: {prof.get_profile_id()}，Name: {prof.get_name()}")
        if print_objects:
            objects = self.get_objects()
            objects = sorted(objects, key=lambda o: o.get_kind(), reverse=True)
            logger.info(f"该模型共包含{len(objects)}个组件，如下所示：")
            logger.info(f"{'name':^35}|{'type':^10}")
            for obj in objects:
                logger.info(f"{obj.get_name():^35}|{obj.get_kind():^10}")

    def exists(self):
        """
        当前模型是否存在

        :return:
        """
        if self.model is None:
            return False
        else:
            return True


class EbsProfile:
    def __init__(self, profile):
        """
        Ebsilon软件的Profile类，其中，考虑到循环引用和动态更新的问题，将成员变量更改为相应的成员方法
        :param profile:
        """
        self.profile = profile

    def get_configuration(self):
        return self.profile.Configuration

    def has_new_nominal_values(self):
        return self.profile.HasNewNominalValues

    def has_parent(self):
        return bool(self.profile.HasParent)

    def get_profile_id(self):
        return self.profile.ProfileId

    def is_active(self):
        return bool(self.profile.IsActive)

    def get_name(self):
        return str(self.profile.Name)

    def get_parent(self):
        # 不能定义为成员变量self.parent，否则和EbsApp类的构造方法循环引用
        return EbsProfile(self.profile.Parent)

    def get_app(self):
        # 不能定义为成员变量self.app，否则和EbsApp类的构造方法循环引用
        return EbsApp(self.profile.Application)

    def get_model(self):
        # 不能定义为成员变量，否则和EbsModel类的构造方法循环引用
        return EbsModel(self.profile.Model)

    def activate(self):
        result: bool = self.profile.Activate()
        return result

    def change_name(self, new_name: str):
        result: str = self.profile.ChangeName(new_name, allow_modify=True, check_only=False)
        return result

    def get_children(self):
        children = self.profile.Children
        result = []
        for child in children:
            result.append(EbsProfile(child))
        return result

    def copy(self, copied_profile, deep=True, parent_of_copied_profile=None):
        """
        方法未调试

        :param copied_profile:
        :param deep:
        :param parent_of_copied_profile:
        :return:
        """
        result: bool = self.profile.Copy(copied_profile, deep, parent_of_copied_profile)
        return result

    def delete(self):
        result: bool = self.profile.Delete()
        return result

    def make_to_root(self):
        result: bool = self.profile.MakeToRoot()
        return result

    def new_child(self):
        result: EbsProfile = EbsProfile(self.profile.NewChild())
        return result

    def saturate(self, profile: Optional["EbsProfile"]):
        """
        可能是全屏操作

        :param profile:
        :return:
        """
        result: bool = self.profile.Saturate(profile)
        return result

    def take_over_nominal_values(self):
        result: bool = self.profile.TakeOverNominalValues()
        return result


class ObjectCaster:
    def __init__(self, caster):
        self.caster = caster

    def cast_to_component(self, component_id: int, obj):
        """
        将IObject类型转换为具体的类型
        :param component_id: 因为Ebsilon有157个不同类型的组件，因此component_id≥1，≤157
        :return:
        """
        _ = self.caster
        obj = obj.obj
        expression = f"_.CastToComp{component_id}(obj)"
        result = eval(expression)
        return result

    def cast_to_data(self, obj):
        """
        将EbsObject类型转换为数据包类型，便于进一步提取组件中的数据

        :param obj:
        :return:
        """
        if isinstance(obj, EbsObject):
            obj = obj.obj
        result = self.caster.CastToData(obj)
        return result


class EbsObject:
    def __init__(self, obj):
        """
        Ebsilon软件的Object类

        :param obj: Ebsilon软件的Object类对象
        """
        self.obj = obj

    def get_data_object(self):
        return self.obj.DataObject

    def get_description(self):
        return self.obj.Description

    def get_description2(self):
        return self.obj.Description2

    def get_description3(self):
        return self.obj.Description3

    def get_description4(self):
        return self.obj.Description4

    def get_name(self):
        return self.obj.Name

    def get_fullname(self):
        return self.obj.FullName

    def get_font(self):
        return self.obj.Font

    def get_font_color(self):
        return self.obj.FontColor

    def get_model(self):
        return EbsModel(self.obj.Model)

    def get_app(self):
        return self.get_model().get_app()

    def get_kind(self):
        return self.obj.Kind

    def get_组件号(self, warning=True):
        组件号 = self.get_kind() - 10000
        if 1 <= 组件号 <= 157:
            return 组件号
        else:
            if warning:
                logger.warning(f"未知组件号：{self.get_kind()}")
                return -1
            else:
                return 组件号 + 10000

    def cast_to_object(self):
        return self.obj.CastToObject()

    def cast_to_component(self):
        """
        将Object对象转换为具体的组件类对象，如果是文本、管道等非组件类对象，则原样返回

        :return:
        """
        组件号 = self.get_组件号()
        if 组件号 == -1:
            return self
        ebs_app = self.get_model().get_app()
        caster = ebs_app.object_caster
        result = caster.cast_to_component(组件号, self)  # 将当前组件转换为对应的组件类对象
        return result

    def change_name(self, new_name: str, allow_modify=True, check_only=False):
        new_name: str = self.obj.ChangeName(new_name, allow_modify, check_only)
        return new_name

    def exists(self):
        if self.obj is None:
            return False
        else:
            return True

    def get_values(self):
        """
        获取部件所有参数的名称、数值和单位

        :return:
        """
        data_obj = self.get_app().get_object_caster().cast_to_data(self)
        parameters = data_obj.EbsValues
        values = []
        for para in parameters:
            values.append((para.Name, para.Value, EbsUnits(para.Unit).name))
        return values

    def get_value(self, abbr: str, unit: EbsUnits = None):
        """
        获取指定参数的值

        :param abbr: 参数名称缩写
        :param unit: 参数的单位，默认为参数当前单位，如需其他单位，传入该参数即可
        :return:
        """
        data_obj = self.get_app().get_object_caster().cast_to_data(self)
        value = data_obj.EbsValues(abbr)
        if value is None:
            logger.warning(f"未知参数名：{self.get_name()}.{abbr}")
            return None
        if unit is None:
            unit = EbsUnits(value.GetUnitValue()[1].Unit)
        if type(unit) == str:
            unit = EbsUnits.str2unit(str(unit))
        value = value.GetValueInUnit(unit.value)
        return value

    def get_abbr_unit(self, abbr) -> EbsUnits:
        """
        获取参数的当前单位

        :param abbr:
        :return: 返回EbsUnits对象
        """
        data_obj = self.get_app().get_object_caster().cast_to_data(self)
        value = data_obj.EbsValues(abbr)
        return EbsUnits(value.GetUnitValue()[1].Unit)

    def set_value(self, abbr: str, value, unit: EbsUnits = None, save_flag=True):
        """
        设置指定参数的值

        :param abbr: 参数名，在Ebsilon中为缩写
        :param value: 参数树值
        :param unit: 默认使用参数现有的单位
        :param save_flag: 为真则设置参数值后保存模型
        :return:
        """
        data_obj = self.get_app().get_object_caster().cast_to_data(self)  # 将当前组件转换为数据对象
        try:
            para = data_obj.EbsValues(abbr)
        except AttributeError:
            logger.error(abbr)
            return
        if para is None:
            logger.warning(f"未知参数名：{self.get_name()}.{abbr}")
            return None
        if unit is None:
            unit = EbsUnits(para.GetUnitValue()[1].Unit)  # 该语句可以查看当前变量的单位

        if is_type(unit, "str"):
            try:
                unit = EbsUnits.str2unit(str(unit))
            except:
                logger.debug(f"未知的单位：{unit}，只设置{self.get_name()}.{abbr}数值，忽略单位")
                unit = EbsUnits(para.GetUnitValue()[1].Unit)  # 该语句可以查看当前变量的单位
        bret_val = para.SetValueInUnit(value, unit.value)
        if bret_val and save_flag:
            self.get_model().save()

        return bret_val


def is_type(obj, type_str: str):
    actual_type_str = str(type(obj)).replace("'>", "")
    if actual_type_str.endswith(type_str):
        return True
    else:
        return False
