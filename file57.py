import random
import os
import time
import sys
import csv
import math

def Set_List(Hash_list, Crypto_Wealth_list, Parameters):
    """Initialize Hash and Wealth lists with input parameters"""
    if Parameters['StaticOrNot'] == 0 :
        for i in range(Parameters['NodeSize']) :
            Hash_list += [RandomDisGen(Parameters)]
            Crypto_Wealth_list += [0]
    elif Parameters['StaticOrNot'] == 1 :
        Hash_list += [RandomDisGen(Parameters)]
        Crypto_Wealth_list += [0]
    else :
        print("Static or Not parameters should be 0 or 1")

def Mining(Hash_list, Crypto_Wealth_list, Parameters):
    """Decide which node will success mining, and get reward"""
    total = 0
    Reward = [1, 10, 30, 50]
    for i in range(len(Hash_list)) :
        total += Hash_list[i]
    index = 0
    Success_Possibility = random.uniform(0, total)
    Success_Indicator = 0
    for i in range(len(Hash_list)) :
        Success_Indicator += Hash_list[i]
        if Success_Indicator >= Success_Possibility:
            Crypto_Wealth_list[i] += Reward[Parameters['Reward']]
            index = i
            break
    return index

def Investment(Hash_list, Crypto_Wealth_list, Parameters):
    """Decide new node enter the system"""
    if Parameters['StaticOrNot'] == 0 :
        for i in range(Parameters['NodeSize']) :
            if Hash_list[i] == 0 :
                Hash_list[i] += RandomDisGen(Parameters)
                break
    elif Parameters['StaticOrNot'] == 1 :
        if len(Hash_list) < Parameters['NodeSize'] :
            Hash_list += [RandomDisGen(Parameters)]
            Crypto_Wealth_list += [0]

def Reinvestment(Hash_list, Crypto_Wealth_list, Parameters, reinvestment_ratio_list):
    if Parameters['ReinvType'] == 0:
        Reinvestment_Simple(Hash_list, Crypto_Wealth_list, Parameters, reinvestment_ratio_list)
    elif Parameters['ReinvType'] == 1:
        Reinvestment_Chance(Hash_list, Crypto_Wealth_list, Parameters, reinvestment_ratio_list)

def Reinvestment_Simple(Hash_list, Crypto_Wealth_list, Parameters, reinvestment_ratio_list):
    """Decide each node reinvest to their hash power and make distribution of wealth"""
    if len(Hash_list) > 1 :
        for i in range(len(Hash_list)):
            Hash_list[i] += reinvestment_ratio_list[Parameters['ReinvestmentParameter']] * Crypto_Wealth_list[i]
            Crypto_Wealth_list[i] -= reinvestment_ratio_list[Parameters['ReinvestmentParameter']] * Crypto_Wealth_list[i]

def Reinvestment_Chance(Hash_list, Crypto_Wealth_list, Parameters, reinvestment_ratio_list):
    """Decide each node reinvest to their hash power and make distribution of wealth"""
    if len(Hash_list) > 1:
        maximum_wealth = 0
        for i in range(len(Hash_list)):
            if maximum_wealth < Crypto_Wealth_list[i]:
                maximum_wealth = Crypto_Wealth_list[i]

        reinvestment_chance = 0
        for i in range(len(Hash_list)) :
            reinvestment_chance = random.uniform(0,1)
            if reinvestment_chance <= (Crypto_Wealth_list[i] / maximum_wealth) :
                Hash_list[i] += reinvestment_ratio_list[Parameters['ReinvestmentParameter']] * Crypto_Wealth_list[i]
                Crypto_Wealth_list[i] -= reinvestment_ratio_list[Parameters['ReinvestmentParameter']] * Crypto_Wealth_list[i]

def Redistribution(Hash_list, Crypto_Wealth_list, Parameters, index, reinvestment_ratio_list):
    redistribution_babo(Hash_list, Crypto_Wealth_list, index, reinvestment_ratio_list, Parameters)

