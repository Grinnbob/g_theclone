from app.providers.closecom.closecom_api import CloseComApiProvider

async def _execute_closecom_api(api_name,
                                payload=None,
                                paginate=False,
                                once=False):

    api_provider = await CloseComApiProvider.create_api_provider()

    api_session = await api_provider.get_client_session()
    async with api_session as session:
        api_method = getattr(api_provider, api_name)
        data = {}
        if payload:
            data = await api_method(payload,
                                    paginate=paginate,
                                    once=once)
        else:
            data = await api_method(paginate=paginate,
                                    once=once)

        return data

    return None