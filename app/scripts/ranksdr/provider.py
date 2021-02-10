from app.providers.nlpprovider.nlp_provider import NlpProvider

async def _execute_nlp_report(report_name,
                                payload):

    provider = await NlpProvider.create_api_provider()

    api_method = getattr(provider, report_name) 

    data = {}
    if payload:
        data = await api_method(payload)
    else:
        data = await api_method()

    return data