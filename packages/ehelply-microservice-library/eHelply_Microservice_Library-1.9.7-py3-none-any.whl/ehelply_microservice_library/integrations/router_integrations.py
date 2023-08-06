import sentry_sdk
from starlette.requests import Request
from fastapi import Header, Query
from fastapi import HTTPException
from ehelply_microservice_library.utils.paginate import SQLPaginator
from ehelply_microservice_library.utils.search_filter_sort import SQLSearch, SQLSort
from ehelply_microservice_library.utils.ehelply_cloud import CloudParticipantAuthRequest


def get_fact(request: Request):
    """
    Get fact service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_fact'):
        return request.state.i_fact
    else:
        raise Exception("Fact integration has not been registered")


def get_log(request: Request):
    """
    Get log service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_log'):
        return request.state.i_log
    else:
        raise Exception("Log integration has not been registered")


def get_monitor(request: Request):
    """
    Get monitor service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_monitor'):
        return request.state.i_monitor
    else:
        raise Exception("Monitor integration has not been registered")


def get_m2m(request: Request):
    """
    Get M2M service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_m2m'):
        return request.state.i_m2m
    else:
        raise Exception("M2M integration has not been registered")


def get_notifications(request: Request):
    """
    Get notifications service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_notifications'):
        return request.state.i_notifications
    else:
        raise Exception("Notifications integration has not been registered")


class Integrations:
    """
    Common integrations
    """

    def __init__(
            self,
            fact,
            log,
            monitor,
            m2m,
            notifications,
    ) -> None:
        super().__init__()

        self.fact = fact
        self.log = log
        self.monitor = monitor
        self.m2m = m2m
        self.notifications = notifications


def get_integrations(
        request: Request
) -> Integrations:
    """
    Dependency injection helper to get all integrations if you're lazy like me and don't want to specify a laundry list
      each time.
    Marginally lower performance on each endpoint this is used. If really trying to optimize common endpoints,
      don't use this.
    :param request:
    :return:
    """
    try:
        fact = get_fact(request=request)
    except:
        fact = None

    try:
        log = get_log(request=request)
    except:
        log = None

    try:
        monitor = get_monitor(request=request)
    except:
        monitor = None

    try:
        m2m = get_m2m(request=request)
    except:
        m2m = None

    try:
        notifications = get_notifications(request=request)
    except:
        notifications = None

    return Integrations(
        fact=fact,
        log=log,
        monitor=monitor,
        m2m=m2m,
        notifications=notifications,
    )


async def get_auth(
        request: Request,
        x_access_token: str = Header(None),
        x_secret_token: str = Header(None),
        authorization: str = Header(None),
        ehelply_active_participant: str = Header(None),
        ehelply_project: str = Header(None),
        ehelply_data: str = Header(None)
):
    """
    Dependency Injection for eHelply headers

    Args:
        request:
        x_access_token:
        x_secret_token:
        authorization:
        ehelply_active_participant:
        ehelply_project:
        ehelply_data:

    Returns:

    """
    with sentry_sdk.start_span(op="forming_cp_auth_request", description="Forming CloudParticipantAuthRequest") as span:
        return CloudParticipantAuthRequest(
            x_access_token=x_access_token,
            x_secret_token=x_secret_token,
            authorization=authorization,
            ehelply_active_participant=ehelply_active_participant,
            ehelply_project=ehelply_project,
            ehelply_data=ehelply_data
        )


def get_pagination(
        request: Request,
        page: int = Query(1),
        page_size: int = Query(25),
):
    """
    Returns an instance of pagination which can be used with a query
    :param request:
    :param page:
    :param page_size:
    :return:
    """
    return SQLPaginator(page=page, page_size=page_size)


def get_search(
        request: Request,
        search: str = Query(None),
        search_on: str = Query(None)
):
    """
    Returns a query with a search applied.

    Args:
        request:
        search:
        search_on:

    Returns:

    """
    if search and len(search) < 3:
        raise HTTPException(status_code=400,
                            detail="Search criteria must be at least 3 characters long - Denied by eHelply")

    return SQLSearch(search_text=search, column=search_on)


def get_sort(
        request: Request,
        sort_on: str = Query(None),
        sort_desc: bool = Query(False),
):
    """
    Returns a query with a sort applied
    Args:
        request:
        sort_on:
        sort_desc:

    Returns:

    """
    return SQLSort(column=sort_on, desc=sort_desc)
