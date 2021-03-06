# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaogangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    count = scrapy.Field()
    grabtime = scrapy.Field()
    ranking = scrapy.Field()
    category = scrapy.Field()
    tag = scrapy.Field()
    model = scrapy.Field()


class NewsItem(scrapy.Item):
    brand = scrapy.Field()
    series = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    postd_date = scrapy.Field()
    view_num = scrapy.Field()
    reply_num = scrapy.Field()
    label = scrapy.Field()
    data_source = scrapy.Field()
    grabtime = scrapy.Field()


class FeijiuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    kind = scrapy.Field()
    label_one = scrapy.Field()
    label_two = scrapy.Field()
    title = scrapy.Field()
    infoNum = scrapy.Field()
    type = scrapy.Field()
    quality = scrapy.Field()
    number = scrapy.Field()
    sale_price = scrapy.Field()
    public_time = scrapy.Field()
    market = scrapy.Field()
    comType = scrapy.Field()
    comTrade = scrapy.Field()
    comProducts = scrapy.Field()
    comIndex = scrapy.Field()
    linkMan = scrapy.Field()
    comName = scrapy.Field()
    comAddress = scrapy.Field()
    comPhone = scrapy.Field()
    mobile = scrapy.Field()
    grabtime = scrapy.Field()
    isvip = scrapy.Field()
    list_url = scrapy.Field()
    vip_type = scrapy.Field()
    area_auth = scrapy.Field()
    info = scrapy.Field()
    debao_auth = scrapy.Field()
    vip_year = scrapy.Field()


class OuyeelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    url = scrapy.Field()
    shop_name = scrapy.Field()
    shop_code = scrapy.Field()
    jj_status = scrapy.Field()
    data_num = scrapy.Field()
    page_num = scrapy.Field()
    data_url = scrapy.Field()
    grabtime = scrapy.Field()
    jj_num = scrapy.Field()
    jj_page_num = scrapy.Field()
    gp_status = scrapy.Field()
    gp_page_num = scrapy.Field()


