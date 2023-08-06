query_before_group = '''select
rpms.SLAB_ID ИД_СЛЯБА,

decode(rpo.HOT_PUT, 'Y', 'HOT') ПР_ГП,

trunc(max(rpm.DISCHARGE)) Д_ПРОКАТА,

       rpo.ORDER_POSITION ПОЗИЦИЯ,
       rpo.HEAT ПЛАВКА,
       decode(nvl(rpo.EAF_TECHNOLOGY_CODE,0), 1, 'ДСП', 2, 'ГМП') ТИПТЕХЭСПЦ,
       decode(rpo.DEGASSING, 'Y', 'УВС') ПР_УВС,
       rpo.ROLLED_LOT_ID ПАРТИЯ,

       to_char(rpo.SHEET_NUM)||'-'||to_char(rpo.SHEET_NUM + rpo.SHEET_AMOUNT -1) ДИАП_ПАРТ,

       rpms.SLAB_NUM N_СЛЯБ,

       to_char(rpms.SHEET_NUM_1)||'-'||to_char(rpms.SHEET_NUM_1+rpo.CUT_AMOUNT-1) ДИАП_СЛЯБ,

       rpo.STEEL_GRADE МАРКА,
       rpo.STD_REQUIREMENTS ТЕХТРЕБ, --иной формат, чем в скинутых ими даннных
       rpo.STEEL_CODE К_МАРКИ,
       rpo.SLAB_THICKNESS H_СЛЯБ,
       rpo.SLAB_WIDTH B_СЛЯБ,
       rpo.SLAB_LENGTH L_СЛЯБ,
       rpo.SLAB_WEIGHT_COUNT/1000 ВЕС_СЛ,

       rpms.SLAB_WEIGHT/1000 ВЕСФ_СЛ,

       rpo.THICKNESS H_ЛИСТ,
       rpo.WIDTH B_ЛИСТ,
       rpo.LENGTH L_ЛИСТ,
       rpo.CUT_AMOUNT КРАТ,

       rpms.LENGTH_PART_1 Д_Н_1_ДЛ,
       rpms.LENGTH_PART_2 Д_Н_2_ДЛ,
       rpms.LENGTH_PART_3 Д_Н_3_ДЛ,
       rpms.FURNACE ПЕЧЬ_РЯД,
       to_char(rpms.FURNACE_IN_DT,'dd.mm.yyyy hh24:mi:ss') ЗАГР_ПЕЧЬ,
       to_char(rpms.FURNACE_OUT_DT,'dd.mm.yyyy hh24:mi:ss') ВЫГР_ПЕЧЬ,
       trunc(rpms.FURNACE_HEAT_DURATION/60)||':'||(rpms.FURNACE_HEAT_DURATION-60*trunc(rpms.FURNACE_HEAT_DURATION/60)) ДЛИТ_ПЕЧЬ,

       rtl.FURNACE_HEAT_TEMPERATURE ПЛ_Т_ПЕЧЬ,

       rpms.FURNACE_HEAT_TEMPERATURE ФК_Т_ПЕЧЬ,

max(rpm.ROLLINGPROGRAM) СХЕМА_ПРОК,

       rpms.DUO_PASS_AMOUNT ДУО_ПРОХ,


sum(decode(substr(rpm.STAFF,1,1),'Q',0,decode(rpm.PASSTYPE,'Idle',1))) ДУО_ХОЛОСТ,
sum(decode(rpm.DESCALINGS1,'ON',1)) ГИДРОСБИВ,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 1,rpm.REDUCTION))) ДУО_ОБЖ_01,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 2,rpm.REDUCTION))) ДУО_ОБЖ_02,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 3,rpm.REDUCTION))) ДУО_ОБЖ_03,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 4,rpm.REDUCTION))) ДУО_ОБЖ_04,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 5,rpm.REDUCTION))) ДУО_ОБЖ_05,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 6,rpm.REDUCTION))) ДУО_ОБЖ_06,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 7,rpm.REDUCTION))) ДУО_ОБЖ_07,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 8,rpm.REDUCTION))) ДУО_ОБЖ_08,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 9,rpm.REDUCTION))) ДУО_ОБЖ_09,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,10,rpm.REDUCTION))) ДУО_ОБЖ_10,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,11,rpm.REDUCTION))) ДУО_ОБЖ_11,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,12,rpm.REDUCTION))) ДУО_ОБЖ_12,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,13,rpm.REDUCTION))) ДУО_ОБЖ_13,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,14,rpm.REDUCTION))) ДУО_ОБЖ_14,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,15,rpm.REDUCTION))) ДУО_ОБЖ_15,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 1,rpm.STANDFORCE))) ДУО_УСС_01,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 2,rpm.STANDFORCE))) ДУО_УСС_02,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 3,rpm.STANDFORCE))) ДУО_УСС_03,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 4,rpm.STANDFORCE))) ДУО_УСС_04,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 5,rpm.STANDFORCE))) ДУО_УСС_05,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 6,rpm.STANDFORCE))) ДУО_УСС_06,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 7,rpm.STANDFORCE))) ДУО_УСС_07,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 8,rpm.STANDFORCE))) ДУО_УСС_08,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 9,rpm.STANDFORCE))) ДУО_УСС_09,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,10,rpm.STANDFORCE))) ДУО_УСС_10,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,11,rpm.STANDFORCE))) ДУО_УСС_11,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,12,rpm.STANDFORCE))) ДУО_УСС_12,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,13,rpm.STANDFORCE))) ДУО_УСС_13,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,14,rpm.STANDFORCE))) ДУО_УСС_14,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,15,rpm.STANDFORCE))) ДУО_УСС_15,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 1,rpm.FORCEMA))) ДУО_УСП_01,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 2,rpm.FORCEMA))) ДУО_УСП_02,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 3,rpm.FORCEMA))) ДУО_УСП_03,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 4,rpm.FORCEMA))) ДУО_УСП_04,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 5,rpm.FORCEMA))) ДУО_УСП_05,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 6,rpm.FORCEMA))) ДУО_УСП_06,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 7,rpm.FORCEMA))) ДУО_УСП_07,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 8,rpm.FORCEMA))) ДУО_УСП_08,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 9,rpm.FORCEMA))) ДУО_УСП_09,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,10,rpm.FORCEMA))) ДУО_УСП_10,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,11,rpm.FORCEMA))) ДУО_УСП_11,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,12,rpm.FORCEMA))) ДУО_УСП_12,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,13,rpm.FORCEMA))) ДУО_УСП_13,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,14,rpm.FORCEMA))) ДУО_УСП_14,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,15,rpm.FORCEMA))) ДУО_УСП_15,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 1,rpm.TOPSPEED))) ДУО_СКР_01,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 2,rpm.TOPSPEED))) ДУО_СКР_02,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 3,rpm.TOPSPEED))) ДУО_СКР_03,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 4,rpm.TOPSPEED))) ДУО_СКР_04,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 5,rpm.TOPSPEED))) ДУО_СКР_05,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 6,rpm.TOPSPEED))) ДУО_СКР_06,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 7,rpm.TOPSPEED))) ДУО_СКР_07,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 8,rpm.TOPSPEED))) ДУО_СКР_08,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 9,rpm.TOPSPEED))) ДУО_СКР_09,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,10,rpm.TOPSPEED))) ДУО_СКР_10,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,11,rpm.TOPSPEED))) ДУО_СКР_11,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,12,rpm.TOPSPEED))) ДУО_СКР_12,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,13,rpm.TOPSPEED))) ДУО_СКР_13,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,14,rpm.TOPSPEED))) ДУО_СКР_14,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER,15,rpm.TOPSPEED))) ДУО_СКР_15,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(rpm.PASSNUMBER, 3,rpm.LSTEMP))) ДУО_Т_3_ПР,
decode( sum(decode(substr(rpm.STAFF,1,1),'Q',0,decode(rpm.PASSTYPE,'Idle',1))),1,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(substr(rpm.STAFF,-1,1),'T',rpm.FSTEMP))),
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(substr(rpm.STAFF,-1,1),'T',rpm.LSTEMP))) ) ДУО_Т_ПОСЛ,

       rpms.INTERCELL_COOLING УМО,
       rpms.SHEET_ROLL ПОДКАТ,

max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 1,rpm.REDUCTION))) КВР_ОБЖ_01,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.REDUCTION))) КВР_ОБЖ_02,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.REDUCTION))) КВР_ОБЖ_03,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.REDUCTION))) КВР_ОБЖ_04,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.REDUCTION))) КВР_ОБЖ_05,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.REDUCTION))) КВР_ОБЖ_06,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.REDUCTION))) КВР_ОБЖ_07,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.REDUCTION))) КВР_ОБЖ_08,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.REDUCTION))) КВР_ОБЖ_09,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.REDUCTION))) КВР_ОБЖ_10,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.REDUCTION))) КВР_ОБЖ_11,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.REDUCTION))) КВР_ОБЖ_12,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.REDUCTION))) КВР_ОБЖ_13,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.REDUCTION))) КВР_ОБЖ_14,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,15,rpm.REDUCTION))) КВР_ОБЖ_15,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 1,rpm.STANDFORCE))) КВР_УСС_01,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.STANDFORCE))) КВР_УСС_02,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.STANDFORCE))) КВР_УСС_03,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.STANDFORCE))) КВР_УСС_04,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.STANDFORCE))) КВР_УСС_05,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.STANDFORCE))) КВР_УСС_06,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.STANDFORCE))) КВР_УСС_07,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.STANDFORCE))) КВР_УСС_08,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.STANDFORCE))) КВР_УСС_09,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.STANDFORCE))) КВР_УСС_10,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.STANDFORCE))) КВР_УСС_11,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.STANDFORCE))) КВР_УСС_12,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.STANDFORCE))) КВР_УСС_13,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.STANDFORCE))) КВР_УСС_14,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,15,rpm.STANDFORCE))) КВР_УСС_15,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 1,rpm.FORCEMA))) КВР_УСП_01,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.FORCEMA))) КВР_УСП_02,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.FORCEMA))) КВР_УСП_03,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.FORCEMA))) КВР_УСП_04,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.FORCEMA))) КВР_УСП_05,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.FORCEMA))) КВР_УСП_06,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.FORCEMA))) КВР_УСП_07,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.FORCEMA))) КВР_УСП_08,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.FORCEMA))) КВР_УСП_09,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.FORCEMA))) КВР_УСП_10,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.FORCEMA))) КВР_УСП_11,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.FORCEMA))) КВР_УСП_12,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.FORCEMA))) КВР_УСП_13,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.FORCEMA))) КВР_УСП_14,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,15,rpm.FORCEMA))) КВР_УСП_15,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 1,rpm.TOPSPEED))) КВР_СКР_01,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.TOPSPEED))) КВР_СКР_02,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.TOPSPEED))) КВР_СКР_03,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.TOPSPEED))) КВР_СКР_04,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.TOPSPEED))) КВР_СКР_05,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.TOPSPEED))) КВР_СКР_06,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.TOPSPEED))) КВР_СКР_07,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.TOPSPEED))) КВР_СКР_08,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.TOPSPEED))) КВР_СКР_09,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.TOPSPEED))) КВР_СКР_10,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.TOPSPEED))) КВР_СКР_11,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.TOPSPEED))) КВР_СКР_12,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.TOPSPEED))) КВР_СКР_13,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.TOPSPEED))) КВР_СКР_14,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,15,rpm.TOPSPEED))) КВР_СКР_15,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 1,rpm.FORCEEND))) delta1_2,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 2,rpm.FORCEEND))) delta2_3,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 3,rpm.FORCEEND))) delta3_4,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 4,rpm.FORCEEND))) delta4_5,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 5,rpm.FORCEEND))) delta5_6,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 6,rpm.FORCEEND))) delta6_7,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 7,rpm.FORCEEND))) delta7_8,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 8,rpm.FORCEEND))) delta8_9,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT, 9,rpm.FORCEEND))) delta9_10,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,10,rpm.FORCEEND))) delta10_11,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,11,rpm.FORCEEND))) delta11_12,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,12,rpm.FORCEEND))) delta12_13,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,13,rpm.FORCEEND))) delta13_14,
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,15,rpm.FORCESTART)))-
max(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSNUMBER-rpms.DUO_PASS_AMOUNT,14,rpm.FORCEEND))) delta14_15,

       rtl.QUARTO_TEMPERATURE_OUT КВР_Т_ПЛАН,

max(decode(rpm.STAFF,'Q1',rpm.FSTEMP)) КВР_Т_1_ПР,
max(rpm.S2START) s2_start,

       rpms.QUARTO_TEMPERATURE КВР_Т_ПОСЛ,


max(rpm.PLATETEMPBIAS) ВМЕШ_ТЕМП,

       rpms.QUARTO_PASS_AMOUNT КВР_ПРОХ,

sum(decode(substr(rpm.STAFF,1,1),'Q',decode(rpm.PASSTYPE,'Idle',1))) КВР_ХОЛОСТ,

       rtl.COOLING_STRATEGY УКО_СТРАТ,
       rtl.COOLING_TEMPERATURE_OUT УКО_Т_ПЛАН,
       rtl.COOLING_INTENSITY УКО_И_ПЛАН,

to_char(max(rpm.DISCHARGE),'dd.mm.yyyy hh24:mi:ss')  НАЧ_ПРОКАТ,
max(decode(substr(rpm.STAFF,1,2),'H1',rpm.FORCESTART,'L1',rpm.FORCESTART)) ПЕЧЬ_ДУО,
max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(substr(rpm.STAFF,2,1),'N',rpm.FORCEEND))) - max(decode(substr(rpm.STAFF,1,2),'H1',rpm.FORCESTART,'L1',rpm.FORCESTART)) ДУО_ВРЕМЯ,
max(decode(substr(rpm.STAFF,1,2),'Q1',rpm.FORCESTART)) - max(decode(substr(rpm.STAFF,1,1),'Q',to_number(null),decode(substr(rpm.STAFF,2,1),'N',rpm.FORCEEND))) ДУО_КВР,
max(decode(rpm.STAFF,'QN',rpm.FORCEEND,'QNT',rpm.FORCEEND))- max(decode(substr(rpm.STAFF,1,2),'Q1',rpm.FORCESTART)) КВР_ВРЕМЯ,
to_char(max(rpm.COMPLETION),'dd.mm.yyyy hh24:mi:ss')  КОН_ПРОКАТ,
--count(*) over(order by max(rpm.COMPLETION) range between numtodsinterval(nvl(max(rpm.COMPLETION),sysdate)-nvl(max(rpm.DISCHARGE),sysdate),'day') preceding and current row) КОЛ_СЛ_НАЧ,
--count(*) over(order by nvl(max(rpm.DISCHARGE),rpms.FURNACE_OUT_DT)  range between current row and numtodsinterval(nvl(max(rpm.COMPLETION),sysdate)-nvl(max(rpm.DISCHARGE),sysdate),'day') following) КОЛ_СЛ_КОН,


       rpms.VIOLATION_CODE КОД_ОШИБКИ,
       rpms.TEXT_VIOLATION КОД_ЦЛК,

       rhc.CEV УГЛ_ЭКВ,
       rhc.CHEM_COMPOS_COEFF КХС,
       rhc.ELEMENT_C c,
       rhc.ELEMENT_SI si,
       rhc.ELEMENT_MN mn,
       rhc.ELEMENT_P p,
       rhc.ELEMENT_S s,
       rhc.ELEMENT_CR cr,
       rhc.ELEMENT_NI ni,
       rhc.ELEMENT_CU cu,
       rhc.ELEMENT_TI ti,
       rhc.ELEMENT_AL al,
       rhc.ELEMENT_N n2,
       rhc.ELEMENT_NB nb,
       rhc.ELEMENT_V v,
       rhc.ELEMENT_B b,
       rhc.ELEMENT_MO mo,

       decode(rpo.ASSIGN_STOWING, 'Y', 1, 'N', 0) СТОППИР, -- не соответствует кодам в файле 2019-2021.csv
       rtmr.ROLLED_LOT_ID NOMP,
       rtmr.HEAT_TREATMENT_CODE VTR,
       rtmr.SHEET_NUM NISP,
       rtmr.EQUIPMENT_TEST_CODE ISP_OB,
       rtmr.YIELD_STRENGTH FPT,
       rtmr.TENSILE_STRENGTH FVS,
       rtmr.ELOGATION FOYD,
       --rtmr.YIELD_TO_TENSILE_STRENGTH,
       rtmr.REDUCTION_OF_AREA FOS,
       rtmr.YIELD_STR_COMPLETE FPTP,
       rtmr.TENSILE_STRENGTH_ALONG FVSP,
       rtmr.ELOGATION_ALONG FOYDP,
       rtmr.UNIFROM_ELOGATION_ALONG FYDR,
       rtmr.SAMPLE_TYPE_KCU TUV1,
       rtmr.KCU_TEMPERATURE T_KCU,
       rtmr.IMPACT_STRENGTH_KCU_1 FUV_1,
       rtmr.IMPACT_STRENGTH_KCU_2 FUV_2,
       rtmr.IMPACT_STRENGTH_KCU_3 FUV_3,
       rtmr.SAMPLE_TYPE_KCV TUV2,
       rtmr.KCV_TEMPERATURE T_KCV,
       rtmr.IMPACT_STRENGTH_KCV_1 FDV_1,
       rtmr.IMPACT_STRENGTH_KCV_2 FDV_2,
       rtmr.IMPACT_STRENGTH_KCV_3 FDV_3,
       rtmr.DWTT_TEMPERATURE T_KCD,
       rtmr.DWTT_1 DWTT1,
       rtmr.DWTT_2 DWTT2,
       rtmr.KV_KCV_TEMPERATURE T_KCDV,
       rtmr.VISCOUS_COMPONENT_1 DVC1,
       rtmr.VISCOUS_COMPONENT_2 DVC2,
       rtmr.VISCOUS_COMPONENT_3 DVC3,
       rtmr.HARDNESS_1 NB1,
       rtmr.HARDNESS_2 NB2,
       rtmr.PARAMETER_OVERSTEPPING VPN,
       rtmr.PARAMETER_OVERSHOOT VPV,
       rtmr.YIELD_STR_PLASTIC_05 FPT05,
       rtmr.YIELD_STR_COMPLETE_05 FPTP05,
       rtmr.IMPACT_STR_FAILURE_1 PRVLU,
       rtmr.IMPACT_STR_FAILURE_2 PRVLV,
       rtmr.VISCOUS_COMPONENT_FAILURE PRVVC,
       rtmr.DWTT_FAILURE PRLDW

from ROLL_REPORT_MILL_SHORT rpms

left outer join ROLL_REPORT_MILL rpm
on rpms.SLAB_ID = rpm.SLAB_ID

left outer join ROLL_TASK_LEVEL3 rtl
on rpms.REPORT_ORDER_ID= rtl.REPORT_ORDER_ID

inner join ROLL_REPORT_ORDER rpo
on rpms.REPORT_ORDER_ID = rpo.REPORT_ORDER_ID

inner join ROLL_TEST_MECHANIC_RESULT rtmr
on rtmr.HEAT = rpo.HEAT

left outer join ROLL_HEAT_CHEMISTRY rhc
on (rpo.HEAT= rhc.HEAT and rpo.STD_REQUIREMENTS= rhc.STD_REQUIREMENTS)

where
rtmr.SHEET_NUM between rpms.SHEET_NUM_1 and rpms.SHEET_NUM_1+rpo.CUT_AMOUNT-1
\t
'''

