import requests
import json

ACCOUNT_IDS=["00000000-0000-0000-0000-000000000000", "11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222", "24592261-a672-4ada-8091-a3612acba499", "76204e5c-4920-4710-acae-64eb06087171"]
#ACCOUNT_IDS=["00000000-0000-0000-0000-000000000000"]

ADMIN_TOKEN = ""
#Removed hardcoded trokens, find way to load from file NOT in repo
JWT_TOKENS = {
    "00000000-0000-0000-0000-000000000000": "",
    "11111111-1111-1111-1111-111111111111": "",
    "22222222-2222-2222-2222-222222222222": ""
}

NEON_API_PATH='tracemark/neon/api/v1/'

#stacks = ["dev", "test", "stage", "prod"]
stacks = ["dev", "test", "stage"]

for stack in stacks:
    NEON_URL="https://" + stack + ".tracemark.irdeto.com/"
    #ASSET_API_URL = NEON_URL + NEON_API_PATH + "assets?tmidType=V4.0" #Doesnt seem to work for now...
    ASSET_API_URL = NEON_URL + NEON_API_PATH + "assets"

    for account_id in ACCOUNT_IDS:

        ASSET_API_URL_accnt = ASSET_API_URL + "?accountId=" + account_id
        print("processing account :", account_id)
        #token = JWT_TOKENS[account_id]
        token = ADMIN_TOKEN

        print("Issuing GET request from ", ASSET_API_URL_accnt)
        headers = {'Authorization': 'Bearer ' + token}
        #foo = headers
        proxies = {}
        #print("Sending command: ", ASSET_API_URL, foo, proxies)
        r = requests.get(ASSET_API_URL_accnt, headers = headers, proxies = proxies)
        print("Requested assets. Response code: ", r.status_code)

        if r.status_code != 200:
            print("Encountered error")
            #exit(1)
        else:

            assets = json.loads(r.text)
            #print("Assets: ", assets)
            assetsToFix = []
            for asset in assets:
                #print(asset)
                if asset['tmidType'] == 'V4.0' and asset['emergencyTMID'] == '':
                #if asset['tmidType'] == 'V4.0' and asset['emergencyTMID'] == '' and asset['state'] == 'Created':
                    assetsToFix.append(asset['assetId'])
            #print(assetsToFix)
                
            print("Fixing {} assets".format(len(assetsToFix)))
            for asset in assetsToFix:
                #url = ASSET_API_URL + '/' + asset 
                url = ASSET_API_URL + '/' + asset + "?accountId=" + account_id
                headers = {'Authorization': 'Bearer ' + token}
                #foo = headers
                proxies = {}
                #print("Sending command: ", url, foo, proxies)
                r = requests.get(url, headers = headers, proxies = proxies)
                print("Requested asset {0}. Response code: {1}".format(asset, str(r.status_code)))

                if r.status_code != 200:
                    print("Encountered error")
                    #exit(2)