class OuyeelDetailItem(scrapy.Item):
    canCompensateFlag = scrapy.Field()
    flag_yinpiao = scrapy.Field()
    pack_comments2 = scrapy.Field()
    quality_grade = scrapy.Field()
    active_date = scrapy.Field()
    cangfeikuaijie = scrapy.Field()
    video_inspection_flag = scrapy.Field()
    show_tel = scrapy.Field()
    depositAmt = scrapy.Field()
    balanceQuantity = scrapy.Field()
    warehouse_score = scrapy.Field()
    surfaceDispose = scrapy.Field()
    packCode = scrapy.Field()
    manufacture_date = scrapy.Field()
    price = scrapy.Field()
    bid_status = scrapy.Field()
    weightMethod = scrapy.Field()
    pack_code = scrapy.Field()
    pack_comments = scrapy.Field()
    morgage_type = scrapy.Field()
    id = scrapy.Field()
    is_in_cart = scrapy.Field()
    out_fee = scrapy.Field()
    merge_grade = scrapy.Field()
    balance_quantity = scrapy.Field()
    warehouse_name = scrapy.Field()
    manufactureName = scrapy.Field()
    coating_type = scrapy.Field()
    quickInvoicingFlag = scrapy.Field()
    shopType = scrapy.Field()
    estimate_unit_price = scrapy.Field()
    productTypeCode = scrapy.Field()
    claddingZnLayer = scrapy.Field()
    shop_sign2 = scrapy.Field()
    warehouse_code = scrapy.Field()
    estimate_price = scrapy.Field()
    jewel_status = scrapy.Field()
    production_date = scrapy.Field()
    packType = scrapy.Field()
    paintType = scrapy.Field()
    product_code = scrapy.Field()
    can_bargaining = scrapy.Field()
    manufacturer = scrapy.Field()
    spec3 = scrapy.Field()
    pieces = scrapy.Field()
    sort_score = scrapy.Field()
    provider_name = scrapy.Field()
    spec1 = scrapy.Field()
    storate_rate = scrapy.Field()
    is_quickly_delivery = scrapy.Field()
    contact_name = scrapy.Field()
    daiyunbutie = scrapy.Field()
    putin_date = scrapy.Field()
    star = scrapy.Field()
    res_status = scrapy.Field()
    splitable = scrapy.Field()
    factory_send = scrapy.Field()
    packingTypeName = scrapy.Field()
    flag_rongzi = scrapy.Field()
    prodCat = scrapy.Field()
    flag_youhuiquan = scrapy.Field()
    balance_weight = scrapy.Field()
    penaltyAmt = scrapy.Field()
    qualityType = scrapy.Field()
    surfaceQuality = scrapy.Field()
    providerCode = scrapy.Field()
    contact_phone = scrapy.Field()
    store_city_name = scrapy.Field()
    shopLogoUrl = scrapy.Field()
    coatingType = scrapy.Field()
    toShopUrl = scrapy.Field()
    is_subsidy = scrapy.Field()
    spec = scrapy.Field()
    flag_manlijian = scrapy.Field()
    flag_redeem = scrapy.Field()
    productTypeName = scrapy.Field()
    sales_mode = scrapy.Field()
    allow_buy = scrapy.Field()
    shopLevel = scrapy.Field()
    resource_type = scrapy.Field()
    weight = scrapy.Field()
    product_name = scrapy.Field()
    houjiesuan = scrapy.Field()
    rongzizhifu = scrapy.Field()
    packComment1 = scrapy.Field()
    close_status = scrapy.Field()
    color = scrapy.Field()
    is_weighed = scrapy.Field()
    baoyou = scrapy.Field()
    shopName = scrapy.Field()
    negativeRange = scrapy.Field()
    storate_freedays = scrapy.Field()
    salesMethod = scrapy.Field()
    edgeMorphology = scrapy.Field()
    has_zhibaoshu = scrapy.Field()
    surfaceStructure = scrapy.Field()
    penaltyAmtRate = scrapy.Field()
    factory_res_code = scrapy.Field()
    store_city_code = scrapy.Field()
    invoiceFromNameList = scrapy.Field()
    factoryResCode = scrapy.Field()
    has_pic = scrapy.Field()
    special = scrapy.Field()
    pack_type = scrapy.Field()
    storage_site = scrapy.Field()
    flag_dingjin = scrapy.Field()
    location = scrapy.Field()
    unit_weight = scrapy.Field()
    shop_sign = scrapy.Field()
    gongfangdaiyun = scrapy.Field()
    # add------------------------------------
    partiNum = scrapy.Field()
    bidEndTime = scrapy.Field()
    _id = scrapy.Field()
    grabtime = scrapy.Field()
    isAddBid = scrapy.Field()
    currentDateTime = scrapy.Field()
    firstPriceIncrement = scrapy.Field()
    stdIncrement = scrapy.Field()
    bidResult = scrapy.Field()
    bidBeginTime = scrapy.Field()
    partiStatus = scrapy.Field()
    bidWinFlag = scrapy.Field()
    startingPrice = scrapy.Field()
    isDelayAllowed = scrapy.Field()
    bidDate = scrapy.Field()
    remark = scrapy.Field()
    auctionCode = scrapy.Field()
    bidSection = scrapy.Field()
    auctionId = scrapy.Field()
    auctionType = scrapy.Field()
    

    # list---------------------------------------

    # flag_yinpiao = scrapy.Field()
    # contact_phone = scrapy.Field()
    # store_city_name = scrapy.Field()
    # active_date = scrapy.Field()
    # cangfeikuaijie = scrapy.Field()
    # show_tel = scrapy.Field()
    # is_subsidy = scrapy.Field()
    # spec = scrapy.Field()
    buyerFlag = scrapy.Field()
    # flag_manlijian = scrapy.Field()
    flag_targeting_resources = scrapy.Field()
    # price = scrapy.Field()
    # bid_status = scrapy.Field()
    # flag_redeem = scrapy.Field()
    # pack_code = scrapy.Field()
    # id = scrapy.Field()
    # is_in_cart = scrapy.Field()
    # sales_mode = scrapy.Field()
    # allow_buy = scrapy.Field()
    flag_gongyinglian = scrapy.Field()
    # resource_type = scrapy.Field()
    # weight = scrapy.Field()
    # product_name = scrapy.Field()
    # balance_quantity = scrapy.Field()
    # warehouse_name = scrapy.Field()
    # houjiesuan = scrapy.Field()
    # rongzizhifu = scrapy.Field()
    sales_method = scrapy.Field()
    provider_code = scrapy.Field()
    # estimate_unit_price = scrapy.Field()
    # warehouse_code = scrapy.Field()
    # jewel_status = scrapy.Field()
    # estimate_price = scrapy.Field()
    # baoyou = scrapy.Field()
    # can_bargaining = scrapy.Field()
    # manufacturer = scrapy.Field()
    abholung = scrapy.Field()
    # has_zhibaoshu = scrapy.Field()
    flag_new_resources = scrapy.Field()
    # provider_name = scrapy.Field()
    flag_zhibaoshu = scrapy.Field()
    # is_quickly_delivery = scrapy.Field()
    # contact_name = scrapy.Field()
    # store_city_code = scrapy.Field()
    # daiyunbutie = scrapy.Field()
    # res_status = scrapy.Field()
    # has_pic = scrapy.Field()
    # splitable = scrapy.Field()
    promise_time = scrapy.Field()
    # factory_send = scrapy.Field()
    # flag_rongzi = scrapy.Field()
    # flag_youhuiquan = scrapy.Field()
    # pack_type = scrapy.Field()
    # flag_dingjin = scrapy.Field()
    shop_type = scrapy.Field()
    # balance_weight = scrapy.Field()
    # unit_weight = scrapy.Field()
    # shop_sign = scrapy.Field()
    # gongfangdaiyun = scrapy.Field()
    # add ---------------------------
    # assume = scrapy.Field()


