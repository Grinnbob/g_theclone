import argparse
import asyncio
import uvloop
from app.core.config import settings

from app.scripts.closecom.sequences import *
from app.scripts.closecom.subscriptions import *
from app.scripts.closecom.activities import *
from app.scripts.closecom.smartviews import *
from app.scripts.closecom.accounts import *
from app.scripts.closecom.cron import *
from app.scripts.closecom.lead import *
from app.scripts.closecom.stats import *

from app.scripts.closecom.contact import *

from app.scripts.zerobounce.credits import *
from app.scripts.zerobounce.validate import *

from app.scripts.ranksdr.report import *

async_actions = {
    'analyze_ranksdr_data' : analyze_ranksdr_data,
    'show_ranksdr_data' : show_ranksdr_data,

    'update_all' : update_all,
    'launch_all' : launch_all,

    'show_stats' : show_stats,
    'update_stats_spreadsheet': update_stats_spreadsheet,

    'show_leads' : show_leads,
    'update_leads' : update_leads,

    'show_all_status' : show_all_status,
    'lead_change_status' : lead_change_status,

    'show_accounts' : show_accounts,
    'update_accounts' : update_accounts,

    'show_sequences' : show_sequences,
    'show_sequence' : show_sequence,
    'update_sequences': update_sequences,

    'show_subscriptions' : show_subscriptions,
    'show_subscription' : show_subscription,
    'show_duplicated_subscriptions': show_duplicated_subscriptions,
    'unsubscribe_duplicated_subscriptions': unsubscribe_duplicated_subscriptions,
    'update_subscriptions': update_subscriptions,
    'finish_subscription': finish_subscription,

    'show_activities': show_activities,
    'show_email_threads': show_email_threads,
    'show_emails' : show_emails,
    'update_emails' : update_emails,

    'show_smartviews': show_smartviews,
    'update_smartviews': update_smartviews,
    'show_smartview_leads': show_smartview_leads,
    'check_smartview_leads_duplicates': check_smartview_leads_duplicates,
    'launch_subscribe' : launch_subscribe,
    'subscribe_smartview' : subscribe_smartview,

    'zerobounce_credits' : zerobounce_credits,
    'zerobounce_validate_email' : zerobounce_validate_email,
    'zerobounce_check_credits' : zerobounce_check_credits,

    'show_contacts' : show_contacts,
    'update_contacts' : update_contacts,

}

