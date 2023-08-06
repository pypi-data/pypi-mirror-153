import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from esi.decorators import token_required


from .models import UserToken
from .helper import _get_personal_jobs, _get_corp_jobs, _process_jobs

logger = logging.getLogger(__name__)

_scopes = [
    'esi-industry.read_character_jobs.v1',
    'esi-industry.read_corporation_jobs.v1',
    'esi-universe.read_structures.v1',
]

cache_facility_id = {}
cache_character_id = {}


@login_required
@permission_required("industry.view_industry")
def index(request):
    ut = UserToken.objects.filter(user=request.user).first()

    if not ut:
        return redirect('industry:selector')

    return redirect('industry:list_jobs', pk_token=ut.pk)


@login_required
@permission_required("industry.view_industry")
@token_required(scopes=_scopes)
def char_selector(request, t):
    ut = UserToken.objects.filter(token=t).first()

    if not ut:
        ut = UserToken(user=request.user, token=t, character_id=t.character_id)
        ut.save()

    return redirect('industry:list_jobs', pk_token=ut.pk)


@login_required
@permission_required("industry.view_industry")
def list_jobs(request, pk_token):

    corp_id = request.user.profile.main_character.corporation_id

    ut = UserToken.objects.get(pk=pk_token)

    if ut.user.pk != request.user.pk:
        logger.warn(f'user {request.user.profile.main_character} trying to access a service that he does not own {pk_token}')
        return redirect('industry:selector')

    if not ut:
        return redirect('industry:selector')

    t = ut.token

    _request_headers = {
        'accept': 'application/json',
        'Cache-Control': 'no-cache',
        'authorization': 'Bearer ' + t.valid_access_token()
    }

    jobs = _get_personal_jobs(t.character_id, _request_headers)
    _processed_jobs = _process_jobs(_request_headers, jobs)

    jobs = _get_corp_jobs(corp_id, _request_headers)
    _corp_jobs = _process_jobs(_request_headers, jobs, True)

    if _corp_jobs:
        _processed_jobs += _corp_jobs

    character_data = {
        'character_name': t.character_name,
        'character_id' : t.character_id,
        'token_id': ut.pk
    }

    context = {
        "items": _processed_jobs,
        "character_data": character_data,
        "user_tokens": UserToken.objects.filter(user=request.user)
    }

    return render(request, "industry/index.html", context)


@method_decorator(login_required, name='dispatch')
class UserTokenDelete(DeleteView):
    """ Delete flow for an Order """
    model = UserToken
    success_url = reverse_lazy('industry:index')
    permission_required = ('industry.view_industry',)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            messages.error(request, 'You do not have permission to delete this character.')
            return redirect(request.path)
        return super().delete(request, *args, **kwargs)