def add_where_for_last_months(month: int):
       return f' and rpm.DISCHARGE BETWEEN ADD_MONTHS(SYSDATE,-{month}) AND SYSDATE '

query_with_group = '''\t
group by
rpms.REPORT_ORDER_ID,
rpms.SLAB_ID,

rpo.HOT_PUT,

rpms.SLAB_NUM,

rpo.ROLLING_DT, rpo.ORDER_NUM, rpo.ORDER_POSITION, rpo.HEAT,
rpo.EAF_TECHNOLOGY_CODE, rpo.DEGASSING, rpo.ROLLED_LOT_ID, rpo.SHEET_NUM,

rpms.SHEET_NUM_1,

rpo.SHEET_AMOUNT,
rpo.STEEL_GRADE, rpo.STEEL_CODE,
rpo.STD_REQUIREMENTS, rpo.THICKNESS, rpo.WIDTH,
rpo.LENGTH, rpo.SLAB_THICKNESS, rpo.SLAB_WIDTH, rpo.SLAB_LENGTH,
rpo.SLAB_WEIGHT_COUNT,

rpms.SLAB_WEIGHT,

rpo.CUT_AMOUNT, rpo.WEIGHT_SHEET_COUNT, rpo.ASSIGN_STOWING,

rpms.LENGTH_PART_1, rpms.LENGTH_PART_2, rpms.LENGTH_PART_3,
rpms.FURNACE, rpms.FURNACE_IN_DT,
rpms.FURNACE_OUT_DT,
rpms.FURNACE_HEAT_DURATION,

rtl.FURNACE_HEAT_TEMPERATURE,

rpms.FURNACE_HEAT_TEMPERATURE, rpms.DUO_PASS_AMOUNT,
rpms.INTERCELL_COOLING,

rtl.QUARTO_TEMPERATURE_OUT,

rpms.QUARTO_TEMPERATURE,
rpms.SHEET_ROLL,
rpms.QUARTO_PASS_AMOUNT,

rtl.COOLING_STRATEGY,
rtl.COOLING_TEMPERATURE_OUT,
rtl.COOLING_INTENSITY,

rpms.VIOLATION_CODE, rpms.TEXT_VIOLATION,

rtl.FURNACE_HEAT_TEMPERATURE,
rtl.QUARTO_TEMPERATURE_OUT, rtl.COOLING_STRATEGY, rtl.COOLING_TEMPERATURE_OUT,
rtl.COOLING_INTENSITY,

rhc.CEV,
rhc.CHEM_COMPOS_COEFF,
rhc.ELEMENT_C,
rhc.ELEMENT_SI,
rhc.ELEMENT_MN,
rhc.ELEMENT_P,
rhc.ELEMENT_S,
rhc.ELEMENT_CR,
rhc.ELEMENT_NI,
rhc.ELEMENT_CU,
rhc.ELEMENT_TI,
rhc.ELEMENT_AL,
rhc.ELEMENT_N,
rhc.ELEMENT_NB,
rhc.ELEMENT_V,
rhc.ELEMENT_B,
rhc.ELEMENT_MO,

--n.udo??

rtmr.ROLLED_LOT_ID, --nomp
rtmr.HEAT_TREATMENT_CODE, --vtr
rtmr.SHEET_NUM, --nisp
rtmr.EQUIPMENT_TEST_CODE, --isp_ob

rtmr.YIELD_STRENGTH,
rtmr.TENSILE_STRENGTH,
rtmr.ELOGATION,

rtmr.REDUCTION_OF_AREA,
rtmr.YIELD_STR_COMPLETE,
rtmr.TENSILE_STRENGTH_ALONG,
rtmr.ELOGATION_ALONG,
rtmr.UNIFROM_ELOGATION_ALONG,

rtmr.SAMPLE_TYPE_KCU,
rtmr.KCU_TEMPERATURE,
rtmr.IMPACT_STRENGTH_KCU_1,
rtmr.IMPACT_STRENGTH_KCU_2,
rtmr.IMPACT_STRENGTH_KCU_3,

rtmr.SAMPLE_TYPE_KCV,
rtmr.KCV_TEMPERATURE,
rtmr.IMPACT_STRENGTH_KCV_1,
rtmr.IMPACT_STRENGTH_KCV_2,
rtmr.IMPACT_STRENGTH_KCV_3,

rtmr.DWTT_TEMPERATURE, rtmr.DWTT_1, rtmr.DWTT_2,

rtmr.KV_KCV_TEMPERATURE, rtmr.VISCOUS_COMPONENT_1, rtmr.VISCOUS_COMPONENT_2,
rtmr.VISCOUS_COMPONENT_3,

rtmr.HARDNESS_1, rtmr.HARDNESS_2,
rtmr.PARAMETER_OVERSTEPPING, rtmr.PARAMETER_OVERSHOOT,
rtmr.YIELD_STR_PLASTIC_05, rtmr.YIELD_STR_COMPLETE_05,
rtmr.IMPACT_STR_FAILURE_1, rtmr.IMPACT_STR_FAILURE_2,
rtmr.VISCOUS_COMPONENT_FAILURE, rtmr.DWTT_FAILURE
'''