async def dispatch(args):
    settings.LOGGER.info("...execution started")

    if args.update_all == True:
        return await async_actions['update_all']()
    elif args.launch_all:
        return await async_actions['launch_all'](args.launch_all)

    elif args.show_all_status == True:
        return await async_actions['show_all_status']()
    elif args.lead_change_status:
        return await async_actions['lead_change_status'](args.lead_change_status[0],
                                                         args.lead_change_status[1])

    elif args.analyze_ranksdr_data:
        return await async_actions['analyze_ranksdr_data'](args.analyze_ranksdr_data)

    elif args.show_ranksdr_data:
        return await async_actions['show_ranksdr_data'](args.show_ranksdr_data[0], args.show_ranksdr_data[1])

    elif args.show_stats:
        return await async_actions['show_stats'](args.show_stats[0],
                                                 args.show_stats[1],
                                                 args.show_stats[2])
    elif args.update_stats_spreadsheet:
        return await async_actions['update_stats_spreadsheet'](args.update_stats_spreadsheet)

    elif args.show_contacts:
        return await async_actions['show_contacts'](args.show_contacts)
    elif args.update_contacts:
        return await async_actions['update_contacts'](args.update_contacts)

    elif args.show_sequences == True:
        return await async_actions['show_sequences']()
    elif args.show_sequence:
        return await async_actions['show_sequence'](args.show_sequence)
    elif args.update_sequences:
        return await async_actions['update_sequences']()

    elif args.show_accounts:
        return await async_actions['show_accounts']()
    elif args.update_accounts:
        return await async_actions['update_accounts']()

    elif args.show_activities == True:
        return await async_actions['show_activities']()
    elif args.show_email_threads:
        return await async_actions['show_email_threads'](args.show_email_threads[0],
                                                         args.show_email_threads[1],
                                                         args.show_email_threads[2])
    elif args.show_emails:
        return await async_actions['show_emails'](args.show_emails[0],
                                                  args.show_emails[1],
                                                  args.show_emails[2])
    elif args.update_emails:
        return await async_actions['update_emails'](args.update_emails[0],
                                                  args.update_emails[1],
                                                  args.update_emails[2])

    elif args.show_subscriptions == True:
        return await async_actions['show_subscriptions']()
    elif args.show_subscription:
        return await async_actions['show_subscription'](args.show_subscription)
    elif args.finish_subscription:
        return await async_actions['finish_subscription'](args.finish_subscription)
    elif args.show_duplicated_subscriptions:
        return await async_actions['show_duplicated_subscriptions'](sequence_groups=sequence_groups)
    elif args.unsubscribe_duplicated_subscriptions:
        return await async_actions['unsubscribe_duplicated_subscriptions'](sequence_groups=sequence_groups)
    elif args.update_subscriptions:
        return await async_actions['update_subscriptions']()
    elif args.launch_subscribe:
        return await async_actions['launch_subscribe'](args.launch_subscribe)

    elif args.subscribe_smartview:
        return await async_actions['subscribe_smartview'](args.subscribe_smartview[0],
                                                          args.subscribe_smartview[1])

    elif args.check_smartview_leads_duplicates:
        return await async_actions['check_smartview_leads_duplicates'](args.check_smartview_leads_duplicates[0],
                                                                       args.check_smartview_leads_duplicates[1])
    elif args.show_smartview_leads:
        return await async_actions['show_smartview_leads'](args.show_smartview_leads)
    elif args.update_smartviews:
        return await async_actions['update_smartviews']()
    elif args.show_smartviews:
        return await async_actions['show_smartviews']()


    elif args.show_leads:
        return await async_actions['show_leads'](args.show_leads)
    elif args.update_leads:
        return await async_actions['update_leads'](args.update_leads)

    elif args.zerobounce_credits:
        return await async_actions['zerobounce_credits']()
    elif args.zerobounce_validate_email:
        return await async_actions['zerobounce_validate_email'](args.zerobounce_validate_email)
    elif args.zerobounce_check_credits:
        return await async_actions['zerobounce_check_credits'](args.zerobounce_check_credits)

    else:
        print("usage: prog [OPTION] [PARAMETER]")
        return

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(usage="%(prog)s [OPTION] [PARAMETER]...",
                                     description="Working with close.com API."
                                     )
    parser.add_argument("--show-all-status",
                        help="list all current statuses in close.com",
                        action="store_true")
    parser.add_argument("--lead-change-status",
                        help="<lead_id> <status> - change lead_id status to status",
                        nargs=2,
                        type=str)

    parser.add_argument("--launch-all",
                        help="<need-update-all:0|1> launch sequences to smartviews for all active globals.smartviews_launch_list plan",
                        type=str)

    parser.add_argument("--update-all",
                        help="update: accounts, sequences, smartviews, subscriptions in the database",
                        action="store_true")


    parser.add_argument("--show-accounts",
                        help="show all accounts",
                        action="store_true")
    parser.add_argument("--update-accounts",
                        help="update: accounts in the database",
                        action="store_true")


    parser.add_argument("--show-contacts",
                        help="<once|all> if 'once' will request only 1 page and finish",
                        type=str)
    parser.add_argument("--update-contacts",
                        help="<once|all> if not once will update all contact in the database started from the last page",
                        type=str)

    parser.add_argument("--show-smartviews",
                        help="show all smartviews",
                        action="store_true")
    parser.add_argument("--update-smartviews",
                        help="update all smartviews in the database",
                        action="store_true")
    parser.add_argument("--show-smartview-leads",
                        help="<smartview_id> - show leads for thr given smartview_id",
                        type=str)
    parser.add_argument("--check-smartview-leads-duplicates",
                        help="<smartview_id> <sequence_id> - show all contacts for smartview_id that can be subscribed to sequence_id without duplicating sequences from the same group",
                        nargs=2,
                        type=str)
    parser.add_argument("--subscribe-smartview",
                        help="<sequence_id> <smartview_id> will subscribe smartview_id leads to sequence_id, will check DUPLICATES before",
                        nargs=2,
                        type=str)

    parser.add_argument("--update-sequences",
                        help="update all sequences in database",
                        action="store_true")
    parser.add_argument("--show-sequences",
                        help="show all sequences",
                        action="store_true")
    parser.add_argument("--show-sequence",
                        help="<sequence_id> - show details for given sequence_id",
                        type=str)



    parser.add_argument("--show-subscriptions",
                        help="show all subscriptions",
                        action="store_true")
    parser.add_argument("--show-duplicated-subscriptions",
                        help="will show all contacts that are subscribed to sequences from the same globals.sequence_groups NNED TO CALL --update-all first",
                        action="store_true"),
    parser.add_argument("--unsubscribe-duplicated-subscriptions",
                        help="will pause all active duplicated subscriptions NNED TO CALL --update-all",
                        action="store_true"),
    parser.add_argument("--update-subscriptions",
                        help="will update all subscriptions in the database",
                        action="store_true")
    parser.add_argument("--launch-subscribe",
                        help="<launch_id> for the given launch_id will subscribe all contacts with status=never_subscribed to sequence",
                        type=str)


    parser.add_argument("--finish-subscription",
                        help="<subscription_id> will paused given subscription_id",
                        type=str)
    parser.add_argument("--show-subscription",
                        help="<subscription_id> details about given subscription_id",
                        type=str)


    parser.add_argument("--show-activities",
                        help="list all activities",
                        action="store_true")
    parser.add_argument("--show-email-threads",
                        help="<date_from YYYY-MM-DD> <date_to YYYY-MM-DD> <once|all> show all emails threads activities for given period",
                        nargs=3,
                        type=str)
    parser.add_argument("--show-emails",
                        help="<date_from YYYY-MM-DD> <date_to YYYY-MM-DD> <once|all> show all emails  activities for given period",
                        nargs=3,
                        type=str)
    parser.add_argument("--update-emails",
                        help="<date_from YYYY-MM-DD> <date_to YYYY-MM-DD> <once|all> show all emails  activities for given period",
                        nargs=3,
                        type=str)


    parser.add_argument("--stats-launch",
                        help="<created_day> - format YYYY-MM-DD show aggregated dayly launch for created_day",
                        type=str)

    parser.add_argument("--do-nothing",
                        help="do nothing",
                        action="store_true")

    parser.add_argument("--zerobounce-credits",
                        help="showind available zerobounce credtis for current api_key in config",
                        action="store_true")
    parser.add_argument("--zerobounce-validate-email",
                        help="<email> - validate provided email address for test use: invalid@example.com, valid@example.com",
                        type=str)
    parser.add_argument("--zerobounce-check-credits",
                        help="<need_credits> - will check if the current amount >= need_credits",
                        type=str)

    parser.add_argument("--show-leads",
                        help="<once|all> will show all current leads",
                        type=str)
    parser.add_argument("--update-leads",
                        help="<once|all> will update all leads in the database",
                        type=str)

    parser.add_argument("--show-stats",
                        help="<date_from YYYY-MM-DD> <date_to YYYY-MM-DD> <customer> show all stats for given period FIRST call: --update-leads --update-emails",
                        nargs=3,
                        type=str)
    parser.add_argument("--update-stats-spreadsheet",
                        help="<customer> ",
                        type=str)

    parser.add_argument("--analyze-ranksdr-data",
                        help="<filename.csv> upload and analyze data",
                        type=str)

    parser.add_argument("--show-ranksdr-data",
                        help="<email> <filepath> for find and save report",
                        nargs=2,
                        type=str)


    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(dispatch(args))

if __name__ == '__main__':
    main()