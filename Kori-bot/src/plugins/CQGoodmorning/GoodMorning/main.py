# -*- coding: utf-8 -*-

from . import utils
from .config import *
import random

async def userRegistration(userQQ, model):
    registrationStructure = {
        'qq': userQQ,
        'model': model,
        'time': await utils.getTheCurrentTime(),
        'accurateTime': await utils.getAccurateTimeNow()
    }
    await utils.userInformationWriting(userQQ, registrationStructure)
    return SUCCESS

async def createACheckInPool(userGroup, model):
    signInPoolStructure = {
        'qun': userGroup,
        'time': await utils.getTheCurrentTime(),
        'accurateTime': await utils.getAccurateTimeNow(),
        'userList': [],
        'number': 0
    }
    await utils.groupWrite(str(userGroup) + '-' + model, signInPoolStructure)
    return SUCCESS

async def addToCheckInPoolAndGetRanking(userQQ, userGroup, model):
    if model == MORNING_MODEL:
        # Check if there is a check-in pool
        content = await utils.groupRead(str(userGroup) + '-' + model)
        if content == ERROR:
            # Create a check-in pool
            await createACheckInPool(userGroup, model)
            content = await utils.groupRead(str(userGroup) + '-' + model)
        # Check if the pool has expired
        if content['time'] != await utils.getTheCurrentTime():
            # Expired, rebuild the pool
            await createACheckInPool(userGroup, model)
            content = await utils.groupRead(str(userGroup) + '-' + model)
        # Add users to the check-in pool
        user = await utils.userInformationReading(userQQ)
        content['userList'].append(user)
        content['number'] += 1
        await utils.groupWrite(str(userGroup) + '-' + model, content)
        return content['number']
    if model == NIGHT_MODEL:
        # Check if there is a check-in pool
        content = await utils.groupRead(str(userGroup) + '-' + model)
        if content == ERROR:
            # Create a check-in pool
            await createACheckInPool(userGroup, model)
            content = await utils.groupRead(str(userGroup) + '-' + model)
        # Check if the pool has expired
        hourNow = await utils.getTheCurrentHour()
        expiryId = False
        if content['time'] != await utils.getTheCurrentTime():
            if await utils.judgeTimeDifference(content['accurateTime']) < 24:
                if hourNow >= 12:
                    expiryId = True
            else:
                expiryId = True
        if expiryId:
            # Expired, rebuild the pool
            await createACheckInPool(userGroup, model)
            content = await utils.groupRead(str(userGroup) + '-' + model)
        # Add users to the check-in pool
        user = await utils.userInformationReading(userQQ)
        content['userList'].append(user)
        content['number'] += 1
        await utils.groupWrite(str(userGroup) + '-' + model, content)
        return content['number']
            
async def goodMorningInformation(userQQ, userGroup, sender):
    # Check if registered
    registered = await utils.userInformationReading(userQQ)
    send = await utils.at(userQQ)
    if registered == ERROR:
        # registered
        await userRegistration(userQQ, MORNING_MODEL)
        # Add to check-in pool and get ranking
        rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, MORNING_MODEL)
        send += (await utils.extractRandomWords(MORNING_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                MORNING_MODEL)).replace(r'{number}', str(rank)))
        return send
    # Already registered
    if registered['model'] == MORNING_MODEL:
        # too little time
        if await utils.judgeTimeDifference(registered['accurateTime']) <= 4:
            send += await utils.extractConfigurationInformationAccordingToSpecifiedParameters('triggered', MORNING_MODEL)
            return send
        # Good morning no twice a day
        if registered['time'] != await utils.getTheCurrentTime():
            await userRegistration(userQQ, MORNING_MODEL)
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, MORNING_MODEL)
            send += (await utils.extractRandomWords(MORNING_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                MORNING_MODEL)).replace(r'{number}', str(rank)))
            return send
    if registered['model'] == NIGHT_MODEL:
        sleepingTime = await utils.judgeTimeDifference(registered['accurateTime'])
        # too little time
        if sleepingTime <= 4:
            send += await utils.extractConfigurationInformationAccordingToSpecifiedParameters('unable_to_trigger', MORNING_MODEL)
            return send
        # Sleep time cannot exceed 24 hours
        await userRegistration(userQQ, MORNING_MODEL)
        if sleepingTime < 24:
            send += await utils.extractRandomWords(MORNING_MODEL, sender)
            # Calculate Wake Up Ranking
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, MORNING_MODEL)
            send += ((await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                MORNING_MODEL)).replace(r'{number}', str(rank)) + '\n')
            # Calculate precise sleep time
            sleepPreciseTime = await utils.calculateTheElapsedTimeCombination(registered['accurateTime'])
            if sleepPreciseTime[0] >= 9:
                send += await utils.replaceHourMinuteAndSecond(sleepPreciseTime, 
                            (await utils.readConfiguration(MORNING_MODEL))['sleeping_time'][1]['content'])
            elif sleepPreciseTime[0] >= 7:
                send += await utils.replaceHourMinuteAndSecond(sleepPreciseTime, 
                            (await utils.readConfiguration(MORNING_MODEL))['sleeping_time'][0]['content'])
            else:
                send += await utils.replaceHourMinuteAndSecond(sleepPreciseTime, 
                            (await utils.readConfiguration(MORNING_MODEL))['too_little_sleep'])
        else:
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, MORNING_MODEL)
            send += (await utils.extractRandomWords(MORNING_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                MORNING_MODEL)).replace(r'{number}', str(rank)))
        return send
    return ERROR