class XingzhengItem(scrapy.Item):
    shiji = scrapy.Field()
    zhudi = scrapy.Field()
    people = scrapy.Field()
    area = scrapy.Field()
    xz_code = scrapy.Field()
    area_code = scrapy.Field()
    postal_code = scrapy.Field()
    grabtime = scrapy.Field()
    parent = scrapy.Field()
    shengji = scrapy.Field()
    diji = scrapy.Field()
    xianji = scrapy.Field()
    xingzheng_level = scrapy.Field()
    area_type = scrapy.Field()



class YicheKoubeiItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    status = scrapy.Field()
    grabtime = scrapy.Field()
    u_carinfo = scrapy.Field()
    carinfo = scrapy.Field()
    userinfo = scrapy.Field()
    familyname = scrapy.Field()
    familynameid = scrapy.Field()
    shortdesc = scrapy.Field()
    guideprice = scrapy.Field()
    usage = scrapy.Field()
    fuel = scrapy.Field()
    buy_date = scrapy.Field()
    buy_location = scrapy.Field()
    buy_pure_price = scrapy.Field()
    buyerid = scrapy.Field()
    buyername = scrapy.Field()
    comment_detail = scrapy.Field()
    comment_people = scrapy.Field()
    isGoodComment = scrapy.Field()
    mileage = scrapy.Field()
    oil_consume = scrapy.Field()
    picurl = scrapy.Field()
    score = scrapy.Field()
    score_star = scrapy.Field()
    score_appearance = scrapy.Field()
    score_appearance_compare = scrapy.Field()
    score_comfort = scrapy.Field()
    score_comfort_compare = scrapy.Field()
    score_control = scrapy.Field()
    score_control_compare = scrapy.Field()
    score_cost = scrapy.Field()
    score_cost_compare = scrapy.Field()
    score_fuel = scrapy.Field()
    score_fuel_compare = scrapy.Field()
    score_power = scrapy.Field()
    score_power_compare = scrapy.Field()
    score_space = scrapy.Field()
    score_space_compare = scrapy.Field()
    score_trim = scrapy.Field()
    score_trim_compare = scrapy.Field()

    # ucid = scrapy.Field()
    brand = scrapy.Field()
    satisfied = scrapy.Field()
    unsatisfied = scrapy.Field()

    visitCount = scrapy.Field()
    helpfulCount = scrapy.Field()
    commentCount = scrapy.Field()
    post_time = scrapy.Field()
    spec_id = scrapy.Field()

    description = scrapy.Field()
    # urlspell = scrapy.Field()
    score_comfor = scrapy.Field()
    serise = scrapy.Field()
    tag_list = scrapy.Field()
    like_series = scrapy.Field()
    model = scrapy.Field()
    tag = scrapy.Field()
    ranking = scrapy.Field()
    create_time = scrapy.Field()
    total_score = scrapy.Field()
    space = scrapy.Field()
    power = scrapy.Field()
    manipulation = scrapy.Field()
    fuel_consumption = scrapy.Field()
    comfortability = scrapy.Field()
    appearance = scrapy.Field()
    bitauto_car_score = scrapy.Field()
    interior_trim = scrapy.Field()
    series_score = scrapy.Field()
    serise_id = scrapy.Field()


