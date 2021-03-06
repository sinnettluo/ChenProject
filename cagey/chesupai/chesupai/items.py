# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChesupaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class chesupaiItem(scrapy.Item):
    id = scrapy.Field()
    carid = scrapy.Field()
    car_source = scrapy.Field()
    grab_time = scrapy.Field()
    update_time = scrapy.Field()
    post_time = scrapy.Field()
    sold_date = scrapy.Field()
    pagetime = scrapy.Field()
    parsetime = scrapy.Field()
    shortdesc = scrapy.Field()
    pagetitle = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()
    statusplus = scrapy.Field()
    newcarid = scrapy.Field()
    brand = scrapy.Field()
    series = scrapy.Field()
    factoryname = scrapy.Field()
    modelname = scrapy.Field()
    brandid = scrapy.Field()
    familyid = scrapy.Field()
    seriesid = scrapy.Field()
    makeyear = scrapy.Field()
    registeryear = scrapy.Field()
    produceyear = scrapy.Field()
    bodystyle = scrapy.Field()
    level = scrapy.Field()
    fueltype = scrapy.Field()
    dirveray = scrapy.Field()
    body = scrapy.Field()
    output = scrapy.Field()
    guideprice = scrapy.Field()
    guidepricetax = scrapy.Field()
    doors = scrapy.Field()
    emission = scrapy.Field()
    gear = scrapy.Field()
    geartype = scrapy.Field()
    seats = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    gearnumber = scrapy.Field()
    wheelbase = scrapy.Field()
    generation = scrapy.Field()
    fuelnumber = scrapy.Field()
    lwv = scrapy.Field()
    lwvnumber = scrapy.Field()
    maxnm = scrapy.Field()
    maxpower = scrapy.Field()
    maxps = scrapy.Field()
    frontgauge = scrapy.Field()
    compress = scrapy.Field()
    registerdate = scrapy.Field()
    years = scrapy.Field()
    paytype = scrapy.Field()
    price1 = scrapy.Field()
    pricetag = scrapy.Field()
    mileage = scrapy.Field()
    usage = scrapy.Field()
    color = scrapy.Field()
    city = scrapy.Field()
    prov = scrapy.Field()
    guarantee = scrapy.Field()
    totalcheck_desc = scrapy.Field()
    totalgrade = scrapy.Field()
    contact_type = scrapy.Field()
    contact_name = scrapy.Field()
    contact_phone = scrapy.Field()
    contact_address = scrapy.Field()
    contact_company = scrapy.Field()
    contact_url = scrapy.Field()
    change_date = scrapy.Field()
    change_times = scrapy.Field()
    insurance1_date = scrapy.Field()
    insurance2_date = scrapy.Field()
    hascheck = scrapy.Field()
    repairinfo = scrapy.Field()
    yearchecktime = scrapy.Field()
    carokcf = scrapy.Field()
    carcard = scrapy.Field()
    carinvoice = scrapy.Field()
    accident_desc = scrapy.Field()
    accident_score = scrapy.Field()
    outer_desc = scrapy.Field()
    outer_score = scrapy.Field()
    inner_desc = scrapy.Field()
    inner_score = scrapy.Field()
    safe_desc = scrapy.Field()
    safe_score = scrapy.Field()
    road_desc = scrapy.Field()
    road_score = scrapy.Field()
    lastposttime = scrapy.Field()
    newcartitle = scrapy.Field()
    newcarurl = scrapy.Field()
    img_url = scrapy.Field()
    first_owner = scrapy.Field()
    carno = scrapy.Field()
    carnotype = scrapy.Field()
    carddate = scrapy.Field()
    changecolor = scrapy.Field()
    outcolor = scrapy.Field()
    innercolor = scrapy.Field()
    desc = scrapy.Field()