async def goodNightInformation(userQQ, userGroup, sender):
    # Check if registered
    registered = await utils.userInformationReading(userQQ)
    send = await utils.at(userQQ)
    if registered == ERROR:
        # registered
        await userRegistration(userQQ, NIGHT_MODEL)
        # Add to check-in pool and get ranking
        rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, NIGHT_MODEL)
        send += (await utils.extractRandomWords(NIGHT_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                NIGHT_MODEL)).replace(r'{number}', str(rank)))
        return send
    # Already registered
    if registered['model'] == NIGHT_MODEL:
        # too little time
        if await utils.judgeTimeDifference(registered['accurateTime']) <= 4:
            send += await utils.extractConfigurationInformationAccordingToSpecifiedParameters('triggered', NIGHT_MODEL)
            return send
        # Two good nights can not be less than 12 hours
        if await utils.judgeTimeDifference(registered['accurateTime']) >= 12:
            await userRegistration(userQQ, NIGHT_MODEL)
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, NIGHT_MODEL)
            send += (await utils.extractRandomWords(NIGHT_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                NIGHT_MODEL)).replace(r'{number}', str(rank)))
            return send
    if registered['model'] == MORNING_MODEL:
        soberTime = await utils.judgeTimeDifference(registered['accurateTime'])
        # too little time
        if soberTime <= 4:
            send += await utils.extractConfigurationInformationAccordingToSpecifiedParameters('unable_to_trigger', NIGHT_MODEL)
            return send
        # sober time cannot exceed 24 hours
        await userRegistration(userQQ, NIGHT_MODEL)
        if soberTime < 24:
            send += await utils.extractRandomWords(NIGHT_MODEL, sender)
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, NIGHT_MODEL)
            send += ((await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                NIGHT_MODEL)).replace(r'{number}', str(rank)) + '\n')
            soberAccurateTime = await utils.calculateTheElapsedTimeCombination(registered['accurateTime'])
            if soberAccurateTime[0] >= 12:
                send += await utils.replaceHourMinuteAndSecond(soberAccurateTime, 
                            (await utils.readConfiguration(NIGHT_MODEL))['working_hours'][2]['content'])
            else:
                send += await utils.replaceHourMinuteAndSecond(soberAccurateTime, 
                            random.choice((await utils.readConfiguration(NIGHT_MODEL))['working_hours'])['content'])
        else:
            rank = await addToCheckInPoolAndGetRanking(userQQ, userGroup, NIGHT_MODEL)
            send += (await utils.extractRandomWords(NIGHT_MODEL, sender) + '\n' +
                (await utils.extractConfigurationInformationAccordingToSpecifiedParameters('suffix',
                NIGHT_MODEL)).replace(r'{number}', str(rank)))
        return send
    return ERROR

