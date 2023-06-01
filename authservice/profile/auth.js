import { Issuer, Strategy} from "openid-client";
import config from './_secrets/config.js';

import dotenv from 'dotenv';
import path from 'path';

let _kcClient;
const envPath = path.join(path.resolve(), '_secrets/.env');

dotenv.config({
    path:envPath
});

export const getClient = async ()=>{

    if (_kcClient){
        return _kcClient
    }
    const issuer_url = config.KC_ISSUE_URL;
    const kcIssuer = await Issuer.discover(issuer_url);

    _kcClient = new kcIssuer.Client(
        {
            client_id:process.env.KC_CLIENT_ID,
            client_secret:process.env.KC_CLIENT_SECRET,
            redirect_uris:config.KC_REDIRECT_URIS,
            response_types:['code']
        }
    );
    return _kcClient;
}




