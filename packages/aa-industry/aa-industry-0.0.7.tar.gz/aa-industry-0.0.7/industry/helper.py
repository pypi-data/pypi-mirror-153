import logging

from eveuniverse.models import EveEntity, EveSolarSystem
from .models import Facility

from datetime import datetime, timedelta
import json
import requests

logger = logging.getLogger(__name__)

cache_character_id = {}


def _process_jobs(_request_headers, jobs, is_corp: bool = False) -> list:
    _processed = list()
    cache_character_id.clear()

    if jobs:
        for j in jobs:
            job_details = dict()
            job_details['is_corp_job'] = is_corp

            a = EveEntity.objects.get_or_create_esi(id=j.get('blueprint_type_id'))[0]
            job_details['blueprint_name'] = a.name
            job_details['blueprint_id'] = a.id

            job_details['activity_id'] = _get_activity_by_id(j.get('activity_id'))

            job_details['duration'] = _secondsToTime(j.get('duration'))
            job_details['start_date'] = _fromStrToDate(j.get('start_date'))
            job_details['end_date'] = _fromStrToDate(j.get('end_date'))
            job_details['status'] = j.get('status')
            job_details['installer_id'] = j.get('installer_id')

            station = _get_structure(_request_headers, j.get('facility_id'))
            if not station:
                logger.error('error getting station')
                job_details['station_name'] = ''
            else:
                job_details['station_name'] = station.name

            if is_corp:
                job_details['installer_name'] = _get_character_name(_request_headers, job_details['installer_id'])

            _processed.append(job_details)

    cache_character_id.clear()
    return _processed


def _get_activity_by_id(activity_id: int) -> str:
    activities = {
        1: "Manufacturing",
        2: "Researching Technology",
        3: "Time Efficiency Research",
        4: "Material Efficiency Research",
        5: "Copying",
        6: "Duplicating",
        7: "Reverse Engineering",
        8: "Invention",
        9: "Reaction",
    }

    return activities[activity_id] if activity_id in activities.keys() else activity_id


def _get_structure(_request_headers: dict, facility_id: str) -> Facility:
    try:
        facility = Facility.objects.filter(facility_id=facility_id).first()

        if facility and facility.solar_system is not None:
            return facility

        # get structure
        r = requests.get(
            f'https://esi.evetech.net/latest/universe/structures/{facility_id}/?datasource=tranquility',
            headers=_request_headers
        )
        if r.status_code == 200:
            station = json.loads(r.content)

            if not facility:
                facility = Facility()

            _solar_system = EveSolarSystem.objects.get_or_create(id=station['solar_system_id'])

            if len(_solar_system) > 0:
                solar_system = _solar_system[0]

            facility.facility_id = facility_id
            facility.name = station['name']
            facility.owner_id = station['owner_id']
            facility.solar_system = solar_system
            facility.type_id = station['type_id']
            facility.save()

            return facility

    except Exception as exxx:
        logger.error(exxx)
        return None


def _get_character_name(_request_headers: dict, character_id: str) -> str:
    try:
        if character_id in cache_character_id.keys():
            return cache_character_id.get(character_id)

        # get character name
        r = requests.get(
            f'https://esi.evetech.net/latest/characters/{character_id}/?datasource=tranquility',
            headers=_request_headers
        )
        if r.status_code == 200:
            character = json.loads(r.content)
            cache_character_id[character_id] = character['name']
            return character['name']

    except Exception as ex:
        logger.error(f'error getting character name by id => {ex}')
        return None


def _get_personal_jobs(user_id: int, _request_headers: dict, completed: bool = False) -> list:
    _url = f'https://esi.evetech.net/latest/characters/{user_id}/industry/jobs/?datasource=tranquility'

    if completed:
        _url = _url + '&include_completed=true'

    return _get_jobs(_url, _request_headers)


def _get_corp_jobs(corp_id: int, _request_headers: dict, completed: bool = False) -> list:
    _url = f'https://esi.evetech.net/latest/corporations/{corp_id}/industry/jobs/?datasource=tranquility'

    if completed:
        _url = _url + '&include_completed=true'

    return _get_jobs(_url, _request_headers)


def _get_jobs(url: str, _request_headers: dict) -> list:
    try:
        r = requests.get(url, headers=_request_headers)

        if r.status_code == 200:
            return json.loads(r.content)
    except requests.exceptions.ConnectionError:
        logger.error("connection failed")
        return []
    else:
        logger.error(f'requests error {r.status_code}')
        return []


def _secondsToTime(seconds: int) -> str:
    return str(timedelta(seconds=seconds))


def _fromStrToDate(date_time_str: str) -> datetime:
    time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%SZ')
    return time_obj
