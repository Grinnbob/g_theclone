from app.core.config import settings
from app.scripts.globals import *
from app.services.closecom.lead_service import ClosecomLeadService
from app.services.closecom.emailactivity_service import ClosecomEmailActivityService
from pprint import pprint
import traceback
from .data import *
from .utils import update_dates
from .calc_stats import *
from .print_data import *
from .spreadsheet import update_spreadsheet

# calculate stats for sequences ONLY, group by:
# total
# by day
# by sequence/template
# by segment/sequence/template

# sent - кол-во уникальных отправленных писем (sequence_name != '',  direction='outgoing')
# bounced - кол-во уникальных bounced email'ов (is_postmaster(email_from) == True, direction='incoming', replied_to_sequence=True)
#            * Считаем только уникальные bounced EMAILS_BOUNCED = []

# delivered = (sent - bounced)
# opened - уникальные открытия писем за вычитом google bot (если отправили 3 письма sequence и каждое открыто то opened=3)
# replied - кол-во уникальных ответов (is_postmaster(email_from) == False, is_autreply(email_data) == False, direction='incoming', replied_to_sequence=True)
#            * Считаем только уникальные ответы EMAILS_REPLIED = []

# auto_replied - кол-во уникальных auto_replied email'ов (is_autreply(email_data) == True, direction='incoming', replied_to_sequence=True)
#            * Считаем только уникальные ответы EMAILS_AUTO_REPLIED = []

# Далее считаем кол-во уникальных лидов в конкретном статусе
# для всего КРОМЕ дней имеем LEADS_STATUS_CALC (если лид в этом массиве, то повторно его не считаем)
# для ДНЕЙ мы берем date_updated для лида и приписываем текущий статус к этому дню

# Показываем только:
# dialogs - кол-во лидов в статусу dialog
# meeting booked - кол-во лидов в статусе meeting booked


# bounce rate -
# open rate -
# reply rate -
# appointment rate -


async def _load_leads_data():
    service = ClosecomLeadService()
    all_leads = await service.all_leads()

    async for lead in all_leads:
        LEAD_DATA[lead.lead_id] = lead['data']

    return LEAD_DATA

async def _load_email_ectivities(date_from,
                                 date_to,
                                 customer):

    service = ClosecomEmailActivityService()

    customer_emails = customer_to_emails[customer]

    return await service.group_by_thread_id(date_from,
                                            date_to,
                                            customer_emails)

def _is_black_listed(customer, email_data):
    blacklist = customers_blacklist.get(customer, None)
    if not blacklist:
        return False

    email_blacklist = blacklist.get('emails', [])
    domains_blacklist = blacklist.get('domains', [])
    if not email_blacklist and not domains_blacklist:
        return False

    f_email = from_email(email_data)
    t_email = to_email(email_data)

    if (f_email in email_blacklist) or (t_email in email_blacklist):
        return True

    for d in domains_blacklist:
        if d in f_email or d in t_email:
            return True

    return False

async def show_stats(date_from, date_to, customer):
    await _load_leads_data()
    email_activities = await _load_email_ectivities(date_from,
                                                    date_to,
                                                    customer)

    async for act in email_activities:
        emails = act.get('emails')
        for email_data in emails:
            if _is_black_listed(customer,
                                email_data):
                continue

            update_dates(email_data)
            try:
                calc_sent(email_data)
                calc_bounced(email_data)
                calc_opens(email_data)
                calc_replies(email_data)
                calc_autoreplies(email_data)
                calc_leads_status(email_data)
            except Exception as e:
                traceback.print_exc()
                print(f"error: {str(e)}")
                return None

    post_calc()
    print_all(customer)
    #pprint(EMAILS_TO_STATUS)

async def update_stats_spreadsheet(customer):
    _date_from = '1900-01-01'
    _date_to = '2222-01-01'

    await _load_leads_data()
    email_activities = await _load_email_ectivities(date_from=_date_from,
                                                    date_to=_date_to,
                                                    customer=customer)

    async for act in email_activities:
        emails = act.get('emails')
        for email_data in emails:
            if _is_black_listed(customer,
                                email_data):
                continue
            update_dates(email_data)
            try:
                calc_sent(email_data)
                calc_bounced(email_data)
                calc_opens(email_data)
                calc_replies(email_data)
                calc_autoreplies(email_data)
                calc_leads_status(email_data)
            except Exception as e:
                traceback.print_exc()
                print(f"error: {str(e)}")
                return None

    post_calc()

    total_df = get_total_stats_df()
    daily_df = get_daily_stats_df()
    sequence_df, best_sequence_df = get_sequence_stats_df()
    segment_df, best_segment_df = get_segment_stats_df()
    emails_df = get_email_to_status_df()
    await update_spreadsheet(customer=customer,
                            total_dataframe=total_df,
                             daily_dataframe=daily_df,
                             best_sequences_dataframe=best_sequence_df,
                             sequence_dataframe=sequence_df,
                             best_segments_dataframe=best_segment_df,
                             segment_dataframe=segment_df,
                             emails_dataframe=emails_df)