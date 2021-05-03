import requests, time, subprocess, sys
from book_slot import book_slot

base_URL = 'https://www.cowin.gov.in/api'
req_URL = base_URL+'/v2/appointment/sessions/public/calendarByDistrict'
district_code = 395


def book_slot_helper(*args, **kwargs):
    session_id= kwargs['session_id']
    slot= kwargs['slot']
    if book_slot(session_id=session_id, slot=slot, beneficiary_id=beneficiary_id, mobile=mobile)==0:
        return 0
    return 1

if len(sys.argv)<3:
    print("Usage: python check_and_book_slots.py <beneficary_id> <mobile_number>")
    sys.exit()

beneficiary_id = sys.argv[1]
mobile = sys.argv[2]


while True:
    print('searching slots: ',time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
    try:
        found = False
        res = requests.get(req_URL+'?district_id={}&date={}'.format(district_code, time.strftime('%d-%m-%Y', time.localtime())))
        if res.status_code!=200:
            print("fetch error")
        else:
            res = res.json()
            for center in res['centers']:
                for session in center['sessions']:
                    if session['min_age_limit']==18 and session['available_capacity']>0:
                        for slot in session['slots']:
                            found = True
                            print("\n")
                            print('name: ',str(center['name']))
                            print('block_name: ', str(center['block_name']))
                            print('district/city: ', str(center['district_name']))
                            print('vaccine: ',str(session['vaccine']))
                            print('available_capacity: ', session['available_capacity'])
                            print('session_id: ',session['session_id'])
                            print('slot: ', slot)
                            print("##############################")
                            subprocess.call(['spd-say', 'Slot found attempting to schedule appointment'])
                            if book_slot_helper(session_id=session['session_id'], slot=slot, beneficiary_id=beneficiary_id, mobile=mobile)==1:
                                sys.exit("Congrats you're done. Please note down your appointment details") 
                            else:
                                print("Failed to schedule appointment, searching again ...")
                                time.sleep(5)
    except Exception as e:
        print(e)
    # finally:
    #     if found:
    #         x=5
    #         while x:
    #             subprocess.call(['spd-say', 'vaccine'])
    #             time.sleep(1)
    #             x-=1
