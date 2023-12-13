#!/usr/local/bin/python

from random import random
from datetime import date, timedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff
from contracts.models import Contract, EnergyBill
from users.models import UniversityUser

TODAY = date.today()
YEAR_LATER = TODAY + timedelta(days=365)

university = University.objects.create(
    name='Universidade de Brasília',
    acronym='UnB',
    cnpj='63025530000104'
)

university_user = UniversityUser.objects.create(
    university=university,
    password='user',
    email='user@user.com',
)

unit1 = ConsumerUnit.objects.create(
    name='Darcy Ribeiro',
    code='1111111',
    is_active=True,
    university=university,
)

distributor = Distributor.objects.create(
    name='Neoenergia',
    cnpj='00038174000143',
    university=university,
)

unit2 = ConsumerUnit.objects.create(
    name='FGA',
    code='2222222',
    is_active=True,
    university=university,
)

unit3 = ConsumerUnit.objects.create(
    name='Campus Planaltina',
    code='3333333',
    is_active=True,
    university=university,
)

unit4 = ConsumerUnit.objects.create(
    name='Campus Ceilândia',
    code='4444444',
    is_active=True,
    university=university,
)

distributor1 = Distributor.objects.create(
    name='Neoenergia',
    cnpj='01083200000118',
    university=university,
)

distributor2 = Distributor.objects.create(
    name='CEB',
    cnpj='07522669000192',
    university=university,
)

contract1 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=unit1,
    distributor=distributor1,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=24,
    peak_contracted_demand_in_kw=400,
    off_peak_contracted_demand_in_kw=400,
)

contract2 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit2,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=69,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

contract3 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit3,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=1.1,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

contract4 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=unit4,
    distributor=distributor2,
    start_date=TODAY,
    end_date=YEAR_LATER,
    supply_voltage=1.1,
    peak_contracted_demand_in_kw=270,
    off_peak_contracted_demand_in_kw=150,
)

blue = {
    "peak_tusd_in_reais_per_kw": 89.29,
    "peak_tusd_in_reais_per_mwh": 117.13,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_kw": 31.53,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02
}
green = {
    "peak_tusd_in_reais_per_mwh": 2280.15,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02,
    "na_tusd_in_reais_per_kw": 31.53
}

Tariff.objects.bulk_create([
    Tariff(subgroup='A4', distributor=distributor1, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A4', distributor=distributor1, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor1, flag=Tariff.BLUE, **blue, start_date=TODAY, end_date=YEAR_LATER),
    Tariff(subgroup='A3', distributor=distributor1, flag=Tariff.GREEN, **green, start_date=TODAY, end_date=YEAR_LATER),
])

def bill(**kwargs):
    return EnergyBill(invoice_in_reais=random()*10, contract=contract1, consumer_unit=unit1, **kwargs)

# FIXME: Essas datas têm que ser dinâmicas pra "hoje" (date.today())
EnergyBill.objects.bulk_create([
    bill(date='2022-01-01', peak_consumption_in_kwh=6036.00, off_peak_consumption_in_kwh=74963.00, peak_measured_demand_in_kw=152.46, off_peak_measured_demand_in_kw=328.86),
    bill(date='2022-02-01', peak_consumption_in_kwh=7304.00, off_peak_consumption_in_kwh=89052.00, peak_measured_demand_in_kw=141.12, off_peak_measured_demand_in_kw=335.16),
    bill(date='2022-03-01', peak_consumption_in_kwh=11701.00, off_peak_consumption_in_kwh=90147.00, peak_measured_demand_in_kw=294.89, off_peak_measured_demand_in_kw=419.50),
    bill(date='2022-04-01', peak_consumption_in_kwh=13513.00, off_peak_consumption_in_kwh=104291.00, peak_measured_demand_in_kw=286.02, off_peak_measured_demand_in_kw=415.80),
    bill(date='2022-05-01', peak_consumption_in_kwh=11824.00, off_peak_consumption_in_kwh=95312.00, peak_measured_demand_in_kw=260.82, off_peak_measured_demand_in_kw=375.48),
    bill(date='2022-06-01', peak_consumption_in_kwh=9855.00, off_peak_consumption_in_kwh=75999.00, peak_measured_demand_in_kw=217.98, off_peak_measured_demand_in_kw=349.02),
    bill(date='2022-07-01', peak_consumption_in_kwh=6162.00, off_peak_consumption_in_kwh=55884.00, peak_measured_demand_in_kw=153.72, off_peak_measured_demand_in_kw=244.44),
    bill(date='2022-08-01', peak_consumption_in_kwh=8655.00, off_peak_consumption_in_kwh=66206.00, peak_measured_demand_in_kw=207.90, off_peak_measured_demand_in_kw=284.76),
    bill(date='2022-09-01', peak_consumption_in_kwh=14504.00, off_peak_consumption_in_kwh=101701.00, peak_measured_demand_in_kw=313.74, off_peak_measured_demand_in_kw=454.86),
    bill(date='2022-10-01', peak_consumption_in_kwh=13062.00, off_peak_consumption_in_kwh=100019.00, peak_measured_demand_in_kw=309.96, off_peak_measured_demand_in_kw=471.24),
    bill(date='2022-11-01', peak_consumption_in_kwh=13792.00, off_peak_consumption_in_kwh=116523.00, peak_measured_demand_in_kw=332.64, off_peak_measured_demand_in_kw=506.52),
    bill(date='2022-12-01', peak_consumption_in_kwh=10959.00, off_peak_consumption_in_kwh=96363.00, peak_measured_demand_in_kw=296.10, off_peak_measured_demand_in_kw=454.86),
])