def redistribution_babo(Hash_list, Crypto_Wealth_list, index, reinvestment_ratio_list, Parameters):
    """
    multi = 50.0 / (len(Hash_list) - 1)
    for i in range(len(Hash_list)):
        if i != index:
            Crypto_Wealth_list[i] += multi * reinvestment_ratio_list[Parameters['ReinvestmentParameter']]
        else:
            Crypto_Wealth_list[i] -= multi * reinvestment_ratio_list[Parameters['ReinvestmentParameter']]
    """
    if len(Hash_list) > 1:
        temp_list = list()
        multi = 1.0/ (len(Hash_list) - 1)
        for i in range(len(Hash_list)):
            temp_list += [Crypto_Wealth_list[i] * reinvestment_ratio_list[Parameters['RedistributionParameter']]]
            Crypto_Wealth_list[i] -= Crypto_Wealth_list[i] * reinvestment_ratio_list[Parameters['RedistributionParameter']]

        temp = 0
        for i in range(len(Hash_list)):
            temp += temp_list[i]

        for i in range(len(Hash_list)):
            temp_list[i] = (temp - temp_list[i]) * multi
            Crypto_Wealth_list[i] += temp_list[i]

def FilePrint(Hash_list, Crypto_Wealth_list, Parameters):
    """Print out CSV file of hash power and crypto-currency"""

    filename_hash = str(Parameters['Repeat']) + 'h' + \
                    'di' + str(Parameters['DistributionFormat']) + \
                    'dp' + str(Parameters['InitialParameter']) + \
                    's' + str(Parameters['NodeSize']) + \
                    'n' + str(Parameters['ProcessingNumber']) + \
                    'G' + str(Parameters['StaticOrNot']) + \
                    're' + str(Parameters['ReinvestmentParameter']) + \
                    'rdi' + str(Parameters['RedistributionParameter']) + \
                    'rw' + str(Parameters['Reward']) + \
                    'rit' + str(Parameters['ReinvType']) + '.csv'
    fileout_hash = open(filename_hash, 'w')
    wrh = csv.writer(fileout_hash)
    wrh.writerow(['Hash', 'Accumulated frequency'])

    ach = 0
    for i in range(len(Hash_list) - 1) :
        ach += 1
        if Hash_list[i+1] < Hash_list[i] :
            wrh.writerow([Hash_list[i], ach])

    ach += 1
    wrh.writerow([Hash_list[Parameters['NodeSize'] - 1], ach])
    fileout_hash.close()

    filename_crypto = str(Parameters['Repeat']) + 'c' + \
                      'di' + str(Parameters['DistributionFormat']) + \
                      'dp' + str(Parameters['InitialParameter']) + \
                      's' + str(Parameters['NodeSize']) + \
                      'n' + str(Parameters['ProcessingNumber']) + \
                      'G' + str(Parameters['StaticOrNot']) + \
                      're' + str(Parameters['ReinvestmentParameter']) + \
                      'rdi' + str(Parameters['RedistributionParameter']) + \
                      'rw' + str(Parameters['Reward']) + \
                      'rit' + str(Parameters['ReinvType']) + '.csv'
    fileout_crypto = open(filename_crypto, 'w')
    wrc = csv.writer(fileout_crypto)
    wrc.writerow(['Cryptocurrency, Accumulated frequency'])

    acc = 0
    for i in range(len(Crypto_Wealth_list) - 1) :
        acc += 1
        if Crypto_Wealth_list[i+1] < Crypto_Wealth_list[i] :
            wrc.writerow([Crypto_Wealth_list[i], acc])

    acc += 1
    wrc.writerow([Crypto_Wealth_list[Parameters['NodeSize'] - 1], acc])
    fileout_crypto.close()

