import requests, hashlib, sys


def book_slot(*args, **kwargs):
    # Beneficiary id can be 
    # 1. Aadhaar Card
    # 2. Driving License
    # 3.PAN Card
    # 4.Passport
    # 5.Pension Passbook
    # 6.Pension Passbook
    # 7.Voter ID
    beneficiary_ids = [str(kwargs['beneficiary_id'])]  
    mobile_number = str(kwargs['mobile'])
    base_URL = 'https://www.cowin.gov.in/api'
    payload = {
        "dose": 1,
        "session_id": kwargs['session_id'],
        "slot": kwargs['slot'],
        "beneficiaries": beneficiary_ids
    }

    try:
        gen_otp = requests.post(base_URL+'/v2/auth/generateOTP', data={"mobile": mobile_number})
        if gen_otp.status_code!=200:
            print("opt generation error")
        else:
            gen_otp = gen_otp.json()
    except Exception as e:
        print(e)

    otp = input('enter otp: ')
    gen_otp['otp']=hashlib.sha256(str(otp)).hexdigest()

    try:
        confirm_otp = requests.post(base_URL+'/v2/auth/confirmOTP', data=gen_otp)
        if confirm_otp.status_code!=200:
            print("opt confirmation error")
        else:
            confirm_otp = confirm_otp.json()
    except Exception as e:
        print(e)

    token = str(confirm_otp['token'])

    try:
        appointment_res = requests.post(base_URL+'/v2/appointment/schedule', data=payload, headers={"Authorization" : "Bearer "+token})
        if appointment_res.status_code==200:
            print("Appointment scheduled successfully.")
            print("Details: \n",appointment_res.json())
            return 1
        else:
            print("Scheduling failed")
    except Exception as e:
        print(e)
        return 0