def FilePrint_babo(Hash_list, Crypto_Wealth_list, Parameters):
    """Print out CSV file of hash power and crypto-currency for Babo model"""

    filename_hash = str(Parameters['Repeat']) + 'h' + 'di' + \
                    str(Parameters['DistributionFormat']) + 'dp'+ \
                    str(Parameters['InitialParameter']) + 's' + \
                    str(Parameters['NodeSize']) + 'n' + \
                    str(Parameters['ProcessingNumber']) + 'G' + \
                    str(Parameters['StaticOrNot']) + 'rd' + \
                    str(Parameters['ReinvOrRediv']) + 're'+ \
                        str(Parameters['ReinvestmentParameter'])  + '.csv'
    fileout_hash = open(filename_hash, 'w')
    wrh = csv.writer(fileout_hash)
    wrh.writerow(['Hash', 'Accumulated frequency'])

    ach = 0
    for i in range(len(Hash_list) - 1) :
        ach += 1
        if Hash_list[i+1] < Hash_list[i] :
            wrh.writerow([Hash_list[i], ach])

    ach += 1
    wrh.writerow([Hash_list[Parameters['NodeSize'] - 1], ach])
    fileout_hash.close()

    filename_crypto = str(Parameters['Repeat']) + 'c' + 'di' + \
                      str(Parameters['DistributionFormat']) + 'dp' + \
                      str(Parameters['InitialParameter']) + 's' + \
                      str(Parameters['NodeSize']) + 'n' + \
                      str(Parameters['ProcessingNumber']) + 'G' + \
                      str(Parameters['StaticOrNot']) + 'rd' + \
                      str(Parameters['ReinvOrRediv']) + 're' + \
                        str(Parameters['ReinvestmentParameter']) + '.csv'
    fileout_crypto = open(filename_crypto, 'w')
    wrc = csv.writer(fileout_crypto)
    wrc.writerow(['Cryptocurrency, Accumulated frequency'])

    acc = 0
    for i in range(len(Crypto_Wealth_list) - 1) :
        acc += 1
        if Crypto_Wealth_list[i+1] < Crypto_Wealth_list[i] :
            wrc.writerow([Crypto_Wealth_list[i], acc])

    acc += 1
    wrc.writerow([Crypto_Wealth_list[Parameters['NodeSize'] - 1], acc])
    fileout_crypto.close()

def RandomDisGen(Parameters):
    """Create random number to make specific types of distribution"""
    Uniform_Parameters = [1, 5, 10]
    Exponential_Parameters = [0.1, 1, 5]
    Power_Parameters = [1.5, 2, 2.5]
    Regular_Parameters = [1, 5, 10, 30]

    if Parameters['DistributionFormat'] == 0 :
        return random.uniform(0, Uniform_Parameters[Parameters['InitialParameter']])
    elif Parameters['DistributionFormat'] == 1 :
        return RandomExp(Parameters, Exponential_Parameters)
    elif Parameters['DistributionFormat'] == 2 :
        return RandomPow(Parameters, Power_Parameters)
    elif Parameters['DistributionFormat'] == 3 :
        return Regular_Parameters[Parameters['InitialParameter']]
    else :
        print("Distribution Format should be 0 to 3")

def RandomExp(Parameters, Exponential_Parameters):
    """Create random number that follow exp distribution"""
    UncheckedChance = random.uniform(0,1)
    while UncheckedChance == 0 or UncheckedChance == 1:
        UncheckedChance = random.uniform(0,1)

    return (-1 / Exponential_Parameters[Parameters['InitialParameter']]) * math.log(1 - UncheckedChance)

def RandomPow(Parameters, Power_Parameters):
    """Create random number that follow Power distribution"""
    UncheckedChance = random.uniform(0,1)
    while UncheckedChance == 0 or UncheckedChance == 1:
        UncheckedChance = random.uniform(0,1)

    return 1.0 / pow(1 - UncheckedChance, (1.0 / Power_Parameters[Parameters['InitialParameter']]))
